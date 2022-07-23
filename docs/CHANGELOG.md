# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.1.1] (MINOR UPDATE + PATCH)

### Additions

- A new cascade has been made for two Menus - Credits and Attributions.
- The credits window features the following:
  - Name and assigned task of the developers of the project.
  - Links to their GitHub profiles.
  - Special thanks
- The attributions window features the follwing:
  - All of the icon authors with respective links to their works.
  - Special thanks

### Changes in GUI

- Three new font styles have been added to make the GUI more consistent.
- Icons have been added for the new `Credits` and `Attributions` windows.
- For hyperlinks in the app, a new color `Teal Green` has been added with a `HEX` value of `006D5B`.

### Minor Changes

- Unused font `Nunito` has been removed from the app files completely.
- Attributions in form of comments have been removed from the end of `main.py` file.

### Known issues (will not be fixed being rare)

- On clicking on any song in the `Listbox` in the `listframel` widget, the keyboard shortcuts cease to operate.
- There are very little distortions in the GUI on some rare occasions.

## [v2.0.0] (MAJOR UPDATE)

### Additions

- Added the functionality to use the app offline.
- Adressed issue #10 - `WASAPI can't find requested audio endpoint`.
- Fixed a bug where previously written values in `Seek` were pre-filled on opening it the next time.
- `Pyglet` library is now used to import fonts instead of the in-built `tkFont` library.
- The title of the song now contains the current loaded directory, as it was removed in previous update.
- Version number is now encoded as a more understandable set of values, instead of a hardcoded value.
- Autoplay Menu option is currently disabled due to a major bug, it will be enabled in the next minor update or patch.
- Now on the ending of last song, the `song_index` variable sets to `0`, to enable the user to play the list of songs again, instead of repeating the last song.
- The seek buttons now seek to next or previous five seconds instead of ten seconds as it was previously.
- `check_for_updates()` function has been made non-parameterised as the parameter was of no use.
- Now the version returning from GitHub file is divided into three parts `MAJOR`, `MINOR` and `PATCH` and each variable is matched independently instead of as a whole.
- `TinyTag` library is now used to read the metadata stored in a song, and display it on `listframer` widget.

### Changes in GUI

