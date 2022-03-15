import os
from tkinter import *
from pygame import mixer

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


listbox = Listbox(listframel)
listbox.grid(row=0, column=0, rowspan=5, sticky=NSEW)

for song in song_list:
    if song.endswith(".mp3"):
        lst.append(str(song))
        path="E:\TEAM YTB\Songs\\"+song
        mixer.music.load(str(path))

def play_song():
    mixer.music.play()

def pause_song():
    mixer.music.pause()

play = Button(root, command=play_song, text="Play")
play.grid(row=5, column=0)

pause = Button(root, command=pause_song, text="Pause")
pause.grid(row=5, column=1)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

root.mainloop()
