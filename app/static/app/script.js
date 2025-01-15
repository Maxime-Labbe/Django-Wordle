async function script() {
    async function fetchData() {
        try {
            const response = await fetch(API_ENDPOINT, {
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

    function verifyUniqueLetter(letter, index, word_to_guess, state) {
        if (letter === word_to_guess[index]) {
            state[index] = 'correct';
        } else if (word_to_guess.includes(letter)) {
            state[index] = 'misplaced';
        } else {
            state[index] = 'wrong';
        }

        return state;
    }

    function verifyWellPlacedLetter(letter, index, word_to_guess, state, count) {
        if (letter === word_to_guess[index]) {
            state[index] = 'correct';
            count++;
        }
        return state, count;
    }

    function verifyOtherLetter(letter, index, word_to_guess, state, count) {
        if (word_to_guess.includes(letter) && count < word_to_guess.split(letter).length - 1) {
            state[index] = 'misplaced';
            count++;
        } else {
            state[index] = 'wrong';
        }
        return state, count;
    }

    function verifyLetters(letters, word_to_guess, correct_letters) {
        const dict = {};
        let state_letters = Array(word_to_guess.length).fill('wrong');
        letters.forEach((letter, index) => {
            letter = letter.textContent.trim().toLowerCase();
            if (!dict[letter]) {
                dict[letter] = [index];
            } else {
                dict[letter].push(index);
            }
        });
        Object.keys(dict).forEach(key => {
            if (dict[key].length > 1) {
                count = 0;
                dict[key].forEach(index => {
                    state_letters, count = verifyWellPlacedLetter(key, index, word_to_guess, state_letters, count);
                });
                dict[key].forEach(index => {
                    if (state_letters[index] === 'wrong') {
                        state_letters, count = verifyOtherLetter(key, index, word_to_guess, state_letters, count);
                    }
                });
            } else {
                state_letters = verifyUniqueLetter(key, dict[key][0], word_to_guess, state_letters);
            }
        });
        state_letters.forEach((state, index) => {
            const key = document.querySelector(`.key#${letters[index].textContent.trim().toLowerCase()}`);
            if (state === 'correct') {
                correct_letters[index] = word_to_guess[index];
                letters[index].className += ' correct-letter';
                if (!key.className.includes('correct-key')) {
                    key.className = 'key correct-key';
                }
            } else if (state === 'misplaced') {
                letters[index].className += ' misplaced-letter';
                if (!key.className.includes('correct-key') && !key.className.includes('misplaced-key')) {
                    key.className = 'key misplaced-key';
                }
            } else {
                letters[index].className += ' wrong-letter';
                if (!key.className.includes('correct-key') && !key.className.includes('misplaced-key') && !key.className.includes('wrong-key')) {
                    key.className = 'key wrong-key';
                }
            }
        });
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

    function displayPopUp(state) {
        const popUp = document.querySelector('.pop-up-container');
        popUp.style.transitionDelay = `${word_animation_duration}s`;
        popUp.style.visibility = 'visible';
        if (state === true) {
            popUp.querySelector('.pop-up>h2').textContent = 'Bravo !';
            popUp.querySelector('.pop-up>p').textContent = 'Vous avez battu le robot !';
        } else if (state === false) {
            popUp.querySelector('.pop-up>h2').textContent = 'Dommage !';
            popUp.querySelector('.pop-up>p').textContent = 'Vous avez perdu contre le robot !';
        } else {
            popUp.querySelector('.pop-up>h2').textContent = 'Égalité !';
            popUp.querySelector('.pop-up>p').textContent = 'Vous n\'avez rien de spécial...';
        }
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

    const wordChecker = async (word) => {
        try {
            const response = await fetch('/static/app/mots.txt');
            const contents = await response.text().then(data => data.replace(/\u0000/g, ''));
            return contents.includes(word);
        } catch (err) {
            console.error(err);
        }
        return false;
    }

    async function handleKeydown(event) {
        const letters = words[current_word].querySelectorAll('.letter');
        let word = words[current_word].getAttribute('data-word');
        simulateKeydown(event);
        if (!end) {
            if (event === "Enter") {
                const word_exists = await wordChecker(word);
                if (word_exists) {
                    if (current_letter === word_data.len_word_to_guess && word_exists) {
                        addAnimationLetters(letters);
                        correct_letters = verifyLetters(letters, word_data.word_to_guess, correct_letters);
                        if (type_of_game === 'robot') {
                            if (current_word < word_data.all_guesses.length - 1) {
                                addRobotWord(word_data.all_guesses, words, current_word, word_data.len_word_to_guess);
                            }
                        }
                        if (word === word_data.word_to_guess) {
                            end = true;
                            if (current_word < word_data.all_guesses.length - 1) {
                                displayPopUp(true);
                            } else if (current_word === word_data.all_guesses.length - 1) {
                                displayPopUp('draw');
                            } else {
                                displayPopUp(false);
                            }
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
                            displayPopUp(false);
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
                } else if (!word_exists) {
                    const wrong_word = document.querySelector('.wrong-word');
                    wrong_word.style.opacity = 1;
                    setTimeout(() => {
                        wrong_word.style.transition = 'opacity 1s ease-in-out';
                        wrong_word.style.opacity = 0;
                        setTimeout(() => wrong_word.style.transition = 'none', 1000);
                    }, 3000);
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