def message_validator(data):
    if len(data) < 1000:
        prep = []
        for i in data:
            i = data_checker(i)
            prep.append(str(i))
        return ''.join(prep)
    else:
        return False


def data_checker(data):
    if data == '"':
        data = '&quot;'
    elif data == '/':
        data = '&#47;'
    elif data == "'":
        data = '&apos;'
    elif data == '<':
        data = '&lt;'
    elif data == '>':
        data = '&gt;'
    elif data == '\\':
        data = '&#92;'
    elif data == '#':
        data = '&#35;'
    elif data == '@':
        data = '&#64;'
    return data
