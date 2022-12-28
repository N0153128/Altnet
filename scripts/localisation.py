import scripts.loc as loc


def loc_resolver(specific):
    load = {}
    if specific == 'home':
        load['me'] = loc.Me
        load['UI'] = loc.Ui
        load['errors'] = loc.Errors
        load['headers'] = loc.Headers
    elif specific == 'board':
        load['headers'] = loc.Headers
        load['errors'] = loc.Errors
        load['board_'] = loc.Board
        load['locThread'] = loc.Thread
        load['categories'] = loc.Categories
        load['UI'] = loc.UI
    elif specific == 'thread':
        load['headers'] = loc.Headers
        load['errors'] = loc.Errors
        load['board_'] = loc.Board
        load['locThread'] = loc.Thread
        load['categories'] = loc.Categories
        load['UI'] = loc.UI
    elif specific == 'account':
        load['profile'] = loc.Profile
        load['errors'] = loc.Errors
        load['headers'] = loc.Headers
        load['UI'] = loc.UI
    elif specific == 'category':
        load['loc'] = loc.UI
        load['headers'] = loc.Headers
        load['errors'] = loc.Errors
        load['board'] = loc.Board
        load['thread'] = loc.Thread
        load['categories'] = loc.Categories
    elif specific == 'lobby':
        load['UI'] = loc.UI
        load['headers'] = loc.Headers
        load['errors'] = loc.Errors
        load['board_'] = loc.Board
        load['thread'] = loc.Thread
        load['categories'] = loc.Categories
        load['chat'] = loc.Chat
    elif specific == 'room':
        load['UI'] = loc.UI
        load['headers'] = loc.Headers
        load['errors'] = loc.Errors
        load['board_'] = loc.Board
        load['thread'] = loc.Thread
        load['categories'] = loc.Categories
    elif specific == 'info':
        load['UI'] = loc.UI
        load['info'] = loc.Info

    return load
