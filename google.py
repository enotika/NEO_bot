import webbrowser

def open_google_search(query):
    # Форматирование URL для поиска в Google
    text = f"Открываю запрос \"{query}\""
    query = query.replace(' ', '+')  # Заменяем пробелы на +
    url = f"https://www.google.com/search?q={query}"
    
    # Открываем страницу в веб-браузере
    webbrowser.open_new(url)
    return text

# Пример использования
# search_query = "как программировать на Python"
# open_google_search(search_query)

# url = 'https://docs.python.org/'

# # Open URL in a new tab, if a browser window is already open.
# webbrowser.open_new_tab(url)

# # Open URL in new window, raising the window if possible.
# webbrowser.open_new(url)