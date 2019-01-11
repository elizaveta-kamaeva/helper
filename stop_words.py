import re


file = open('stop-words.txt', 'r', encoding='utf-8')
outfile = open('stop-words_rus.txt', 'w', encoding='utf-8')

for line in file:
    if not re.match('\s', line[0]):
        word = re.match('\w+(?=\s)', line).group()
        outfile.write(word + '\n')

file.close()
outfile.close()
