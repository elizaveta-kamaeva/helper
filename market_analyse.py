from collections import Counter


def get_data(filename):
    filepath = 'infiles\\market anaysis summary\\' + filename
    file = open(filepath, 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()

    category_cnt = Counter()

    for line in lines[1:]:
        if line.split(';')[0] != '':
            splitted = line.strip().split(';')
            category, count = splitted[0], int(splitted[1])
            category_cnt[category] += count
    return category_cnt


def write_counter(categories_cnt):
    filepath = 'outfiles\\' + outname
    file = open(filepath, 'a', encoding='utf-8')
    for category in categories_cnt:
        file.write('{}\t{}\n'.format(category, categories_cnt[category]))
    file.close()



filenames = ['123.csv',
             'comfy.csv',
             'holodilnik.csv',
             'kotofoto.csv',
             'megabitcomp.csv',
             'ogo.csv',
             'oldi.csv',
             'sulpak.csv']
outname = 'electronics_cat.csv'
categories_cnt = Counter()

for filename in filenames:
    cat_cnt = get_data(filename)
    categories_cnt += cat_cnt


write_counter(categories_cnt)
print('Categories united under your flag, my liege.')
