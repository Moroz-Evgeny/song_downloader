html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Музыкальный плеер</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎵</text></svg>">
   <style>
    :root {
    --primary-color: #6c5ce7;
    --primary-light: #a29bfe;
    --dark-color: #2d3436;
    --light-color: #f5f6fa;
    --gray-color: #dfe6e9;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
    color: var(--dark-color);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.player-app {
    width: 100%;
    max-width: 400px;
    background-color: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    height: 700px;
}

.header {
    background-color: white;
    padding: 20px;
    text-align: center;
    box-shadow: var(--shadow);
}

.logo {
    font-size: 22px;
    font-weight: 700;
    color: var(--primary-color);
}

.search-container {
    display: flex;
    margin-top: 15px;
}

.search-input {
    flex: 1;
    padding: 12px 16px;
    border: 2px solid var(--gray-color);
    border-radius: 30px 0 0 30px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s;
}

.search-input:focus {
    border-color: var(--primary-color);
}

.search-button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 0 30px 30px 0;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.search-button:hover {
    background-color: var(--primary-light);
}

.content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

.results-container {
    margin-top: 10px;
}

.results-title {
    margin-bottom: 15px;
    font-size: 18px;
    font-weight: 600;
    color: var(--dark-color);
}

.track-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.track-card {
    background-color: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
    display: flex;
    align-items: center;
    padding: 12px;
}

.track-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.track-artwork {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    object-fit: cover;
    margin-right: 12px;
    background-color: var(--gray-color);
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--primary-color);
    font-size: 20px;
    overflow: hidden;
}

.track-artwork img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}

.track-info {
    flex: 1;
    min-width: 0;
}

.track-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.track-artist {
    color: #636e72;
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.play-button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    display: flex;
    justify-content: center;
    align-items: center;
}

.play-button:hover {
    background-color: var(--primary-light);
}

.player-container {
    background-color: white;
    padding: 20px;
    border-top: 1px solid var(--gray-color);
}

.now-playing {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.now-playing-artwork {
    width: 80px;
    height: 80px;
    border-radius: 12px;
    object-fit: cover;
    margin-right: 15px;
    background-color: var(--gray-color);
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--primary-color);
    font-size: 30px;
    overflow: hidden;
}

.now-playing-artwork img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 12px;
}

.now-playing-info {
    flex: 1;
    min-width: 0;
}

.now-playing-title {
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.now-playing-artist {
    font-size: 14px;
    color: #636e72;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.player-controls {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.progress-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.time {
    font-size: 12px;
    color: #636e72;
    min-width: 35px;
}

.progress-bar {
    flex: 1;
    height: 4px;
    background-color: var(--gray-color);
    border-radius: 2px;
    overflow: hidden;
    cursor: pointer;
}

.progress {
    height: 100%;
    background-color: var(--primary-color);
    width: 0%;
    transition: width 0.1s;
}

.control-buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 25px;
}

.control-button {
    background: none;
    border: none;
    font-size: 20px;
    color: var(--dark-color);
    cursor: pointer;
    transition: color 0.3s;
}

.control-button:hover {
    color: var(--primary-color);
}

.play-pause {
    font-size: 36px;
}

.loading {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--gray-color);
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #636e72;
}

.empty-state h3 {
    margin-bottom: 10px;
    font-weight: 600;
}

.hidden {
    display: none;
}
   </style>
