import sys

from __init__ import main
from errors   import ArgumentError

try:
    main()
except ArgumentError as err:
    print(f"Error: {err}")
    sys.exit(1)