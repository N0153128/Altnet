from zipfile import ZipFile
from os.path import basename


def make_copy(path, title, target):
    archive = ZipFile(f'{path}/{title}.zip', 'w')
    for i in target:
        archive.write(i, basename(i))
    archive.close()
    return f'{path}/{title}.zip'

# pat = '/home/noise/Desktop/'
# targ = [f'{pat}test1', f'{pat}test2', f'{pat}test3']
# make_copy(pat, 'test', targ)
