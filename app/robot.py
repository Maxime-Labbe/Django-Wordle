import random

def read_words():
    list = []
    with open('app/static/app/mots.txt', 'r', encoding='utf-16') as f:
        for line in f:
            list.append(line.strip().lower())
    return list

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
        unique_letters = []
        for letter in attempt:
            if letter not in unique_letters:
                unique_letters.append(letter)
            if attempt.count(letter) > number_of_letters:
                success = False
                break
        if len(unique_letters) <= len(attempt) // 2:
            success = False
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
    alphabet_frequencies = [0.0]*len(alphabet)
    for letter in range(len(alphabet)):
        for word in words:
            alphabet_frequencies[letter] += word.count(alphabet[letter])
        if letter_count:
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

def search_word_most_unique_validated_letters(words,words_left,validated_letters):
    max_letters = 0
    guesses = []
    letters = []
    for word in words_left:
        for letter in word:
            if letter not in validated_letters:
                letters.append(letter)
    for word in words:
        count = 0
        count_letters = []
        for letter in word:
            if letter in letters and letter not in count_letters:
                count += 1
                count_letters.append(letter)
        if count == max_letters:
            guesses.append(word)
        elif count > max_letters:
            max_letters = count
            guesses = [word]
    if max_letters < 2:
        return words_left
    return guesses

