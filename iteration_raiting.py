import requests
from bs4 import BeautifulSoup

# Список URL-адресов
urls = [
    "https://2gis.ru/moscow/firm/4504128908692489",
    "https://2gis.ru/moscow/firm/70000001075883171",
    "https://2gis.ru/moscow/firm/4504127908730763",
    "https://2gis.ru/moscow/firm/4504128908927772",
    "https://2gis.ru/moscow/firm/4504128908692471",
    "https://2gis.ru/moscow/firm/70000001024590137",
    "https://2gis.ru/moscow/firm/70000001021638184",
    "https://2gis.ru/moscow/firm/70000001045067707",
    "https://2gis.ru/moscow/firm/4504127908669448",
    "https://2gis.ru/moscow/firm/4504127919941973",
    "https://2gis.ru/moscow/firm/4504127908575502",
    "https://2gis.ru/shchelkovo/firm/70000001052133720",
    "https://2gis.ru/moscow/firm/70000001086874241",
    "https://2gis.ru/moscow/firm/4504127915873896",
    "https://2gis.ru/moscow/firm/4504128908431383",
    "https://2gis.ru/moscow/firm/70000001045068990",
    "https://2gis.ru/moscow/firm/70000001077021315",
    "https://2gis.ru/moscow/firm/70000001068037941",
    "https://2gis.ru/moscow/firm/70000001066037776",
    "https://2gis.ru/moscow/firm/70000001066795842",
    "https://2gis.ru/moscow/firm/70000001066876850",
    "https://2gis.ru/moscow/firm/70000001065611234",
    "https://2gis.ru/moscow/firm/70000001063143981",
    "https://2gis.ru/moscow/firm/70000001062516235",
]


def extract_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешность запроса
        soup = BeautifulSoup(response.content, 'html.parser')

        # Предположим, что интересующий вас контент хранится внутри тегов <div> или <p>
        content_divs = soup.find_all(['div', 'p'])  # Можно изменить на конкретный тег и класс, если требуется
        text_content = "\n".join(div.get_text() for div in content_divs)
        return text_content.strip()
    except requests.RequestException as e:
        print(f"Ошибка при обработке URL {url}: {str(e)}")
        return None


# Перебор URL и сбор контента
for url in urls:
    content = extract_content(url)
    if content:
        print(f"Содержимое URL {url}:\n{content}\n")
    else:
        print(f"Не удалось получить содержимое для URL {url}.\n")
