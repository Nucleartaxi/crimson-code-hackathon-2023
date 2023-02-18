from file_tree import FileTree, TreeNode
import os

#current directory, previous directory 
#

class FileTreeNavigator:
    def __init__(self, file_tree: FileTree):
        self.tree = file_tree
        self.root = file_tree.root
        self.current = self.root #the current node 
    
    def get_current_directory(self): #returns the current directory path
        return self.current.path
    def cd_parent(self): #changes to the parent node
        self.current = self.current.parent
    def cd(self, path: str): #cd to a file within the current folder
        for node in self.current.child_node_list:
            if node.path == self.current.path + "/" + path: #if the path is the same, change directory
                self.current = node
    def get_songs(self):
        return self.current.song_list
    def get_directories(self): #returns the names of all the directories in the current directory
        return [os.path.basename(node.path) for node in self.current.child_node_list]
