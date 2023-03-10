class Song:
    """Simple class containing a song and its name"""
    def __init__(self, name: str, song: str):
        self.display_name = name #the name to display to the user 
        self.song = song #either an absolute path to an audio file or a youtube url

