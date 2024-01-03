from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header
from unctl.interactive.headers import HEADERS
from unctl.interactive.screens.reports import ReportsTableScreen

from unctl.lib.models.remediations import FailureGroup
from unctl.scanrkube import ResourceChecker


class GroupsTableScreen(Screen):
    TITLE = "Triaged errors"

    BINDINGS = []

    _current_group: ReportsTableScreen

    def __init__(self, checker: ResourceChecker, provider: str):
        super().__init__()
        self._checker = checker
        self._provider = provider

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield DataTable(zebra_stripes=True, cursor_type="row", id="group-table")

    def on_mount(self):
        data_table = self.query_one(DataTable)
        headers = [
            "Group",
            "Failed Objects",
            "Summary",
        ]
        data_table.add_columns(*headers)

        rows = list(
            map(
                lambda item: [
                    item.title,
                    item.failed_count,
                    item.summary,
                ],
                self._checker.failure_groups,
            )
        )
        data_table.add_rows(rows)

    def on_data_table_row_selected(self, row_selected):
        group: FailureGroup = self._checker.failure_groups[row_selected.cursor_row]
        self._current_group = ReportsTableScreen(
            HEADERS[self._provider],
            items=group.objects,
            checker=self._checker,
            group=True,
        )

        self.app.push_screen(self._current_group)

    def update(self):
        self._current_group.update()