- [Open Sans](https://fonts.google.com/specimen/Open+Sans) font is now used throught the app for better readability, and keeping a beautiful GUI.
- Changed all the icons except a few to keep a monochromatic color scheme.
- Added many labels to help display the song metadata on the `listframer` widget in the best way possible.
- The volume label has now been shifted to the `listframer` widget as it was causing major distortions in the GUI.
- `Menu` will now use your default system font, instead of using a custom font.

### Minor changes

- The sample songs have been moved to the directory ~/samples, and the code has been updated to adapt the change.
- The Autoplay Menu option has been assigned a toggle icon which changes its on-off state on toggling autoplay.
- Now an `Error` dialog will show if you open the app with no internet and you can use the app normally, instead of instant app crash.
- `About` dialog will hide the `Go to update` button when you are not connected to the internet and will show a message accordingly.
- Edited some text in `Help` dialog.
- Changed some shortcuts in the app:
  - Next song -> Control/Cmd + Right
  - Previous song -> Control/Cmd + Left
  - Up arrow -> Increase volume
  - Down arrow -> Decrease volume
- Attributed the new icon authors.

## [v1.3.0] (MINOR UPDATE)

### Additions

- Added comments on every function and hard-to-understand piece of code for better understanding what each function does.
- Removed the Current Directory label, as it caused distortions in the GUI.
- Restuctured the code for a better view.

## [v1.2.0] (MAJOR FEATURE ADDITIONS AND BUG FIXES)

### Bug fixes and feature addtions

- Added logging to the main python script. Now every action will be recorded in a 'player.log' file, and now it will be easier to search for `runtime` errors.
- Removed a feature which was causing a major bug (not able to change songs) in the app. This feature was one of the least used, and was introduced in the first pre-release.
- Fixed a major bug, causing peculiar behaviour of the `Scale` widget, not allowing it to move in certain scenarios, and also the songs not able to play correctly in the same event.
- Added a label for current song duration, total song duration, current volume and current directory, which is the major addition in this release.

## [v1.1.1] (MAJOR BUG FIX AND FEATURE ADDITION)

### Bug fixes and feature additions

- Fixed a major bug : If song has ended, the `Scale` doesn't reset to zero if there's only one song, and after ending in that case, the play `Button` does not work.
- Added two new buttons with the following fucntionalities:
    1. Two arrows pointing right : Seek 10 seconds forward
    2. Two arrows pointing left : Seek 10 seconds backward
- Added the respective keybindings for the above:
    1. Control + Period (.) -> Seek 10 seconds forward
    2. Control + Comma (,) -> Seek 10 seconds backward
- Major feature addition : Quitting the app now saves the directory you were in and the song you were playing. When you will reopen the app the next time, it will continue from the directory and song which you played last time.
- If an update is available, the help menu now shows the version number to which the update is available.

## [v1.0.0] (MAJOR UPDATE & FIRST PRODUCTION-READY RELEASE) - 2022-03-25

### First major release

- All dialog boxes have now been completely built.
- Added the necessary help needed to use the app.
- Added buttons to directly take you to Issues and Pull requests page to submit bug reports or features.
- Added a 'Get source code' button in the About window.
- Added icons to all `Menu` items.
- Added many more shortcuts, and added `accelerators` to `Menu` items to help you know about available shortcuts.
- Fixed some grammatical errors.
- Attributed icon authors at the end of [main.py](https://github.com/warrior-guys/musical-memory/blob/main/main.py) file.
- And many other minor changes.

## [v0.29.0-alpha] - 2022-03-25

### Enhancements

- Enhanced the automatic updates feature.
- Now clicking the Update button directly takes user to the update.

## [v0.28.2-alpha] (MAJOR BUG FIX) - 2022-03-25

### Bug fixes

- Fixed a major bug causing the program to crash if an empty directory is selected, or a directory with no music is selected.
- Fixed a bug causing problems in playing music when using Seek menu.
- Made the window resizable.

## [v0.28.0-alpha] - 2022-03-24

### First pre-release

- A  `Menubar` with all the necessary actions.
- An auto-update feature to enable automatic checking for new versions before starting the program.
- Options to Browse folders, Seek in audio, Toggle Autoplay, Help, About and Quit divided in three `cascades`.
- A fully-fuctional `Listbox` containing the `.mp3` files from the current working directory or from a browsed directory.
- Three `Buttons` to help in navigation and ease to play songs, namely: Play button, previous song button and next song button.
- A fully-functional seekbar to help you know where is the position of current song.
- Three buttons to control volume of the current song, namely: mute volume, decrease volume and increase volume.
- Autoplay functionality for your ease of using the program.
- Various Keybindings to enable easy use of the app:
  1. Space : Play/Pause
  2. Control/Cmd + Shift + Right arrow : Skip to next song
  3. Control/Cmd + Shift + Left arrow : Skip to previous song
  4. Control/Cmd + Up arrow : Increase volume
  5. Control/Cmd + Down arrow : Decrease volume
  6. Control/Cmd + `m` : Mute/Unmute volume
- Beautiful GUI with royalty-free icons for every window, and every button provided by [Flaticon](https://www.flaticon.com), and the authors attributed therein.
- Mini-windows to enable every action from the `Menubar`.

[v2.1.1]: https://github.com/warrior-guys/music-player/releases/tag/v2.1.1
[v2.0.0]: https://github.com/warrior-guys/music-player/releases/tag/v2.0.0
[v1.3.0]: https://github.com/warrior-guys/musical-memory/releases/tag/v1.3.0
[v1.2.0]: https://github.com/warrior-guys/musical-memory/releases/tag/v1.2.0
[v1.1.1]: https://github.com/warrior-guys/musical-memory/releases/tag/v1.1.1
[v1.0.0]: https://github.com/warrior-guys/musical-memory/releases/tag/v1.0.0
[v0.29.0-alpha]: https://github.com/warrior-guys/musical-memory/releases/tag/v0.29.0-alpha
[v0.28.2-alpha]: https://github.com/warrior-guys/musical-memory/releases/tag/v0.28.2-alpha
[v0.28.0-alpha]: https://github.com/warrior-guys/musical-memory/releases/tag/v0.28.0-alpha
