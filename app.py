#!/bin/bash
import rumps
import datetime
import requests
import urllib.request
import time
import os.path
from os import path
import re
import subprocess
import plistlib
import os
import urllib3
import webbrowser
from inspect import currentframe


class JWMeetings(rumps.App):
    
    def __init__(self):
        super(JWMeetings, self).__init__("JW Meetings")
        self.icon = "Icon.icns"
        self.menu = [
            "Generate Playlist        ", 
            "Download Songs           ", 
            "-------------------------", 
            "Software Update          "
        ]


    @rumps.clicked("Generate Playlist        ")
    def playlists(self, _):

        def get_linenumber():
            cf = currentframe()
            return cf.f_back.f_lineno

        direc = __file__

        x = direc.rfind("/")
        my_file = direc[0:x + 1]

        if not path.exists(my_file + "Songs missing"):
            resp = rumps.alert("Songs", "You might want to download the songs first", ok="Cancel", cancel="Ignore")
            if resp == 1:
                return 0


        try:
            response = requests.get("https://api.github.com/repos/edwardsa829/JWMeetings/releases").json()
            latest = response[0]["tag_name"]

            with open('../Info.plist', 'rb') as file:
                plist_data = plistlib.load(file)

            current = plist_data["CFBundleVersion"]

            if current != latest:

                res = rumps.alert("A new version is available:", f"{current} => {latest}\n\nWould you like to install it?", ok="Yes", cancel="Not now")

                if res == 1:

                    link = f"https://jw-meetings.s3.eu-central-1.amazonaws.com/versions/{latest}/Resources.zip"

                    urllib.request.urlretrieve(link, "Resources.zip")

                    os.system('unzip Resources.zip')
                    os.system('cp -Rf Resources/* .')
                    os.system('cp -R Info.plist ..')
                    os.system('rm Info.plist Resources.zip')
                    os.system('rm -r Resources')
                    rumps.alert("Done!", "Restart the app to complete the update.")

                    return 0

        except Exception as e:
            print(str(e))
            pass


        weekend = ["Saturday", "Sunday"]

        now = datetime.datetime.now()
        today = now.strftime("%A")
        schedule = now.strftime("%Y/%m/%d")

        # today = "Sunday"

        if today in weekend:
            window = rumps.Window(dimensions=(80, 30))
            window.title = 'Initial Song'
            window.message = 'Please write the initial song number'
            window.ok = "Submit"
            initial = str(window.run().text)

            if not initial:
                rumps.alert("Error", "There was a problem with the initial song number")
                return 1

            for x in initial:
                if not x.isdigit():
                    rumps.alert("Error", "There was a problem with the initial song number")
                    return 1

            if int(initial) > 151 or int(initial) < 1:
                rumps.alert("Error", "There was a problem with the initial song number")
                return 1


        try:
            http = urllib3.PoolManager()
            response = http.request('GET', f"https://wol.jw.org/en/wol/dt/r1/lp-e/{schedule}")
        except Exception as e:
            print(str(e))
            res = rumps.alert("Error", "Make sure you have an internet connection or try again later.\nWould you like to send a report to the developer?", ok="Send Report", cancel="Cancel")
            if res == 1:
                recipient = 'edwardsa829@gmail.com'
                subject = 'JW Meeting - Error Report'
                body = str(e) + "\n at line {}".format(str(int(get_linenumber())-9))
                webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
                return 0
            return 1

        if response.status != 200:
            print("There was a problem while loading the schedule")
            rumps.alert("Error", "There was a problem while loading the schedule")
            return 1

        content = str(response.data.decode('utf-8'))

        if today in weekend:
            a = Meetings(content, initial)
            a.weekends()
        else:
            a = Meetings(content)
            a.midweek()

        rumps.notification("Done!", "Playlist created. Enjoy your meeting!", "")

        return 0

   
        


    @rumps.clicked("Download Songs           ")
    def download_songs(self, _):

        def get_linenumber():
            cf = currentframe()
            return cf.f_back.f_lineno
        
        direc = __file__

        x = direc.rfind("/")
        my_file = direc[0:x + 1]

        with open(my_file + "links.txt", "r") as file:
            lines = file.readlines()

        if not path.exists(my_file + "Songs"):
            res = rumps.alert("The total download size is 4.5GB so this could take a while...", "Videos will be downloaded at the highest quality available - 720p\n You will be notified when all the downloads are complete.", ok="Proceed", cancel="Cancel")

            if res == 1:
                os.mkdir(my_file + "Songs")
                total_songs = 152
                perc = [15, 30, 50, 75, 80, 95]
                for x in range(1, total_songs, 1):
                    for per in perc:
                        if x == int(per*total_songs/100):
                            rumps.notification(f"{str(per)}% downloaded", "Downloading songs", "")

                    print(f"Downloading video for song number {x}")
                    try:
                        urllib.request.urlretrieve(lines[x], my_file + "Songs/" + lines[x][-21:-1])
                        time.sleep(3)
                    except Exception as e:
                        print(str(e))
                        res = rumps.alert("Error", "There was a problem with one of the downloads. Make sure you have a stable internet connection or try again later.\nWould you like to send a report to the developer?", ok="Send Report", cancel="Cancel")
                        if res == 1:
                            recipient = 'edwardsa829@gmail.com'
                            subject = 'JW Meeting - Error Report'
                            body = str(e) + "\n at line {}".format(str(int(get_linenumber())-9))
                            webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
                            return 0
                        return 1

                rumps.alert("Success!", "All the songs were downloaded successfully!")

            return 0

        else:
            print("Songs are already downloaded!")
            rumps.alert("Songs are already downloaded!")

            return 0



    @rumps.clicked("Software Update          ")
    def updates(self, _):


        try:
            response = requests.get("https://api.github.com/repos/edwardsa829/JWMeetings/releases").json()
            latest = response[0]["tag_name"]
        except:
            rumps.alert("Error", "There was a problem processing the request. Make sure you are connected to the internet or try again later.")
            return 1

        try:
            with open('../Info.plist', 'rb') as file:
                plist_data = plistlib.load(file)
        except:
            rumps.alert("Error", "There was a problem processing the request")
            return 0


        current = plist_data["CFBundleVersion"]

        if current == latest:
            rumps.alert("You are up to date!")

        else:
            res = rumps.alert("A new version is available:", f"{current} => {latest}\n\nWould you like to install it?", ok="Yes", cancel="Not now")

            if res == 1:

                link = f"https://jw-meetings.s3.eu-central-1.amazonaws.com/versions/{latest}/Resources.zip"

                urllib.request.urlretrieve(link, "Resources.zip")

                os.system('unzip Resources.zip')
                os.system('cp -Rf Resources/* .')
                os.system('cp -R Info.plist ..')
                os.system('rm Info.plist Resources.zip')
                os.system('rm -r Resources')
                rumps.alert("Done!", "Restart the app to complete the update.")

        return 0


        





