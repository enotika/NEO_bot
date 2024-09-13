from imdb import IMDb
from googletrans import Translator

import requests
from bs4 import BeautifulSoup

import re


def search_movie_description(query):
    query = f"{query} фильм википедия описание"
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return "Ошибка при получении данных из Google."
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.find('span', class_='hgKElc')
    # print(first_result)

    if not first_result:
        return "Результат не найден."
    
    return first_result.get_text()

# # Пример использования
# movie_title = "головоломка фильм википедия описание"  # Замените на название фильма (английское название для IMDb)
# description = search_movie_description(movie_title)
# print(f"Описание фильма '{movie_title}':\n{description}")


def translate_genres(genres, dest_language='ru'):
    translator = Translator()
    translations = translator.translate(genres, dest=dest_language)
    return [translation.text for translation in translations]

movie_title = "головоломка"  # Замените на название фильма (английское название для IMDb)

def search_movie_on_google(query):
    query = f"{query} фильм жанры"
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return "Ошибка при получении данных из Google."
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.find('div', class_='bVj5Zb FozYP')
    # print(first_result)

    all_genres=[]
    second_result = soup.find_all('div', class_='bVj5Zb FozYP')
    # print(second_result)
    for i in second_result:
        # print(i.get_text())
        all_genres.append(i.get_text())
    if not first_result:
        return "Результат не найден."
    
    # return all_genres
    return (f"Первый результат поиска в Google:\n{all_genres}")

# <div class="bVj5Zb FozYP">Боевик</div>

# search_query = f"{movie_title} фильм жанры"
# search_result = search_movie_on_google(search_query)
# print(f"Первый результат поиска в Google:\n{search_result}")