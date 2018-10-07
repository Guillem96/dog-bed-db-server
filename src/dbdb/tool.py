from __future__ import print_function
import sys

import dbdb

# Define exit codes
OK = 0
BAD_ARGS = 1
BAD_VERB = 2
BAD_KEY = 3

def usage(): # -m Runs python module as a script
    print("Usage:", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME get KEY", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME set KEY VALUE", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME delete KEY", file=sys.stderr)


def main(argv):
    if not (4 <= len(argv) <= 5): # Use of intervals
        usage()
        return BAD_ARGS
    dbname, verb, key, value = (argv[1:] + [None])[:4] # Adding None in case of get
    if verb not in {'get', 'set', 'delete'}: # Creating a set
        usage()
        return BAD_VERB
    db = dbdb.connect(dbname)
    try:
        if verb == 'get':
            sys.stdout.write(db[key]) # No need to use print db[key] returns always an string
        elif verb == 'set':
            db[key] = value
            db.commit()
        else:
            del db[key]
            db.commit()
    except KeyError:
        print("Key not found", file=sys.stderr)
        return BAD_KEY
    return OK


if __name__ == '__main__':
    sys.exit(main(sys.argv))
