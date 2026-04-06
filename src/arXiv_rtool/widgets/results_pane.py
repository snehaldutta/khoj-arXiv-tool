from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Label, ListView, ListItem, Static
from ..models import Paper
from textual.message import Message


class ResultsPane(Widget):
    def __init__(self) -> None:
        super().__init__()
        self._papers: list[Paper] = []

    class PaperSelected(Message):
        def __init__(self, paper: Paper) -> None:
            super().__init__()
            self.paper = paper

    def compose(self) -> ComposeResult:
        yield Label("Search results will appear here.")
        yield ListView(id="results_list")

    def update_results(self, papers: list[Paper]) -> None:
        self._papers = papers
        is_empty = len(papers) == 0
        self.query_one(Label).display = is_empty
        results_list = self.query_one("#results_list", ListView)
        results_list.clear()
        for i, paper in enumerate(self._papers):
            results_list.append(ListItem(Static(f"{i + 1}. {paper.title}")))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        if index is not None:
            self.post_message(self.PaperSelected(self._papers[index]))

    def clear(self) -> None:
        self._papers = []
        self.query_one(Label).display = True
        self.query_one("#results_list", ListView).clear()
