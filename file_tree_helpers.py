from file_tree import FileTree
from os import getcwd

MUSIC_DIRECTORY = getcwd() + "/Music" #the hardcoded music directory for testing and demo

def create_tree_from_cwd(): #creates the tree from the current directory
    return FileTree(getcwd())

def create_tree_from_music_directory(): #creates the tree from a preconfigured music directory. 
    return FileTree(MUSIC_DIRECTORY)
