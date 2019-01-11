import re


file = open('files\\358-brands.csv', 'r', encoding='utf-8')
text = file.readlines()
file.close()

outfile = open('files\\358-brands-new.csv', 'w', encoding='utf-8')
known_words = set()

for line in text:
    repl_line = re.sub('\d|;', '', line)
    line_list = repl_line.split()
    for word in line_list:
        if len(word) < 3:
            repl_line = repl_line.replace(word, '')
    repl_line = repl_line.strip(' ')
    if len(repl_line) > 2 and not repl_line in known_words:
        known_words.add(repl_line)
        outfile.write(';'+repl_line)
outfile.close()

print('The garbage hunted down, sir.')