import unicodedata

def remove_accents(word):
    return unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8')

def read_words():
    list = []
    with open('app/static/app/mots.dic', 'r', encoding='utf-16') as f:
        for line in f:
            line = line.strip().split(",")[0]
            if line.count(" ") == 0 and line.isalpha() and len(line) > 3 and len(line) < 9:
                list.append(remove_accents(line))
    return list

def write_words():
    words = read_words()
    with open('app/static/app/mots.txt', 'w', encoding='utf-16') as f:
        for word in words:
            f.write(word + '\n')

write_words()