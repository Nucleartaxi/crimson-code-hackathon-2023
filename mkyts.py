#!/bin/python
from song import Song

def get_inputs():
    song_name = input("Song name: ")
    url = input("url: ")
    return Song(song_name, url)


def make_yts(song: Song):
    with open(song.display_name + ".yts", "w") as f:
        f.write(song.song)
    print("Wrote url " + song.song + " to file "+ song.display_name + ".yts")

make_yts(get_inputs())
