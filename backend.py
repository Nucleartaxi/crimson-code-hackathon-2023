from file_tree_navigator import FileTreeNavigator
from file_tree import FileTree
import file_tree_helpers
import copy
from song import song

class Backend:
    def __init__(self):
        #utils for navigating the file tree
        self.file_tree = file_tree_helpers.create_tree_from_music_directory()
        self.navigator = FileTreeNavigator(self.file_tree)

        #lists used for display
        self.previous_folder_list = []
        self.current_folder_list_display = []
        self.current_folder_list = []
        self.right_pane_list = [] 

        self._create_display_lists() #generate all the display lists on startup



    def _previous_folder_list(self): #left pane, displays the previous folder
        parent_navigator = copy.copy(self.navigator)
        parent_navigator.cd_parent()

        parent_list = parent_navigator.get_directories() + [x.display_name for x in parent_navigator.get_songs()]
        self.previous_folder_list = parent_list
    def _current_folder_list(self): #center pane, displays the current folder
        current_folder_list = self.navigator.get_directories() + self.navigator.get_songs()
        self.current_folder_list_display = self.navigator.get_directories() + [x.display_name for x in self.navigator.get_songs()]
        self.current_folder_list = current_folder_list
    def _right_pane_list(self): #right pane, used for displaying other things such as song info and help.
        right_pane_list = ["hello", "there", "general", "kenobi"]
        self.right_pane_list = right_pane_list
    def _create_display_lists(self): #creates all display lists 
        self._previous_folder_list()
        self._current_folder_list()
        self._right_pane_list()

    #private helpers for other functions
    def _seek(self, seconds: int): #,.<>
        pass

    #menu navigation and actions
    def pressed_index(self, index: int): #pressed an index in the current_list #enter, l
        """
        Handles every action taking place on a specific menu item in the list current_folder_list.
        For example, when you press enter on a directory, we should change to that directory.
        When pressing enter on a song, we should play that song.

        Regenerates lists as needed based on the action. (changing directory will regenerate lists, 
        playing song will add a marker on the currently playing song)
        """

        item = self.current_folder_list[index]
        if isinstance(item, str): #is directory
            self.navigator.cd(item)
            self._create_display_lists()
        elif isinstance(item, song): #is song
            print("playing song " + item.song)

        #handle enter folder, etc.
    def previous_directory(self): #h
        """Navigates to the previous directory and regenerates lists."""
        self.navigator.cd_parent() #change to previous dir
        self._create_display_lists()


    #playback
    def play_pause(self): #space, p
        pass
    def shuffle(self): #s
        pass
    def next_song(self): #L
        pass
    def previous_song(self): #H
        pass
    def seek_forward_slight(self): #.
        pass
    def seek_backward_slight(self): #,
        pass
    def seek_forward_alot(self): #>
        pass
    def seek_backward_alot(self): #<
        pass

