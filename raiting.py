import bs4
import time
import csv
import openpyxl
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

# Загрузка файла Excel
workbook = openpyxl.load_workbook('рестораны.xlsx')
sheet = workbook.active

# Извлечение ссылок из указанного столбца
urls = []
for row in sheet.iter_rows(min_row=2, max_col=1,
                           values_only=True):  # min_row=2 предполагает, что первая строка - заголовок
    if row[0] is not None:
        urls.append(row[0])

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        for url in urls:
            with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_options) as driver:  # Открываем хром
                driver.get(url)  # Открываем страницу
                time.sleep(5)
                soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
                name = soup.find('h1', {'class': 'orgpage-header-view__header'}).text.strip()
                print(name)
                raiting = soup.find('span', {'class': 'business-rating-badge-view__rating-text'}).text.strip()
                print(raiting)
                ocenky = soup.find('div', {'class': 'business-header-rating-view__text _clickable'}).text.strip()
                print(ocenky)

                storage = {'name': name, 'raiting': raiting, 'ocenky': ocenky}

                # fields = ['Name', 'Raiting', 'Ocenky']
                # with open('ya_maps.csv', 'a+', encoding='utf-16') as f:
                #     pisar = csv.writer(f, delimiter=';', lineterminator='\r')
                #     # Проверяем, находится ли файл в начале и пуст ли
                #     f.seek(0)
                #     if len(f.read()) == 0:
                #         pisar.writerow(fields)  # Записываем заголовки, только если файл пуст
                #     pisar.writerow([storage['name'], storage['raiting'], storage['ocenky']])
