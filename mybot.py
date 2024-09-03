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
        self.responses = {
            "привет": "Привет! Как я могу помочь?",
            "как дела?": "У меня всё хорошо, спасибо!",
            "пока": "До свидания! Удачи!",
            "спасибо": "Не за что! Был рад вам помочь!",
        }
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
            # Простой поиск ответа
            # Регулярное выражение для проверки формата
        pattern = r'^открой папку (.+?)$'
        match_open_folder = re.match(pattern, user_input.lower())

        pattern = r'^какого жанра фильм (.+)$'
        match_get_genres = re.match(pattern, user_input.lower())

        pattern = r'^о чем фильм (.+)$'
        match_get_film_desc = re.match(pattern, user_input.lower())
        pattern = r'^найди в интернете (.+)$'
        match_google_query = re.match(pattern, user_input.lower())
        pattern = r'^зайди в папку (\d+)$'  # Ожидаем слово "зайди в папку" и номер папки
        match_number_folder = re.match(pattern, user_input.lower())
        pattern = r'^включи (песню|видео|видос) (.+)$'
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
            media_type = match_youtube.group(1)  # Извлекаем тип медиа (песня, видео, видос)
            media_name = match_youtube.group(2)  # Извлекаем номер медиа
            search_youtube(media_name)
            return f"Включаю {media_type}: {media_name}"
        elif user_input.startswith("cd "):  # Переход в папку
            folder_name = user_input[3:].strip()
            new_path = os.path.join(self.current_path, folder_name)

            if os.path.isdir(new_path):
                self.current_path = new_path
                return f"Перешел в папку {folder_name}"
            else:
                return("Папка не найдена.")

        elif user_input == "up":  # Переход на уровень выше
            self.current_path = os.path.dirname(self.current_path)
            return f"Перешел на уровень выше. Текущая папка {self.current_path}"
        elif user_input.lower() == "где я":  # Переход на уровень выше
            return f"Текущая папка {self.current_path}"
        elif user_input == "ls":  # Показать содержимое
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
        
        elif user_input.startswith("touch "):
            file_name = user_input[6:].strip()
            file_path = os.path.join(self.current_path, file_name)

            with open(file_path, 'w') as file:
                file.write("Это новый файл.\n")
                file.write("Файл был создан успешно!")
            return(f'Файл "{file_name}" создан в {self.current_path}.')
        
        elif user_input.startswith("delete "):  # Удаление файла
            file_name = user_input[7:].strip()
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