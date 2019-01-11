import re


file = open('brands-mirbeer.txt', 'r', encoding='utf-8')
brand_list = file.readlines()
file.close()

new_brands = set()
bad_brands = set()
for raw_brand in brand_list:
    raw_brand = raw_brand.strip()
    brand = raw_brand if(raw_brand[-1] not in set('0123456789')) else ''

    if brand in new_brands or brand in bad_brands or not brand:
        continue
    solid_letters_len = len(re.search('[A-Za-z\s\'`-]+', brand).group())
    if solid_letters_len == 3:
        eval = input('{} = {}. Is it ok? '.format(raw_brand, brand))
        if len(eval) == 1:
            bad_brands.add(brand)
        else:
            new_brands.add(brand)
    elif solid_letters_len > 3:
        new_brands.add(brand)

new_file = open('new-brands-mirbeer.txt', 'w', encoding='utf-8')
for elt in new_brands:
    new_file.write(elt + '\n')
new_file.close()
