from os import listdir
from os.path import isdir, isfile, splitext
from song import song

# python mpv wrapper https://github.com/jaseg/python-mpv

audio_file_formats = {
    ".aac", ".flac", ".m4a", ".mp3", ".ogg", ".oga", ".mogg", ".opus", ".wav", ".wma", ".webm", ".alac", ".aiff", ".wv"
}

class TreeNode:
    def init_helper(self):
        for entry in listdir(self.path): #for every entry in this directory
            display_entry = entry
            entry = self.path + "/" + entry
            # print(entry)
            if isdir(entry): #if is dir
                self.child_node_list.append(TreeNode(parent=self, path=entry))
            elif isfile(entry): #if is file
                filename, file_extension = splitext(display_entry)
                if file_extension in audio_file_formats: #it is audio
                    self.song_list.append(song(name=filename, song=entry)) #display name without filename, actual file is exact path to the entry
                elif file_extension == ".yts": #it is a youtube song
                    with open(entry, "r") as f:
                        url = f.readline().strip()
                        self.song_list.append(song(name=filename, song=url)) #file name, url 

    def __init__(self, parent, path):
        self.child_node_list = []
        self.song_list = []
        self.parent = parent
        self.path = path
        self.init_helper()

class FileTree:
    def __init__(self, path):
        print(path)
        self.root = TreeNode(None, path) 
        self.root.parent = self.root


