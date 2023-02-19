import os
from file_tree import TreeNode


class FileTreeNavigator:
    def __init__(self, file_tree: TreeNode):
        self.root: TreeNode = file_tree
        self.current: TreeNode = self.root #the current node 
        self.focuses: dict[str, int] = dict()
    
    def get_current_directory(self) -> str:
        """Returns the current directory path"""
        return self.current.path

    def cd_parent(self) -> bool:
        """Focuses the parent node"""
        match self.current.parent:
            case None:
                return False
            case TreeNode:
                self.current = self.current.parent
        return True

    def cd(self, path: str) -> bool:
        """Focuses a subdirectory inside the present working directory"""
        lookup_path = self.current.path + "/" + path;
        for node in self.current.child_node_list:
            if node.path == lookup_path: #if the path is the same, change directory
                self.current = node
                return True
        return False

    def get_songs(self):
        """Returns the list of songs in this directory"""
        return self.current.song_list

    def get_directories(self) -> list[str]:
        """Returns the name of all subdirectories in the current directory"""
        return [os.path.basename(node.path) for node in self.current.child_node_list]

    def set_focus(self, index: int) -> None:
        """Sets the current focus index in this directory"""
        self.focuses[self.current.path] = index

    def get_focus(self) -> int:
        if self.current.path in self.focuses:
            return self.focuses[self.current.path]
        else:
            self.focuses[self.current.path] = 0
            return 0


