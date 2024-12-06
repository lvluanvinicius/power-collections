from datetime import time, datetime
from itertools import count
from os import system
from sys import argv

if not len(argv) <= 2:
    if argv[1] == "migration":
        dateActual = datetime.now().strftime("%Y%m%d%H%M%S")
        system(f"cd Database/Migrations && touch {argv[2]}-{dateActual}.py")