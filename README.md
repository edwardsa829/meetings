```bash
python3.7 install.py py2app
```
![](./Logo.png)
# JW Meetings
### A playlist generator for the meetings

If you are a Jehovah’s Witness and use a Mac computer you will know that there is no native JW Library App. It can be tedious, especially if you are working in the AV department, to have to download and prepare all the songs and pictures in advance for every meeting. This application eliminates that process by doing it all for you! You will be able to create a VLC playlist containing all the media of the meeting of the current week in just a press of a button! Make sure you have VLC downloaded along with the other requirements listed below. Be sure to follow the instructions and enjoy your meeting!

##### SYSTEM REQUIREMENTS

- Mac OS X 10.9 or later
- [VLC latest version](https://www.videolan.org/vlc/download-macosx.html)
- [Python 3.7](https://www.python.org/downloads/release/python-379/)


> **Please note**: installing and running the application requires an internet connection

##### VLC
https://www.videolan.org/vlc/download-macosx.html

##### Python 3.7
https://www.python.org/downloads/release/python-379/

Download link: https://www.python.org/ftp/python/3.7.9/python-3.7.9-macosx10.9.pkg



Songs and videos are all downloaded in the highest quality available - **720p**.
Pictures are streamed.


Some have reported images not working due to VPN.



### DOWNLOAD

You will see a green button called “Code”. Press it and then select “Download ZIP”.
(https://github.com/edwardsa829/JWMeetings)



### INSTALLATION

Run the command:

```bash
python3.7 install.py py2app
```

And in a minute the application is ready for use!


#### HOW DO I RUN THE COMMAND?

First of all, make sure you have an internet connection throughout this whole process, but also whenever you are using the application.
If you downloaded the code in zip you will want to unzip it just by double clicking it. This will generate a folder called “JWMeetings-main” then:

- right-click on the folder named *JWMeetings-main*

- press *New Terminal at Folder*

- copy and paste into Terminal: `python3.7 install.py py2app`

- press enter and wait

Done!


If for some reason you can’t open Terminal by right clicking on the folder you can open Terminal directly.
You will find it in: *Applications -> Utilities*. Then you will need to navigate into the right folder where the app is. You can do this by typing `cd` and the path to the folder. So if for example the folder is in Downloads, do this:
```bash
cd Downloads/JWMeetings-main/
```

- press enter

- copy and paste in the command: `python3.7 install.py py2app`

- press enter and wait


You are now good to go!


If you are not used to seeing code you might be asking:
#### WHAT DOES THIS COMMAND DO?

You are running some code that will download some small pieces of software for the application to work and will build it.

Going into a little bit more detail, this command downloads software packages for the Python language which are listed in the *requirements.txt* file which are necessary for the application to function. After that, the code will build making it into a usable app you can then open just by double clicking it. When this is done, all the unnecessary files and folders will be deleted leaving you with just the app. 
This whole process should take a minute or less.
You are then free to move the application anywhere you like on your computer. You might want to place it in your *Applications* folder for easy access.



### HOW DO I USE THE APPLICATION?

The way you interact with the application is through the menu bar only. It’s the bar that runs along the top of your screen where all the menus are (File, Edit, View, ect..).
You will find the app towards the right side. By clicking the app's icon a little dropdown menu will appear with 4 options.


#### Download Songs
Before you start generating playlists you will want to first download all the videos for the songs otherwise they won’t work. You can do this by simply pressing *Download Songs* (2nd item in the dropdown menu).
This process will take quite a while as you are downloading over 150 heavy files. So you will have to wait. The time it takes depends on your internet connection speed. The total download size is 4.5 GB.
Once download is complete you will be notified. Be sure in the meantime your computer stays on and that you have a stable internet connection. 

#### Generate Playlist
Now that you have downloaded all the songs you can press this 1st button in the menu and your playlist will be created. This process will take 20 seconds or less. The playlist will contain all the media for the meeting of the current week also depending whether you are in the middle of the week or at the weekend (Saturday, Sunday). For the weekend meetings you will be asked for the initial song which you can then just type in the number and press “Ok”.

#### Software Update
This 3rd button checks to see if there are any new versions of the application to download. These could be changes such as new features or bug fixes. Making these changes just requires accepting the download and then restarting the app.

#### Quit
This last button closes the app.



For information on how to use VLC playlists:
https://wiki.videolan.org/Documentation:Playlist
