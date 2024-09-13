import os
import subprocess
import re

# Функция для поиска папок
def search_folders(path, folder_name):
    found_folders = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            if dir_name == folder_name:
                found_folders.append(os.path.join(root, dir_name))
    return found_folders

def find_and_open_folders(folder_name, search_path='/'):

    # Начинаем поиск с корневой директории
    
    found_folders = search_folders(search_path, folder_name)

    # Открытие найденных папок
    for folder in found_folders:
        subprocess.run(['xdg-open', folder])  # Для Linux
        # subprocess.run(['open', folder])  # Для MacOS
        # subprocess.run(['explorer', folder])  # Для Windows
    if not found_folders:
        return("Папки не найдены.")
    return(f"Открываю папки: {found_folders}")

    

# # Пример использования
# folder_to_find = "bot_with_gui"
# find_and_open_folders(folder_to_find)