import sqlite3
from sqlite3 import Error
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")


# Функция для подключения к базе данных и создания таблицы
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS ratings (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                rating text NOT NULL,
                                ocenky text NOT NULL
                            ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_data(conn, name, rating, ocenky):
    sql = ''' INSERT INTO ratings(name, rating, ocenky)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, rating, ocenky))
    conn.commit()
    return cur.lastrowid


# Извлечение данных с сайта
with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                      options=chrome_options) as driver:  # Открываем хром
    driver.get(
        "https://yandex.ru/maps/org/medsi/1236981588/?ll=37.324155%2C55.873561&z=17")  # Открываем страницу
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    name = soup.find('h1', {'class': 'orgpage-header-view__header'}).text.strip()
    print(name)
    rating = soup.find('span', {'class': 'business-rating-badge-view__rating-text'}).text.strip()
    print(rating)
    ocenky = soup.find('div', {'class': 'business-header-rating-view__text _clickable'}).text.strip()
    print(ocenky)

    # Подключение к базе данных
    database = "test.db"

    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        insert_data(conn, name, rating, ocenky)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
