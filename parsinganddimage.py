from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import pickle
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import json
import os
import shutil


def parsing_olx(page = 1, request = 'Python this is power <3'):
    try:
        shutil.rmtree(f'data_{request}')
    except:
        pass
    _all_ads = []
    image_iterator = 0
    for i in range(1, page + 1):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.headless = True
        browser = webdriver.Chrome(r'D:\pyqtpractice\chromedriver.exe', options=options)

        try:
            browser.get(url=f'https://www.olx.ua/d/list/q-{request}/?page={i}')
            time.sleep(4)
            print(f'Зашёл на страницу {i}.')
            for position, x in enumerate(range(0, 13000, 1000)):
                browser.execute_script(f"window.scrollTo(0, {x});")
                time.sleep(2)
                print(f'{position} / 12 scrolls')
            print(f'Записываю html страницу {i}')
            try:
                with open(f'data_{request}/source_page{i}_olx.html', 'w', encoding='utf8') as file:
                    file.write(browser.page_source)
                    time.sleep(2)
            except:
                os.mkdir(f'data_{request}')
                with open(f'data_{request}/source_page{i}_olx.html', 'w', encoding='utf8') as file:
                    file.write(browser.page_source)
                    time.sleep(2)

        except Exception as ex:
            print(ex)


        with open(f"data_{request}/source_page{i}_olx.html", 'r', encoding='utf8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        all_ads = soup.find_all('div', class_='css-19ucd76')
        for position, ad in enumerate(all_ads):
            try:

                ad_title = ad.find('h6', class_='css-v3vynn-Text eu5v0x0').text
                ad_url = 'https://olx.ua' + ad.find('a', class_='css-1bbgabe').get('href')
                image_url = ad.find('div', class_='css-gl6djm').find('img').get('src')

                r = requests.get(url=image_url).content
                with open(f'data_{request}/{ad_title}.png', 'wb') as file:
                    file.write(r)
                print(f"Скачал картинку {image_iterator}")
                image_iterator += 1
                _all_ads.append({
                    'ad_title': ad_title,
                    'ad_url': ad_url,
                })
                print(f'Засунул в лист {ad_title}')

            except Exception:
                print(None)

    with open(f'data_{request}/resultparsingolx_{request}.json', 'w', encoding='utf8') as file:
        json.dump(_all_ads, file, indent=4, ensure_ascii=False)

    browser.close()
    browser.quit()


def main():
    parsing_olx()


if __name__ == '__main__':
    main()