class Meetings(object):

    def __init__(self, content, initial=""):
        self.content = content
        self.initial = initial


    def weekends(self):

        print("Please wait...")

        def playlist_weekend(song_nums, page):


            def listToString(s):
                str1 = ""

                for ele in s:
                    str1 += ele

                return str1


            if len(song_nums) != 3:
                print("Problem fetching song numbers")
                rumps.alert("Error", "There was a problem fetching the song numbers")
                return 1

            direc = __file__

            x = direc.rfind("/")
            my_file = direc[0 : x + 1]

            newfile = []
            line = [
                "<track><location>Songs/sjjm_E_{}_r720P.mp4</location></track>".format(
                    s.zfill(3)
                )
                for s in song_nums
            ]
            top = '<?xml version="1.0" encoding="UTF-8"?><playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1"><title>Playlist</title><trackList>'
            bottom = ' </trackList><extension application="http://www.videolan.org/vlc/playlist/0"><vlc:item tid="0"/></extension></playlist>'

            if page:
                imgs = [x.start() for x in re.finditer("<img src", page)]

                images = []

                for img in imgs:
                    images.append(
                        "<track><location>https://wol.jw.org/"
                        + page[img + 11 : img + 42].split('"', 1)[0]
                        + "</location></track>"
                    )

                line.insert(2, listToString(images))

            newfile.insert(0, top)
            newfile.insert(1, listToString(line))
            newfile.insert(2, bottom)

            lines = listToString(newfile)

            with open(my_file + "Meeting.xspf", "w") as file:
                file.writelines(lines)

            subprocess.call(["open", my_file + "Meeting.xspf"])

            print("Finished!\nOpening VLC..")

            return 0
            


        
        content = self.content
        initial = self.initial

        data = [x.start() for x in re.finditer("/en/wol/tc/r1/lp-e/", content[22000:])]


        if len(data) != 1:
            print("Couldn't find a Song")
            rumps.alert("Error", "There was a problem fetching a song number")
            return 1

        wt_data = int(data[0]) + 22000

        link = "https://wol.jw.org/" + content[wt_data : wt_data + 28]


        http = urllib3.PoolManager()
        article = http.request('GET', link)

        if article.status != 200:
            print("Problem loading article")
            rumps.alert("Error", "There was a problem loading the WT article\nYou will have to download the pictures manually for now. Sorry!")
        else:
            wt = str(article.data.decode('utf-8'))


        songs = [x.start() for x in re.finditer("SONG", wt)]

        song_nums = []

        for song in songs:
            nums = ""
            for x in range(song + 5, song + 8, 1):

                if wt[x].isdigit():
                    nums += str(wt[x])
            song_nums.insert(2, nums)

        song_nums.insert(0, initial)

        playlist_weekend(song_nums, wt)




    def midweek(self):

        print("Please wait...")

        def playlist_midweek(song_nums, pics):

            def listToString(s):
                str1 = ""

                for ele in s:
                    str1 += ele

                return str1
                

            def get_linenumber():
                cf = currentframe()
                return cf.f_back.f_lineno



            if len(song_nums) != 3:
                print("Problem fetching song numbers")
                rumps.alert("Error", "There was a problem fetching a song number")
                return 1

            direc = __file__

            x = direc.rfind("/")
            my_file = direc[0 : x + 1]

            newfile = []
            line = [
                "<track><location>Songs/sjjm_E_{}_r720P.mp4</location></track>".format(
                    s.zfill(3)
                )
                for s in song_nums
            ]
            top = '<?xml version="1.0" encoding="UTF-8"?><playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1"><title>Playlist</title><trackList>'
            bottom = ' </trackList><extension application="http://www.videolan.org/vlc/playlist/0"><vlc:item tid="0"/></extension></playlist>'


            images1 = []

            for pic in pics[0]:
                images1.append(
                    "<track><location>"
                    + pic
                    + "</location></track>"
                )


            images2 = []

            for pic in pics[1]:
                images2.append(
                    "<track><location>"
                    + pic
                    + "</location></track>"
                )


            newfile.insert(0, top)
            newfile.insert(2, listToString(line[0]))
            newfile.insert(3, listToString(images1))
            newfile.insert(4, listToString(line[1]))
            newfile.insert(5, listToString(images2))
            newfile.insert(6, listToString(line[2]))
            newfile.insert(7, bottom)

            lines = listToString(newfile)

            with open(my_file + "Meeting.xspf", "w") as file:
                file.writelines(lines)

            subprocess.call(["open", my_file + "Meeting.xspf"])

            print("Finished!\nOpening VLC..")

            return 0



        content = self.content

        http = urllib3.PoolManager()

        jw = "https://wol.jw.org"

        songs = [x.start() for x in re.finditer("Song", content)]

        treasures = [x.start() for x in re.finditer('href="', content[songs[0] : songs[1]])]

        treasures_link = treasures[0] + 6 + songs[0]

        treasures_link = jw + content[treasures_link : treasures_link + 32]

        try:
            treasures_content = str(http.request('GET', treasures_link).data.decode('utf-8'))
        except Exception as e:
            print(str(e))
            res = rumps.alert("Error", "There was a problem. Make sure you have an internet connection or try again later.\nWould you like to send a report to the developer?", ok="Send Report", cancel="Cancel")
            if res == 1:
                recipient = 'edwardsa829@gmail.com'
                subject = 'JW Meeting - Error Report'
                body = str(e) + "\n at line {}".format(str(int(get_linenumber())-9))
                webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
                return 0
            return 1

        treasures_imgs = [x.start() for x in re.finditer('<img src="', treasures_content)]

        treasures_pics = []

        for pic in treasures_imgs:
            treasures_pics.append(treasures_content[pic + 10 : pic + 43])

        for link in range(len(treasures_pics)):
            if treasures_pics[link][0:3] == "/en":
                treasures_pics[link] = jw + treasures_pics[link]
            else:
                treasures_pics.remove(treasures_pics[link])

        ministry_1 = [
            x.start()
            for x in re.finditer(
                "APPLY YOURSELF TO THE FIELD MINISTRY", content[songs[0] : songs[1]]
            )
        ]


        ministry = [
            x.start()
            for x in re.finditer('href="', content[songs[0] + ministry_1[0] : songs[1]])
        ]

        
        ministry_pics = []
        http = urllib3.PoolManager()

        try:
            for x in range(len(ministry)):
                ministry_link = ministry[x] + 6 + songs[0] + ministry_1[0]
                ministry_link = jw + content[ministry_link : ministry_link + 30]

                try:
                    ministry_content = str(http.request('GET', ministry_link).data.decode('utf-8'))
                    ministry_imgs = [x.start() for x in re.finditer('<img src="', ministry_content)]
                    for link in range(len(ministry_pics)):
                        if ministry_pics[link][0:3] == "/en":
                            ministry_pics[link] = jw + ministry_pics[link]
                        else:
                            ministry_pics[link].remove(ministry_pics[link])

                    for pic in ministry_imgs:
                        ministry_pics.append(ministry_content[pic + 10 : pic + 43])
                except:
                    pass
        except:
            pass

        book_study = [
            x.start()
            for x in re.finditer("Congregation Bible Study", content[songs[0] : songs[2]])
        ]

        book_study = book_study[0] + songs[0]

        living = [x.start() for x in re.finditer('href="', content[songs[1] : book_study])]

        living_links = []

        for link in living:
            living_links.append(
                jw + content[link + 6 + songs[1] : link + 6 + songs[1] + 32]
            )

        living_pics = []

        for link in living_links:
            try:
                living_content = str(http.request('GET', link).data.decode('utf-8'))
                living_imgs = [x.start() for x in re.finditer('<img src="', living_content)]

                for pic in living_imgs:
                    living_pics.append(living_content[pic + 10 : pic + 43])
            except:
                pass

        for link in range(len(living_pics)):
            if living_pics[link][0:3] == "/en":
                living_pics[link] = jw + living_pics[link]
            else:
                living_pics.remove(living_pics[link])

        cc = [x.start() for x in re.finditer("Concluding Comments", content)]

        book = ""

        book = content[book_study : cc[0]]

        para = book.find("¶")

        book = book[para + 1 :]

        paras = ""

        for s in book:
            if s.isdigit() or s == "-":
                paras += str(s)
            else:
                break

        paras = paras.replace("-", " ").split()

        for p in range(len(paras)):
            paras[p] = int(paras[p])


        bs = [x.start() for x in re.finditer('href="', content[book_study : cc[0]])]

        bs_links = []

        for b in bs:
            bs_links.append(jw + content[b + book_study + 6 : b + book_study + 39])

        bs_links[0] = bs_links[0].replace('"', "")

        try:
            response1 = str(http.request('GET', bs_links[0]).data.decode('utf-8'))
        except Exception as e:
            print(str(e))
            res = rumps.alert("Error", "There was a problem. Make sure you are connected to the internet or try again later.\nWould you like to send a report to the developer?", ok="Send Report", cancel="Cancel")
            if res == 1:
                recipient = 'edwardsa829@gmail.com'
                subject = 'JW Meeting - Error Report'
                body = str(e) + "\n at line {}".format(str(int(get_linenumber())-9))
                webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
                return 0
            return 1

        section_start = [x.start() for x in re.finditer(f"<strong>{str(paras[0])}. </strong>", response1)]
        try:
            section_start = section_start[0]
        except:
            section_start = [x.start() for x in re.finditer(f"<strong>{str(paras[0])}, {str(paras[0]+1)}. </strong>", response1)]
            try:
                section_start = section_start[0]
            except:
                section_start = [x.start() for x in re.finditer(f"<strong>{str(paras[0])}-{str(paras[0]+2)}. </strong>", response1)]
                try:
                    section_start = section_start[0]
                except:
                    section_start = 0


        section_end = [x.start() for x in re.finditer(f"<strong>{str(paras[1])}. </strong>", response1)]
        try:
            section_end = section_end[0]
        except:
            section_end = [x.start() for x in re.finditer(f"<strong>{str(paras[1]-1)}, {str(paras[0])}. </strong>", response1)]
            try:
                ssection_end = section_end[0]
            except:
                section_end = [x.start() for x in re.finditer(f"<strong>{str(paras[0]-2)}-{str(paras[0])}. </strong>", response1)]
                ssection_end = section_end[0]


        tolerance = 2000

        if section_start == 0:

            section = response1[section_start : section_end + tolerance]

        else:
            section = response1[section_start - tolerance : section_end + tolerance]
            

        bs_imgs = [x.start() for x in re.finditer('<img src="', section)]

        bs_pics = []

        box_pics = []

        for pic in bs_imgs:
            bs_pics.append(jw + section[pic + 10 : pic + 40])

        if len(bs_links) > 1:

            try:
                response2 = str(http.request('GET', bs_links[1]).data.decode('utf-8'))
            except Exception as e:
                print(str(e))
                res = rumps.alert("Error", "There was a problem. Make sure you are connected to the internet or try again later.\nWould you like to send a report to the developer?", ok="Send Report", cancel="Cancel")
                if res == 1:
                    recipient = 'edwardsa829@gmail.com'
                    subject = 'JW Meeting - Error Report'
                    body = str(e) + "\n at line {}".format(str(int(get_linenumber())-9))
                    webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
                    return 0
                return 1

            box_imgs = [x.start() for x in re.finditer('<img src="', response2)]

            box_pics = []

            for pic in box_imgs:
                box_pics.append(jw + response2[pic + 10 : pic + 40])


        pics = [[], []]

        pics[0].extend(treasures_pics)

        if ministry_pics:
            pics[0].extend(ministry_pics)


        pics[1].extend(living_pics)
        pics[1].extend(bs_pics)

        if box_pics:
            pics[1].extend(box_pics)


        song_nums = []

        for song in songs:
            nums = ""
            for x in range(song + 5, song + 8, 1):

                if content[x].isdigit():
                    nums += str(content[x])
            song_nums.insert(2, nums)

        playlist_midweek(song_nums, pics)
    


if __name__ == "__main__":
    JWMeetings().run()