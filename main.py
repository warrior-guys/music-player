import contextlib
import os
import pygame
import functools
import requests
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scale, Separator
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from math import floor, ceil
from bs4 import BeautifulSoup
import webbrowser
import logging
from tinytag import TinyTag
import pyglet

# Initializes the Tkinter window along with necessary libraries.
root = Tk()
root.geometry('1280x720')

root.grid_rowconfigure((0,1,2,3,4), weight=2)
root.grid_rowconfigure((5,6,7), weight=1)
root.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), weight=1)
root.iconbitmap('icons/appicon.ico')

# This empties the log file before starting the program, to not clutter it.
with open('player.log', 'w') as f:
    f.write("")

# Sets up the logger and it's format.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(thread)d - %(asctime)s - %(levelname)s : %(lineno)d - %(message)s')
file_handler = logging.FileHandler('player.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.warning("This file has all the logging information needed to check for bugs to the greatest extent. Avoid modifying this file.")

# This block checks if there are any errors in initializing Pygame.
try:
    pygame.mixer.pre_init()
    pygame.init()
    pygame.mixer.init()
except pygame.error:
    logger.exception("Failed to initialize pygame, no audio endpoints available")
    messagebox.showerror("Error", "Failed to initialize pygame, no audio endpoints available")
    root.destroy()

# Define all the images and icons needed.
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
browse_icon = ImageTk.PhotoImage(Image.open('icons/browse.png').resize((10,10)))
quit_icon = ImageTk.PhotoImage(Image.open('icons/quit.png').resize((10,10)))
seek_icon = ImageTk.PhotoImage(Image.open('icons/new_seek.png').resize((10,10)))
autoplay_on_icon = ImageTk.PhotoImage(Image.open('icons/on.png').resize((10,10)))
autoplay_off_icon = ImageTk.PhotoImage(Image.open('icons/off.png').resize((10,10)))
help_icon = ImageTk.PhotoImage(Image.open('icons/help.png').resize((10,10)))
about_icon = ImageTk.PhotoImage(Image.open('icons/about.png').resize((10,10)))

# Define all the pre-defined variables.
played_song = 0
changed_song = 0
dir_changed = False
update_checked = False
update_available = False
was_playing = False
ap = "Autoplay: On"
clicked_mute = False
l = True
initial_vol = 1.0
info = []
song_mut = None
song_length = 0.0
val = 0.1
minute = StringVar()
second = StringVar()
song_dur = 0.0
mini_seek = Toplevel(root)
mini_seek.destroy()
music_end = False

# App version is defined here.
MAJOR = 2
MINOR = 0
PATCH = 0
__version__ = f"v{MAJOR}.{MINOR}.{PATCH}"

# Define all the fonts
pyglet.font.add_file('fonts/open_sans.ttf')
pyglet.font.add_file('fonts/nunito.ttf')
open_sans = ('Open Sans', 11)
open_sans_listbox = ('Open Sans', 12)
open_sans_big = ('Open Sans', 20)
open_sans_big_2 = ('Open Sans', 20, 'bold')
nunito = ('Nunito', 14, 'bold')

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

current_dur = StringVar()
current_dur_label = Label(root, textvariable=current_dur, font=open_sans)
current_dur_label.grid(row=6, column=0)
current_dur.set("00:00")

total_dur = StringVar()
total_dur_label = Label(root, textvariable=total_dur, font=open_sans)
total_dur_label.grid(row=6, column=17)
total_dur.set("00:00")

current_volume_txt = StringVar()
current_volume_txt.set(f'{100}')

listframel = Frame(root)
listframel.grid(row=0, column=0, sticky=NSEW, rowspan=5, columnspan=3)
listframel.configure(bg="white")
listframer = Frame(root)
listframer.grid(row=0, column=3, sticky=NSEW, rowspan=5, columnspan=15)
listframer.configure(bg="white")

listframel.grid_rowconfigure((0,1,2,3,4), weight=1)
listframel.grid_columnconfigure((0,), weight=1)

listframer.grid_rowconfigure((0,1,2,3,4,5), weight=1)
listframer.grid_columnconfigure((0,1), weight=1)

listframe = Frame(listframer, background='white')
listframe.grid(row=5, rowspan=5, column=1)

song_name_initials = StringVar()
song_name_initials.set(f'Song Name : ')
song_artist_initials = StringVar()
song_artist_initials.set(f'Artist Name(s) : ')
song_bitrate_initials = StringVar()
song_bitrate_initials.set(f'Bitrate : ')
song_duration_initials = StringVar()
song_duration_initials.set(f'Duration : ')
song_genre_initials = StringVar()
song_genre_initials.set(f'Genre : ')
song_volume_initials = StringVar()
song_volume_initials.set(f'Volume : ')

song_name = StringVar()
song_name.set("")
song_artist = StringVar()
song_artist.set("")
song_bitrate = StringVar()
song_bitrate.set("")
song_duration = StringVar()
song_duration.set("")
song_genre = StringVar()
song_genre.set("")

song_name_initials_label = Label(listframer, textvariable=song_name_initials, font=open_sans_big_2, background='white')
song_artist_initials_label = Label(listframer, textvariable=song_artist_initials, font=open_sans_big_2, background='white')
song_bitrate_initials_label = Label(listframer, textvariable=song_bitrate_initials, font=open_sans_big_2, background='white')
song_duration_initials_label = Label(listframer, textvariable=song_duration_initials, font=open_sans_big_2, background='white')
song_genre_initials_label = Label(listframer, textvariable=song_genre_initials, font=open_sans_big_2, background='white')
song_volume_initials_label = Label(listframer, textvariable=song_volume_initials, font=open_sans_big_2, background='white')

song_name_label = Label(listframer, textvariable=song_name, font=open_sans_big, background='white')
song_artist_label = Label(listframer, textvariable=song_artist, font=open_sans_big, background='white')
song_bitrate_label = Label(listframer, textvariable=song_bitrate, font=open_sans_big, background='white')
song_duration_label = Label(listframer, textvariable=song_duration, font=open_sans_big, background='white')
song_genre_label = Label(listframer, textvariable=song_genre, font=open_sans_big, background='white')
song_volume_label = Label(listframer, textvariable=current_volume_txt, font=open_sans_big, background='white')

song_name_initials_label.grid(row=0, column=0, sticky=E)
song_artist_initials_label.grid(row=1, column=0, sticky=E)
song_bitrate_initials_label.grid(row=2, column=0, sticky=E)
song_duration_initials_label.grid(row=3, column=0, sticky=E)
song_genre_initials_label.grid(row=4, column=0, sticky=E)
song_volume_initials_label.grid(row=5, column=0, sticky=E)

song_name_label.grid(row=0, column=1, sticky=W)
song_artist_label.grid(row=1, column=1, sticky=W)
song_bitrate_label.grid(row=2, column=1, sticky=W)
song_duration_label.grid(row=3, column=1, sticky=W)
song_genre_label.grid(row=4, column=1, sticky=W)
song_volume_label.grid(row=5, column=1, sticky=W)

scrollbar = Scrollbar(listframel)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar2 = Scrollbar(listframel, orient='horizontal')
scrollbar2.pack(side=BOTTOM, fill=X)

listbox = Listbox(listframel, xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, font=open_sans_listbox, borderwidth=0)
listbox.pack(fill=BOTH, expand=1)

scrollbar.config(command=listbox.yview)
scrollbar2.config(command=listbox.xview)

current_value = DoubleVar()
slider = Scale(root, from_=0, to=100, orient='horizontal', variable=current_value)
slider.grid(row=6, column=1, columnspan=16, sticky='we')

# This reads the info.txt file, to check if previous instance was saved and if it was saved, it will load the previous instance.
try:
    if os.path.getsize('info.txt') > 0:
        with open('info.txt', 'r') as f:
            f.readline()
            pth = f.readline()[:-1]
            song_index = int(f.readline()[:-1])
            logger.debug("Loaded previous instance")
    else:
            pth = f'{os.getcwd()}/samples'
            song_index = 0
            logger.debug("Loaded a new instance")
except FileNotFoundError:
    pth = f'{os.getcwd()}/samples'
    song_index = 0
    logger.exception("No file info.txt, loaded a new instance")

song_list = os.listdir(pth)
root.title(f"{pth} - Music Player")
lst = [str(song) for song in song_list if song.endswith(".mp3")]

with contextlib.suppress(IndexError):
    tpath = f'{pth}/{lst[song_index]}'
    logger.debug("Initial directory loaded, no IndexError")

# This function implements when you click the browse option in Menu.
def browse():
    global pth, song_list, lst, listbox, dir_changed
    temp = pth
    logger.info("Opened select directory dialog")
    try:
        pth = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a folder")
        song_list = os.listdir(pth)
        lst = [str(song) for song in song_list if song.endswith(".mp3")]
        if not lst:
            pth = temp
            song_list = os.listdir(pth)
            lst = [str(song) for song in song_list if song.endswith(".mp3")]
            messagebox.showerror("Music not found", "Please select a directory with music. Operation unsuccessful.")
            logger.warning("No music was found in selected directory, switched to previous directory")
        else:
            dir_changed = True
            pygame.mixer.music.stop()
            listbox.delete(0, END)
            lst = [str(song) for song in song_list if song.endswith(".mp3")]

            for i in range(len(lst)):
                lg = lst[i]
                lgl = len(lg)
                listbox.insert(i+1, lg[:lgl - 4])
                logger.info("Moved to a new directory")
    except FileNotFoundError:
        pth = temp
        song_list = os.listdir(pth)
        logger.exception("Cancelled select directory dialog")

# This function is the toggle for autoplay.
def tgautoplay():
    global ap, l

    if l:
        audiomenu.entryconfigure(0, label="Autoplay: Off")
        audiomenu.entryconfigure(0, image=autoplay_off_icon)
        l = False
        logger.info("Autoplay turned off")
    else:
        audiomenu.entryconfigure(0, label="Autoplay: On")
        audiomenu.entryconfigure(0, image=autoplay_on_icon)
        l = True
        logger.info("Autoplay turned on")

# This function records your clicks on the list on songs.
def fileSelection(self):
    global song_index, changed_song, pth, tpath

    s = song_index
    selection = listbox.curselection()
    song_index = functools.reduce(lambda sub, ele: sub * 10 + ele, selection)
    if s != song_index:
        changed_song = 1

listbox.bind("<<ListboxSelect>>", fileSelection)

# This function implements when you click the play button.
def play_song():
    global played_song, changed_song, song_index, pth, tpath, song_dur, music_end

    try:
        tpath = f'{pth}/{lst[song_index]}'
    except IndexError:
        tpath = f'{pth}/{lst[0]}'

    if pygame.mixer.music.get_busy(): # If song is playing, pause it.
        pygame.mixer.music.pause()
        play.config(image=play_img)
        logger.info("Paused current song")
    else:
        if played_song == 0:
            try:
                path = f'{pth}/{lst[song_index]}'
            except IndexError:
                path = f'{pth}/{lst[0]}'
                logger.exception("Opened the app with a different directory than the previous one, with len less than the previous one")
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play()
            song_dur = 0
            played_song = 1
            logger.info("Played current song")
        elif played_song == 1:
            if changed_song == 0:
                if not music_end: # Unpause current song if it has not ended
                    pygame.mixer.music.unpause()
                    logger.info("Unpaused current song")
                else: # Play the first song if last song ended and there's no song after it
                    pygame.mixer.music.unpause()
                    logger.info("Last song ended, played the first song")
                    music_end = False
            elif changed_song == 1:
                path = f'{pth}/{lst[song_index]}'
                if path == tpath:
                    pygame.mixer.music.load(str(path))
                    pygame.mixer.music.play()
                    song_dur = 0
                    logger.info("Played a new song")
                else:
                    pygame.mixer.music.unpause()
                    play.config(image=play_img)
                    logger.info("Unpaused current song")
                changed_song = 0
        play.config(image=pause_img)

# This function implements every 0.1 seconds to check some important values, and to update the UI if needed.
def new_thread():
    global changed_song, song_index, tpath, current_value, dir_changed, val, slider, song_dur, update_checked, song_length, song_mut, music_end

    if not update_checked: # Check for updates before starting the app
        try:
            check_for_updates()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("No internet", "Sorry, can't check for updates! You need to be connected to the internet to check for updates.")
            logger.critical("User not connected to the internet, can't check for updates.")
        update_checked = True
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            if song_index == len(lst) - 1: # If on the last song, stop the music, and set next song to be played to the first song
                play.config(image=play_img)
                music_end = True
                song_index = 0
                path = f'{pth}/{lst[song_index]}'
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.play()
                pygame.mixer.music.pause()
            elif dir_changed: # If directory is changed, skip to the first song in the list
                changed_song = 1
                song_index = 0
                play_song()
                dir_changed = False
                pygame.mixer.music.pause()
                play.config(image=play_img)
            elif l: # If autoplay is on, skip to next song
                if song_index == len(lst) - 1:
                    changed_song = 1
                    song_index = 0
                    play_song()
                else:
                    changed_song = 1
                    song_index += 1
                    play_song()
            else:
                play.config(image=play_img)
            song_dur = 0
    try:
        song_mut = MP3(tpath)
        song_length = song_mut.info.length
    except NameError:
        song_length = 1

    if pygame.mixer.music.get_busy(): # Increment the value of Scale widget by 0.1 units every 0.1 seconds while song is being played
        if song_dur <= song_length:
            song_dur += 0.1
        else:
            song_dur = 0
    slider.config(to=song_length)

    if floor(song_dur % 60) < 10: # Format the string which contains current duration in the form MM:SS
        current_dur.set(str(floor(song_dur // 60)) + ":0" + str(floor(song_dur % 60)))
    else:
        current_dur.set(str(floor(song_dur // 60)) + ":" + str(floor(song_dur % 60)))

    if floor(song_length % 60) < 10: # Format the string which total duration in the form MM:SS
        total_dur.set(str(floor(song_length // 60)) + ":0" + str(floor(song_length % 60)))
    else:
        total_dur.set(str(floor(song_length // 60)) + ":" + str(floor(song_length % 60)))
    
    slider.set(song_dur)

    # Disable or enable the song increment buttons according to the place at which the Scale is
    if song_dur + 5 >= song_length:
        seektna.config(state="disabled")
    else:
        seektna.config(state="active")

    if song_dur <= 5:
        seektnb.config(state="disabled")
    else:
        seektnb.config(state="active")

    plol()
    root.title(f"{pth} - Music Player")
    root.after(100, new_thread)

# This function displays the Yes/No dialog on the quit command, and saves the necessary info in the info.txt and player.log files.
def cquit():
    mb = messagebox.askyesno('QUITTING', 'Are you sure you want to quit the application?')

    if mb:
        with open('info.txt', 'w') as f:
            f.write("* WARNING * - MODIFYING THIS FILE CAN CAUSE UNEXPECTED PROBLEMS IN THE MUSIC PLAYER APP! IF YOU HAVE MISTAKENLY MODIFIED THE FILE, PLEASE CLEAR ALL CONTENTS OR DELETE THIS FILE." + '\n')
            f.write(pth + '\n')
            f.write(str(song_index) + '\n')
        logger.info("Quitted the app with logging info stored in player.log")
        root.destroy()

# This function gives the skip to previous song functionality.
def previous_song():
    global changed_song, song_index, lst

    if song_index == 0: # If you're on the first song, show an error message.
        messagebox.showerror("Error", "This is the first song")
        logger.warning("Didn't skip to previous song, currently at first song")
    else:
        changed_song = 1
        song_index -= 1
        pygame.mixer.music.pause()
        play_song()
        logger.info("Skipped to previous song")

# This function gives the skip to next song functionality.
def next_song():
    global changed_song, song_index, lst
    
    if song_index == len(lst) - 1: # If you're on the last song, show an error message.
        messagebox.showerror("Error", "This is the last song")
        logger.warning("Didn't skip to next song, currently at last song")
    else:
        changed_song = 1
        song_index += 1
        pygame.mixer.music.pause()
        play_song()
        logger.info("Skipped to next song")

# This function gives the functionality to increase volume.
def ivol():
    global initial_vol

    if initial_vol > 0.95:
        pygame.mixer.music.set_volume(initial_vol+0.05)
        initial_vol = 1.0
    else:
        pygame.mixer.music.set_volume(initial_vol+0.05)
        initial_vol += 0.05
    current_volume_txt.set(f'{ceil(round(pygame.mixer.music.get_volume() * 100, 0))}')

# This function gives the functionality to decrease volume.
def dvol():
    global initial_vol

    if initial_vol < 0.05:
        pygame.mixer.music.set_volume(initial_vol-0.05)
        initial_vol = 0.0
    else:    
        pygame.mixer.music.set_volume(initial_vol-0.05)
        initial_vol -= 0.05
    current_volume_txt.set(f'{ceil(round(pygame.mixer.music.get_volume() * 100, 0))}')

# This function gives the functionality to mute the volume.
def mvol():
    global clicked_mute, initial_vol

    if clicked_mute: # If mute was clicked previously, return to the last stored volume.
        pygame.mixer.music.set_volume(initial_vol)
        vol_mute.config(image=unmute_img)
        clicked_mute = False
    else:
        pygame.mixer.music.set_volume(0.0)
        vol_mute.config(image=mute_img)
        clicked_mute = True
    current_volume_txt.set(f'{ceil(round(pygame.mixer.music.get_volume() * 100, 0))}')

# This function gets called when Help menu is clicked.
def ahelp():
    logger.info("Opened help menu")
    help_window = Toplevel(root)
    help_window.geometry('400x700')
    help_window.resizable(False, False)
    help_window.title("Help")
    help_window.grab_set()
    help_window.grid_rowconfigure((0,1,2,3,4), weight=1)
    help_window.grid_columnconfigure((0,), weight=1)
    help_window.iconbitmap('icons/help.ico')

    var_temp = StringVar()
    var_temp.set("This is a simple media player! To get started:\n\n1. Select a directory with some songs.\n2. Press the play button.\n3. Boom! You know how to use the app.\n\nThe app has simple icons with functionality similar to their look, you will be easily able to do all the tasks on your own. We have provided a list of shortcuts below which you can use as per your ease of use!\n\nSpacebar : Play/Pause\nControl + Right Arrow : Next song\nControl + Left Arrow : Previous song\nRight Arrow : Seek 5 seconds forward\nLeft Arrow : Seek 5 seconds backward\nUp Arrow : Increase Volume\nDown Arrow : Decrease Volume\n Control + M : Mute Volume\nControl + O : Browse a directory\nControl + Q : Quit")
    
    help_label = Label(help_window, textvariable=var_temp, font=open_sans, wraplength=400)
    help_label.grid(row=0, column=0)

    separator = Separator(help_window, orient='horizontal')
    separator.grid(row=1, column=0, sticky='we')

    issue_pull = StringVar()
    issue_pull.set("Encountering any bug or issue, or want to ask for a feature? Submit them below and we will respond as quick as possible!")

    issue_pull_label = Label(help_window, textvariable=issue_pull, font=open_sans, wraplength=400)
    issue_pull_label.grid(row=2, column=0)

    issue_btn_text = StringVar()
    issue_btn_text.set("Report a Bug/Issue")
    pull_btn_text = StringVar()
    pull_btn_text.set("Ask for a feature")

    issue_btn = Button(help_window, borderwidth=0.5, textvariable=issue_btn_text, font=open_sans, command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory/issues", new=1))
    pull_btn = Button(help_window, borderwidth=0.5, textvariable=pull_btn_text, font=open_sans, command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory/pulls", new=1))
    issue_btn.grid(row=3, column=0)
    pull_btn.grid(row=4, column=0)

    help_window.mainloop()

# This function gets called when About menu is clicked.
def about():
    logger.info("Opened about menu")
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
    
    about_label = Label(about_window, textvariable=var_temp, font=open_sans, wraplength=350)
    about_label.grid(row=0, column=0)

    src_btn = Button(about_window, text="Go to source code", command=lambda: webbrowser.open(url="https://github.com/warrior-guys/musical-memory", new=1), font=open_sans)
    src_btn.grid(row=1, column=0)
    
    separator = Separator(about_window, orient='horizontal')
    separator.grid(row=2, column=0, sticky='we')

    version_var = StringVar()
    version_var.set(f"Current version: {__version__}")

    version_number = Label(about_window, textvariable=version_var, font=open_sans)
    version_number.grid(row=3, column=0)

    temp_var = StringVar()
    lbl1 = Label(about_window, textvariable=temp_var, font=open_sans, wraplength=300)
    lbl1.grid(row=5, column=0)

    try:
        logger.debug(f"Link in go to update button: {info[1]}")
        update_button = Button(about_window, borderwidth=0.5, command=lambda: webbrowser.open(url=info[1], new=1), font=open_sans)
        update_button.grid(row=4, column=0)

        if update_available: # If an update is available, activate the button.
            update_button.config(text="Go to update")
            temp_var.set(f"An update to version {info[0]} is available. Click above to go our GitHub and download the latest version.")
        else:
            update_button.config(text="No updates available", state="disabled")
            temp_var.set("No updates were found on our GitHub. The app is up-to-date.")
    except IndexError:
        temp_var.set("You aren't connected to a network. We can't check for updates.")
        logger.error("User not connected to the internet, button not visible.")

    about_window.mainloop()

# This function checks for updates, and takes the current app version as a parameter.
def check_for_updates():
    global update_available, info

    r = requests.get('https://github.com/warrior-guys/musical-memory/blob/main/docs/version.txt') # Get the version.txt file in a HTML-type form.

    soup = BeautifulSoup(r.content, 'html.parser')
    gh_td = soup.findAll('td', attrs={"class":"blob-code blob-code-inner js-file-line"}) # Get the text stored in the version.txt file.

    for td in gh_td:
        info.append(td.text) # Add the information to list info[].

    # Check if current app version matches with the version in version.txt file.
    __github_version__ = info[0][1:]
    GITHUB_MAJOR_VERSION = int(__github_version__.split('.')[0])
    GITHUB_MINOR_VERSION = int(__github_version__.split('.')[1])
    GITHUB_PATCH_VERSION = int(__github_version__.split('.')[2])

    if (MAJOR != GITHUB_MAJOR_VERSION) or (MINOR != GITHUB_MINOR_VERSION) or (PATCH != GITHUB_PATCH_VERSION):
        update_available = True
        logger.info(f"Update available to version {__github_version__}.")
        messagebox.showinfo("Update available", "An update is available. To update the app - In the menu bar, go to Help -> About and click on the 'Update' button.")
    else:
        update_available = False
        logger.info(f"No updates available, current version {__version__} matches with GitHub version {__github_version__}.")

# This function gets called when the Seek menu is clicked.
def seek():
    global minute, second, mini_seek, play, was_playing

    logger.info("Opened seek menu")

    mini_seek = Toplevel(root)
    mini_seek.title("Seek")
    mini_seek.resizable(False, False)
    mini_seek.geometry('300x150')
    mini_seek.grab_set()
    mini_seek.grid_rowconfigure((0,2,3), weight=1)
    mini_seek.grid_rowconfigure((1,), weight=2)
    mini_seek.grid_columnconfigure((0,2), weight=3)
    mini_seek.grid_columnconfigure((1,), weight=1)
    mini_seek.iconbitmap('icons/new_seek.ico')

    minute.set("")
    second.set("")

    tmpvar = StringVar()
    tmpvar.set("Seek to the duration of audio you want")

    was_playing = bool(pygame.mixer.music.get_busy())
    play.config(image=play_img)
    pygame.mixer.music.pause()

    txt1 = Label(mini_seek, textvariable=tmpvar, font=open_sans)
    txt1.grid(row=0, column=0, columnspan=3)

    song_mut = MP3(tpath)
    song_length = song_mut.info.length

    colon = StringVar()
    colon.set(":")
    colon = Label(mini_seek, textvariable=colon, font=open_sans)
    colon.grid(row=1, column=1)

    min_entry = Entry(mini_seek, textvariable=minute, font=open_sans, width=5, borderwidth=0.5)
    sec_entry = Entry(mini_seek, textvariable=second,font=open_sans, width=3, borderwidth=0.5)
    min_entry.grid(row=1, column=0)
    sec_entry.grid(row=1, column=2)

    song_duration = StringVar()
    if floor(song_length % 60) < 10:
        song_duration.set("Current song length: " + str(floor(song_length // 60)) + ":0" + str(floor(song_length % 60)))
    else:
        song_duration.set("Current song length: " + str(floor(song_length // 60)) + ":" + str(floor(song_length % 60)))
    sngdur = Label(mini_seek, textvariable=song_duration, font=open_sans)
    sngdur.grid(row=2, column=0, columnspan=3)

    minute.trace("w", lambda *args: limitSizeMinute(minute))
    second.trace("w", lambda *args: nsymbol(second))

    submit_btn = Button(mini_seek, text="Seek", font=open_sans, borderwidth=0.5, command=seekto)
    submit_btn.grid(row=3, column=0, columnspan=3)

    mini_seek.protocol("WM_DELETE_WINDOW", destroy)
    mini_seek.mainloop()

# If you didn't seek to any duration, this method gets called.
def destroy():
    global mini_seek, was_playing

    if was_playing:
        play.config(image=pause_img)
        pygame.mixer.music.unpause()
    else:
        play.config(image=play_img)

    logger.info("Didn't seek, quitted seek menu")
    mini_seek.destroy()

# This function regulates the text entered in the Minute entry box of Seek menu.
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

# This function regulates the text entered in the Seconds entry box of Seek menu.
def nsymbol(args):
    if len(args.get()) > 0:
        for i in args.get():
            if not i.isdigit():
                l = args.get()
                dex = l.index(i)
                toset = l[:dex] + l[dex + 1:]
                args.set(toset)
    if len(args.get()) > 2 : args.set(args.get()[:2])

# This function gets called when you click Seek Button in Seek menu.
def seekto():
    global minute, second, current_value, slider, song_dur, mini_seek

    song_mut = MP3(tpath)
    song_length = song_mut.info.length

    try:
        if (int(minute.get()) * 60 + int(second.get())) > floor(song_length): # If you entered a value more than total duration
            messagebox.showerror("Error", "Please type a value less than the duration")
            logger.warning("Seeked a value greater than current duration")
        else:
            song_dur = floor((int(minute.get()) * 60 + int(second.get())))
            if was_playing: # If song was already playing.
                pygame.mixer.music.play(start=float((int(minute.get()) * 60 + int(second.get()))))
                play.config(image=pause_img)
            else: # If song was paused before.
                pygame.mixer.music.play(start=float((int(minute.get()) * 60 + int(second.get()))))
                pygame.mixer.music.pause()
                play.config(image=play_img)
            logger.info("Seeked to a new duration")
            mini_seek.destroy()
    except ValueError: # If you did'nt fill all the fields.
        messagebox.showwarning("Warning", "Please fill all fields")
        logger.exception("Didn't seek, all fields not filled")
    except pygame.error: # If you did'nt select any song, and still clicked on Seek button.
        messagebox.showerror("Error", "Please select and play a song first.")
        logger.exception("Didn't seek, no song selected")

# This function gets called if you click on the Seek ten seconds right arrow button.
def seenfivea():
    global song_dur, song_length, song_mut

    if song_dur + 5 < song_length:
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.play(start=(song_dur + 5))
                song_dur += 5
            else:
                pygame.mixer.music.play(start=(song_dur + 5))
                song_dur += 5
                pygame.mixer.music.pause()
        except pygame.error:
            messagebox.showerror("Error", "Please select and play a song first.")
            logger.exception("Didn't select a song, tried to seek five seconds after")

# This function gets called if you click on the Seek ten seconds before right arrow button.
def seekfiveb():
    global song_dur, song_length, song_mut
    
    if song_dur > 5:
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.play(start=(song_dur - 5))
                song_dur -= 5
            else:
                pygame.mixer.music.play(start=(song_dur - 5))
                song_dur -= 5
                pygame.mixer.music.pause()
        except pygame.error:
            messagebox.showerror("Error", "Please select and play a song first.")
            logger.exception("Didn't select a song, tried to seek five seconds before")

def plol():
    global song_name, song_artist, song_bitrate, song_duration, song_genre

    try:
        tag = TinyTag.get(f'{pth}/{lst[song_index]}')
        if len(lst[song_index]) <= 20:
            song_name.set(f"{lst[song_index][:-4]}")
        else:
            song_name.set(f"{lst[song_index][:20]}...")
    except IndexError:
        print(f'{pth}/{lst[0]}')
        tag = TinyTag.get(f'{pth}/{lst[0]}')
        if len(lst[0]) <= 20:
            song_name.set(f"{lst[0][:-4]}")
        else:
            song_name.set(f"{lst[0][:20]}...")
        logger.exception("Didn't select a song, tried to get tags")

    if tag.artist != None:
        if len(tag.artist) <= 20:
            song_artist.set(f"{tag.artist}")
        else:    
            song_artist.set(f"{tag.artist[:20]}...")
    else:
        song_artist.set(f"Not found")
    if tag.bitrate != None:
        song_bitrate.set(f"{int(tag.bitrate * 8 / 1000)} MB/s")
    else:
        song_bitrate.set(f"Not found MB/s")
    duration = f"{int(tag.duration // 60)} minutes and {floor(tag.duration % 60)} seconds"
    if tag.duration != None:
        song_duration.set(f"{duration}")
    else:
        song_duration.set(f"Not found")
    if tag.genre != None:
        song_genre.set(f"{tag.genre}")
    else:
        song_genre.set(f"Not found")

seektna = Button(root, command=seenfivea, image=seek_img, borderwidth=0)
seektna.grid(row=5, column=13)

seektnb = Button(root, command=seekfiveb, image=prev_img, borderwidth=0)
seektnb.grid(row=5, column=3)

play = Button(root, image=play_img, command=play_song, borderwidth=0)
play.grid(row=5, column=8)

previous = Button(root, image=previous_img, command=previous_song, borderwidth=0)
previous.grid(row=5, column=6)
nexts = Button(root, image=next_img, command=next_song, borderwidth=0)
nexts.grid(row=5, column=10)

vol_up = Button(root, command=ivol, borderwidth=0, image=up_img)
vol_up.grid(row=7,column=9)

vol_down = Button(root, command=dvol, borderwidth=0, image=down_img)
vol_down.grid(row=7,column=8)

vol_mute = Button(root, command=mvol, borderwidth=0, image=unmute_img)
vol_mute.grid(row=7,column=7)

menu = Menu(root)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label="Open folder", command=browse, compound='left', image=browse_icon, accelerator="Ctrl+O")
filemenu.add_command(label="Quit", command=cquit, compound='left', image=quit_icon, accelerator="Ctrl+Q")
menu.add_cascade(label="File", menu=filemenu, font=open_sans)

audiomenu = Menu(menu, tearoff=0)
audiomenu.add_command(label=ap, command=tgautoplay, compound='left', image=autoplay_on_icon, accelerator="Ctrl+P")
audiomenu.add_command(label="Seek in audio", command=seek, compound='left', image=seek_icon, accelerator="Ctrl+E")
menu.add_cascade(label="Audio", menu=audiomenu, font=open_sans)

helpmenu = Menu(menu, tearoff=0)
helpmenu.add_command(label="Help", command=ahelp, compound='left', image=help_icon, accelerator="Ctrl+H")
helpmenu.add_command(label="About", command=about, compound='left', image=about_icon, accelerator="Ctrl+B")
menu.add_cascade(label="Help", menu=helpmenu)

for i in range(len(lst)):
    lg = lst[i]
    lgl = len(lg)
    listbox.insert(i+1, lg[:lgl - 4])

# Bind functions to key-clicks.
root.bind("<space>" , lambda event : play_song())
root.bind("<Control-Right>" , lambda event : next_song())
root.bind("<Control-Left>" , lambda event : previous_song())
root.bind("<Up>" , lambda event : ivol())
root.bind("<Down>" , lambda event : dvol())
root.bind("<Control-o>", lambda event : browse())
root.bind("<Control-m>" , lambda event : mvol())
root.bind("<Control-q>", lambda event : cquit())
root.bind("<Control-h>", lambda event : ahelp())
root.bind("<Control-b>", lambda event : about())
root.bind("<Control-e>", lambda event : seek())
root.bind("<Control-p>", lambda event : tgautoplay())
root.bind("<Right>", lambda event : seenfivea())
root.bind("<Left>", lambda event : seekfiveb())

root.config(menu=menu)
root.protocol("WM_DELETE_WINDOW", cquit)

new_thread()
root.mainloop()

#Attributions :
# Play -> https://www.flaticon.com/free-icons/video - Video icons created by Freepik
# Pause -> https://www.flaticon.com/free-icons/pause - Pause icons created by Good Ware
# App icon -> https://www.flaticon.com/free-icons/music - Music icons created by Freepik
# Quit -> https://www.flaticon.com/free-icons/quit - Quit icons created by alkhalifi design
# Directory -> https://www.flaticon.com/free-icons/folder - Folder icons created by Freepik
# Skip 5 -> https://www.flaticon.com/free-icons/next - Next icons created by Arkinasi
# Previous 5 -> https://www.flaticon.com/free-icons/previous - Previous icons created by Arkinasi
# Seek -> https://www.flaticon.com/free-icons/search - Search icons created by Royyan Wijaya
# Autoplay on -> https://www.flaticon.com/free-icons/button - Button icons created by Pixel perfect
# Autoplay off -> https://www.flaticon.com/free-icons/button - Button icons created by Pixel perfect
# Next song -> https://www.flaticon.com/free-icons/next - Next icons created by Freepik
# Previous song -> https://www.flaticon.com/free-icons/next - Next icons created by Freepik
# Volume down -> https://www.flaticon.com/free-icons/ui - Ui icons created by nawicon
# Volume up -> https://www.flaticon.com/free-icons/volume - Volume icons created by nawicon
# Mute -> https://www.flaticon.com/free-icons/ui - Ui icons created by nawicon
# Unmute -> https://www.flaticon.com/free-icons/ui - Ui icons created by nawicon
# Help -> https://www.flaticon.com/free-icons/question - Question icons created by Freepik
# About -> https://www.flaticon.com/free-icons - Info icons created by Freepik
