import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListItem, ListView, Static, Button
from textual.containers import Container
from textual import events









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
        ("k", "cursor_up", "Move down"),
    ]

    #Binding("enter", "select_cursor", "Select", show=False),
    #Binding("up", "cursor_up", "Cursor Up", show=False),
    #Binding("down", "cursor_down", "Cursor Down", show=False),

    #def compose(self) -> ComposeResult:
    #    """Create child widgets."""

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
        yield CurPane(
            ListItem(Label("hi")),
            ListItem(Label("hi")),
            ListItem(Label("hi")),
            ListItem(Label("hi")),
            ListItem(Label("hi")),
            id="cur", initial_index = 0


        )

        yield RightPane(id="right")
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
        self.set_focus(self.get_widget_by_id("cur"))

    def on_resize(self):
        self.get_widget_by_id("main").styles.height = os.get_terminal_size()[1] - 3

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""
        self.set_focus(self.get_widget_by_id("cur"))
        try:
            x = self.get_widget_by_id("right")
            key = event.key
            print(key)
            print("sup")
            x.update_text("testing")
        except Exception as e:
            with open("output.txt", "w") as file:
                file.write(str(e))


if __name__ == "__main__":
    app = vimusApp()
    app.run()
