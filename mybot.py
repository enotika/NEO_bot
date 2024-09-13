from folder_finder import find_and_open_folders
import re
import os
from films import search_movie_on_google, search_movie_description
from google import open_google_search
from find_youtube_video import search_youtube

import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from fuzzywuzzy import process
import re

commands = {
    'open_folder': 
        r'.*?(?:открой папку|зайди в папку|открой|зайди) (.+)$',
        
    'get_genres': 
        r'.*?(?:какого жанра фильм|жанр фильма|жанры фильма|жанры мультфильма|жанры сериала|жанры кино) (.+)$',
        
    'get_film_desc': 
        r'.*?(?:о чем фильм|что за фильм|расскажи про что фильм|опиши фильм|о чем мультфильм|что за мультфильм|расскажи про что мультфильм|опиши мультфильм|о чем сериал|что за сериал|расскажи про что сериал|опиши сериал) (.+)$',
        
    'google_query': 
        r'.*?(?:найди в интернете|поиск в интернете|найди|загугли) (.+)$',
        
    'number_folder': 
        r'.*?(?:зайди в папку номер|открой папку номер) (\d+)$',
        
    'youtube': 
        r'.*?(?:включи песню|включи видео|включи видос|запусти песню|запусти видео|хочу послушать|хочу посмотреть|включи музыку|включи трек|включи клип|поставь песню|включи что-то) (.+)$',
        
    'where_am_i': 
        r'.*?(?:где я|в какой папке я|в какой директории я|где нахожусь|в каком месте я|где ты меня оставил) ?$',
        
    'show_current_folder': 
        r'.*?(?:ls|покажи что в папке текущей|покажи содержимое текущей папки|что в текущей папке|что в папке|покажи содержимое папки) ?$',
        
    'go_up_folder': 
        r'.*?(?:up|выйди в папку выше|подняться на уровень вверх|выйти на уровень выше|перейти в родительскую папку|подняться на один уровень) ?$',
        
    'enter_subfolder': 
        r'.*?(?:cd|войди в подпапку|зайди в подпапку|открой подпапку|перейди в подпапку) (.+)$',
        
    'create_file': 
        r'.*?(?:touch|создай файл|создать файл|создай документ|добавь файл) (.+)$',
        
    'delete_file': 
        r'.*?(?:delete|удали файл|удалить файл|убери файл|сотри файл) (.+)$',
}

# Инициализация устройства
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Загрузка данных для модели
with open("intents.json") as json_data:
    intents = json.load(json_data)

