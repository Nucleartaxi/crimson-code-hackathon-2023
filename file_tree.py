from os import listdir
from os.path import isdir, isfile, splitext
from os import getcwd
from song import Song

# python mpv wrapper https://github.com/jaseg/python-mpv

audio_file_formats = {
    ".aac", ".flac", ".m4a", ".mp3", ".ogg", ".oga", ".mogg", ".opus", ".wav", ".wma", ".webm", ".alac", ".aiff", ".wv"
}
"""List of supported audio file formats"""


MUSIC_DIRECTORY = getcwd() + "/Music"
MUSIC_DIRECTORY = "/home/alexander/Music"
"""Harded music directory for testing and demo"""



class TreeNode:
    """Class representing a node in a tree, containing children and songs."""
    def __init__(self, parent, path: str): #constructor. 
        self.child_node_list: list[TreeNode] = []
        self.song_list: list[Song] = []
        self.parent: TreeNode | None = parent
        self.path = path
        self.init_helper()

    def init_helper(self):
        """Helps initialize node and children"""
        for entry in listdir(self.path): #for every entry in this directory
            display_entry = entry
            entry = self.path + "/" + entry
            if isdir(entry): #if is dir
                self.child_node_list.append(TreeNode(parent=self, path=entry))
            elif isfile(entry): #if is file
                filename, file_extension = splitext(display_entry)
                if file_extension in audio_file_formats: #it is audio
                    self.song_list.append(Song(name=filename, song=entry)) #display name without filename, actual file is exact path to the entry
                elif file_extension == ".yts": #it is a youtube song
                    with open(entry, "r") as f:
                        url = f.readline().strip()
                        self.song_list.append(Song(name=filename, song=url)) #file name, url 

            #sort the lists for organized output
            self.child_node_list = sorted(self.child_node_list, key=(lambda x: x.path))
            self.song_list = sorted(self.song_list, key=(lambda x: x.display_name))


def create_tree_from_cwd() -> TreeNode:
    """Creates the tree from the current directory"""
    return TreeNode(None, getcwd())

def create_tree_from_music_directory() -> TreeNode:
    """Creates the tree from the preconfigured music directory"""
    return TreeNode(None, MUSIC_DIRECTORY)

