import requests
import csv
import re

from ua import ua_random, slep_random

from bs4 import BeautifulSoup

URL = 'https://podolskmd.ru/'
useragent = ua_random()
headers = {'UserAgent': useragent}
params = {'page=': 1}


def get_html(url):
    """
    Одаем текст страницы
    :param url: Основной домен донера
    :return: str html
    """
    r = requests.get(url, headers=headers)
    try:
        return r.text
    except:
        print(f'Не доступный урл {r.url}')


def get_url(html):
    """Собираем урлы категорий"""
    url_list = []
    soup = BeautifulSoup(html, 'lxml')
    url_menu = soup.find(id='menu').find_all('a')
    for i in url_menu:
        if len(i.get('href').split('/')) == 5 and (
                not re.search('albomy', i.get('href')) and not re.search('monety', i.get('href')) and not re.search(
                'index', i.get('href')) and not re.search('bu', i.get('href')) and not re.search('sale',
                                                                                                 i.get('href'))):
            url_list.append(i.get('href'))
    return url_list


def pagination(url):
    """
    Принимает лист с категориями
    Собираем урлы страниц пагинации"""
    pg_url = []

    for i in url:
        soup = BeautifulSoup(get_html(i), 'lxml')
        slep_random()
        try:
            s = str(soup.find('ul', attrs={'class': 'pagination'}).find_all('a')[-1])
            s2 = s.replace('">&gt;|</a>', '')
            pg = int(s2.split('=')[-1])
            for ul in range(1, pg + 1):
                pg_url.append(i + f'?page={ul}')
                print(i + f'?page={ul}')
        except:
            pg_url.append(i + f'?page=1')
    return pg_url


def get_row_product(url_list):
    """
    Делаем сет с линками карточки товара
    :param url_list: Лист ссылок
    :return: отдаем сет ссылок карточки товара
    """
    row_product = []
    for i in url_list:
        soup = BeautifulSoup(get_html(i), 'lxml')
        slep_random()
        row_product_href = soup.find_all('div', attrs={'class': 'row'})[6]
        for url in row_product_href.find_all('div', attrs={'class': 'caption'}):
            row_product.append(url.find('a').get('href'))
            print(url.find('a').get('href'))
    return row_product


def write_csv(data):
    """
    Пишем в csv
    :param data: dict
    :return: csv file
    """
    with open('new_price_data.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((
            data['url'], data['category5'], data['category4'], data['category3'], data['category2'],
            data['category1'], data['h1'], data['brand'], data['model'], data['price'], data['description'],
            data['img0'], data['img1'], data['img2'], data['img3'], data['img4'], data['img5'], data['img6'],
            data['img7'], data['img8'], data['img9']
        ))


def get_data(url):
    """
    Собираем данные со страницы в dict
    :param url: url страницы для парсинга
    :return: dict
    """
    data = {}
    obj_soup = BeautifulSoup(get_html(url))

    try:
        data['url'] = obj_soup.find('link').get('href')
    except:
        data['url'] = None
    try:
        data['category5'] = obj_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[5].text
    except:
        data['category5'] = None

    try:
        data['category4'] = obj_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[4].text
    except:
        data['category4'] = None

    try:
        data['category3'] = obj_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[3].text
    except:
        data['category3'] = None

    try:
        data['category2'] = obj_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[2].text
    except:
        data['category2'] = None

    try:
        data['category1'] = obj_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[1].text
    except:
        data['category1'] = None

    try:
        data['h1'] = obj_soup.find('h1').text
    except:
        data['h1'] = None

    try:
        data['brand'] = obj_soup.find(id='product').find(attrs={'itemprop': 'brand'}).text
    except:
        data['brand'] = None

    try:
        data['model'] = obj_soup.find(id='product').find(attrs={'itemprop': 'model'}).text
    except:
        data['model'] = None

    try:
        data['price'] = obj_soup.find(id='product').find(attrs={'class': 'list-unstyled price'}).find(
            'li').text.replace(' Р.', '').replace(' ', '')
    except:
        data['price'] = None

    try:
        data['img0'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[0].get('href')

    except:
        data['img0'] = None

    try:
        data['img1'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[1].get('href')
    except:
        data['img1'] = None

    try:
        data['img2'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[2].get('href')
    except:
        data['img2'] = None

    try:
        data['img3'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[3].get('href')
    except:
        data['img3'] = None

    try:
        data['img4'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[4].get('href')
    except:
        data['img4'] = None

    try:
        data['img5'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[5].get('href')
    except:
        data['img5'] = None

    try:
        data['img6'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[6].get('href')
    except:
        data['img6'] = None

    try:
        data['img7'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[7].get('href')
    except:
        data['img7'] = None

    try:
        data['img8'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[8].get('href')
    except:
        data['img8'] = None

    try:
        data['img9'] = obj_soup.find(id='product').find_all(attrs={'class': 'thumbnail'})[9].get('href')
    except:
        data['img9'] = None

    try:
        data['description'] = obj_soup.find(id='tab-description')
    except:
        data['description'] = None

    write_csv(data)
    print(data)


def main():
    num = 0
    u_list = get_url(get_html(URL))
    slep_random()
    print(u_list)
    all_url_product = get_row_product(pagination(u_list))
    print(all_url_product)
    for i in all_url_product:
        get_data(i)
        num += 1
        print(f'{num} забрал! {i}')
        slep_random()


if __name__ == '__main__':
    main()
