import bs4
import time
import csv
import pyautogui
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                      options=chrome_options) as driver:  # Открываем хром
    driver.get(
        "https://yandex.ru/maps/org/medsi/1236981588/?ll=37.324155%2C55.873561&z=17")  # Открываем страницу
    # pyautogui.moveTo(260, 250, duration=0.25)
    # pyautogui.middleClick()
    # pyautogui.move(0, 200, duration=0.25)
    # time.sleep(25)  # Время на прогрузку страницы
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
                site = 'None'
                print('None')
            social = soup.find('div', class_='business-contacts-view__social-button').find_all('a', href=True)
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

            # fields = ['Maps', 'City', 'Value', 'Name', 'Reiting', 'Adress', 'Phone', 'URL', 'Site', 'Social_1',
            #           'Social_2', 'Social_3', 'Social_4', 'Social_5']
            # storage = {'maps': maps, 'city': city, 'value': value, 'name': head, 'reiting': otzivy, 'adress': adress,
            #            'phone': phone, 'url': url, 'site': web_site, 'social_1': soc_net_1, 'social_2': soc_net_2,
            #            'social_3': soc_net_3, 'social_4': soc_net_4, 'social_5': soc_net_5}
            #
            # with open('maps_yandex.csv', 'a+', encoding='utf-16') as file:
            #     pisar = csv.writer(file, delimiter=';', lineterminator='\r')
            #
            #     # Проверяем, находится ли файл в начале и пуст ли
            #     file.seek(0)
            #     if len(file.read()) == 0:
            #         pisar.writerow(fields)  # Записываем заголовки, только если файл пуст
            #
            #     pisar.writerow([storage['maps'], storage['city'], storage['value'], storage['name'], storage['reiting'],
            #                     storage['adress'], storage['phone'], storage['url'], storage[web_site],
            #                     storage[soc_net_1], storage[soc_net_2], storage[soc_net_3], storage[soc_net_4],
            #                     storage[soc_net_5]])
