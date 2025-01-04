async function script() {
    function verifyLetter(letter, index, word_to_guess) {
        if (letter.textContent.trim() != "." && letter.textContent.trim() != "") {
            if (letter.textContent.trim() === word_to_guess[index]) {
                letter.style.backgroundColor = '#018E42';
            } else if (word_to_guess.includes(letter.textContent.trim())) {
                letter.style.backgroundColor = '#F07A05';
            } else {
                letter.style.backgroundColor = '#BF1A2F';
            }
        }
    }

    async function displayDots(current_word, len_word) {
        const letters = words[current_word].querySelectorAll('.letter');
        for (let i = 0; i < len_word; i++) {
            letters[i].textContent = ".";
        }
    }

    function displayPopUp(win) {
        const popUpContainer = document.querySelector('.pop-up-container');
        if (win) {
            popUpContainer.querySelector('h2').textContent = 'Bravo !';
            popUpContainer.querySelector('p').textContent = 'Vous avez gagné !';
        } else {
            popUpContainer.querySelector('h2').textContent = 'Dommage !';
            popUpContainer.querySelector('p').textContent = 'Vous avez perdu !';
        }
        popUpContainer.style.visibility = 'visible';
    }


    function handleKeydown(event) {
        const letters = words[current_word].querySelectorAll('.letter');
        let word = words[current_word].getAttribute('data-word');
        if (!end) {
            if (event.key === "Enter") {
                if (current_letter == word_data.len_word_to_guess) {
                    letters.forEach((letter, index) => {
                        verifyLetter(letter, index, word_data.word_to_guess);
                    });
                    if (word === word_data.word_to_guess) {
                        end = true;
                        document.removeEventListener("keydown", handleKeydown, true);
                        displayPopUp(true);
                    } else if (current_word == 5) {
                        end = true;
                        document.removeEventListener("keydown", handleKeydown, true);
                        displayPopUp(false);
                    } else {
                        current_word += 1;
                        current_letter = 0;
                        displayDots(current_word, word_data.len_word_to_guess);
                    }
                }
            } else if (event.key === "Backspace") {
                if (current_letter > 0) {
                    current_letter--;
                    word = word.slice(0, -1);
                    letters[current_letter].textContent = '.';
                }
            } else {
                if (current_letter < word_data.len_word_to_guess && event.key.match(/[a-z]/i) && event.key.length === 1) {
                    word += event.key;
                    words[current_word].setAttribute('data-word', word);
                    letters[current_letter].textContent = event.key;
                    current_letter++;
                }
            }
        }

    }

    document.addEventListener("DOMContentLoaded", () => {
        const letters = document.querySelectorAll('.letter');
        letters.forEach(letter => {
            const width = letter.getAttribute('data-width');
            letter.style.width = width;
        });
        document.addEventListener("keydown", handleKeydown);
    });

    let current_word = 0;
    let current_letter = 0;
    let word_data;
    const words = document.querySelectorAll('.word');
    const letters = words[current_word].querySelectorAll('.letter');
    let word = words[current_word].getAttribute('data-word');
    let end = false;
    await fetch('/api/get_word_to_guess', {
        headers: {
            'X-SECRET-TOKEN': 'dzabvyu546456DJSQD6DAZ6TDQU6fa'
        }
    })
        .then(response => response.json())
        .then(data => {
            word_data = data.data;
        });
    displayDots(current_word, word_data.len_word_to_guess);
};

script();