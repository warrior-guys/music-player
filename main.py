import os
from tkinter import *
from pygame import mixer
from PIL import Image, ImageTk
import functools

root = Tk()
root.geometry('1280x720')
root.title("Music Player")
root.grid_rowconfigure((0,1,2,3,4,5), weight=1)
root.grid_columnconfigure((0,), weight=1)
root.grid_columnconfigure((1,), weight=5)
root.resizable(False, False)
mixer.init()

song_list = os.listdir("E:\TEAM YTB\Songs\\")
lst = list()

listframel = Frame(root, highlightbackground="black", highlightthickness=5)
listframel.grid(row=0, column=0, sticky=NSEW, rowspan=5)
listframer = Frame(root, highlightbackground="black", highlightthickness=5)
listframer.grid(row=0, column=1, sticky=NSEW, rowspan=5)

listframel.grid_rowconfigure((0,1,2,3,4), weight=1)
listframel.grid_columnconfigure((0,), weight=1)

listframer.grid_rowconfigure((0,1,2,3,4), weight=1)
listframer.grid_columnconfigure((1,), weight=1)

played_song = 0
song_index = 0
changed_song = 0

listbox = Listbox(listframel)
listbox.grid(row=0, column=0, rowspan=5, sticky=NSEW)
song_name = ""

def fileSelection(self):
    global song_index, changed_song
    s = song_index
    selection = listbox.curselection()
    song_index = functools.reduce(lambda sub, ele: sub * 10 + ele, selection)
    if s != song_index:
        changed_song = 1
    
listbox.bind("<<ListboxSelect>>", fileSelection)

for song in song_list:
    if song.endswith(".mp3"):
        lst.append(str(song))

def play_song():
    global played_song, changed_song, song_index
    print(changed_song)
    print(song_index)

    if played_song == 0:
        path = "E:\TEAM YTB\Songs\\" + lst[song_index]
        mixer.music.load(str(path))
        mixer.music.play()
        played_song = 1
    elif played_song == 1:
        if changed_song == 0:
            mixer.music.unpause()
        elif changed_song == 1:
            path = "E:\TEAM YTB\Songs\\" + lst[song_index]
            mixer.music.load(str(path))
            mixer.music.play()
            changed_song = 0

def pause_song():
    mixer.music.pause()

play_img = ImageTk.PhotoImage(Image.open('play.png').resize((100,100)))
pause_img = ImageTk.PhotoImage(Image.open('pause.png').resize((100,100)))

play = Button(root, image=play_img, command=play_song)
play.grid(row=5, column=0)

pause = Button(root, image=pause_img, command=pause_song)
pause.grid(row=5, column=1)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

root.mainloop()
