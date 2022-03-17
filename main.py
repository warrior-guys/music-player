#pause button attribution - <a href="https://www.flaticon.com/free-icons/pause" title="pause icons">Pause icons created by Good Ware - Flaticon
#play button attribution - <a href="https://www.flaticon.com/free-icons/play-button" title="play button icons">Play button icons created by Freepik - Flaticon

import os
from tkinter import *
from tkinter import font as tkFont
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk
import functools

root = Tk()
root.geometry('1280x720')
root.title("Music Player")
root.grid_rowconfigure((0,1,2,3,4,5), weight=1)
root.grid_columnconfigure((0,), weight=1)
root.grid_columnconfigure((1,), weight=5)
root.resizable(False, False)
root.configure(bg="black")
root.option_add('*Dialog.msg.font', 'Segoe 11')
pygame.init()
pygame.mixer.init()

song_list = os.listdir("E:\TEAM YTB\Songs\\")
lst = list()
conforta = tkFont.Font(family="conforta", size=11)

listframel = Frame(root)
listframel.grid(row=0, column=0, sticky=NSEW, rowspan=5)
listframel.configure(bg="white")
listframer = Frame(root)
listframer.grid(row=0, column=1, sticky=NSEW, rowspan=5)
listframer.configure(bg="white")

listframel.grid_rowconfigure((0,1,2,3,4), weight=1)
listframel.grid_columnconfigure((0,), weight=1)

listframer.grid_rowconfigure((0,1,2,3,4), weight=1)
listframer.grid_columnconfigure((1,), weight=1)

play_img = ImageTk.PhotoImage(Image.open('E:\Projects\Media Player\play.png').resize((50,50)))
pause_img = ImageTk.PhotoImage(Image.open('E:\Projects\Media Player\pause.png').resize((50,50)))

played_song = 0
song_index = 0
changed_song = 0

scrollbar = Scrollbar(listframel)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar2 = Scrollbar(listframel, orient='horizontal')
scrollbar2.pack(side=BOTTOM, fill=X)

listbox = Listbox(listframel, xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, font=conforta, borderwidth=0)
listbox.pack(fill=BOTH, expand=1)
song_name = ""

path = ""

def browse():
    global path
    path = filedialog.askdirectory(initialdir="E:\\",title="Select a directory")

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

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play.config(image=play_img)
    else:
        if played_song == 0:
            path = "E:\TEAM YTB\Songs\\" + lst[song_index]
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play()  
            played_song = 1
        elif played_song == 1:
            if changed_song == 0:
                pygame.mixer.music.unpause()
            elif changed_song == 1:
                path = "E:\TEAM YTB\Songs\\" + lst[song_index]
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.play()
                changed_song = 0
        play.config(image=pause_img)

def pause_song():
    pygame.mixer.music.pause()

    if pygame.mixer.music.get_busy():
        play.config(image=play_img)
    else:
        play.config(image=pause_img)

def change_song():
    global changed_song, song_index

    for event in pygame.event.get():
        if event.type == MUSIC_END:
            changed_song = 1
            song_index += 1
            play.config(image=play_img)
            play_song()
    
    root.after(100, change_song)

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

play = Button(root, image=play_img, command=play_song, borderwidth=0, bg="black")
play.grid(row=5, column=0)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

menu = Menu(root)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Browse", command=browse)
menu.add_cascade(label="File", menu=filemenu)

scrollbar.config(command=listbox.yview)
scrollbar2.config(command=listbox.xview)
root.config(menu=menu)
change_song()
root.mainloop()
