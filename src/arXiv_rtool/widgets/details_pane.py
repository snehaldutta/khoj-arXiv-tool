from textual.widgets import Label, Static
from textual.widget import Widget
from textual.app import ComposeResult
from ..models import Paper
import webbrowser


class DetailsPane(Widget):
    BINDINGS = [("o", "open_link", "Open paper")]

    def __init__(self) -> None:
        super().__init__()
        self._curr_paper: Paper | None = None

    def compose(self) -> ComposeResult:
        yield Label("Select a paper to see details.")
        yield Label(id="title_label")
        yield Label(id="authors_label")
        yield Label(id="published_date_label")
        yield Static(id="summary_label")
        yield Label(id="url_label")

    def update_details(self, paper: Paper) -> None:
        self._curr_paper = paper
        self.query_one(Label).display = False
        self.query_one("#title_label", Label).update(f"Title: {paper.title}")
        self.query_one("#authors_label", Label).update(
            f"Authors: {', '.join(paper.authors)}"
        )
        self.query_one("#published_date_label", Label).update(
            f"Published: {paper.published_date or 'N/A'}"
        )
        self.query_one("#summary_label", Static).update(
            f"Summary: {paper.summary or 'N/A'}"
        )
        self.query_one("#url_label", Label).update(f"URL: {paper.url}")

    def action_open_link(self) -> None:
        if self._curr_paper is not None:
            webbrowser.open(self._curr_paper.url)

    def clear(self) -> None:
        self._curr_paper = None
        self.query_one(Label).display = True
        self.query_one("#title_label", Label).update("")
        self.query_one("#authors_label", Label).update("")
        self.query_one("#published_date_label", Label).update("")
        self.query_one("#summary_label", Static).update("")
        self.query_one("#url_label", Label).update("")
