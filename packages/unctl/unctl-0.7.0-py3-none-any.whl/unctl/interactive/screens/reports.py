from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header
from unctl.interactive.screens.resolving import ResolvingScreen

from unctl.lib.checks.check_report import CheckReport
from unctl.scanrkube import ResourceChecker


class ReportsTableScreen(Screen):
    TITLE = "Interactive remediation"

    BINDINGS = [
        ("r", "re_run_check", "Re-run checks"),
    ]

    def __init__(
        self,
        columns: list[str],
        items: list[CheckReport],
        checker: ResourceChecker,
        group=False,
    ):
        super().__init__()
        self.columns = columns
        self._items = items
        self._checker = checker

        if group:
            self._bindings.bind("escape", "app.pop_screen", "Back")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield DataTable(zebra_stripes=True, cursor_type="row", id="table")

    def on_mount(self):
        data_table = self.query_one(DataTable)
        data_table.add_columns(*self.columns)

        rows = list(map(lambda item: item.display_row, self._items))
        data_table.add_rows(rows)

    def action_re_run_check(self):
        table = self.query_one(DataTable)
        table.loading = True

        self.re_run_checks()

    def update(self):
        table = self.query_one(DataTable)

        failing_reports = self._checker.failing_reports

        for item in self._items:
            if not any(
                report
                for report in failing_reports
                if report.object_id == item.object_id
            ):
                item.status = "PASS"

        rows = list(map(lambda item: item.display_row, self._items))
        table.rows = {}
        table.add_rows(rows)
        table.loading = False

    @work()
    async def re_run_checks(self):
        await self._checker.execute()

        self.update()

    def on_data_table_row_selected(self, row_selected):
        item: CheckReport = self._items[row_selected.cursor_row]

        if not self.app.is_screen_installed(item.object_id):
            self.app.install_screen(
                ResolvingScreen(
                    item=item,
                    checker=self._checker,
                    masks=self.app._app_config.anonymisation.masks,
                ),
                item.object_id,
            )
        self.app.push_screen(item.object_id)
