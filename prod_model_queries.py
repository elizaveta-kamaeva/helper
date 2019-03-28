from urllib.request import urlopen, pathname2url
from urllib.parse import quote
from json import load
import ssl


def ask_input():
    # спрашивает API для сайта и путь к файлу с данными QA
    apikey = input('Enter API key: ')
    filepath = 'files\\' + input('Enter file name: ')
    return apikey, filepath

def list_items(filepath):
    # получает исходные запросы из файла с QA
    queries = {}
    text = open(filepath, 'r', encoding='utf-8').readlines()
    header = text[0].strip().split('\t')
    searchstring, count = header.index('searchstring'), header.index('count')
    del text[0]
    for row in text:
        splitted = row.strip().split('\t')
        if len(splitted) == len(header):
            query = splitted[searchstring]
            number = splitted[count]
            queries[query] = number
    return queries

def get_prod_fix(apikey, item):
    # получает исправленный запрос с API
    json_url = 'https://queries.diginetica.net/{}/search?q={}'.format(apikey, quote(item))
    context = ssl._create_unverified_context()
    json_site = urlopen(json_url, context=context)
    json_data = load(json_site)
    typo = json_data['typos']
    return typo

def list_proddata(queries_list):
    # делает словарь с данными API
    same_queries = {}
    different_queries = {}
    n = 0
    for query in queries_list.keys():
        fixed = get_prod_fix(apikey, query)
        if query == fixed:
            same_queries[query] = fixed
        else:
            different_queries[query] = fixed

        n += 1
        if n % 20 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return same_queries, different_queries

def write_data(queries_dict, items_counted, filepath, mode = 'w', header='\n'*3):
    new_path = filepath.replace('.csv', '-prod.csv')
    outfile = open(new_path, mode, encoding='utf-8')
    outfile.write(header)
    for query in queries_dict:
        outfile.write('{}\t{}\t{}\n'.format(items_counted[query], query, queries_dict[query]))
    outfile.close()


# apikey, path = '7936JCD8GN', 'files\\224-balanced.csv'
apikey, path = ask_input()
queries = list_items(path)
same_matches, different_matches = list_proddata(queries)
write_data(same_matches, queries, path, header='count\tinitial_query\tfixed_by_prod_model\n')
write_data(different_matches, queries, path, mode='a')
print('Done accessing API.')
