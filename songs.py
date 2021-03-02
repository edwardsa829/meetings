import urllib.request
import time
import os.path
from os import path

direc = __file__

x = direc.rfind("/")
my_file = direc[0:x + 1]

with open(my_file + "links.txt", "r") as file:
    lines = file.readlines()

for x in range(1, 152, 1):

    time.sleep(3)
    print(f"Downloading video for song number {x}")

    if not path.exists(my_file + "Songs"):
        os.mkdir(my_file + "Songs")

    urllib.request.urlretrieve(lines[x], my_file + "Songs/" + lines[x][-21:-1])

