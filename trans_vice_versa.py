infile = open('translit-known-pets.csv', 'r', encoding='utf-8')
pairs = infile.readlines()
infile.close()
outfile = open('trans-known-pets.csv', 'w', encoding='utf-8')

for pair in pairs:
    rus_word, eng_word = pair.strip().split(';')
    outfile.write('{};{}\n'.format(eng_word, rus_word))
outfile.close()

print('Vica-versing done.')
