from random import randint


name = 'Me'
TITLE = ['Home', 'Домашняя']
WELCOME_RANDOM_RU = ['Добро пожаловать!', 'Вечер в хату!', 'привет........', 'ХОЙ!!']
WELCOME_RANDOM_EN = ['Welcome to the HQ!', 'helo.......', 'Cyber-greetings', 'Pog?']


def greet(language_code):
    if language_code == 0:
        return WELCOME_RANDOM_EN[randint(0, 3)]
    elif language_code == 1:
        return WELCOME_RANDOM_RU[randint(0, 3)]
