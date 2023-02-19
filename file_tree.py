from os import listdir
from os.path import isdir, isfile, splitext
from os import getcwd

# python mpv wrapper https://github.com/jaseg/python-mpv

#list of audio file formats. 
audio_file_formats = {
    ".aac", ".flac", ".m4a", ".mp3", ".ogg", ".oga", ".mogg", ".opus", ".wav", ".wma", ".webm", ".alac", ".aiff", ".wv"
}


MUSIC_DIRECTORY = getcwd() + "/Music" #the hardcoded music directory for testing and demo


class Song:
    def __init__(self, name, song):
        self.display_name = name #the name to display to the user 
        self.song = song #either an absolute path to an audio file or a youtube url


class TreeNode:
    """class representing a node in a tree, containing children and songs."""
    def __init__(self, parent, path: str): #constructor. 
        self.child_node_list: list[TreeNode] = []
        self.song_list: list[Song] = []
        self.parent: TreeNode | None = parent
        self.path = path
        self.init_helper()

    def init_helper(self): #helps initialize this node and child nodes.
        for entry in listdir(self.path): #for every entry in this directory
            display_entry = entry
            entry = self.path + "/" + entry
            # print(entry)
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



#class FileTree: #class representing a file tree.
#    def __init__(self, path):
#        self.root: TreeNode = TreeNode(None, path) 
#        self.root.parent = self.root


def create_tree_from_cwd() -> TreeNode: #creates the tree from the current directory
    #return FileTree(getcwd())
    return TreeNode(None, getcwd())

def create_tree_from_music_directory() -> TreeNode: #creates the tree from a preconfigured music directory. 
    #return FileTree(MUSIC_DIRECTORY)
    return TreeNode(None, MUSIC_DIRECTORY)

