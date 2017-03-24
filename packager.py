import sys
import re
from src import Packager


def main():
    pkg = Packager()

    while(True):
        cmd = raw_input("> ")

        # read all the words the use entered but without any surrounding spaces
        words = [word.strip() for word in re.split('\W+', cmd) if word.strip()]

        # if you didn't enter anything and press <ENTER>
        if len(words) == 0:
            continue

        # the first word is the main command
        command = words[0]

        # the following words are the arguments
        if len(words) > 1:
            arguments = words[1:]

        if command == 'DEPEND':
            pkg.depend(arguments[0], *arguments[1:])

        elif command == 'INSTALL':
            pkg.install(arguments[0])

        elif command == 'REMOVE':
            pkg.remove(arguments[0])

        elif command == 'LIST':
            for package_name in pkg.list():
                print("\t%s" % package_name)

        elif command == 'END':
            sys.exit(0)

        else:
            print "ERROR: unknow command %s" % (command)

if __name__ == '__main__':
    main()
