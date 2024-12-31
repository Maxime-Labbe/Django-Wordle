import random
import unicodedata

def read_words():
    list = []
    with open('app/static/app/mots.dic', 'r', encoding='utf-16') as f:
        for line in f:
            line = line.strip().split(",")[0]
            if line.count(" ") == 0 and line.isalpha():
                list.append(line)
    return list

def remove_accents(word):
    return unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8')

def filter_words(words, length):
    return [word for word in words if len(word) == length]

def filter(words,letters,not_placed,alphabet):
    valid_words = []
    for word in words:
        valid = True
        for i in range(len(letters)):
            if letters[i]!=word[i] and letters[i]!='':
                valid = False
                break
        for letter in not_placed.keys():
            if not(letter in word):
                valid = False
                break
            else:
                for index in not_placed[letter]:
                    if word[index] == letter:
                        valid = False
                        break
        for letter in word:
            if not(letter in alphabet):
                valid = False
                break
        if valid:
            valid_words.append(word)
    return valid_words

def search_for_x_letter_per_word(words):
    attempts = 0
    number_of_letters = 1
    attempts_words = [word for word in words]
    good_guesses = []
    while True:
        success = True
        attempt = attempts_words[attempts]
        for letter in attempt:
            if attempt.count(letter) > number_of_letters:
                success = False
                break
        if success:
            good_guesses.append(attempt)
        attempts+=1
        if attempts == len(words):
            if len(good_guesses) > 0:
                break
            else:
                attempts = 0
                number_of_letters +=1
                attempts_words = [word for word in words]
    return good_guesses

def calculate_letter_frequencies(words,alphabet,word_len):
    letter_count = len(words) * word_len
    alphabet_frequencies = [0.0]*26
    for letter in range(len(alphabet)):
        for word in words:
            alphabet_frequencies[letter] += word.count(alphabet[letter])
        alphabet_frequencies[letter] = round((alphabet_frequencies[letter]/letter_count)*100,2)
    return alphabet_frequencies

def search_word_most_frequent_letters(words,alphabet_frequencies,alphabet):
    frequencies = {}
    for i in range(len(words)):
        frequencies[words[i]] = 0
        for letter in words[i]:
            index = alphabet.index(letter)
            frequencies[words[i]] += alphabet_frequencies[index]
    maxi = 0
    guess = ''
    for key in frequencies.keys():
        if frequencies[key] > maxi:
            maxi = frequencies[key]
            guess = key
    return guess

def most_frequent_letters(alphabet,alphabet_frequencies,word_len,banned_letters=[]):
    most_frequent = []
    index = []
    for _ in range(word_len):
        current_index = -1
        maxi = 0
        for j in range(len(alphabet_frequencies)):
            if alphabet_frequencies[j] > maxi and j not in index and alphabet[j] not in banned_letters:
                maxi = alphabet_frequencies[j]
                current_index = j
        index.append(current_index)
        most_frequent.append(alphabet[current_index])
    return "".join(most_frequent)

def most_frequent_positions(letters,words,word_len):
    position = {}
    for letter in letters:
        position[letter] = []
        for word in words:
            cpt = word.count(letter)
            if cpt > 1:
                for j in range(len(word)):
                    if word[j]==letter:
                        position[letter].append(j)
            elif cpt == 1:
                position[letter].append(word.index(letter))
        position[letter] = round(sum(position[letter])/len(position[letter]),2)
    guess = ''
    for _ in range(word_len):
        mini = float(word_len)
        letter = ''
        for key in position.keys():
            if position[key] < mini:
                mini = position[key]
                letter = key
        guess += letter
        position.pop(letter)
    return guess

def update_alphabet(alphabet,alphabet_frequencies,words):
    for letter in alphabet:
        total_count = 0
        for word in words:
            total_count += word.count(letter)
        if total_count == 0:
            index = alphabet.index(letter)
            alphabet.remove(letter)
            alphabet_frequencies.remove(alphabet_frequencies[index])
    return alphabet,alphabet_frequencies

def enough_available_letters(alphabet,alphabet_frequencies,word_len,banned_letters):
    available = 0
    for i in range(len(alphabet)):
        if alphabet[i] not in banned_letters and alphabet_frequencies[i] > 0:
            available += 1
    return available >= word_len
    

def play_game():
    random_len = random.randint(3, 8)
    words = filter_words(read_words(), random_len)
    words = [remove_accents(word) for word in words]
    word_to_guess = random.choice(words)

    letters = [""]*random_len
    not_placed = {}
    alphabet = []
    banned_letters = ''

    for i in range(ord('a'),ord('z')+1):
        alphabet.append(chr(i))
    alphabet_frequencies = [0.0]*26
    guess = ''
    all_guess = []

    while guess != word_to_guess:
        result = ['0']*random_len
        if guess:
            for i in range(random_len):
                if guess[i] == word_to_guess[i]:
                    result[i] = '3'
                elif guess[i] in word_to_guess:
                    result[i] = '2'
                else:
                    result[i] = '1'
        for i in range(len(result)):
            if result[i] == '0':
                break
            elif result[i] == '1':
                if guess[i] in alphabet:
                    index = alphabet.index(guess[i])
                    alphabet.remove(guess[i])
                    alphabet_frequencies.remove(alphabet_frequencies[index])
            elif result[i] == '2':
                if guess[i] not in not_placed.keys():
                    not_placed[guess[i]] = []
                not_placed[guess[i]].append(i)
            else:
                if guess[i] in not_placed:
                    not_placed.pop(guess[i])
                letters[i] = guess[i]
        banned_letters += guess
        words = filter(words,letters,not_placed,alphabet)
        alphabet, alphabet_frequencies = update_alphabet(alphabet,alphabet_frequencies,words)
        alphabet_frequencies = calculate_letter_frequencies(words,alphabet,random_len)
        if len(words) > 5 and ((26 - len(banned_letters)) >= random_len) and enough_available_letters(alphabet,alphabet_frequencies,random_len,banned_letters):
            guess = most_frequent_positions(most_frequent_letters(alphabet,alphabet_frequencies,random_len,banned_letters),words,random_len)
        elif len(words) > 1:
            guess = search_word_most_frequent_letters(words,alphabet_frequencies,alphabet)
        else:
            guess = words[0]
        if guess in words:
            words.remove(guess)
        all_guess.append(guess)

    print(guess,word_to_guess)
    data = {'len_word_to_guess': len(word_to_guess), 'word_to_guess': word_to_guess, 'all_guesses': all_guess}
    return data