document.addEventListener('DOMContentLoaded', () => {
    fetchPopularAnime();
    initializePlayer();
});

async function fetchPopularAnime() {
    try {
        const response = await fetch('/api/anime/popular');
        const animeList = await response.json();
        displayAnime(animeList);
    } catch (error) {
        console.error('Error fetching anime:', error);
    }
}

function displayAnime(animeList) {
    const animeGrid = document.getElementById('popularAnime');
    if (!animeGrid) return;
    
    animeGrid.innerHTML = '';

    animeList.forEach(anime => {
        const animeCard = document.createElement('div');
        animeCard.className = 'anime-card';
        animeCard.innerHTML = `
            <a href="/anime/${anime.id}">
                <img src="${anime.image}" alt="${anime.title}">
                <div class="anime-info">
                    <h3>${anime.title}</h3>
                    <div class="anime-meta">
                        <div class="rating">
                            <i class="fas fa-star"></i>
                            <span>${anime.rating}</span>
                        </div>
                        <div class="episodes">
                            <i class="fas fa-film"></i>
                            <span>${anime.episodes} eps</span>
                        </div>
                    </div>
                    <div class="anime-type">${anime.type}</div>
                </div>
            </a>
        `;
        
        animeCard.addEventListener('mouseenter', () => {
            animeCard.style.transform = 'translateY(-10px)';
        });
        
        animeCard.addEventListener('mouseleave', () => {
            animeCard.style.transform = 'translateY(0)';
        });

        animeGrid.appendChild(animeCard);
    });
}

// Initialize Plyr video player
function initializePlayer() {
    const player = document.querySelector('#player');
    if (player) {
        new Plyr(player, {
            controls: [
                'play-large',
                'play',
                'progress',
                'current-time',
                'duration',
                'mute',
                'volume',
                'captions',
                'settings',
                'pip',
                'fullscreen'
            ],
            settings: ['captions', 'quality', 'speed'],
            quality: {
                default: 720,
                options: [1080, 720, 480, 360]
            }
        });
    }
}

// Function to load episode (this is a placeholder - you'll need to implement actual video sources)
async function loadEpisode(animeId, episodeNumber) {
    const videoContainer = document.querySelector('.video-player-container');
    const player = document.querySelector('#player');
    
    if (videoContainer && player) {
        videoContainer.style.display = 'block';
        // Here you would normally fetch the video URL from your backend
        // For now, we'll just show a message
        alert('Video playback functionality will be implemented with actual video sources');
    }
}

// Add smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});
