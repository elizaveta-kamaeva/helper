file = open('files\\translit-221.csv', 'r', encoding='utf-8')
text = file.readlines()
file.close()

for line in text:
    if line.count(',') != 1:
        print('Problem string:')
        print(line)