def search_word_more_left_letters(words,alphabet,not_placed,letters):
    max_letters = 0
    guesses = []
    for word in words:
        count = 0
        count_letters = []
        word_letters = []
        index = 0
        for letter in word:
            if letter not in word_letters:
                word_letters.append(letter)
            if not letter in alphabet or letters.count(letter) <= word.count(letter):
                count = -len(word)
            if letter not in count_letters and (letter not in not_placed.keys() or (letter in not_placed.keys() and index not in not_placed[letter])) and letters[index] != letter:
                count += 1
                count_letters.append(letter)
            index += 1
        if count >= max_letters and len(word_letters) > len(word) // 2:
            max_letters = count
            guesses.append(word)
    if guesses == [] or max_letters < (len(guesses[0]) // 2) :
        return words
    return guesses

def add_most_frequent_letter(words,alphabet,alphabet_frequencies,letters,not_placed):
    frequencies = [f for f in alphabet_frequencies]
    new_alphabet = [l for l in alphabet]
    new_letters = [l for l in letters]
    letters_index = [i for i in range(len(letters)) if letters[i] == ''][0]
    max_consonant = 0
    consonant = ''
    max_vowel = 0
    vowel = ''
    while new_letters[letters_index] == '' and len(frequencies) != 0:
        frequency = max(frequencies)
        index = frequencies.index(frequency)
        if (new_alphabet[index] in not_placed.keys() and letters_index not in not_placed[new_alphabet[index]]) or new_alphabet[index] not in not_placed.keys():
            if new_alphabet[index] not in 'aeiouy' and frequency > max_consonant:
                consonant = new_alphabet[index]
                max_consonant = frequency
            elif new_alphabet[index] in 'aeiouy' and frequency > max_vowel:
                vowel = new_alphabet[index]
                max_vowel = frequency
            if new_alphabet[index] not in letters:
                new_letters[letters_index] = new_alphabet[index]
                if ''.join(new_letters) in words:
                    break
                else:
                    new_letters[letters_index] = ''
        frequencies.remove(frequency)
        new_alphabet.remove(new_alphabet[index])
    if new_letters[letters_index] == '':
        if consonant != '':
            new_letters[letters_index] = consonant
        else:
            new_letters[letters_index] = vowel
    return "".join(new_letters)       

def update_alphabet(alphabet,alphabet_frequencies,words):
    for letter in alphabet:
        total_count = 0
        for word in words:
            total_count += word.lower().count(letter)
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

def calculate_not_placed_letters(letters,not_placed):
    nb_not_placed = 0
    for letter in not_placed.keys():
        if letter not in letters:
            nb_not_placed += 1
    return nb_not_placed
    
def place_in_letters(not_placed,letters,word_to_guess):
    possible_letters = ['']*len(letters)
    available_index = [i for i in range(len(letters))]
    for i in range(len(letters)):
        if letters[i]!='':
            possible_letters[i] = letters[i]
            available_index.remove(i)
    for letter in not_placed.keys():
        index = -1
        if letter not in letters or letters.count(letter) < word_to_guess.count(letter):
            for i in available_index:
                if i not in not_placed[letter]:
                    if index == -1:
                        index = i
                    else:
                        index = -2
        if index > 0:
            possible_letters[index] = letter
            available_index.remove(index)
    return possible_letters
    
def verify_guess(guess,word_to_guess):
    result = ['0']*len(guess)
    for i in range(len(guess)):
        if guess[i] == word_to_guess[i]:
            result[i] = '3'
        elif guess[i] in word_to_guess:
            result[i] = '2'
        else:
            result[i] = '1'
    return result

def play_game():
    global data
    random_len = random.randint(4, 8)
    words = filter_words(read_words(), random_len)
    words_left = [word for word in words]
    word_to_guess = random.choice(words)

    letters = [""]*random_len
    not_placed = {}
    alphabet = []
    banned_letters = ''

    for i in range(ord('a'),ord('z')+1):
        alphabet.append(chr(i))
    alphabet_left = [letter for letter in alphabet]
    alphabet_frequencies = calculate_letter_frequencies(words,alphabet,random_len)
    alphabet_frequencies_left = [f for f in alphabet_frequencies]
    guess = ''
    all_guess = []
    bug_index = []

    while guess != word_to_guess and len(all_guess) < 6:
        if guess in words_left:
            words_left.remove(guess)
        result = ['0']*random_len
        if guess:
            result = verify_guess(guess,word_to_guess)
        for i in range(len(result)):
            if result[i] == '0':
                break
            elif result[i] == '1':
                if guess[i] in alphabet_left:
                    index = alphabet_left.index(guess[i])
                    alphabet_left.remove(guess[i])
                    alphabet_frequencies_left.remove(alphabet_frequencies_left[index])
            elif result[i] == '2':
                if guess[i] not in not_placed.keys():
                    not_placed[guess[i]] = []
                not_placed[guess[i]].append(i)
            else:
                letters[i] = guess[i]
        new_letters = []
        while new_letters != letters:
            new_letters = place_in_letters(not_placed,letters,word_to_guess)
            letters = [letter for letter in new_letters]
        banned_letters += guess
        words_left = filter(words_left,letters,not_placed,alphabet_left)
        alphabet_left, alphabet_frequencies_left = update_alphabet(alphabet_left,alphabet_frequencies_left,words_left)
        alphabet_frequencies_left = calculate_letter_frequencies(words_left,alphabet_left,random_len)
        # if len(words) > 5 and ((26 - len(banned_letters)) >= random_len) and enough_available_letters(alphabet_left,alphabet_frequencies_left,random_len,banned_letters):
        #     guess = most_frequent_positions(most_frequent_letters(alphabet_left,alphabet_frequencies_left,random_len,banned_letters),words,random_len)
        # print(letters.count(''),len(words_left),len(all_guess))
        if len(words_left) == 1:
            guess = words_left[0]
            bug_index.append('Last word')
        elif letters.count('') == 1 and len(words_left) >= 3 and len(all_guess) < 5 :
            guess = search_word_most_unique_validated_letters(words,words_left,letters)
            if len(guess) > 1:
                guess = search_word_most_frequent_letters(guess,alphabet_frequencies,alphabet)
            else:
                guess = guess[0]
            bug_index.append('1 lettre and +1 guess LEFT')
        elif letters.count('') == 1:
            guess = add_most_frequent_letter(words_left,alphabet_left,alphabet_frequencies_left,letters,not_placed)
            bug_index.append('1 lettre LEFT')
        elif len(words_left) > 10 and letters.count('') >= (len(letters) // 2) and len(all_guess) >= 1:
            guess = search_word_more_left_letters(words,alphabet_left,not_placed,letters)
            if guess == words:
                guess = search_word_most_frequent_letters(search_for_x_letter_per_word(words_left),alphabet_frequencies_left,alphabet_left)
            elif len(guess) > 1:
                guess = search_word_most_frequent_letters(search_for_x_letter_per_word(guess),alphabet_frequencies,alphabet)
            else:
                guess = guess[0]
            bug_index.append('More than half letters LEFT')
        elif len(words_left) > 10:
            guess = search_word_most_frequent_letters(search_for_x_letter_per_word(words_left),alphabet_frequencies_left,alphabet_left)
            bug_index.append('More than 50 words SEARCH')
        elif len(words_left) > 1:
            guess = search_word_most_frequent_letters(words_left,alphabet_frequencies_left,alphabet_left)
            bug_index.append('Less than 50 words SEARCH')
        # if len(all_guess) > 0 and  guess == all_guess[-1]:
            # print(word_to_guess,guess,all_guess,alphabet_left,alphabet_frequencies_left,words_left,letters,not_placed)
        all_guess.append(guess)

    data = {'len_word_to_guess': len(word_to_guess), 'word_to_guess': word_to_guess, 'all_guesses': all_guess, 'bug_index': bug_index}
    return data

def set_data(data_to_assign):
    global data
    data = data_to_assign

def get_data():
    global data
    return data

def set_word_to_guess():
    global data
    random_len = random.randint(4, 8)
    words = filter_words(read_words(), random_len)
    word_to_guess = random.choice(words)
    data = {'len_word_to_guess': len(word_to_guess), 'word_to_guess': word_to_guess}

def get_word_to_guess():
    return data