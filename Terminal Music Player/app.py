
#### IMPORTS #####


from mutagen.id3 import ID3
import pygame.mixer as mix #for playing music
# from PIL import ImageTk,Image #For coverting bytes to an image
# from mutagen.id3 import ID3 #for extracting song info like artist name, and album art.
# import os,io #for system commands & the bytesIO function
# import threading  #
import os
####    VARIABLES   ####
toscandirs = ['./']
songlist = [] #contains all songs with full address.
current_index = 0  #index of currently playing music -1 -> no music playing
stopped = True
playing = False
song_title = ""
song_artist = ""
song_album = ""

logo = """
  ___                   ____        __  __           _      
 / _ \ _ __   ___ _ __ |  _ \ _   _|  \/  |_   _ ___(_) ___ 
| | | | '_ \ / _ \ '_ \| |_) | | | | |\/| | | | / __| |/ __|
| |_| | |_) |  __/ | | |  __/| |_| | |  | | |_| \__ \ | (__ 
 \___/| .__/ \___|_| |_|_|    \__, |_|  |_|\__,_|___/_|\___|
      |_|                     |___/                         [V-0.1]
"""

goodbye = """
 _                  _ 
| |__  _   _  ___  | |
| '_ \| | | |/ _ \ | |
| |_) | |_| |  __/ |_|
|_.__/ \__, |\___| (_)
       |___/          

"""

options = """
play            -   Plays Music
pause           -   Pauses Music
toggle          -   Toggle Play Pause
next            -   skip to the next song
prev            -   go to the previous song
status          -   to get status of current settings
info            -   minimal info of the media playing right now
playagain       -   playagain the music.
exit            -   Close everything.
set             -   set options like repeat, shuffle, music_directory... etc.
help            -   used to get help for any of the above commands USE 'help <cmd>'
songlist        -   to view the currently discovered songlist.
"""

def cmd(c):
    os.system(c)
def newFrame():
    cmd('clear')
    print(logo)
def segregate(isd):
    isd = isd.strip() + ' '
    i=0
    f=0
    returnlist = []
    temp=''
    for ch in isd:
        if ch == ' ':
            temp = isd[i:f]
            returnlist.append(temp.strip())
            temp = ''
            i=f
        f+=1
    return returnlist
    
def ScanDir():
    for dirs in toscandirs:
        temp_list = os.listdir(dirs)
        for files in temp_list:
            if files.endswith('.mp3'):
                songlist.append(dirs+files)
#Media Functions

def play(index):
    # playing = True
    mix.music.stop()
    mix.music.load(songlist[index])
    mix.music.play()
    newFrame()
    m = ID3(songlist[current_index])
    try:
        song_title = m['TIT2'].text[0]
    except:
        song_title = 'Unavailable'
    try:                
        song_artist = m['TPE1'].text[0]
    except:
        song_artist ='Unavailable'
    try:
        song_album = m['TALB'].text[0]
    except:
        song_album = 'Unavailable'
    status = f"""


NOW PLAYING : {song_title}\t\tARTIST : {song_artist}\t\tALBUM : {song_album}
"""
    print(status)
def pause():
    mix.music.pause()
    # playing = False

def unpause():
    mix.music.unpause()
    # playing = True

def stop():
    mix.music.stop()
    playing = False
    stopped = True

cmd('clear')
run_till = True
print(logo)
print(options)
ScanDir()
mix.init()
play(0)
while run_till:
    print('[i] type help for options')
    # print(stopped)
    inp = input('')
    seg = segregate(inp)   #segregating the input by spaces to a list
    if len(seg) == 3:
        pass
    elif len(seg) == 2:
        pass

    elif len(seg) == 1:
        key = seg[0].lower()

        if key == 'exit':
            cmd('clear')
            run_till = False
            print(goodbye)
        
        elif key == 'help':
            cmd('clear')
            print(options)

        elif key == 'songlist':
            newFrame()
            songlist = [] #refreshing the songlist for a new scan & to evade repitions.
            ScanDir()
            for i in range(len(songlist)):
                print(f'[{i}] {songlist[i]}')
            
            # print(songlist)
        
        elif key == 'play':
            unpause()
        
        elif key == 'pause':
            pause()
        elif key == 'n':
            current_index+=1
            if current_index >= len(songlist):
                current_index = 0
            play(current_index)
        elif key == 'next':
            current_index+=1
            if current_index >= len(songlist):
                current_index = 0
            play(current_index)
        
        elif key == 'prev':
            current_index-=1
            if current_index <= 0:
                current_index = len(songlist)-1
            play(current_index)
        elif key == 'p':
            current_index-=1
            if current_index <= 0:
                current_index = len(songlist)-1
            play(current_index)
        elif key == 'status':
            newFrame()
            # status = f"""PLAYING NOW: {songlist[current_index]}"""
            m = ID3(songlist[current_index])
            # print(m)
            try:
                song_title = m['TIT2'].text[0]
            except:
                song_title = 'Unavailable'
            try:                
                song_artist = m['TPE1'].text[0]
            except:
                song_artist ='Unavailable'
            try:
                song_album = m['TALB'].text[0]
            except:
                song_album = 'Unavailable'
            status = f"""


NOW PLAYING : {song_title}\tARTIST : {song_artist}\tALBUM : {song_album}
"""
            print(status)
            # print('Song   NAME: '+m['TIT2'].text[0])
            # print('Artist NAME: '+m['TPE1'].text[0])
            # print('Album  NAME: '+m['TALB'].text[0])

