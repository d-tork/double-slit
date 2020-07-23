from os import path

PROJ_PATH = path.normpath(path.join(path.dirname(path.realpath(__file__)), '..'))
NAMES_FILE = path.join(PROJ_PATH, 'src', 'names.csv')