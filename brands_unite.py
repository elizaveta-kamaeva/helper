import pandas as pd


def ru_eng(filename, sep='\t'):
    filepath = 'infiles\\' + filename
    df = pd.read_csv(filepath, sep=sep, dtype='str', error_bad_lines=False)
    en_ru_dict = df.set_index('alias')['brand'].to_dict()

    print('Items from {} extracted.'.format(filename))
    return en_ru_dict

loaded = set(ru_eng('av_trans_known.csv', sep=',').keys())
checked = set(ru_eng('av_trans-checked.csv', sep=',').keys())
possible2generate = ru_eng('221-translit.txt', sep=';')

known = loaded | checked
ru_en_checked = {}
for trans in possible2generate.keys():
    if trans not in known:
        known.add(trans)
        ru_en_checked[trans] = possible2generate[trans]

outfile = open('outfiles\\av_trans-auto.csv', 'w', encoding='utf-8')
outfile.write('{},{}\n'.format('brand', 'alias'))
for checked_trans in ru_en_checked.keys():
    checked_brand = ru_en_checked[checked_trans]
    outfile.write('{},{}\n'.format(checked_brand, checked_trans))

outfile.close()
print('United and checked brands.')
