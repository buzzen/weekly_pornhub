import sys

foo = ("default" if len(sys.argv) < 2 
    else sys.argv[1])

print(foo)