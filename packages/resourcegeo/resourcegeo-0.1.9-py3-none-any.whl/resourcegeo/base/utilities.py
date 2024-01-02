'Statistics calculation'

__author__ = 'Harold Velasquez'
__date__ = '2023-011'

import os, re
def purge(dir, pattern):
    '''Delete files in that match a pattern
    in a directory.
    
    dir(str): path to directory
    pattern(str): pattern to match in files
    '''
    to_del = []
    for f in os.listdir(dir):
        if re.search(pattern, f):
            to_del.append(f)

    if len(to_del)==0:
        print('pattern not found')
    else:
        print(f'The following files are about to be removed:\n')
        for f in to_del:
            print(f)
        if input("are you sure? (y/n)") == "y":
            for f in to_del:
                try:
                    os.remove(os.path.join(dir, f))
                except Exception as e:
                    print(f'Error while removing {f}')
            print('\nRemoving files finished')
    return