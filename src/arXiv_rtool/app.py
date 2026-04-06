from .rateLimiter import RateLimiter
from .arXivClient import ArXivClient
from .widgets.search_input import SearchInput
from .widgets.results_pane import ResultsPane
from .widgets.details_pane import DetailsPane
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual import work
from textual.widgets import Footer, Static, Label
from textual.screen import Screen


class SplashScreen(Screen):
    BINDINGS = [("enter", "start", "Let's Khoj")]

    def compose(self) -> ComposeResult:
        yield Static(
            """
██╗  ██╗██╗  ██╗ ██████╗      ██╗
██║ ██╔╝██║  ██║██╔═══██╗     ██║
█████╔╝ ███████║██║   ██║     ██║
██╔═██╗ ██╔══██║██║   ██║██   ██║
██║  ██╗██║  ██║╚██████╔╝╚█████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚════╝
        """,
            id="ascii_art",
        )
        yield Static("ArXiv Research Tool", id="subtitle")
        yield Label("Press Enter to Let's Khoj →", id="prompt")
        yield Footer()

    def action_start(self) -> None:
        self.app.pop_screen()


class ArXivResearchToolApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self._client = ArXivClient(RateLimiter(3))  # 1 request in every 3 seconds

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield ResultsPane()
                yield DetailsPane()
            yield SearchInput()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(SplashScreen())

    @work
    async def on_search_input_search_submitted(
        self, event: SearchInput.SearchSubmitted
    ) -> None:
        results_pane = self.query_one(ResultsPane)
        details_pane = self.query_one(DetailsPane)

        results_pane.clear()
        details_pane.clear()

        papers = await self._client.fetch(event.query, event.sort_by)  # type: ignore
        if not papers:
            return
        results_pane.update_results(papers)

    def on_results_pane_paper_selected(self, event: ResultsPane.PaperSelected) -> None:
        details_pane = self.query_one(DetailsPane)
        details_pane.update_details(event.paper)
