from concurrent.futures import thread
import os
import pygame
import functools
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import font as tkFont
from tkinter.ttk import Scale
from PIL import Image, ImageTk
from mutagen.mp3 import MP3

root = Tk()
root.geometry('1280x720')
root.title("Music Player")
root.grid_rowconfigure((0,1,2,3,4,5), weight=1)
root.grid_columnconfigure((0,1,2), weight=1)
root.grid_columnconfigure((3,), weight=15)
root.resizable(False, False)
root.option_add('*Dialog.msg.font', 'Conforta 11')
root.iconbitmap('appicon.ico')
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

song_list = os.listdir(os.getcwd())
lst = list()
conforta = tkFont.Font(family="conforta", size=11)

for song in song_list:
    if song.endswith(".mp3"):
        lst.append(str(song))

listframel = Frame(root)
listframel.grid(row=0, column=0, sticky=NSEW, rowspan=5, columnspan=3)
listframel.configure(bg="white")
listframer = Frame(root)
listframer.grid(row=0, column=3, sticky=NSEW, rowspan=5)
listframer.configure(bg="white")

listframel.grid_rowconfigure((0,1,2,3,4), weight=1)
listframel.grid_columnconfigure((0,), weight=1)

listframer.grid_rowconfigure((0,1,2,3,4), weight=1)
listframer.grid_columnconfigure((1,), weight=1)

play_img = ImageTk.PhotoImage(Image.open('play.png').resize((50,50)))
pause_img = ImageTk.PhotoImage(Image.open('pause.png').resize((50,50)))
previous_img = ImageTk.PhotoImage(Image.open('previous.png').resize((35,35)))
next_img = ImageTk.PhotoImage(Image.open('next.png').resize((35,35)))
up_img = ImageTk.PhotoImage(Image.open('up.png').resize((35,35)))
down_img = ImageTk.PhotoImage(Image.open('down.png').resize((35,35)))
mute_img = ImageTk.PhotoImage(Image.open('mute.png').resize((35,35)))
unmute_img = ImageTk.PhotoImage(Image.open('sound.png').resize((35,35)))

played_song = 0
song_index = 0
changed_song = 0
dir_changed = False

scrollbar = Scrollbar(listframel)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar2 = Scrollbar(listframel, orient='horizontal')
scrollbar2.pack(side=BOTTOM, fill=X)

listbox = Listbox(listframel, xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, font=conforta, borderwidth=0)
listbox.pack(fill=BOTH, expand=1)
song_name = ""

listframed = Frame(root)
listframed.grid(row=5, column=1, sticky='NSEW')

current_value = DoubleVar()
slider = Scale(root, from_=0, to=100, orient='horizontal', variable=current_value)
slider.grid(row=5, column=3, sticky='we')

pth = os.getcwd()
ap = "Autoplay: On"
clicked_mute = False
l = True
initial_vol = 1.0
tpath = pth + "/" + lst[song_index]
val = 0.1

def browse():
    global pth, song_list, lst, listbox, dir_changed
    temp = pth
    try:
        pth = filedialog.askdirectory(initialdir=os.getcwd(),title="Select a folder")
        song_list = os.listdir(pth)
        dir_changed = True
        pygame.mixer.music.stop()
    except FileNotFoundError:
        pth = temp
        song_list = os.listdir(pth)
    lst = list()
    listbox.delete(0, END)
    for song in song_list:
        if song.endswith(".mp3"):
            lst.append(str(song))
    for i in range(len(lst)):
        lg = lst[i]
        lgl = len(lg)
        listbox.insert(i+1, lg[:lgl - 4])

def tgautoplay():
    global ap, l

    if l:
        audiomenu.entryconfigure(0, label="Autoplay: Off")
        l = False
    else:
        audiomenu.entryconfigure(0, label="Autoplay: On")
        l = True

def fileSelection(self):
    global song_index, changed_song, pth, tpath

    s = song_index
    selection = listbox.curselection()
    song_index = functools.reduce(lambda sub, ele: sub * 10 + ele, selection)
    if s != song_index:
        changed_song = 1
    
listbox.bind("<<ListboxSelect>>", fileSelection)

