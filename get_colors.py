import re
import xml.etree.cElementTree as ET


def get_colors():
    # кладет себе в сет цвета
    text = open('infiles//colors.txt', 'r', encoding='utf-8').readlines()
    color_set = set()
    for line in text:
        words = re.findall('[а-яё]+', re.split('[\t\n]', line)[0].lower())
        for word in words:
            # отрезаем окончания
            word = re.sub('(о|е|ий|ой|ый)\Z', '', word)
            word = re.sub('ё', 'е', word)
            if len(word) > 2:
                color_set.add(word)
    return color_set


def get_queries(filename):
    # загружает запросы
    path = 'infiles//' + filename
    infile = open(path, 'r', encoding='utf-8').readlines()
    del infile[0]
    queries = {}
    for line in infile:
        try:
            line = re.sub('ё', 'е', line)
            string, fixed, is_fixed, amount = line.strip().split('\t')
        except ValueError:
            continue
        queries[fixed] = amount
    return queries


def find_colored_queries(qudict, colors):
    # ищет цвета в запросах
    colored_queries = {}
    found_colors = {}
    is_stop = False
    n = 0
    for query in qudict.keys():
        for query_word in re.split('\W', query):
            # проверяет, нет ли стоп-слова в слове запроса
            for st_word in stop_words:
                if st_word in query_word:
                    is_stop = True
                    break
                else:
                    is_stop = False
            if is_stop:
                continue

            # ищет цвет в слове запроса
            for color in colors:
                if re.match(color, query_word):
                    found_colors[color] = query
                    if query not in colored_queries:
                        colored_queries[query] = qudict[query]

        n += 1
        if n % 1000 == 0:
            print(n, 'queries done.')
    print('Total number of queries:', n)
    return colored_queries, found_colors


def find_colors_in_feed(feed_path):
    feed_path = "infiles\\" + feed_path
    # ищет цвета по фиду
    feed_colors = set()
    feed = ET.parse(feed_path)
    root = feed.getroot().findall("shop")[0]
    offers = root.findall('offers')[0]
    for child in offers:
        for param in child:
            if param.tag == 'param':
                if param.attrib['name'].lower() == 'цвет':
                    feed_colors.add(param.text.lower())
    print('Found colors in feed.')
    return feed_colors


def match_colors(feed_colors, query_colors):
    # сопоставляет цвета фида и запросов
    matched_colors = set()
    unknown_colors = set(query_colors.values())
    # ищет обрезанное слово из запроса в цветах фида
    for fcolor in feed_colors:
        for qucolor in query_colors.keys():
            if qucolor in fcolor:
                matched_colors.add(query_colors[qucolor])
                unknown_colors.remove(query_colors[qucolor])
                break

    print('Colors matched.')
    return matched_colors, unknown_colors


def write_set(set, filename, suffix='new'):
    # пишет сеты в файл, добавляя нужный суффикс
    outfile = open('outfiles//' + filename.replace('.csv', '-'+suffix+'.csv'), 'w', encoding='utf-8')
    for elt in set:
        outfile.write(elt + '\n')
    outfile.close()


def write_queries(filename, qudict):
    # пишет запросы с цветами и ставит им в соответствие count
    outfile = open('outfiles//' + filename.replace('.csv', '-colors.csv'), 'w', encoding='utf-8')
    outfile.write('{}\t{}\n'.format('query', 'count'))
    for key in qudict:
        outfile.write('{}\t{}\n'.format(key, qudict[key]))
    outfile.close()


stop_words = {'бель', 'синт', 'красноярск', 'краснодар', 'серпухов',
              'сертификат', 'белгород'}

filename = '273_finnflare.csv'
known_colors = get_colors()
queries_dict = get_queries(filename)
fit_queries_dict, detected_colors_dict = find_colored_queries(queries_dict, known_colors)
feed_colors = find_colors_in_feed("export_yandex_db1.xml")
bound_colors, loose_colors = match_colors(feed_colors, detected_colors_dict)
write_set(bound_colors, filename, suffix='known')
write_set(loose_colors, filename, suffix='unknown')
write_set(feed_colors, filename, suffix='feed-colors')

write_queries(filename, fit_queries_dict)
print('I\'ve found colored queries. And some garbage possible, too.')