data_dir = os.path.dirname(__file__)
FILE = os.path.join(data_dir, 'chatdata.pth')
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Инициализация модели
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
class ChatBot:
    def __init__(self):
        self.current_path = os.getcwd()  # Начинаем с текущей директории
        # self.responses = {
        #     "привет": "Привет! Как я могу помочь?",
        #     "как дела?": "У меня всё хорошо, спасибо!",
        #     "пока": "До свидания! Удачи!",
        #     "спасибо": "Не за что! Был рад вам помочь!",
        # }
    def handle_chatbot_response(self, msg):
        # Обработка сообщения с использованием нейронной сети
        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        
        return "Извините, я не понимаю. Можете переформулировать?"
    def get_response(self, user_input):
        # Обработка пользовательского ввода
        
        # pattern = r'^открой папку (.+?)$'
        pattern = commands["open_folder"]
        # print(pattern)
        match_open_folder = re.match(pattern, user_input.lower())
        # print('goodf')
        # pattern = r'^какого жанра фильм (.+)$'
        pattern = commands["get_genres"]
        # print(pattern)
        match_get_genres = re.match(pattern, user_input.lower())

        # pattern = r'^о чем фильм (.+)$'
        pattern = commands["get_film_desc"]
        # print(pattern)
        match_get_film_desc = re.match(pattern, user_input.lower())

        # pattern = r'^найди в интернете (.+)$'
        pattern = commands["google_query"]
        match_google_query = re.match(pattern, user_input.lower())

        # pattern = r'^зайди в папку (\d+)$'  # Ожидаем слово "зайди в папку" и номер папки
        pattern = commands["number_folder"]
        match_number_folder = re.match(pattern, user_input.lower())

        # pattern = r'^включи (песню|видео|видос) (.+)$'
        pattern = commands["youtube"]
        match_youtube = re.match(pattern, user_input.lower())

        if match_open_folder:
            folder_name = match_open_folder.group(1)  # Извлекаем название папки
            return find_and_open_folders(folder_name)
            # print(f"Команда корректна. Название папки: {folder_name}")

        elif match_get_genres:
            film_name = match_get_genres.group(1).strip() # Извлекаем название папки
            return search_movie_on_google(film_name)
        
        elif match_get_film_desc:
            film_name = match_get_film_desc.group(1).strip() # Извлекаем название папки
            return search_movie_description(film_name)
        elif match_google_query:
            google_query = match_google_query.group(1).strip() # Извлекаем название папки
            return open_google_search(google_query)
        elif match_youtube:
            # media_type = match_youtube.group(1)  # Извлекаем тип медиа (песня, видео, видос)
            media_name = match_youtube.group(1)  # Извлекаем номер медиа
            search_youtube(media_name)
            return f"Включаю {media_name}: {media_name}"
        elif re.match(commands['enter_subfolder'], user_input):  # Переход в папку
            # folder_name = user_input[3:].strip()
            folder_name = re.match(commands["enter_subfolder"], user_input).group(1).strip()
            new_path = os.path.join(self.current_path, folder_name)

            if os.path.isdir(new_path):
                self.current_path = new_path
                return f"Перешел в папку {folder_name}"
            else:
                return("Папка не найдена.")

        elif re.match(commands["go_up_folder"], user_input.lower()):  # Переход на уровень выше
            self.current_path = os.path.dirname(self.current_path)
            return f"Перешел на уровень выше. Текущая папка {self.current_path}"
        elif re.match(commands['where_am_i'], user_input.lower()):  # Переход на уровень выше
            return f"Текущая папка {self.current_path}"
        elif re.match(commands['show_current_folder'], user_input.lower()):  # Показать содержимое
            try:
                items = os.listdir(self.current_path)
            except PermissionError:
                return("Нет доступа к этой папке.")
            ans = ""
            ans += "Содержимое текущей папки:\n"
            # print("Содержимое текущей папки:")
            for index, item in enumerate(items):
                # print(f"{index + 1}. {item}")
                ans += f"{index + 1}. {item}\n"
            return ans
        
        elif re.match(commands['create_file'], user_input.lower()):
            # file_name = user_input[6:].strip()
            file_name = re.match(commands['create_file'], user_input.lower()).group(1).strip()
            file_path = os.path.join(self.current_path, file_name)

            with open(file_path, 'w') as file:
                file.write("Это новый файл.\n")
                file.write("Файл был создан успешно!")
            return(f'Файл "{file_name}" создан в {self.current_path}.')
        
        elif re.match(commands['delete_file'], user_input.lower()):  # Удаление файла
            # file_name = user_input[7:].strip()
            file_name = re.match(commands['delete_file'], user_input.lower()).group(1).strip()
            file_path = os.path.join(self.current_path, file_name)

            if os.path.isfile(file_path):
                os.remove(file_path)
                return(f'Файл "{file_name}" удален.')
            else:
                return("Файл не найден.")
        elif match_number_folder:
            folder_number = int(match_number_folder.group(1).strip())  # Извлекаем номер папки
            try:
                items = os.listdir(self.current_path)
            except PermissionError:
                return("Нет доступа к этой папке.")
            if folder_number > len(items) or folder_number < 1:
                return "Нет такой папки!"
            if os.path.isfile(items[folder_number-1]):
                return(f"{items[folder_number-1]} — файл, нельзя в него перейти.")
            elif os.path.isdir(items[folder_number-1]):
                new_path = os.path.join(self.current_path, items[folder_number-1])
                if os.path.isdir(new_path):
                    self.current_path = new_path
                return(f"{self.current_path} — папка. Перехожу в нее.")
            return(f"{items[folder_number-1]} — файл, нельзя в него перейти.")
        return self.handle_chatbot_response(user_input)
        # return self.responses.get(user_input.lower(), "Извините, я не понимаю. Можете переформулировать?")