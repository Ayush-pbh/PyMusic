import platform
import threading
#from ctypes import windll
from PIL import Image, ImageTk
import tkinter as tk
from mutagen.id3 import ID3
import pygame
import os,io
import time
from subprocess import call   # for volume controlls
#from win10toast import ToastNotifier















class App(threading.Thread):
    # from tkinter import *
    global player
    global m
    GWL_EXSTYLE=-20
    WS_EX_APPWINDOW=0x00040000
    WS_EX_TOOLWINDOW=0x00000080
    resizeTuple=(150,150)
    r=150
    defaultImg = './logo.jpg'
    toSetImg = "./logo.jpg"
    voll = 50
    didmovelasttime = False
    def run(self):
        print("[ APP STARTED ]")
        self.main()

    def set_appwindow(self,root):
        #hwnd = windll.user32.GetParent(root.winfo_id())
        #style = windll.user32.GetWindowLongPtrW(hwnd, self.GWL_EXSTYLE)
        #style = style & ~self.WS_EX_TOOLWINDOW
        #style = style | self.WS_EX_APPWINDOW
        #res = windll.user32.SetWindowLongPtrW(hwnd, self.GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())

    def main(self):
        self.root = tk.Tk()
        self.root.wm_title("AppWindow Test")
        self.root.maxsize(150,150)   #only one fixed size from version 2 and above.
        self.root.title("Project Arrival")
        #making icon
        self.icon = tk.PhotoImage(file='./icon.png')
        self.root.iconphoto(False,self.icon)
        #making canvas
        self.canvas = tk.Canvas(self.root, width=150,height=150,highlightthickness=0)
        # self.canvas.bind('<Button-3>',self.do_popup)
        self.canvas.bind('<Button-3>',self.do_popup)
        
        self.canvas.bind('<Double-1>',player.Toggle)

        self.canvas.pack()
        self.img = ImageTk.PhotoImage(Image.open(self.defaultImg).resize(self.resizeTuple)) # the one-liner I used in my app
        self.canvasCreateImage = self.canvas.create_image(75,75,image=self.img)
        #Menu
        self.m =tk.Menu(self.root, tearoff=0)
        self.m.add_command(label ="Next", command=player.NextSong) 
        self.m.add_command(label ="Prev", command=player.PrevSong) 
        self.m.add_command(label ="Stop",command=player.Stop) 
        self.m.add_separator() 
        self.m.add_command(label ="Close",command=self.QuitProgram)     
        
        self.root.overrideredirect(True)
        self.root.after(10, lambda: self.set_appwindow(self.root))
        #making it dragable
        self.canvas.bind('<Button-1>',self.start_move)
        self.canvas.bind('<Left>',self.keys)
        self.canvas.bind("<Button-4>", self.volume)
        self.canvas.bind("<Button-5>", self.volume)
        self.canvas.bind('<ButtonRelease-1>',self.stop_move)
        self.canvas.bind('<B1-Motion>',self.do_move)
        #the mainloop
        self.root.mainloop()

    def QuitProgram(self):
        self.root.quit()
        print("Quitting Program")
        m.joinall()
    def volume(self,event):
        i=event.num
        #change 5 to 4 if want to reverse the scroll-volume behaviour!
        if(i==5):
            #i is +ive i.e increase volume...
            if(self.voll>=100):
            	#volume already full
            	return 0
            else:
            	self.voll=self.voll+1
            	a = call(["amixer", "-D", "pulse", "sset", "Master", f"{self.voll}%"])
        else:
       	    #i is -ve i.e decrease volume
            if(self.voll<=0):
            	#no more decrase...
            	return 0
            else:
            	self.voll=self.voll-1
            	a =call(["amixer", "-D", "pulse", "sset", "Master", f"{self.voll}%"])
    def start_move(self,event):
        self.x = event.x
        self.y = event.y
        self.canimove = True
        self.didmovelasttime = False

    def stop_move(self, event):
        self.x = None
        self.y = None
        # self.canimove = False
        # if not self.didmovelasttime:
        #     player.PrevSong()
        



    def do_move(self, event):
        # if not self.canimove:
        #     return
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')
        # self.didmovelasttime = True

    def AlbumArtChanger(self):
        # This fucntion changes the image of the canvass to the current default image this
        # function assumnes that the calling fuction has already changed the value of the self.toSetImg
        # to the current wanted Image.
        self.img = self.toSetImg
        self.canvas.itemconfigure(self.canvasCreateImage, image=self.img)

    def do_popup(self,event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()
    def keys(self,event):
        print("Left Working!")
       










def SongEndedFunction():
    while True:
        time.sleep(2)
        songend2()

def songend2():
    for event in pygame.event.get():
            if event.type == player.MusicEnd:
                print("Hey Music has ended. So moving to the next one")
                player.NextSong()












class Player(threading.Thread):
    global app
    global songend
    playable_list=[]
    folder = ''
    Playing = False
    Stopped = True
    index = 0
    MusicEnd = 0
    def run(self):
        #this function will intialize the songs and then continue playing the songs.
        #the other funcitons will be accsisible by other calsses and would handle pausing and other functions
        #print("This is Player Class")
        app.start()
        # songend.start()
        #first scan the folder containing songs.
        self.ScanFolder()
        
        self.MusicEnd = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MusicEnd)
        self.Play(self.index)
        
        
    def Play(self,index):
        song_addr = self.folder+self.playable_list[index]

        pygame.mixer.music.stop()
        pygame.mixer.music.load(song_addr)
        pygame.mixer.music.play()
        print('Playing :>'+song_addr)
        self.Playing = True
        self.index = index
        self.Stopped = False
        pic = self.getRawImage()
        app.toSetImg = ImageTk.PhotoImage(Image.open(pic).resize(app.resizeTuple)) # the one-liner I used in my app
        app.AlbumArtChanger()
        notify = Notify()
        notify.start()
        # notify.join()
        
        
    def NextSong(self):
        self.index += 1
        self.Play(self.index)
    def PrevSong(self):
        if self.index !=0:
            self.index-=1
        self.Play(self.index)
    def Pause(self):
        pygame.mixer.music.pause()
        self.Playing = False
    def Unpause(self):
        pygame.mixer.music.unpause()
        self.Playing = True
    def Stop(self):
        pygame.mixer.music.stop()
        self.isPlaying = False
        self.Stopped = True
    def Toggle(self,event):
        if self.Stopped:
            self.Play(self.index)
            return
        if self.Playing:
            self.Pause()
        else:
            self.Unpause()

    def getRawImage(self):
        img_name = self.folder+self.playable_list[self.index]
        #print('Image is :>'+img_name)
        img = ID3(img_name)
        #print('getting albumart for: '+img_name)
        datab = ''
        try:
            datab = img['APIC:'].data
        except:
            try:
                datab = img['APIC:3.jpeg'].data
            except:
                try:
                    datab = img['APIC:FRONT_COVER'].data
                except:
                    try:
                        datab = img['APIC:"Album cover"'].data
                    except:
                    	try:
                    		datab = img['APIC:3.png'].data
                    	except:
                        	return './logo.jpg'
        return io.BytesIO(datab)

    def ScanFolder(self):
        fp = open('src.txt','r')
        text = fp.read()
        fp.close()
        self.folder  = text[:len(text)-1]

        if not self.folder.endswith('/'):
            self.folder+='/'
        print(self.folder)
        #looping in the folder to find all the songs.
        try:
            import sys
            args = sys.argv

            self.source = ''
            if len(args)>1 :
                #we expect if there more than sys.argv then the last arg is the Music Folder :)
                self.source = args[-1]
            print("User Song Location",self.source)
            for item in os.listdir(self.source):
                if item.endswith('.mp3'):
                    self.playable_list.append(item)
            print("Folder Scanned")
            print("Changing the def folder to user folder")
            self.folder = self.source
        except:
            print("Exception in getting user defined Song locartion")
            for item in os.listdir(self.folder):
                if item.endswith('.mp3'):
                    self.playable_list.append(item)
            print("Folder Scanned")












