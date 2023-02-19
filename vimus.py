import os
from textual import events
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer, Label, ListItem, ListView, Static, Button
from textual.containers import Container
from backend import Backend
from debug import debug, debug_clear


term_height: int = 0 #the height of the terminal
"""Height of the terminal"""


class Text(Static):
    """Displays text to the screen."""

    def update_text(self, text: str):
        self.update(text)

class TopBar(Static):
    """Displays text to the screen."""

    def update_text(self, text: str):
        self.update(text)

class TopPane(Static):
    """Contains all elements in the bottom pane."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield TopBar("", id="directory")

class BottomSpacerLeft(Static):
    """Displays text to the screen."""

    def update_text(self, text: str):
        self.update(text)

class BottomSpacerRight(Static):
    """Displays text to the screen."""

    def update_text(self, text: str):
        self.update(text)

class ElapsedPane(Static):
    """Provides a view of the track details."""

    def update_text(self, text: str):
        self.update(text)

class ProgressPane(Static):
    """Provides a view of the track details."""

    def update_text(self, text: str):
        self.update(text)

class TotalPane(Static):
    """Provides a view of the track details."""

    def update_text(self, text: str):
        self.update(text)

class BottomPane(Static):
    """Contains all elements in the bottom pane."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield BottomSpacerLeft()
        yield BottomSpacerRight()
        yield ElapsedPane("00:00", id="elapsed")
        yield ProgressPane("", id="progress")
        yield TotalPane("00:00", id="total")


class PrevPane(ListView):
    """Provides a view of the previous directory."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield ListItem(Label("test"))
        yield ListItem(Label("test1"))
        yield ListItem(Label("test2"))
        yield ListItem(Label("test3"))
        yield ListItem(Label("test3"))


class CurPane(ListView):
    """Provides a view of the current directory."""

    BINDINGS = [
        ("j", "cursor_down", "Move down"),
        ("k", "cursor_up", "Move up"),
    ]

    SEARCHING: bool = False
    """Denotes whether we're in searching mode after pressing 'f'"""

    DISPLAY_LIST: list[str] = []
    """Stores a string version of the current list"""

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""
        global term_height

        key = event.key
        if self.SEARCHING:
            for i in range(self.index, len(self.DISPLAY_LIST)):
                name = self.DISPLAY_LIST[i]
                if name != None and len(name) > 0 and name[0] == key:
                    self.index = i
                    break
            self.SEARCHING = False
            return

        #handle keybinds, replace with match later
        if key == "g":
            self.index = 0
        elif key == "G":
            self.index = len(self.children) - 1
        elif key == "d":
            self.index = min(int(self.index + term_height / 2), len(self.children) - 1)
        elif key == "u":
            self.index = max(int(self.index - term_height / 2), 0)
        elif key == "f":
            self.SEARCHING = True


class RightPane(Static):
    """Provides a view of the track details."""

    def update_text(self, text: str):
        self.update(text)


