from textual.widgets import Input, Button
from textual.widget import Widget
from textual.app import ComposeResult
from textual.message import Message
from typing import Literal


class SearchInput(Widget):
    SORT_OPTIONS: list[Literal["relevance", "lastUpdatedDate", "submittedDate"]] = [
        "relevance",
        "lastUpdatedDate",
        "submittedDate",
    ]

    def __init__(self) -> None:
        super().__init__()
        self._sort_index = 0

    class SearchSubmitted(Message):
        def __init__(
            self,
            query: str,
            sort_by: Literal["relevance", "lastUpdatedDate", "submittedDate"],
        ) -> None:
            super().__init__()
            self.query = query
            self.sort_by = sort_by

    def compose(self) -> ComposeResult:
        yield Button("Sort: Relevance", id="sort_btn")
        yield Input(placeholder="Search arXiv...", id="search_query")
        yield Button("Search", id="search_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        print(f"Button pressed: {event.button.id}")
        if event.button.id == "sort_btn":
            self._sort_index = (self._sort_index + 1) % len(self.SORT_OPTIONS)
            self.query_one(
                "#sort_btn", Button
            ).label = f"Sort: {self.SORT_OPTIONS[self._sort_index]}"

        elif event.button.id == "search_button":
            query_input = self.query_one("#search_query", Input)
            query = query_input.value.strip()
            if query:
                sort_by = self.SORT_OPTIONS[self._sort_index]
                self.post_message(self.SearchSubmitted(query, sort_by))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search_query":
            query = event.value.strip()
            if query:
                sort_by = self.SORT_OPTIONS[self._sort_index]
                self.post_message(self.SearchSubmitted(query, sort_by))
