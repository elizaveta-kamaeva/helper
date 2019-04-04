import re


def remove_spaces(string):
    despaced = re.sub('\s+', '', string)
    return despaced


filename = '217-dataset-balanced-automatic.tsv'
infile = open('infiles\\' + filename, 'r', encoding='utf-8')
outfile = open('outfiles\\' + filename, 'w', encoding='utf-8')
n = 0

for line in infile:
    n += 1
    try:
        query, correction = line.strip().split('\t')
    except ValueError:
        continue
    jammed_query = remove_spaces(query)
    jammed_correction = remove_spaces(correction)
    if jammed_query == jammed_correction and len(query) == len(correction):
        pass
    else:
        outfile.write('{}\t{}\n'.format(query, correction))
    if n % 5000 == 0:
        print('{:.0f}K lines processed'.format(n / 1000))

infile.close()
outfile.close()
