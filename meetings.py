import datetime
import requests
import re
import os
import subprocess


def meetings():
    print("Please wait...")

    weekend = ["Saturday", "Sunday"]

    now = datetime.datetime.now()
    today = now.strftime("%A")
    schedule = now.strftime("%Y/%m/%d")


    response = requests.get(f"https://wol.jw.org/en/wol/dt/r1/lp-e/{schedule}")

    if response.status_code != 200:
        print("Problem loading page")
        exit(1)

    content = str(response.text)

    #today = "Sunday"

    if today in weekend:
        weekends(content)
    else:
        midweek(content)



def weekends(content):
    data = [x.start() for x in re.finditer('/en/wol/tc/r1/lp-e/', content[22000:])]

    if len(data) != 1:
        print("Couldn't find a Song")
        exit(1)

    wt = int(data[0]) + 22000

    link = "https://wol.jw.org/" + content[wt:wt+28]

    article = requests.get(link)

    if article.status_code != 200:
        print("Problem loading article")
        exit(1)

    initial = str(input("Initial song number: "))

    page = str(article.text)

    songs = [x.start() for x in re.finditer('SONG', page)]

    song_nums = []

    for song in songs:
        nums = ""
        for x in range(song + 5, song + 8, 1):

            if page[x].isdigit():
                nums += str(page[x])
        song_nums.insert(2, nums)

    song_nums.insert(0, initial)

    playlist(song_nums, page)


def midweek(content):

    songs = [x.start() for x in re.finditer('Song', content)]

    song_nums = []

    for song in songs:
        nums = ""
        for x in range(song+5, song+8, 1):

            if content[x].isdigit():
                nums += str(content[x])
        song_nums.insert(2, nums)

    playlist(song_nums)


def playlist(song_nums, page=""):

    if len(song_nums) != 3:
        print("Problem fetching song numbers")
        exit(1)

    my_file = os.getcwd() + "/"

    newfile = []
    line = ["<track><location>{}/sjjm_E_{}_r720P.mp4</location></track>".format(my_file + "Songs", s.zfill(3)) for s in song_nums]
    top = '<?xml version="1.0" encoding="UTF-8"?><playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1"><title>Playlist</title><trackList>'
    bottom = ' </trackList><extension application="http://www.videolan.org/vlc/playlist/0"><vlc:item tid="0"/></extension></playlist>'

    newfile.insert(0, top)
    newfile.insert(1, listToString(line))
    newfile.insert(2, bottom)
    lines = listToString(newfile)


    if page:
        imgs = [x.start() for x in re.finditer('<img src', page)]

        images = []

        for img in imgs:
            images.append("<track><location>https://wol.jw.org/" + page[img+11:img+42].split("\"", 1)[0] + "</location></track>")

        pics = listToString(images)


        found = lines.find(" </trackList>")
        lines = lines[:found] + pics + lines[found:]


    with open(my_file + "Meeting.xspf", 'w') as file:
        file.writelines(lines)


    subprocess.call(['open', my_file + "Meeting.xspf"])

    print("Finished!\nOpening VLC..")


def listToString(s):
    str1 = ""

    for ele in s:
        str1 += ele

    return str1

if __name__ == "__main__":
    meetings()