def play_song():
    global played_song, changed_song, song_index, pth, tpath

    tpath = pth + "/"  + lst[song_index]

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play.config(image=play_img)
    else:
        if played_song == 0:
            path = pth + "/" + lst[song_index]
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play()  
            played_song = 1
        elif played_song == 1:
            if changed_song == 0:
                pygame.mixer.music.unpause()
            elif changed_song == 1:
                path = pth + "/"  + lst[song_index]
                if path == tpath:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.play()
                    changed_song = 0
                else:
                    pygame.mixer.music.unpause()
                    play.config(image=play_img)
                    changed_song = 0
        play.config(image=pause_img)

def new_thread():
    global changed_song, song_index, tpath, current_value, dir_changed, val
    
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            if song_index == len(lst) - 1:
                play.config(image=play_img)
            else:
                if dir_changed:
                    changed_song = 1
                    play_song()
                    dir_changed = False
                else:
                    if l:
                        changed_song = 1
                        song_index += 1
                        play_song()
                    else:
                        play.config(image=play_img)

    
    song_mut = MP3(tpath)
    song_length = song_mut.info.length
    current_time = pygame.mixer.music.get_pos()  / 1000
    slider_val = (current_time / song_length) * 100
    current_value.set(slider_val)

    root.after(100, new_thread)

def cquit():
    mb = messagebox.askyesno('QUITTING', 'Are you sure you want to quit the application?')

    if mb:
        root.destroy()
    else:
        pass

def previous_song():
    global changed_song, song_index, lst

    if song_index == 0:
        messagebox.showerror("Error", "This is the first song")
    else:
        changed_song = 1
        song_index -= 1
        pygame.mixer.music.pause()
        play_song()

def next_song():
    global changed_song, song_index, lst
    
    if song_index == len(lst) - 1:
        messagebox.showerror("Error", "This is the last song")
    else:
        changed_song = 1
        song_index += 1
        pygame.mixer.music.pause()
        play_song()

def ivol():
    global initial_vol

    if initial_vol > 0.95:
        pass
    else:
        pygame.mixer.music.set_volume(initial_vol+0.05)
        initial_vol += 0.05

def dvol():
    global initial_vol

    if initial_vol < 0.05:
        initial_vol = 0.0
        pass
    else:    
        pygame.mixer.music.set_volume(initial_vol-0.05)
        initial_vol -= 0.05

def mvol():
    global clicked_mute, initial_vol

    if clicked_mute:
        pygame.mixer.music.set_volume(initial_vol)
        vol_mute.config(image=unmute_img)
        clicked_mute = False
    else:
        pygame.mixer.music.set_volume(0.0)
        vol_mute.config(image=mute_img)
        clicked_mute = True

def ahelp():
    pass

def about():
    pass

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

play = Button(root, image=play_img, command=play_song, borderwidth=0)
play.grid(row=5, column=1)

previous = Button(root, image=previous_img, command=previous_song, borderwidth=0)
previous.grid(row=5, column=0)
nexts = Button(root, image=next_img, command=next_song, borderwidth=0)
nexts.grid(row=5, column=2)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

vol_up = Button(root, command=ivol, borderwidth=0, image=up_img)
vol_up.grid(row=6,column=2)

vol_down = Button(root, command=dvol, borderwidth=0, image=down_img)
vol_down.grid(row=6,column=1)

vol_mute = Button(root, command=mvol, borderwidth=0, image=unmute_img)
vol_mute.grid(row=6,column=0)

menu = Menu(root)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Open folder", command=browse)
filemenu.add_command(label="Quit", command=cquit)
menu.add_cascade(label="File", menu=filemenu)

audiomenu = Menu(menu, tearoff=0)
audiomenu.add_command(label=ap, command=tgautoplay)
audiomenu.add_command(label="Increase Volume", command=ivol)
audiomenu.add_command(label="Decrease Volume", command=dvol)
audiomenu.add_command(label="Mute", command=mvol)
menu.add_cascade(label="Audio", menu=audiomenu)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="Help", command=ahelp)
helpmenu.add_command(label="About", command=about)
menu.add_cascade(label="Help", menu=helpmenu)

scrollbar.config(command=listbox.yview)
scrollbar2.config(command=listbox.xview)
root.config(menu=menu)
root.protocol("WM_DELETE_WINDOW", cquit)
new_thread()
root.mainloop()
