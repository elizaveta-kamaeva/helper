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
    queries = set()
    text = open(filepath, 'r', encoding='utf-8').readlines()
    del text[0]
    for row in text:
        query = row.split('\t')[0]
        queries.add(query)
    return queries

def get_prod_fix(apikey, item):
    # получает исправленный запрос с API
    quoted_query = quote(item)
    json_url = 'https://queries.diginetica.net/{}/search?q={}'.format(apikey, quoted_query)
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
    for query in queries_list:
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

def write_data(queries_dict, filepath, repl):
    new_path = filepath.replace('.csv', '-prod_{}.csv'.format(repl))
    outfile = open(new_path, 'w', encoding='utf-8')
    outfile.write('initial_query\tfixed_by_prod_model\n')
    for query in queries_dict:
        outfile.write('{}\t{}\n'.format(query, queries_dict[query]))
    outfile.close()


#apikey, path = 'F14Q0I9IV6', 'files\\368-fixed_1.csv'
apikey, path = ask_input()
queries = list_items(path)
same_matches, different_matches = list_proddata(queries)
write_data(same_matches, path, 'same')
write_data(different_matches, path, 'diff')
print('Done accessing API.')
