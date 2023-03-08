# Crimson Code Hackathon 2023 -- vimus
## Overview
A minimalist keyboard-centric TUI music player. Seamlessly supports playing both local files and streaming youtube audio. Use the keyboard to quickly navigate all functions, no mouse required.

### Features:
- Play local music files directly from your filesystem
- Stream audio from any youtube video from a youtube url
- Supports common music player features including play/pause, next, previous, seeking forward and backward by small and large increments, shuffle mode, and repeat song.
- Full keyboard control
- Dark mode/light mode toggle

## Prerequisites
Make sure mpv and yt-dlp are installed.
For Arch Linux, run this command:
```
yay -S mpv yt-dlp
```
For other distros and operating systems, instructions will differ.

Use the following command to install necessary Python extensions:
```
python -m pip install textual python-mpv
```

## License
This work is dual-licensed under GPL Version 2 and GPL Version 3. You may choose between these licenses on a case-by-case basis.

## Screenshot
![alt text](https://cdn.discordapp.com/attachments/341136221323526144/1076890649623810129/image.png)

