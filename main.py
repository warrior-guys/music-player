import os
import pygame
import functools
import requests
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import font as tkFont
from tkinter.ttk import Scale, Separator
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from math import floor
from bs4 import BeautifulSoup
import webbrowser

root = Tk()
root.geometry('1280x720')
root.title("Music Player")
root.grid_rowconfigure((0,1,2,3,4), weight=2)
root.grid_rowconfigure((5,6,7), weight=1)
root.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), weight=1)
root.option_add('*Dialog.msg.font', 'Conforta 11')
root.iconbitmap('icons/appicon.ico')
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

conforta = tkFont.Font(family="conforta", size=11)

listframel = Frame(root)
listframel.grid(row=0, column=0, sticky=NSEW, rowspan=5, columnspan=3)
listframel.configure(bg="white")
listframer = Frame(root)
listframer.grid(row=0, column=3, sticky=NSEW, rowspan=5, columnspan=15)
listframer.configure(bg="white")

listframel.grid_rowconfigure((0,1,2,3,4), weight=1)
listframel.grid_columnconfigure((0,), weight=1)

listframer.grid_rowconfigure((0,1,2,3,4), weight=1)
listframer.grid_columnconfigure((1,), weight=1)

play_img = ImageTk.PhotoImage(Image.open('icons/play.png').resize((50,50)))
pause_img = ImageTk.PhotoImage(Image.open('icons/pause.png').resize((50,50)))
previous_img = ImageTk.PhotoImage(Image.open('icons/previous.png').resize((35,35)))
next_img = ImageTk.PhotoImage(Image.open('icons/next.png').resize((35,35)))
up_img = ImageTk.PhotoImage(Image.open('icons/up.png').resize((35,35)))
down_img = ImageTk.PhotoImage(Image.open('icons/down.png').resize((35,35)))
mute_img = ImageTk.PhotoImage(Image.open('icons/mute.png').resize((35,35)))
unmute_img = ImageTk.PhotoImage(Image.open('icons/sound.png').resize((35,35)))
seek_img = ImageTk.PhotoImage(Image.open('icons/right.png').resize((35,35)))
prev_img = ImageTk.PhotoImage(Image.open('icons/left.png').resize((35,35)))

played_song = 0
changed_song = 0
dir_changed = False
update_checked = False
version_value = "v1.1.1"
update_available = False
was_playing = False

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
slider.grid(row=6, column=1, columnspan=15, sticky='we')

try:
    if os.path.getsize('info.txt') > 0:
        with open('info.txt', 'r') as f:
            f.readline()
            pth = f.readline()[:-1]
            song_index = int(f.readline()[:-1])
    else:
            pth = os.getcwd()
            song_index = 0
except FileNotFoundError:
    pth = os.getcwd()
    song_index = 0

song_list = os.listdir(pth)
lst = list()

for song in song_list:
    if song.endswith(".mp3"):
        lst.append(str(song))

ap = "Autoplay: On"
clicked_mute = False
l = True
initial_vol = 1.0
info = list()
song_mut = None
song_length = 0.0

try:
    tpath = pth + "/" + lst[song_index]
except IndexError:
    pass

val = 0.1
minute = StringVar()
second = StringVar()
song_dur = 0.0
mini_seek = Toplevel(root)
mini_seek.destroy()
music_end = False

def browse():
    global pth, song_list, lst, listbox, dir_changed
    temp = pth
    try:
        pth = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a folder")
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
    
    if len(lst) == 0:
        messagebox.showerror("Music not found", "Please select a directory with music.")

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
    global played_song, changed_song, song_index, pth, tpath, song_dur, music_end

    tpath = pth + "/"  + lst[song_index]

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play.config(image=play_img)
    else:
        if played_song == 0:
            path = pth + "/" + lst[song_index]
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play()
            song_dur = 0
            played_song = 1
        elif played_song == 1:
            if changed_song == 0:
                if not music_end:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.play()
                    music_end = False
            elif changed_song == 1:
                path = pth + "/"  + lst[song_index]
                if path == tpath:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.play()
                    song_dur = 0
                    changed_song = 0
                else:
                    pygame.mixer.music.unpause()
                    play.config(image=play_img)
                    changed_song = 0
        play.config(image=pause_img)

