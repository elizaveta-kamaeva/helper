import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_queries(filename):
    path = 'infiles//' + filename
    data = pd.read_csv(path, sep=',', dtype=str, error_bad_lines=False)
    queries = data['search_string'].tolist()

    return queries

def get_finn(qulist):
    qudict = {}
    for query in qulist:
        resp = requests.get('https://www.finn-flare.ru/catalog/?SEARCH={}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num_str = soup.find("ul", class_="cat_txt_info").find('li').text
            num = num_str.split(': ')[1]

        except AttributeError:
            num = 0
        qudict[query] = num
    return qudict

def get_sneaker(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://sneakerhead.ru/search/?q={}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num_str = soup.find('div', class_='results').text
            num = max([int(i) for i in re.findall('\d+', num_str)])
        except AttributeError:
            try:
                child_tags = soup.find('div', itemprop='hasOfferCatalog').findAll('div', recursive=False)
                num = len(child_tags)
            except AttributeError:
                num = 0
        qudict[query] = num

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def get_acoola(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://acoolakids.ru/search/find/{}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num = soup.find("div", class_="ak-catalog__amount").find('strong').text

        except AttributeError:
            num = 0
        qudict[query] = num

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def get_profmax(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://www.profmax.pro/search/?q={}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num_str = soup.find("div", class_="b-search-result").text
            num = re.search('\d+(?= товар)', num_str).group()

        except AttributeError:
            num = 0
        qudict[query] = num

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def get_kari(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://kari.com/ru/?q={}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            # если несколько страниц
            pages = soup.find("div", class_="cp_list").findAll('a', recursive=False)
            last_page_num = int(pages[-2].text)

            last_page_url = 'https://kari.com' + pages[-2]['href']
            lp_resp = requests.get(last_page_url)
            lp_soup = BeautifulSoup(lp_resp.text, 'html.parser')

            lp_products = lp_soup.find('div',
                                       class_='catalog_content catalog-pagination-container').findAll('article',
                                                                                            recursive=False)
            lp_num = len(lp_products)
            num = (last_page_num - 1) * 24 + lp_num

        except AttributeError:
            try:
                # если товары умещаются на 1 странице
                page_products = soup.find('div',
                                          class_='catalog_content catalog-pagination-container').findAll('article',
                                                                                                recursive=False)
                num = len(page_products)
            except AttributeError:
                # если товаров не нашлось
                num = 0

        qudict[query] = num

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def get_bosco(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://www.bosco.ru/catalog/?q={}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num_str = soup.find("div", class_="search-result-notice").text
            num = re.search('\d+', num_str).group()

        except AttributeError:
            num = 0
        qudict[query] = num

        n += 1
        if n % 10 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def get_conc(qulist):
    qudict = {}
    n = 0
    for query in qulist:
        resp = requests.get('https://www.conceptclub.ru/search/find/{}'.format(query))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            num = soup.find("span", id="search_goods_cnt").text

        except AttributeError:
            num = 0
        qudict[query] = num

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return qudict

def write_data(qudict, filename):
    outfile = open('outfiles//' + filename.replace('.csv', '-products.csv'), 'w', encoding='utf-8')
    outfile.write('{}\t{}\n'.format('query', 'n of products'))
    for key in qudict:
        outfile.write('{}\t{}\n'.format(key, qudict[key]))


filenames = ('search_terms_stats - sneaker.csv',
             'search_terms_stats - acoola.csv',
             'search_terms_stats - profmax.csv',
             'search_terms_stats - kari.csv',
             'search_terms_stats - bosco.csv',
             'search_terms_stats - conc.csv')
filename = filenames[3]
queries_list = get_queries(filename)
qunum_dict = get_kari(queries_list)
write_data(qunum_dict, filename)
print('Accessing numbers done for', filename)
