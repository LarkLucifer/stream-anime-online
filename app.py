from flask import Flask, render_template, jsonify, request
import requests
import os
import random

# Get the absolute path to the templates directory
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

# Cache untuk menyimpan data anime
anime_cache = {
    'popular': None,
    'trending': None,
    'seasonal': None
}

def fetch_anime_data(endpoint, params=None):
    base_url = "https://api.jikan.moe/v4"
    try:
        response = requests.get(f"{base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {str(e)}")
        return None

@app.route('/')
def index():
    # Fetch popular anime
    if not anime_cache['popular']:
        popular_data = fetch_anime_data('top/anime', {'filter': 'bypopularity', 'limit': 20})
        anime_cache['popular'] = popular_data['data'] if popular_data else []

    # Fetch trending anime
    if not anime_cache['trending']:
        trending_data = fetch_anime_data('top/anime', {'filter': 'airing', 'limit': 10})
        anime_cache['trending'] = trending_data['data'] if trending_data else []

    # Fetch seasonal anime
    if not anime_cache['seasonal']:
        seasonal_data = fetch_anime_data('seasons/now', {'limit': 10})
        anime_cache['seasonal'] = seasonal_data['data'] if seasonal_data else []

    return render_template('index.html', 
                         popular_anime=anime_cache['popular'],
                         trending_anime=anime_cache['trending'],
                         seasonal_anime=anime_cache['seasonal'])

@app.route('/api/anime/popular')
def get_popular_anime():
    if not anime_cache['popular']:
        data = fetch_anime_data('top/anime', {'filter': 'bypopularity', 'limit': 20})
        if data:
            anime_cache['popular'] = data['data']
    return jsonify(anime_cache['popular'] or [])

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    try:
        # Fetch anime details
        response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/full')
        response.raise_for_status()
        anime = response.json()['data']

        # Fetch recommendations
        rec_response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/recommendations')
        recommendations = []
        if rec_response.status_code == 200:
            recommendations = rec_response.json()['data'][:6]  # Limit to 6 recommendations
            recommendations = [rec['entry'] for rec in recommendations]

        return render_template('anime_detail.html', 
                            anime=anime,
                            recommendations=recommendations)
    except requests.RequestException as e:
        app.logger.error(f"Error fetching anime details: {str(e)}")
        return render_template('error.html', message="Failed to load anime details. Please try again later."), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return render_template('error.html', message="An unexpected error occurred."), 500

@app.route('/search')
def search_anime():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    search_data = fetch_anime_data('anime', {
        'q': query,
        'limit': 10,
        'sfw': True
    })
    
    if search_data and 'data' in search_data:
        return jsonify(search_data['data'])
    return jsonify([])

@app.route('/genre/<int:genre_id>')
def genre_anime(genre_id):
    genre_data = fetch_anime_data('anime', {
        'genres': genre_id,
        'limit': 20,
        'sfw': True
    })
    
    if not genre_data or 'data' not in genre_data:
        return render_template('error.html', message="Genre not found")
    
    return render_template('genre.html', 
                         anime_list=genre_data['data'],
                         genre_name=genre_data['data'][0]['genres'][0]['name'])

if __name__ == '__main__':
    app.run(debug=True)
