import bs4
import time
import pyautogui
import csv
import random
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

# Список пользовательских агентов
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/112.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'
]


# Функция для получения случайного пользовательского агента
def get_random_user_agent():
    return random.choice(user_agents)


# Настройка браузера
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

print(
    'Введите категорию из списка: еда, кафе, продукты, салоны красоты, аптеки, гостиницы, азс, спорт, больницы, автосервисы')
category = input().lower()
print('Введите название файла...')
file_name = input().lower()
with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                      options=chrome_options) as driver:  # Открываем хром
    driver.get(
        f"https://yandex.ru/maps/51/samara/search/{category}/?ll=50.181841%2C53.251307&sll=50.061318%2C53.322139&sspn=1.375249%2C0.458164&z=11.52")  # Открываем страницу
    pyautogui.moveTo(260, 250, duration=0.25)
    pyautogui.middleClick()
    pyautogui.move(0, 200, duration=0.25)
    time.sleep(50)  # Время на прогрузку страницы
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    heads = soup.find('ul', class_='search-list-view__list').find_all('li')
    print(len(heads))
    for i in heads:
        w = i.find_next('a', class_='search-snippet-view__link-overlay _focusable', href=True)
        # print('https://yandex.ru'+w['href'])
        url = ('https://yandex.ru' + w['href'])
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options) as driver:  # Открываем хром
            driver.get(url)
            time.sleep(3)
            soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            name = soup.find('div', class_='orgpage-header-view__header-wrapper').find('h1')
            print(name.text.strip())
            head = (name.text.strip())
            reiting = soup.find('span', class_='business-rating-badge-view__rating-text')
            print(reiting.text.strip())
            otzivy = (reiting.text.strip())
            element = soup.find('a', attrs={'class': 'orgpage-header-view__address'})
            # Извлечение данных из атрибута aria-label
            aria_label = element['aria-label'].replace('на карте Самары', '')
            # print("Извлеченные данные из aria-label:")
            print(aria_label.replace('на карте Самарской области', ''))
            adress = (aria_label.replace('на карте Самарской области', ''))
            try:
                tel = soup.find('div', class_='orgpage-phones-view__phone-number')
                print(tel.text.strip())
                phone = (tel.text.strip())
            except:
                print('None')
                phone = 'None'
            uslugy = soup.find('div', class_='business-card-view__breadcrumbs').find_all('a')
            maps = uslugy[0].text.strip()
            print(maps)
            city = uslugy[1].text.strip()
            print(city)
            value = uslugy[2].text.strip()
            print(value)
            try:
                site = soup.find('div', class_='business-urls-view__url')
                print(site.text.strip())
                web_site = (site.text.strip())
            except:
                web_site = 'None'
                print('None')
            try:
                social = soup.find('div', class_='business-contacts-view__social-button').find_all('a', href=True)
            except:
                continue
            try:
                soc_net_1 = social[0]['href']
                print(soc_net_1)
            except:
                soc_net_1 = 'None'
                print('None')
            try:
                soc_net_2 = social[1]['href']
                print(soc_net_2)
            except:
                soc_net_2 = 'None'
                print('None')
            try:
                soc_net_3 = social[2]['href']
                print(soc_net_3)
            except:
                soc_net_3 = 'None'
                print('None')
            try:
                soc_net_4 = social[3]['href']
                print(soc_net_4)
            except:
                soc_net_4 = 'None'
                print('None')
            try:
                soc_net_5 = social[4]['href']
                print(soc_net_1)
            except:
                soc_net_5 = 'None'
                print('None')
            print('\n')

            fields = ['Maps', 'City', 'Value', 'Name', 'Reiting', 'Adress', 'Phone', 'URL', 'Site', 'Social']
            storage = {'maps': maps, 'city': city, 'value': value, 'name': head, 'reiting': otzivy, 'adress': adress,
                       'phone': phone, 'url': url, 'site': web_site, 'social_1': soc_net_1, 'social_2': soc_net_2,
                       'social_3': soc_net_3, 'social_4': soc_net_4, 'social_5': soc_net_5}

            with open(f'{file_name}.csv', 'a+', encoding='utf-16') as file:
                pisar = csv.writer(file, delimiter=';', lineterminator='\r')

                # Проверяем, находится ли файл в начале и пуст ли
                file.seek(0)
                if len(file.read()) == 0:
                    pisar.writerow(fields)  # Записываем заголовки, только если файл пуст

                    # Проверяем, что значение ключа 'name' не равно "Апрель"
                # if storage['name'] != f'{head}':
                pisar.writerow(
                    [storage['maps'], storage['city'], storage['value'], storage['name'], storage['reiting'],
                     storage['adress'], storage['phone'], storage['url'], storage['site'],
                     storage['social_1']])
