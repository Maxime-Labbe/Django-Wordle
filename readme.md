# Wordle Against a Robot

This project is a Wordle game where you can play against a robot and on your own. The game is built using Python and Django for the backend, and HTML, CSS, and JavaScript for the frontend.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## Installation

### Prerequisites

- Python 3.x
- Django

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/Maxime-Labbe/Django-Wordle.git
    cd Django-Wordle
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Django migrations:

    ```bash
    python manage.py migrate
    ```

4. Start the Django development server:

    On local device :

    ```bash
    python manage.py runserver 
    ```

    On local Network:

    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

5. Open your browser and navigate to `http://127.0.0.1:8000` or `https://ip:8000` (from other devices on the network) to play the game.

## Usage

### Playing the Game

- Open the game in your browser.
- Enter your guesses in the input field and press Enter.
- The robot will make its guesses and display the results.
- The game continues until the word is guessed correctly or the maximum number of guesses is reached.

### API Endpoints

- `/api/get_data_robot`: Fetches data for the robot game.
- `/api/get_data_solo`: Fetches data for the solo game.

## Project Structure

Django-Wordle/
├── api/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── app/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── robot.py
│   ├── static/
│   │   ├── app/
│   │   │   ├── fonts/
│   │   │   │   ├── Cocogoose-Pro-Bold-Italic-trial.ttf
│   │   │   │   ├── Cocogoose-Pro-Bold-trial.ttf
│   │   │   │   ├── Cocogoose-Pro-Italic-trial.ttf
│   │   │   │   ├── Cocogoose-Pro-Light-Italic-trial.ttf
│   │   │   │   ├── Cocogoose-Pro-Light-trial.ttf
│   │   │   │   └── Cocogoose-Pro-Regular-trial.ttf
│   │   │   ├── images/
│   │   │   │   ├── github.svg
│   │   │   │   ├── left-arrow.svg
│   │   │   │   ├── linkedin.svg
│   │   │   │   └── right-arrow.svg
│   │   │   ├── style/
│   │   │   │   ├── index.css
│   │   │   │   ├── robot.css
│   │   │   │   ├── solo.css
│   │   │   │   └── style.css
│   │   │   ├── mots.txt
│   │   │   └── script.js
│   │   └── tri.py
│   ├── templates/
│   │   ├── app/
│   │   │   ├── index.html
│   │   │   ├── robot.html
│   │   │   └── solo.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── mysite/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md