class Notify(threading.Thread):
    global SystemOs
    global player
    def run(self):
        print("Notifying!")
        song = ID3(player.folder+player.playable_list[player.index])
        date = ''
        artist = ''
        title = ''
        try:
            date = str(song['TDRC'].text[0])
        except:
            pass
        try:
            artist = str(song['TPE1'].text[0])
        except:
            pass
        try:
            title = str(song['TIT2'].text[0])
        except:
            pass
        print(findOs())
        if(findOs()=="Wind"):
	        print("Kol")
#            WinToast = ToastNotifier()
 #           WinToast.show_toast(f"Playing {title}",f"{artist} {date}",duration=3)
        else:
            os.system(f'notify-send \"Playing {title} by {artist} {date}\"')


















#Woah i made it can't beliave myself.
#class Variables, quite wierd i know.
app = App()
# songlist = Songlist()
notify = Notify()
# songend = SongEnded()
player = Player()
SystemOs = ""

# songend_thread = threading.Thread(target=SongEndedFunction)


#making sure they are runnig
class Main(threading.Thread):
    global app
    global player
    def joinall(self):
        print("Main about to quit.")
        # app.join()
        # player.join()
        # songend.join()
        # songend_thread.join()

    def run(self):
        findOs()
        
        # app.start()
        # songlist.start()
        # notify.start()
        player.start()
        # songend_thread.start()
def findOs():
    global SystemOs
    if platform.system()=="Windows":
        SystemOs = "Wind"
        return "Wind"
    else:
        SystemOs = "Unix"
        return "Unix"    


m = Main()
pygame.init()
pygame.mixer.init()
m.start()
