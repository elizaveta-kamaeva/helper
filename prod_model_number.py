from urllib.request import urlopen, pathname2url
from urllib.parse import quote
from json import load
import ssl
import pandas as pd


def ask_input():
    # спрашивает API для сайта и путь к файлу с данными QA
    apikey = input('Enter API key: ')
    filepath = 'files\\' + input('Enter file name: ')
    return apikey, filepath

def get_queries(filename, sep='\t'):
    filepath = 'infiles\\zero_queries\\' + filename
    df = pd.read_csv(filepath, sep=sep, dtype='str', error_bad_lines=False)
    query_num_dict = df.set_index('query')['count'].to_dict()
    query_url_dict = df.set_index('query')['Код'].to_dict()

    print('Queries from {} extracted.'.format(filename))
    return query_num_dict, query_url_dict

def get_prod_amount(apikey, query):
    # получает исправленный запрос с API
    json_url = 'http://sort.diginetica.net/search?st={1}&apiKey={0}&strategy=simple&size=10'.format(apikey, quote(query))
    context = ssl._create_unverified_context()
    json_site = urlopen(json_url, context=context)
    json_data = load(json_site)
    items_amount = json_data['totalHits']
    return items_amount

def write_data(query_num_dict, query_url_dict, filepath):
    new_path = filepath.replace('.csv', '_filtered.csv')
    outfile = open(new_path, 'w', encoding='utf-8')
    header = 'Код\tquery\tamount\n'
    outfile.write(header)
    for query in query_num_dict.keys():
        outfile.write('{}\t{}\t{}\n'.format(query_url_dict[query], query, query_num_dict[query]))
    outfile.close()


apikeydict = {'123': 'S3R3DJX71L',
              '224': '7936JCD8GN',
              '338': '7DRN52IVBN',
              '370': 'HZ61SQ52K6',
              '17': 'BZQ1NIP98I',
              '26': '94LDSOMRQ3',
              '351': 'G02HGV15GB',
              '302': 'E5045PW6KS',
              '221': '5BZ4H1HRDU',
              '345': '1625TEY0YI',
              '13': '9WYS3K2LYX'}

for siteid in apikeydict.keys():
    apikey = apikeydict[siteid]
    filename = 'auto_zero_{}.csv'.format(siteid)
    query_amount_dict, query_url_dict = get_queries(filename)

    filtered_queries = {}
    filtered_urls = {}
    for query in query_amount_dict.keys():
        returned_amount = get_prod_amount(apikey, query)
        if returned_amount > 0:
            filtered_queries[query] = query_amount_dict[query]
            filtered_urls[query] = query_url_dict[query]
    write_data(filtered_queries, filtered_urls, 'outfiles\\filtered_zeros\\'+filename)
    print('Data for siteid {} written.'.format(siteid))
