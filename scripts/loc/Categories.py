CREATE = ['Create a thread', 'Создать тред']
BROADCAST = ['Broadcast', 'Вещание']
ANIMATION = ['Animation', 'Анимация']
ARTWORK = ['Artwork', 'Искусство']
CINEMATICS = ['Cinematics', 'Кинематограф']
VIDEOGAMES = ['Videogames', 'Игры']
RANDOM = ['Random', 'Бред']
CUSTOM = ['Custom', 'Пользовательские']
NSFW = ['NSFW', 'Для Взрослых']
MEMES = ['Memes', 'Мемы']
ONLINE = ['Online', 'Онлайн']
OFFLINE = ['Offline', 'Оффлайн']
HITECH = ['HiTech', 'Выс. Технологии']
FEEDBACK = ['Feedback', 'Отзывы']
POLITICS = ['Politics', 'Политика']
ESPORTS = ['Esports', 'Киберспорт']
FRESH_AIR = ['Fresh Air', 'Свежий Воздух']
WRITING = ['Writing', 'Писательство']


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
    elif cat == 'Custom':
        return CUSTOM
    elif cat == 'NSFW':
        return NSFW
    elif cat == 'Memes':
        return MEMES
    elif cat == 'Online':
        return ONLINE
    elif cat == 'Offline':
        return OFFLINE
    elif cat == 'HiTech':
        return HITECH
    elif cat == 'Feedback':
        return FEEDBACK
    elif cat == 'Politics':
        return POLITICS
    elif cat == 'Esports':
        return ESPORTS
    elif cat == 'Fresh Air':
        return FRESH_AIR
    elif cat == 'Writing':
        return WRITING
