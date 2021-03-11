# meetings
This is a script to help automate the creation of VLC playlist with all neccesasry media for the meeting. It is only recommended for Mac and Linux users only as Windows users have the native JW Library App.

# Getting Started

# Prerequisites

Install python3 or upgrade to the latest version

# Basic Installation

1. Clone or download the  repository into a designated folder

2. Open terminal, navigate to folder location and run
`songs.py`
This will download all meeting songs into the Songs folder for VLC to use.
Get some coffee it might take a while.

3. Next run this code to create and open a VLC playlist with songs (and pictures in the Watchtower for weekend meeting)
`python3 meetings.py`
If you run the script on Saturday or Sunday, enter Initial song number for the public talk.

VLC should open with the playlist including the songs and images from the watchtower (streamed directly from jw.org) in the order required fro the meeting.
_Some have reported images not ‘playing’ in VLC due to VPN._


# Installation Problems
**Certification verification errors**

`pip3 install --upgrade certifi`

If error persists try 
`open /Applications/Python\ 3.6/Install\ Certificates.command`

**Request library errors**
`pip3 install requests`
