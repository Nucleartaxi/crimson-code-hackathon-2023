import copy
from mpv import MPV
from file_tree_navigator import FileTreeNavigator
from file_tree import Song, create_tree_from_music_directory
from random import randint
from debug import debug

class Backend:
    def __init__(self):
        """Utils for navigating the file tree"""
        self.file_tree = create_tree_from_music_directory()
        self.navigator = FileTreeNavigator(self.file_tree)

        #lists used for display
        self.previous_folder_list: list[str] = []
        self.current_folder_list_display: list[str] = []
        self.current_folder_list: list[str | Song] = []
        self.right_pane_list: list[str] = [] 

        self.mpv: MPV = MPV(ytdl=True, video=False) #create an mpv instance with ytdl enabled and no video (so audio only)
        self.current_song_list = self.navigator.get_songs()
        self.current_song_index = 0
        self.playback_mode = "normal" #possible values: normal, shuffle, repeat

        self.playback_song_history = []

        self._create_display_lists() #generate all the display lists on startup
        self.elapsed_time: float | None = None

        @self.mpv.property_observer('time-pos')
        def get_elapsed_time(_name, value: float):
            if isinstance(value, float):
                self.elapsed_time = value
            else:
                self.elapsed_time = None

    def _previous_folder_list(self):
        """Left pane, displays the previous folder"""
        parent_navigator = copy.copy(self.navigator) #create a temporary navigator
        result = parent_navigator.cd_parent()
        if not result: #set empty if no higher directory
            parent_list = []
        else:
            parent_list = [x + "/" for x in parent_navigator.get_directories()] + [x.display_name for x in parent_navigator.get_songs()]
        self.previous_folder_list = parent_list


    def _current_folder_list(self):
        """Center pane, displays the current folder"""
        current_folder_list = self.navigator.get_directories() + self.navigator.get_songs()
        self.current_folder_list_display = [x + "/" for x in self.navigator.get_directories()] + [x.display_name for x in self.navigator.get_songs()]
        self.current_folder_list = current_folder_list

    def _right_pane_list(self):
        """Right pane, used for displaying other information such as song info and help"""
        # right_pane_list = ["hello", "there", "general", "kenobi"]
        right_pane_list = [
            "h: left",
            "j: down",
            "k: up", 
            "l: right",
            "ENTER: play song",
            "p: play/pause",
            "H: prev song",
            "L: next song",
            "n/m: seek back/forward",
            "N/M: seek back/forward big",
            "s: shuffle mode",
            "r: repeat mode"
        ]
        self.right_pane_list = right_pane_list


    def _create_display_lists(self):
        """Creates all display lists"""
        self._previous_folder_list()
        self._current_folder_list()
        self._right_pane_list()

    def pressed_index(self, index: int, play_songs: bool) -> tuple[bool, int]: #pressed an index in the current_list #enter, l. 
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
        #self.navigator.set_focus(index, )
        if isinstance(item, str): #is directory
            self.navigator.set_focus(index) #record the current focus
            result = self.navigator.cd(item)
            if result:
                self._create_display_lists()
            return (result, self.navigator.get_focus()) #return if this is a directory
        elif isinstance(item, Song): #is song
            if play_songs: #if this action should play songs
                #we only need to update the current song list when a new song is selected.
                self.current_song_list = self.navigator.get_songs() #update the list of songs in the current directory that we are now playing.
                self.playback_mode = "normal" #reset back to normal play mode for this play
                self.playback_song_history = [] #reset history for this new song play
                self.play_song(item) #item is the song to play
            return (False, -1) #return if this is a song so we don't want to refresh
        #impossible else case
        return (False, -1)

    def previous_directory(self, index: int) -> tuple[bool, int]: #h
        """
        Navigates to the previous directory and regenerates lists.
        
        This function refreshes the lists.

        Returns true if changed the directory so we need to refresh. 
        """
        self.navigator.set_focus(index) #record the current focus
        result = self.navigator.cd_parent() #change to previous dir
        if result: #if we were able to move to the previous directory
            self._create_display_lists() #then update the directories
        return (result, self.navigator.get_focus())

    def current_path(self) -> str:
        return self.navigator.get_current_directory()


    #playback 
    def _seek(self, seconds: int): #,.<>
        """Seek forward or back a certain amount of seconds"""
        self.mpv.seek(seconds, reference="relative", precision="exact")
        self.mpv.properties

    def play_song(self, song: Song):
        """
        Plays the given song.
        """
        self.current_song = song.display_name
        self.mpv.play(song.song)
        self.current_song_index = self.current_song_list.index(song) #index of the song we're currently playing
        # self.mpv.wait_for_playback()

    def play_pause(self): #space, p
        self.mpv.cycle("pause")

    def set_mode(self, mode: str):
        """
        "normal", "shuffle", or "repeat" modes allowed
        """
        if mode in ["normal", "shuffle", "repeat"]:
            self.playback_mode = mode
        #else don't change it, since invalid input

    def next_song(self): #L
        if self.playback_mode == "normal": #get the next index
            new_index = self.current_song_index + 1
            if new_index < len(self.current_song_list) and new_index >= 0:
                self.play_song(self.current_song_list[new_index])
        elif self.playback_mode == "shuffle": #make a new random index
            self.playback_song_history.append(self.current_song_list[self.current_song_index]) #record the current song in the history
            new_index = randint(0, len(self.current_song_list)) #generate a new random index
            if new_index < len(self.current_song_list) and new_index >= 0:
                self.play_song(self.current_song_list[new_index])
        elif self.playback_mode == "repeat": #keep the same index
            self.play_song(self.current_song_list[self.current_song_index]) 


    def previous_song(self): #H
        if self.playback_mode == "normal":
            new_index = self.current_song_index - 1
            if new_index >= 0 and new_index < len(self.current_song_list):
                self.play_song(self.current_song_list[new_index])
        elif self.playback_mode == "shuffle":
            if len(self.playback_song_history) > 0:
                self.play_song(self.playback_song_history.pop()) #plays the song off the top of the history
            #else no songs to go back to, do nothing
        elif self.playback_mode == "repeat": #just play current song
            self.play_song(self.current_song_list[self.current_song_index])  


    def seek_forward_slight(self): #m
        self._seek(3)

    def seek_backward_slight(self): #n
        self._seek(-3)

    def seek_forward_alot(self): #M
        self._seek(60)

    def seek_backward_alot(self): #N
        self._seek(-60)



