
import requests
import webbrowser

def search_youtube(song_title):
    api_key = 'AIzaSyD_JQbtkGPQH-0oCsjUAYyp--NpoTv9y5Y'
    api_youtube = 'AIzaSyD_JQbtkGPQH-0oCsjUAYyp--NpoTv9y5Y'
    url = 'https://www.youtube.com/'
    # URL для запроса к YouTube API
    search_url = "https://www.googleapis.com/youtube/v3/search"
    
    # Параметры запроса
    params = {
        'part': 'snippet',
        'q': song_title,
        'type': 'video',
        'key': api_key,
        'maxResults': 1  # Получаем только один результат
    }

    # Выполнение GET-запроса
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['items']:
            video = data['items'][0]
            video_title = video['snippet']['title']
            video_id = video['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            # print(f"Найдена песня: {video_title}\nСсылка: {video_url}")
            webbrowser.open_new(video_url)

        else:
            print("Песня не найдена.")
    else:
        print("Ошибка:", response.status_code)

# Пример использования
# api_key = 'AIzaSyD_JQbtkGPQH-0oCsjUAYyp--NpoTv9y5Y'

# api_key = "ваш_api_ключ"  # Замените на ваш API-ключ
# song_name = input("Введите название песни: ")
# search_youtube(song_name)