class MainPane(Static):
    """Contains all elements in the main pane."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield PrevPane(id="prev", initial_index = 0)
        yield CurPane(ListItem(Label('a')), id="cur", initial_index = 0)
        yield RightPane("aa", id="right")


class vimusApp(App):
    """Music browser and player."""

    BACKEND = Backend()
    CSS_PATH = "vimus.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_dark", "Toggle dark mode"),
    ]
    TIME_COUNTING = False
    TIME_DISPLAY = reactive("")


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield TopPane(expand=False, id="top")
        yield MainPane(expand=True, id="main")
        yield BottomPane(expand=True, id="bottom")
        yield Footer()

    def set_initial_focus(self):
        self.set_focus(self.get_widget_by_id("cur"))

    def action_toggle_dark(self) -> None:
        """Toggles dark mode."""
        self.dark = not self.dark

    def on_mount(self):
        """Gets called when widget is finalized."""
        cur = self.get_widget_by_id("cur")
        self.set_focus(cur)
        self.refresh_panes()
        self.set_interval(1 / 4, self.update_time)

    def update_time(self):
        """Updates the displayed elapsed time"""
        import math
        time_elapsed: float | None = self.BACKEND.elapsed_time
        try:
            progress = self.get_widget_by_id("progress")
            elapsed = self.get_widget_by_id("elapsed")
            if not isinstance(elapsed, ElapsedPane) or not isinstance(progress, ProgressPane):
                raise Exception("Widgets were not initialized correctly")
        except:
            raise Exception("Widgets were not initialized correctly")
        if time_elapsed == None:
            progress.update_text("")
            time_elapsed = 0
        else:
            progress.update_text(self.BACKEND.current_song)
        if not self.TIME_COUNTING:
            self.TIME_DISPLAY = reactive("0:00") 
        minutes = str(math.floor(time_elapsed / 60))
        seconds = str(math.floor(time_elapsed % 60))
        text = ("0" * (2 - len(minutes))) + minutes + ":" + ("0" * (2 - len(seconds))) + seconds
        self.TIME_DISPLAY = reactive(text)
        elapsed.update_text(text)

    def on_resize(self):
        """Called when window is resized"""
        global term_height
        term_height = os.get_terminal_size()[1] - 3
        self.get_widget_by_id("main").styles.height = term_height

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""
        key = event.key
        self.set_focus(self.get_widget_by_id("cur")) #no matter what keybind is called, it should affect cur

        #fix type hinting
        try:
            prev = self.get_widget_by_id("prev")
            cur = self.get_widget_by_id("cur")
            right = self.get_widget_by_id("right")
            if not isinstance(cur, CurPane) or not isinstance(right, RightPane) or not isinstance(prev, PrevPane):
                raise Exception("Widgets were not initialized correctly")
        except:
            raise Exception("Widgets were not initialized correctly")

        if key == "h": #previous dir
            result, index = self.BACKEND.previous_directory(cur.index)
            if result:
                self.refresh_panes() #refresh
            if index > -1: #update index
                cur.index = index
        elif key == "l": #next dir
            result, index = self.BACKEND.pressed_index(cur.index, False)
            if result: #if updating panes
                prev_index = cur.index
                self.refresh_panes()
                prev.index = prev_index
            if index > -1: #update index
                cur.index = index
        elif key == "enter": #next dir or play
            result, index = self.BACKEND.pressed_index(cur.index, True)
            if result: #if updating panes
                prev_index = cur.index
                self.refresh_panes()
                prev.index = prev_index
            if index > -1: #update index
                cur.index = index
        elif key == "p":
            self.BACKEND.play_pause()
        elif key == "L":
            self.BACKEND.next_song()
        elif key == "H":
            self.BACKEND.previous_song()
        elif key == "m":
            self.BACKEND.seek_forward_slight()
        elif key == "n":
            self.BACKEND.seek_backward_slight()
        elif key == "M":
            self.BACKEND.seek_forward_alot()
        elif key == "N":
            self.BACKEND.seek_backward_alot()
        elif key == "s":
            self.BACKEND.set_mode("shuffle")
        elif key == "r":
            self.BACKEND.set_mode("repeat")
        

    def refresh_panes(self):
        """Refresh all panes in the main pane"""

        #fix type hinting
        try:
            directory = self.get_widget_by_id("directory")
            prev = self.get_widget_by_id("prev")
            cur = self.get_widget_by_id("cur")
            right = self.get_widget_by_id("right")
            if not isinstance(cur, CurPane) or not isinstance(right, RightPane) or not isinstance(prev, PrevPane) or not isinstance(directory, TopBar):
                raise Exception("Widgets were not initialized correctly")
        except:
            raise Exception("Widgets were not initialized correctly")

        prev.clear()
        cur.clear()
        for elem in self.BACKEND.previous_folder_list: #populate prev
            prev.append(ListItem(Label(elem)))
        for elem in self.BACKEND.current_folder_list_display: #populate cur
            cur.append(ListItem(Label(elem)))
        right.update_text("\n".join(item for item in self.BACKEND.right_pane_list)) #populate right
        directory.update_text(self.BACKEND.current_path())


if __name__ == "__main__":
    debug_clear()
    app = vimusApp()
    app.run()