def new_thread():
    global changed_song, song_index, tpath, current_value, dir_changed, val, slider, song_dur, update_checked, song_length, song_mut, music_end

    if not update_checked:
        check_for_updates(version_value)
        update_checked = True
    else:
        pass
    
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            if song_index == len(lst) - 1:
                play.config(image=play_img)
                song_dur = 0
                music_end = True
            else:
                if dir_changed:
                    changed_song = 1
                    song_index = 0
                    play_song()
                    song_dur = 0
                    dir_changed = False
                else:
                    if l:
                        changed_song = 1
                        song_index += 1
                        song_dur = 0
                        play_song()
                    else:
                        play.config(image=play_img)
                        song_dur = 0
    
    try:
        song_mut = MP3(tpath)
        song_length = song_mut.info.length
    except NameError:
        song_length = 1

    if pygame.mixer.music.get_busy():
        if song_dur <= song_length:
            song_dur += 0.1
        else:
            song_dur = 0
    else:
        pass

    slider.config(to=song_length)
    slider.set(song_dur)

    if song_dur + 10 >= song_length:
        seektna.config(state="disabled")
    else:
        seektna.config(state="active")

    if song_dur - 10 <= 0:
        seektnb.config(state="disabled")
    else:
        seektnb.config(state="active")

    root.after(100, new_thread)

