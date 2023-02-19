import file_tree_helpers
import copy
from song import Song
from mpv import MPV
from file_tree_navigator import FileTreeNavigator

class Backend:
    def __init__(self):
        """Utils for navigating the file tree"""
        self.file_tree = file_tree_helpers.create_tree_from_music_directory()
        self.navigator = FileTreeNavigator(self.file_tree)

        #lists used for display
        self.previous_folder_list: list[str] = []
        self.current_folder_list_display: list[str] = []
        self.current_folder_list: list[str | Song] = []
        self.right_pane_list: list[str] = [] 

        self.mpv: MPV = MPV(ytdl=True, video=False) #create an mpv instance with ytdl enabled and no video (so audio only)
        self.current_song_list = self.navigator.get_songs()
        self.current_song_index = 0

        self._create_display_lists() #generate all the display lists on startup

    def _previous_folder_list(self):
        """Left pane, displays the previous folder"""
        parent_navigator = copy.copy(self.navigator)
        parent_navigator.cd_parent()

        parent_list = parent_navigator.get_directories() + [x.display_name for x in parent_navigator.get_songs()]
        self.previous_folder_list = parent_list


    def _current_folder_list(self):
        """Center pane, displays the current folder"""
        current_folder_list = self.navigator.get_directories() + self.navigator.get_songs()
        self.current_folder_list_display = self.navigator.get_directories() + [x.display_name for x in self.navigator.get_songs()]
        self.current_folder_list = current_folder_list

    def _right_pane_list(self):
        """Right pane, used for displaying other information such as song info and help"""
        right_pane_list = ["hello", "there", "general", "kenobi"]
        self.right_pane_list = right_pane_list


    def _create_display_lists(self):
        """Creates all display lists"""
        self._previous_folder_list()
        self._current_folder_list()
        self._right_pane_list()

    def pressed_index(self, index: int, play_songs: bool) -> bool: #pressed an index in the current_list #enter, l. 
        """
        Handles every action taking place on a specific menu item in the list current_folder_list.
        For example, when you press enter on a directory, we should change to that directory.
        When pressing enter on a song, we should play that song.

        Regenerates lists as needed based on the action. (changing directory will regenerate lists, 
        playing song will add a marker on the currently playing song)

        set play_songs to true if you want this action to also play songs. Set it to false if you don't want this action to play songs.

        This function refreshes the lists.

        Returns a true if we navigated to a new directory, false if it was a song. 
        """

        item = self.current_folder_list[index]
        if isinstance(item, str): #is directory
            self.navigator.cd(item)
            self._create_display_lists()
            return True #return if this is a directory
        elif isinstance(item, Song): #is song
            if (play_songs): #if this action should play songs
                #we only need to update the current song list when a new song is selected.
                self.current_song_list = self.navigator.get_songs() #update the list of songs in the current directory that we are now playing.
                self.play_song(item) #item is the song to play
            return False #return if this is a song so we don't want to refresh
        return False

    def previous_directory(self) -> bool: #h
        """
        Navigates to the previous directory and regenerates lists.
        
        This function refreshes the lists.

        Returns true if changed the directory so we need to refresh. 
        """
        self.navigator.cd_parent() #change to previous dir
        self._create_display_lists()
        return True

    #playback 
    def _seek(self, seconds: int): #,.<>
        """Seek forward or back a certain amount of seconds"""
        self.mpv.seek(seconds, reference="relative", precision="exact")

    def play_song(self, song: Song):
        """
        Plays the given song.
        """
        self.mpv.play(song.song)
        self.current_song_index = self.current_song_list.index(song) #index of the song we're currently playing

    def play_pause(self): #space, p
        self.mpv.cycle("pause")

    def shuffle(self): #s
        pass

    def next_song(self): #L
        new_index = self.current_song_index + 1
        if new_index < len(self.current_song_list) and new_index >= 0:
            self.play_song(self.current_song_list[new_index])

    def previous_song(self): #H
        new_index = self.current_song_index - 1
        if new_index >= 0 and new_index < len(self.current_song_list):
            self.play_song(self.current_song_list[new_index])

    def seek_forward_slight(self): #m
        self._seek(3)

    def seek_backward_slight(self): #n
        self._seek(-3)

    def seek_forward_alot(self): #M
        self._seek(60)

    def seek_backward_alot(self): #N
        self._seek(-60)


