from fuzzywuzzy import process
import re

import re

def extract_folder_name(user_input):
    # Шаблон для поиска фраз, связанных с открытием папки
    pattern = r'(?:открой папку|зайди в папку|папка|открой|зайди в) (.+)'
    match = re.search(pattern, user_input.lower())
    
    if match:
        return match.group(1).strip()  # Возвращаем название папки
    return None  # Если совпадений нет, возвращаем None
# Определяем команды и их ключевые слова
commands = {
    'open_folder': ['открой папку', 'зайди в папку', 'открой', 'зайди'],
    'get_genres': ['какого жанра фильм', 'что за фильм', 'жанр фильма'],
    'get_film_desc': ['о чем фильм', 'расскажи про что фильм', 'опиши фильм'],
    'google_query': ['найди в интернете', 'поиск в интернете', 'найди'],
    'number_folder': ['зайди в папку', 'открой папку номер'],
    'youtube': ['включи песню', 'включи видео', 'включи видос'],
}
user_input = input("in: ")
# Обработка пользовательского ввода
user_input = user_input.lower()

# Ищем наиболее подходящую команду
best_match = None
best_score = 0

for command, phrases in commands.items():
    for phrase in phrases:
        score = process.extractOne(user_input, [phrase])[1]
        if score > best_score:
            best_score = score
            best_match = command

# Выполняем действие в зависимости от наиболее подходящей команды
if best_match:
    if best_match == 'open_folder':
        print(extract_folder_name(user_input))
        print('open_folder')
    elif best_match == 'get_genres':
        print('get_film_desc')
    elif best_match == 'get_film_desc':
        print('google_query')
    elif best_match == 'google_query':
        print('google_query')
    elif best_match == 'number_folder':
        print('number_folder')
    elif best_match == 'youtube':
        print('youtube')
else:
    print('7')