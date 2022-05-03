# Check if the project is in build mode
from os.path import exists
from platform import system
from sys import path

if not exists('build'):
    operating_system = system()

    if operating_system == 'Linux':
        path.insert(0, '/lib/advaced/1.0.0/')

    elif operating_system == 'Windows':
        path.insert(0, 'C:\\Program Files\\advaced')

    elif operating_system == 'Darwin':
        path.insert(0, '/Library/advaced/1.0.0/')


# Project modules
from cmd import handle_input


def main():
    # Take care of the input
    handle_input()
    return


if __name__ == '__main__':
    main()
