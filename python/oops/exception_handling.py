import sys
import random

try:
    print(f"First argument {sys.argv[1]}")
    args = sys.argv
    random.shuffle(args)
    print(f"Random argument {args[0]}")
except (IndexError, KeyError) as err:
    print(f"Error: no arguments, please provide at least one argument ({err})")
except NameError:
    print(f"Error: random module not loaded")
else:
    print("Else is running")
finally:
    print("Finally is running")
