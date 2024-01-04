"""See top level package docstring for documentation"""

import logging
import pathlib

myself = pathlib.Path(__file__).stem

logger = logging.getLogger(myself)
logging.getLogger(myself).addHandler(logging.NullHandler())

########################################################################

def main():
    pass

if __name__ == '__main__':
    main()
