import os
from functools import reduce

def give_dir(current_file, level_up=0):
    dir = os.path.dirname(current_file)
    dir = reduce(lambda d, _: give_dir(d), range(level_up), dir)
    return dir