def cquit():
    mb = messagebox.askyesno('QUITTING', 'Are you sure you want to quit the application?')

    if mb:
        with open('info.txt', 'w') as f:
            f.write("* WARNING * - MODIFYING THIS FILE CAN CAUSE UNEXPECTED PROBLEMS IN THE MUSIC PLAYER APP! IF YOU HAVE MISTAKENLY MODIFIED THE FILE, PLEASE CLEAR ALL CONTENTS OR DELETE THIS FILE." + '\n')
            f.write(pth + '\n')
            f.write(str(song_index) + '\n')
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
    help_window = Toplevel(root)
    help_window.geometry('500x500')
    help_window.resizable(False, False)
    help_window.title("Help")
    help_window.grab_set()
    help_window.grid_rowconfigure((0,1,2,3,4), weight=1)
    help_window.grid_columnconfigure((0,), weight=1)
    help_window.iconbitmap('icons/help.ico')

    var_temp = StringVar()
    var_temp.set("This is a simple media player! To get started:\n\n1. Select a directory with some songs.\n2. Press the play button.\n3. Boom, you know how to use the app!\n\nThe app has simple icons with functionality similar to their look, you will be easily able to do all the tasks on your own. We have provided a list of shortcuts below which you can use as per your ease of use!\n\nSpacebar : Play/Pause\nControl + Shift + Right Arrow : Next song\nControl + Shift + Back Arrow : Previous song\nControl + Period : Seek 10 seconds forward\nControl + Comma : Seek 10 seconds backward\nControl + Up Arrow : Increase Volume\nControl + Down Arrow : Decrease Volume\n Control + M : Mute Volume\nControl + O : Browse Files\nControl + Q : Exit")
    
    help_label = Label(help_window, textvariable=var_temp, font=conforta, wraplength=400)
    help_label.grid(row=0, column=0)

    separator = Separator(help_window, orient='horizontal')
    separator.grid(row=1, column=0, sticky='we')

    issue_pull = StringVar()
    issue_pull.set("Encountering any bug or issue, or want to ask for a feature? Submit them below and we will respond as quick as possible!")

    issue_pull_label = Label(help_window, textvariable=issue_pull, font=conforta, wraplength=400)
    issue_pull_label.grid(row=2, column=0)

    issue_btn_text = StringVar()
    issue_btn_text.set("Report a Bug/Issue")
    pull_btn_text = StringVar()
    pull_btn_text.set("Ask for a feature")

    issue_btn = Button(help_window, borderwidth=0.5, textvariable=issue_btn_text, font=conforta, command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory/issues", new=1))
    pull_btn = Button(help_window, borderwidth=0.5, textvariable=pull_btn_text, font=conforta, command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory/pulls", new=1))
    issue_btn.grid(row=3, column=0)
    pull_btn.grid(row=4, column=0)

def about():
    about_window = Toplevel(root)
    about_window.geometry('400x400')
    about_window.resizable(False, False)
    about_window.title("About")
    about_window.grab_set()
    about_window.grid_rowconfigure((0,1,2,3,4,5), weight=1)
    about_window.grid_columnconfigure((0,), weight=1)
    about_window.iconbitmap('icons/about.ico')
    
    var_temp = StringVar()
    var_temp.set("This is an advanced music player for one's needs,  with a beautiful GUI, built from scratch with Python, using Tkinter library for GUI, the OS library for file controls, the Pygame library for media controls and many other libraries.\n\nThis project's development started on 13th March, 2022 and is still going on. You can visit our GitHub for the source code by clicking below!")
    
    about_label = Label(about_window, textvariable=var_temp, font=conforta, wraplength=350)
    about_label.grid(row=0, column=0)

    src_btn = Button(about_window, text="Go to source code", command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory", new=1), font=conforta)
    src_btn.grid(row=1, column=0)
    
    separator = Separator(about_window, orient='horizontal')
    separator.grid(row=2, column=0, sticky='we')

    version_var = StringVar()
    version_var.set(f"Current version: {version_value}")

    version_number = Label(about_window, textvariable=version_var, font=conforta)
    version_number.grid(row=3, column=0)

    update_button = Button(about_window, borderwidth=0.5, command=lambda: webbrowser.open(url=info[1], new=1), font=conforta)
    update_button.grid(row=4, column=0)

    temp_var = StringVar()
    lbl1 = Label(about_window, textvariable=temp_var, font=conforta, wraplength=300)
    lbl1.grid(row=5, column=0)

    if update_available:
        update_button.config(text="Go to update")
        temp_var.set(f"An update to version {info[0]} is available. Click above to go our GitHub and download the latest version.")
    else:
        update_button.config(text="No updates available", state="disabled")
        temp_var.set("No updates were found on our GitHub. The app is up-to-date.")

    about_window.mainloop()

def check_for_updates(version_var):
    global update_available, info

    r = requests.get('https://github.com/warrior-guys/musical-memory/blob/main/docs/version.txt')

    soup = BeautifulSoup(r.content, 'html.parser')
    gh_td = soup.findAll('td', attrs={"class":"blob-code blob-code-inner js-file-line"})

    for td in gh_td:
        info.append(td.text)

    if info[0] == version_var:
            update_available = False
    else:
        update_available = True
        messagebox.showinfo(title="Update available", message="An update is available. To update the app - In the menu bar, go to Help -> About and click on the 'Update' button to go to the update if you wish.")

def seek():
    global minute, second, mini_seek, play, was_playing

    mini_seek = Toplevel(root)
    mini_seek.title("Seek")
    mini_seek.resizable(False, False)
    mini_seek.geometry('300x150')
    mini_seek.grab_set()
    mini_seek.grid_rowconfigure((0,2,3), weight=1)
    mini_seek.grid_rowconfigure((1,), weight=2)
    mini_seek.grid_columnconfigure((0,2), weight=3)
    mini_seek.grid_columnconfigure((1,), weight=1)
    mini_seek.iconbitmap('icons/seek.ico')

    tmpvar = StringVar()
    tmpvar.set("Seek to the duration of audio you want")

    if pygame.mixer.music.get_busy():
        was_playing = True
    else:
        was_playing = False

    play.config(image=play_img)
    pygame.mixer.music.pause()
    
    txt1 = Label(mini_seek, textvariable=tmpvar, font=conforta)
    txt1.grid(row=0, column=0, columnspan=3)

    song_mut = MP3(tpath)
    song_length = song_mut.info.length
    
    colon = StringVar()
    colon.set(":")
    colon = Label(mini_seek, textvariable=colon, font=conforta)
    colon.grid(row=1, column=1)

    min_entry = Entry(mini_seek, textvariable=minute, font=conforta, width=5, borderwidth=0.5)
    sec_entry = Entry(mini_seek, textvariable=second,font=conforta, width=3, borderwidth=0.5)
    min_entry.grid(row=1, column=0)
    sec_entry.grid(row=1, column=2)

    song_duration = StringVar()
    if floor(song_length % 60) < 10:
        song_duration.set("Current song length: " + str(floor(song_length // 60)) + ":0" + str(floor(song_length % 60)))
    else:
        song_duration.set("Current song length: " + str(floor(song_length // 60)) + ":" + str(floor(song_length % 60)))
    sngdur = Label(mini_seek, textvariable=song_duration, font=conforta)
    sngdur.grid(row=2, column=0, columnspan=3)

    minute.trace("w", lambda *args: limitSizeMinute(minute))
    second.trace("w", lambda *args: nsymbol(second))

    submit_btn = Button(mini_seek, text="Seek", font=conforta, borderwidth=0.5, command=seekto)
    submit_btn.grid(row=3, column=0, columnspan=3)

    mini_seek.protocol("WM_DELETE_WINDOW", destroy)
    mini_seek.mainloop()

def destroy():
    global mini_seek, was_playing

    if was_playing:
        play.config(image=pause_img)
        pygame.mixer.music.unpause()
    else:
        play.config(image=play_img)

    mini_seek.destroy()

def limitSizeMinute(args):
    value = args.get()
    if len(value) > 0:
        for i in value:
            if not i.isdigit():
                l = args.get()
                dex = l.index(i)
                toset = l[:dex] + l[dex + 1:]
                args.set(toset)
        if len(value) > 3 : args.set(value[:3])

def seekto():
    global minute, second, current_value, slider, song_dur, mini_seek

    song_mut = MP3(tpath)
    song_length = song_mut.info.length

    try:
        if (int(minute.get()) * 60 + int(second.get())) > floor(song_length):
            messagebox.showerror("Error", "Please type a value less than the duration")
        else:
            song_dur = floor((int(minute.get()) * 60 + int(second.get())))
            if was_playing:
                pygame.mixer.music.play(start=float((int(minute.get()) * 60 + int(second.get()))))
                play.config(image=pause_img)
            else:
                pygame.mixer.music.play(start=float((int(minute.get()) * 60 + int(second.get()))))
                pygame.mixer.music.pause()
                play.config(image=play_img)
            mini_seek.destroy()
    except ValueError:
        messagebox.showwarning("Warning", "Please fill all fields")
    except pygame.error:
        messagebox.showerror("Error", "Please select and play a song first.")

def seektena():
    global song_dur, song_length, song_mut

    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.play(start=(song_dur + 10))
            song_dur += 10
        else:
            pygame.mixer.music.play(start=(song_dur + 10))
            song_dur += 10
            pygame.mixer.music.pause()
    except pygame.error:
        messagebox.showerror("Error", "Please select and play a song first.")

seektna = Button(root, command=seektena, image=seek_img, borderwidth=0)
seektna.grid(row=5, column=12)

def seektenb():
    global song_dur, song_length, song_mut

    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.play(start=(song_dur - 10))
            song_dur -= 10
        else:
            pygame.mixer.music.play(start=(song_dur - 10))
            song_dur -= 10
            pygame.mixer.music.pause()
    except pygame.error:
        messagebox.showerror("Error", "Please select and play a song first.")

seektnb = Button(root, command=seektenb, image=prev_img, borderwidth=0)
seektnb.grid(row=5, column=2)

def nsymbol(args):
    if len(args.get()) > 0:
        for i in args.get():
            if not i.isdigit():
                l = args.get()
                dex = l.index(i)
                toset = l[:dex] + l[dex + 1:]
                args.set(toset)
    if len(args.get()) > 2 : args.set(args.get()[:2])

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

play = Button(root, image=play_img, command=play_song, borderwidth=0)
play.grid(row=5, column=7)

previous = Button(root, image=previous_img, command=previous_song, borderwidth=0)
previous.grid(row=5, column=5)
nexts = Button(root, image=next_img, command=next_song, borderwidth=0)
nexts.grid(row=5, column=9)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

vol_up = Button(root, command=ivol, borderwidth=0, image=up_img)
vol_up.grid(row=7,column=8)

vol_down = Button(root, command=dvol, borderwidth=0, image=down_img)
vol_down.grid(row=7,column=7)

vol_mute = Button(root, command=mvol, borderwidth=0, image=unmute_img)
vol_mute.grid(row=7,column=6)

browse_icon = ImageTk.PhotoImage(Image.open('icons/browse.png').resize((10,10)))
quit_icon = ImageTk.PhotoImage(Image.open('icons/quit.png').resize((10,10)))
seek_icon = ImageTk.PhotoImage(Image.open('icons/seek.ico').resize((10,10)))
autoplay_icon = ImageTk.PhotoImage(Image.open('icons/autoplay.png').resize((10,10)))
help_icon = ImageTk.PhotoImage(Image.open('icons/help.ico').resize((10,10)))
about_icon = ImageTk.PhotoImage(Image.open('icons/about.ico').resize((10,10)))

menu = Menu(root)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Open folder", command=browse, compound='left', image=browse_icon, font=conforta, accelerator="Ctrl+O")
filemenu.add_command(label="Quit", command=cquit, compound='left', image=quit_icon, font=conforta, accelerator="Ctrl+Q")
menu.add_cascade(label="File", menu=filemenu, font=conforta)

audiomenu = Menu(menu, tearoff=0)
audiomenu.add_command(label=ap, command=tgautoplay, compound='left', image=autoplay_icon, font=conforta, accelerator="Ctrl+P")
audiomenu.add_command(label="Seek in audio", command=seek, compound='left', image=seek_icon, font=conforta, accelerator="Ctrl+E")
menu.add_cascade(label="Audio", menu=audiomenu, font=conforta)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="Help", command=ahelp, compound='left', image=help_icon, font=conforta, accelerator="Ctrl+H")
helpmenu.add_command(label="About", command=about, compound='left', image=about_icon, font=conforta, accelerator="Ctrl+B")
menu.add_cascade(label="Help", menu=helpmenu, font=conforta)

scrollbar.config(command=listbox.yview)
scrollbar2.config(command=listbox.xview)
root.config(menu=menu)
root.protocol("WM_DELETE_WINDOW", cquit)

root.bind("<space>" , lambda event : play_song())
root.bind("<Control-Shift-Right>" , lambda event : next_song())
root.bind("<Control-Shift-Left>" , lambda event : previous_song())
root.bind("<Control-Up>" , lambda event : ivol())
root.bind("<Control-Down>" , lambda event : dvol())
root.bind("<Control-o>", lambda event : browse())
root.bind("<Control-m>" , lambda event : mvol())
root.bind("<Control-q>", lambda event : cquit())
root.bind("<Control-h>", lambda event : ahelp())
root.bind("<Control-b>", lambda event : about())
root.bind("<Control-e>", lambda event : seek())
root.bind("<Control-p>", lambda event : tgautoplay())
root.bind("<Control-period>", lambda event : seektena())
root.bind("<Control-comma>", lambda event : seektenb())

new_thread()
root.mainloop()

#Attributions:
# Pause  -> https://www.flaticon.com/free-icons/pause - Pause icons created by Good Ware
# Play  -> https://www.flaticon.com/free-icons/play-button - Play button icons created by Freepik
# App icon -> https://www.flaticon.com/free-icons/music - Music icons created by Freepik
# Previous  -> https://www.flaticon.com/free-icons/next - Next icons created by srip
# Next  -> https://www.flaticon.com/free-icons/next - Next icons created by srip
# Volume up  -> https://www.flaticon.com/free-icons/volume-down - Volume down icons created by Freepik
# Volume down  -> https://www.flaticon.com/free-icons/volume-down - Volume down icons created by Freepik
# Mute  -> https://www.flaticon.com/free-icons/mute - Mute icons created by Freepik
# Unmute  -> https://www.flaticon.com/free-icons/enable-sound - Enable sound icons created by Freepik
# Seek  -> https://www.flaticon.com/free-icons/seeking - Seeking icons created by Freepik
# About  -> https://www.flaticon.com/free-icons/info - Info icons created by Freepik
# Help  -> https://www.flaticon.com/free-icons/question - Question icons created by Freepik
# Autoplay -> https://www.flaticon.com/free-icons/autoplay - Autoplay icons created by Flat Icons
# Quit  -> https://www.flaticon.com/free-icons/quit - Quit icons created by alkhalifi design
# Directory -> https://www.flaticon.com/free-icons/folder - Folder icons created by Freepik
# Skip 10 -> https://www.flaticon.com/free-icons/next - Next icons created by Arkinasi
# Previous 10 -> https://www.flaticon.com/free-icons/previous - Previous icons created by Arkinasi
