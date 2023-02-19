import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListItem, ListView, Static, Button
from textual.containers import Container
from textual import events







term_height = 0

class TimeDisplay(Static):
    """A widget to display elapsed time."""


class Stopwatch(Static):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")





class Text(Static):
    """Displays text to the screen."""

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
    """Provides a view of the previous directory."""

    BINDINGS = [
        ("j", "cursor_down", "Move down"),
        ("k", "cursor_up", "Move up"),
    ]

    SEARCHING: bool = False

    #Binding("enter", "select_cursor", "Select", show=False),
    #Binding("up", "cursor_up", "Cursor Up", show=False),
    #Binding("down", "cursor_down", "Cursor Down", show=False),

    #def compose(self) -> ComposeResult:
    #    """Create child widgets."""

    #def __init__(self,
    #    *children: ListItem,
    #    initial_index: int | None = 0,
    #    name: str | None = None,
    #    id: str | None = None,
    #    classes: str | None = None,
    #):
    #    super(CurPane, self).__init__(
    #            *children,
    #            initial_index=initial_index,
    #            name=name,
    #            id=id,
    #            classes=classes
    #    )



    def on_key(self, event: events.Key) -> None:
        global term_height
        """Called when the user presses a key."""

        key = event.key
        if self.SEARCHING:
            for i in range(self.index, len(self.DISPLAY_LIST)):
                name = self.DISPLAY_LIST[i]
                if name != None and len(name) > 0 and name[0] == key:
                    self.index = i
                    break
            self.SEARCHING = False
            return

        #replace with match later
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

    def refresh_list(self):
        self.clear()
        for elem in self.DISPLAY_LIST:
            self.append(ListItem(Label(elem)))


class RightPane(Static):
    """Provides a view of the previous directory."""

    def update_text(self, text: str):
        self.update(text)

class DetailsPane(Static):
    """Provides a view of the previous directory."""

class HelpPane(Static):
    """Provides a view of the previous directory."""

class MainPane(Static):
    """Contains all elements in the main pane."""

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        #yield PrevPane(ListItem(name="hi"), ListItem(name="hello"), id="prev", initial_index=0)
        yield PrevPane(id="prev", initial_index = 0)
        yield CurPane(ListItem(Label('a')), id="cur", initial_index = 0)
        yield RightPane("aa", id="right")
        #self.set_focus(self.get_widget_by_id("cur"))


class vimusApp(App):
    """Music browser and player."""

    CSS_PATH = "vimus.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        #yield Header()
        #yield Stopwatch()
        #yield Container(Stopwatch(), Stopwatch(), Stopwatch())
        yield MainPane(expand=True, id="main")
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
        cur.DISPLAY_LIST = [
            "hi",
            "himmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "hi",
            "lo",
        ]




    def on_resize(self):
        global term_height
        term_height = os.get_terminal_size()[1] - 2
        self.get_widget_by_id("main").styles.height = term_height

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""
        key = event.key
        try:
            self.set_focus(self.get_widget_by_id("cur")) #no matter what keybind is called, it should affect cur

            right = self.get_widget_by_id("right")
            right.update_text("testing")
        except Exception as e:
            with open("output.txt", "w") as file:
                file.write(str(e))
        if key == "h":
            cur = self.get_widget_by_id("cur")
            cur.refresh_list() #refresh
        elif key == "l":
            pass


if __name__ == "__main__":
    app = vimusApp()
    app.run()
