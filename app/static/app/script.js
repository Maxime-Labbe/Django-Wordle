async function script() {
    async function fetchData() {
        try {
            const response = await fetch(API_ENDPOINT, {
                headers: {
                    'X-SECRET-TOKEN': 'dzabvyu546456DJSQD6DAZ6TDQU6fa'
                }
            });
            const data = await response.json();
            return data.data;
        } catch (error) {
            console.error(error);
            return {};
        }
    }

    function addKeyboardEventListener() {
        const keyboard = document.querySelector('.keyboard');
        const keys = document.querySelectorAll('.key');
        keys.forEach(key => {
            key.addEventListener('click', (event) => {
                handleKeydown(event.target.id);
            }
            );
        });
        keyboard.addEventListener('click', (event) => {
            event.preventDefault();
        })
    }

    function verifyLetter(letter, index, word_to_guess, correct_letters) {
        const text = letter.textContent.trim().toLowerCase();
        const keys = document.querySelectorAll('.key');
        const key_index = (Object.keys(keys).filter(key => text === keys[key].id));
        if (text !== "." && text !== "") {
            if (text === word_to_guess[index]) {
                correct_letters[index] = text;
                letter.className += ' correct-letter';
                if (!keys[key_index].className.includes('correct-key')) {
                    keys[key_index].className = 'key correct-key';
                }
            } else if (word_to_guess.includes(text)) {
                letter.className += ' misplaced-letter';
                if (!keys[key_index].className.includes('misplaced-key') && !keys[key_index].className.includes('correct-key')) {
                    keys[key_index].className = 'key misplaced-key';
                }
            } else {
                letter.className += ' wrong-letter';
                keys[key_index].className += ' wrong-key';
            }
        }
        return correct_letters;
    }

    function addRobotWord(guesses, words, current_word, len_word) {
        const letters = words[current_word + 6].querySelectorAll('.letter');
        let word = words[current_word + 6].getAttribute('data-word');
        guesses[current_word] = guesses[current_word].trim();
        for (let i = 0; i < len_word; i++) {
            letters[i].textContent = guesses[current_word][i].toUpperCase();
            word += guesses[current_word][i];
        }
    }

    function addAnimationLetters(letters) {
        for (let i = 0; i < letters.length; i++) {
            letters[i].style.transitionDelay = `${0.2 + i * 0.3}s`;
            letters[i].style.animation = `transition-letter 0.5s ${i * 0.3}s`;
        }
    }

    function displayPopUp() {
        const popUp = document.querySelector('.pop-up-container');
        popUp.style.transitionDelay = `${word_animation_duration}s`;
        popUp.style.visibility = 'visible';
    }

    async function displayPlaceholder(current_word, len_word, correct_letters) {
        const letters = words[current_word].querySelectorAll('.letter');
        for (let i = 0; i < len_word; i++) {
            if (i == 0) {
                letters[i].className = 'letter placeholder current-letter';
            } else {
                letters[i].className = 'letter placeholder';
            }
            letters[i].textContent = correct_letters[i].toUpperCase();
        }
    }

    function simulateKeydown(event) {
        const keys = document.querySelectorAll('.key');
        keys.forEach(key => {
            if (key.id === event) {
                key.className += ' key-pressed';
                setTimeout(() => {
                    key.className = key.className.replace(' key-pressed', '');
                }, 175);
            }
        });
    };

    function handleKeydown(event) {
        const letters = words[current_word].querySelectorAll('.letter');
        let word = words[current_word].getAttribute('data-word');
        simulateKeydown(event);
        if (!end) {
            if (event === "Enter") {
                if (current_letter == word_data.len_word_to_guess) {
                    addAnimationLetters(letters);
                    letters.forEach((letter, index) => {
                        correct_letters = verifyLetter(letter, index, word_data.word_to_guess, correct_letters);
                    });
                    if (type_of_game === 'robot') {
                        if (current_word < word_data.all_guesses.length - 1) {
                            addRobotWord(word_data.all_guesses, words, current_word, word_data.len_word_to_guess);
                        }
                    }
                    if (word === word_data.word_to_guess) {
                        end = true;
                        displayPopUp();
                        document.removeEventListener("keydown", handleKeydown, true);
                        if (type_of_game === 'robot') {
                            if (current_word < word_data.all_guesses.length) {
                                for (let i = 1; i < word_data.all_guesses.length - current_word; i++) {
                                    addRobotWord(word_data.all_guesses, words, current_word + i, word_data.len_word_to_guess);
                                }
                            }
                        }
                    } else if (current_word == 5) {
                        end = true;
                        displayPopUp();
                        document.removeEventListener("keydown", handleKeydown, true);
                        if (type_of_game === 'robot') {
                            addRobotWord(word_data.all_guesses, words, word_data.all_guesses.length - 1, word_data.len_word_to_guess);
                        }
                    } else {
                        current_word += 1;
                        current_letter = 0;
                        displayPlaceholder(current_word, word_data.len_word_to_guess, correct_letters);
                    }
                }
            } else if (event === "Backspace") {
                if (current_letter > 0) {
                    if (letters[current_letter]) letters[current_letter].className = 'letter placeholder';
                    current_letter--;
                    word = word.slice(0, -1);
                    words[current_word].setAttribute('data-word', word);
                    letters[current_letter].className = 'letter placeholder current-letter';
                    letters[current_letter].textContent = correct_letters[current_letter].toUpperCase();
                }
            } else {
                if (current_letter < word_data.len_word_to_guess && event.match(/[a-z]/i) && event.length === 1) {
                    word += event.toLowerCase();
                    words[current_word].setAttribute('data-word', word);
                    letters[current_letter].className = 'letter';
                    letters[current_letter].textContent = event.toUpperCase();
                    current_letter++;
                    if (letters[current_letter]) letters[current_letter].className += ' current-letter';
                }
            }
        }
    }

    addKeyboardEventListener();
    const letter_animation_duration = 0.5;
    const letter_animation_delay = 0.3;
    const type_of_game = document.querySelectorAll('.game').length > 1 ? 'robot' : 'solo';
    const API_ENDPOINT = type_of_game === 'robot' ? '/api/get_data_robot' : '/api/get_data_solo';
    const word_data = await fetchData(API_ENDPOINT);
    const word_animation_duration = (word_data.len_word_to_guess - 1) * letter_animation_delay + letter_animation_duration;
    const words = document.querySelectorAll('.word');
    let current_word = 0;
    let current_letter = 0;
    let correct_letters = (new Array(word_data.len_word_to_guess)).fill('.');
    let end = false;
    displayPlaceholder(current_word, word_data.len_word_to_guess, correct_letters);
    document.addEventListener("keydown", (event) => handleKeydown(event.key));
};

script();