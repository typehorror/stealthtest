import sys
import re
from src import Packager


def main():
    pkg = Packager()

    while(True):
        try:
            cmd = raw_input("> ")
        except KeyboardInterrupt:  # <CTRL> + <C> is error exit
            sys.exit(1)
        except EOFError:  # <CTRL> + <D> is good exit
            sys.exit(0)

        # read all the words the user entered stripped of surrounding spaces
        words = [word.strip() for word in re.split('\W+', cmd) if word.strip()]

        if words:
            # the first word is the main command
            command = words[0]

            # the following words are the arguments
            arguments = words[1:]

            if command == 'DEPEND':
                pkg.depend(*arguments)

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
