CREATE = ['Create a thread', 'Создать тред']
BROADCAST = ['Broadcast', 'Вещание']
ANIMATION = ['Animation', 'Анимация']
ARTWORK = ['Artwork', 'Искусство']
CINEMATICS = ['Cinematics', 'Кинематограф']
VIDEOGAMES = ['Videogames', 'Игры']
RANDOM = ['Random', 'Бред']


def cat_resolver(cat):
    if cat == 'Broadcast':
        return BROADCAST
    elif cat == 'Animation':
        return ANIMATION
    elif cat == 'Artwork':
        return ARTWORK
    elif cat == 'Cinematics':
        return CINEMATICS
    elif cat == 'Videogames':
        return VIDEOGAMES
    elif cat == 'Random':
        return RANDOM