</head>
<body>
    <div class="player-app">
        <div class="header">
            <div class="logo">Музыкальный плеер</div>
            <div class="search-container">
                <input type="text" class="search-input" placeholder="Поиск музыки..." id="searchInput">
                <button class="search-button" id="searchButton">Найти</button>
            </div>
        </div>

        <div class="content">
            <div class="results-container" id="resultsContainer">
                <div class="empty-state">
                    <h3>Начните поиск музыки</h3>
                    <p>Введите запрос в поле поиска, чтобы найти треки</p>
                </div>
            </div>
        </div>

        <div class="player-container hidden" id="playerContainer">
            <div class="now-playing">
                <div class="now-playing-artwork" id="nowPlayingArtwork">🎵</div>
                <div class="now-playing-info">
                    <div class="now-playing-title" id="nowPlayingTitle">Название трека</div>
                    <div class="now-playing-artist" id="nowPlayingArtist">Исполнитель</div>
                </div>
            </div>
            <div class="player-controls">
                <div class="progress-container">
                    <div class="time" id="currentTime">0:00</div>
                    <div class="progress-bar">
                        <div class="progress" id="progress"></div>
                    </div>
                    <div class="time" id="duration">0:00</div>
                </div>
                <div class="control-buttons">
                    <button class="control-button" id="prevButton">⏮</button>
                    <button class="control-button play-pause" id="playPauseButton">▶</button>
                    <button class="control-button" id="nextButton">⏭</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Базовый URL API через CORS прокси
        const API_BASE_URL = 'http://144.31.72.235:8080';
        
        // Элементы DOM
        const searchInput = document.getElementById('searchInput');
        const searchButton = document.getElementById('searchButton');
        const resultsContainer = document.getElementById('resultsContainer');
        const playerContainer = document.getElementById('playerContainer');
        const nowPlayingTitle = document.getElementById('nowPlayingTitle');
        const nowPlayingArtist = document.getElementById('nowPlayingArtist');
        const nowPlayingArtwork = document.getElementById('nowPlayingArtwork');
        const playPauseButton = document.getElementById('playPauseButton');
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        const progress = document.getElementById('progress');
        const currentTime = document.getElementById('currentTime');
        const duration = document.getElementById('duration');

        // Аудио элемент
        const audio = new Audio();
        let currentTrackIndex = 0;
        let tracks = [];

        // Поиск треков
        async function searchTracks(query, limit = 50) {
            try {
                resultsContainer.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
                
                const response = await fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}&limit=${limit}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Добавляем проверку структуры данных
                if (!data || typeof data !== 'object') {
                    throw new Error('Некорректный формат данных от сервера');
                }
                
                displayTracks(data);
            } catch (error) {
                console.error('Ошибка:', error);
                resultsContainer.innerHTML = `
                    <div class="empty-state">
                        <h3>Ошибка при поиске</h3>
                        <p>${error.message}</p>
                        <p>Попробуйте еще раз или используйте другой запрос</p>
                    </div>
                `;
            }
        }

        // Отображение результатов поиска
        function displayTracks(tracksData) {
            // Проверяем, что tracksData существует и имеет поле results
            if (!tracksData || !tracksData.results || tracksData.results.length === 0) {
                resultsContainer.innerHTML = '<div class="empty-state"><h3>Ничего не найдено</h3><p>Попробуйте изменить запрос</p></div>';
                return;
            }

            // Используем tracksData.results вместо tracksData
            tracks = tracksData.results;
            
            let html = '<h2 class="results-title">Результаты поиска</h2>';
            html += '<div class="track-list">';
            
            tracks.forEach((track, index) => {
                const artwork = track.artwork || '';
                html += `
                    <div class="track-card" data-index="${index}">
                        <div class="track-artwork">
                            ${artwork ? `<img src="${artwork}" alt="${track.title}" />` : '🎵'}
                        </div>
                        <div class="track-info">
                            <div class="track-title">${track.title || 'Неизвестный трек'}</div>
                            <div class="track-artist">${track.artist || 'Неизвестный исполнитель'}</div>
                        </div>
                        <button class="play-button" data-index="${index}">▶</button>
                    </div>
                `;
            });
            
            html += '</div>';
            resultsContainer.innerHTML = html;
            
            // Добавляем обработчики событий для кнопок воспроизведения
            document.querySelectorAll('.play-button').forEach(button => {
                button.addEventListener('click', function(e) {
                    e.stopPropagation();
                    const index = parseInt(this.getAttribute('data-index'));
                    playTrack(index);
                });
            });
            
            // Добавляем обработчики для карточек треков
            document.querySelectorAll('.track-card').forEach(card => {
                card.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    playTrack(index);
                });
            });
        }

        // Воспроизведение трека
        async function playTrack(index) {
            if (index < 0 || index >= tracks.length) return;
            
            currentTrackIndex = index;
            const track = tracks[currentTrackIndex];
            
            try {
                // Получаем URL для потокового воспроизведения
                const response = await fetch(`${API_BASE_URL}/stream/${track.id}`);
                
                if (!response.ok) {
                    throw new Error('Ошибка при получении URL трека');
                }
                
                const data = await response.json();
                
                // Устанавливаем источник аудио - исправлено на data.stream_url
                audio.src = data.stream_url;
                
                // Обновляем информацию о текущем треке
                nowPlayingTitle.textContent = track.title || 'Неизвестный трек';
                nowPlayingArtist.textContent = track.artist || 'Неизвестный исполнитель';
                
                // Обновляем обложку трека
                if (track.artwork) {
                    nowPlayingArtwork.innerHTML = `<img src="${track.artwork}" alt="${track.title}" />`;
                } else {
                    nowPlayingArtwork.innerHTML = '🎵';
                }
                
                // Показываем плеер
                playerContainer.classList.remove('hidden');
                
                // Воспроизводим трек
                audio.play();
                playPauseButton.textContent = '⏸';
                
            } catch (error) {
                console.error('Ошибка при воспроизведении:', error);
                alert('Не удалось воспроизвести трек');
            }
        }

        // Форматирование времени
        function formatTime(seconds) {
            if (isNaN(seconds)) return '0:00';
            
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
        }

        // Обновление прогресса воспроизведения
        function updateProgress() {
            const percent = (audio.currentTime / audio.duration) * 100;
            progress.style.width = `${percent}%`;
            currentTime.textContent = formatTime(audio.currentTime);
            
            if (!isNaN(audio.duration)) {
                duration.textContent = formatTime(audio.duration);
            }
        }

        // Обработчики событий
        searchButton.addEventListener('click', () => {
            const query = searchInput.value.trim();
            if (query) {
                searchTracks(query);
            }
        });

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    searchTracks(query);
                }
            }
        });

        playPauseButton.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playPauseButton.textContent = '⏸';
            } else {
                audio.pause();
                playPauseButton.textContent = '▶';
            }
        });

        prevButton.addEventListener('click', () => {
            if (currentTrackIndex > 0) {
                playTrack(currentTrackIndex - 1);
            }
        });

        nextButton.addEventListener('click', () => {
            if (currentTrackIndex < tracks.length - 1) {
                playTrack(currentTrackIndex + 1);
            }
        });

        // Перемотка трека
        progress.parentElement.addEventListener('click', (e) => {
            const progressBar = e.currentTarget;
            const rect = progressBar.getBoundingClientRect();
            const clickPosition = e.clientX - rect.left;
            const width = progressBar.offsetWidth;
            const duration = audio.duration;
            
            if (!isNaN(duration)) {
                audio.currentTime = (clickPosition / width) * duration;
            }
        });

        // События аудио
        audio.addEventListener('timeupdate', updateProgress);
        
        audio.addEventListener('ended', () => {
            playPauseButton.textContent = '▶';
            
            // Автопереход к следующему треку
            if (currentTrackIndex < tracks.length - 1) {
                playTrack(currentTrackIndex + 1);
            }
        });

        audio.addEventListener('loadedmetadata', () => {
            duration.textContent = formatTime(audio.duration);
        });

        audio.addEventListener('error', (e) => {
            console.error('Ошибка воспроизведения:', e);
            alert('Ошибка при воспроизведении трека. Возможно, трек недоступен.');
        });
    </script>
</body>
</html>
"""