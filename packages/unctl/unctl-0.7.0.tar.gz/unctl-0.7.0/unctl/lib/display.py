import re
from collections import defaultdict
import os
from colorama import init, Fore, Style
from prettytable import PrettyTable
import textwrap
from typing import List, Dict
from textwrap import fill
from unctl.lib.checks.check_report import CheckReport

init(autoreset=True)


class Display:
    """Handles display-related functionalities."""

    def __init__(self, options=None):
        self.options = options

    term_width = 80
    options = None

    @staticmethod
    def init(o):
        """Displays the results of the checks in a formatted table."""
        # Initialize colorama for terminal colored output
        init(autoreset=True)

        # Calculate terminal width for dynamic UI formatting
        try:
            Display.term_width = os.get_terminal_size().columns
        except OSError:
            # in case output won't go to the terminal
            Display.term_width = 200

        Display.options = o

    @staticmethod
    def create_default_table(field_names, align):
        fmt_fields = []
        for field_name in field_names:
            fmt_fields.append(
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL
            )

        table = PrettyTable(fmt_fields)
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True
        table.align = align

        return table

    @staticmethod
    def find_substrings(input_str):
        """Find substrings wrapped in double curly braces in a given string."""
        pattern = r"\{\{([^}]+)\}\}"
        matches = re.findall(pattern, input_str)
        return matches if matches else None

    @staticmethod
    def display_progress_bar_header():
        # Display the progress bar header
        print(
            f"\n{Fore.YELLOW}{Style.BRIGHT}"
            f"{'─' * Display.term_width}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'Running Kubernetes Checks'.center(Display.term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'─' * Display.term_width}"
            f"{Style.RESET_ALL}"
            f"\n"
        )

    @staticmethod
    def display_progress_bar(percentage, check_name, bar_length=80):
        """Displays a progress bar with the specified percentage completion."""
        blocks = int(round(bar_length * percentage))
        block_char = "▶"

        if percentage < 1:
            filled_part = Fore.LIGHTRED_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTRED_EX
        else:
            filled_part = Fore.LIGHTGREEN_EX + block_char * blocks + Style.RESET_ALL
            percent_color = Fore.LIGHTGREEN_EX

        empty_part = " " * (bar_length - blocks)
        progress_string = (
            f"\r{Fore.BLUE + Style.BRIGHT}In progress: {check_name}{Style.RESET_ALL}  "
            f"|{filled_part + empty_part}| "
            f"{percent_color + Style.BRIGHT}{percentage*100:.1f}%{Style.RESET_ALL}"
        )
        # Move the cursor up by one line and then clear that line
        move_up_and_clear_line = (
            f"\033[A"  # Move up one line
            f"\r{' ' * (Display.term_width - 1)}"  # Clear the line
            f"\r"  # Move cursor to the beginning of the line again
        )
        print(move_up_and_clear_line, end="", flush=True)

        print(progress_string, end="", flush=True)

    @staticmethod
    def check_progress_bar(checks_list, title):
        """Main function to manage the progress bar and checks."""
        results = []

        print("\n" + Fore.YELLOW + Style.BRIGHT + "=" * 50 + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + title.center(50) + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + "=" * 50 + Style.RESET_ALL + "\n")

        total_checks = len(checks_list)
        completed_checks = 0

        # Print an initial progress bar of 0%
        Display.display_progress_bar(0, checks_list[0][0])

        for check_name, check_func in checks_list:
            check_result = check_func()
            completed_checks += 1

            # Update the progress bar
            next_check_name = (
                checks_list[completed_checks][0]
                if completed_checks < total_checks
                else "Done"
            )
            Display.display_progress_bar(
                completed_checks / total_checks, next_check_name
            )

            if check_result[0]:
                results.append(
                    [check_name, Fore.GREEN + "Passed" + Style.RESET_ALL, "N/A", "N/A"]
                )
            else:
                results.append(
                    [
                        check_name,
                        Fore.RED + "Failed" + Style.RESET_ALL,
                        check_result[1].name,
                        check_result[2],
                    ]
                )

        print()  # New line after the progress bar completion
        print()  # Another new line for separation

        return results

    @staticmethod
    def pad_content(content, width):
        """Pad content to given width."""
        content_length = len(content)
        if content_length < width:
            padding = " " * (width - content_length)
            return content + padding
        return content

    @staticmethod
    def center_content(content, width):
        """Center the content for given width."""
        return content.center(width)

    @staticmethod
    def display_sort_by_check_table(check_details, llm_summary=False):
        """Display per check table."""
        headers = ["Resource Namespace", "Resource Name", "Status", "Severity"]

        if llm_summary:
            headers.append("LLM Explanation")
        else:
            headers.append("Status Extended")

        table = PrettyTable(headers)

        # Set the table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        # Set max width for columns
        table._max_width = {
            "Resource Namespace": 30,
            "Resource Name": 30,
            "Status": 10,
            "Severity": 10,
            "Status Extended": 70,
            "LLM Explanation": 70,
        }

        for detail in check_details:
            if detail.status == "FAIL":
                severity_color = (
                    Fore.RED
                    if detail.check_metadata.Severity == "critical"
                    else (
                        Fore.YELLOW
                        if detail.check_metadata.Severity == "severe"
                        else Fore.WHITE
                    )
                )
                severity = (
                    severity_color + detail.check_metadata.Severity + Style.RESET_ALL
                )

                if llm_summary and detail.llm_failure_summary is not None:
                    status_extended = "🧠 " + detail.llm_failure_summary
                else:
                    status_extended = detail.status_extended

                # Wrap the content based on max widths
                status_extended_wrapped = textwrap.fill(
                    status_extended, width=table._max_width.get("Status Extended", 0)
                )
                status_extended_wrapped = Display.center_content(
                    status_extended_wrapped, table._max_width.get("Status Extended", 0)
                )

                status = Fore.RED + detail.status + Style.RESET_ALL
                status = Display.center_content(
                    status, table._max_width.get("Status", 0)
                )

                severity = Display.center_content(
                    severity, table._max_width.get("Severity", 0)
                )

                resource_namespace_wrapped = textwrap.fill(
                    detail.resource_namespace,
                    width=table._max_width.get("Resource Namespace", 0),
                )
                resource_namespace_wrapped = Display.center_content(
                    resource_namespace_wrapped,
                    table._max_width.get("Resource Namespace", 0),
                )

                resource_name_wrapped = textwrap.fill(
                    detail.resource_name, width=table._max_width.get("Resource Name", 0)
                )
                resource_name_wrapped = Display.center_content(
                    resource_name_wrapped, table._max_width.get("Resource Name", 0)
                )

                row = [
                    resource_namespace_wrapped,
                    resource_name_wrapped,
                    status,
                    severity,
                    status_extended_wrapped,
                ]

                table.add_row(row, divider=True)

        # Color the headers in blue
        table_string = table.get_string()
        for field_name in table.field_names:
            # Use exact match by adding word boundaries \b
            exact_match_pattern = r"\b{}\b".format(re.escape(field_name))

            # Replace the exact match of field_name with color formatting
            table_string = re.sub(
                exact_match_pattern,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                table_string,
                1,
            )
        print(table_string)

    @staticmethod
    def display_list_checks_table(checks: List[CheckReport]):
        print()

        table = PrettyTable(
            [
                "Check",
                "Id",
                "Service",
                "Categories",
                "Severity",
                "Description",
            ]
        )

        # Set table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        for detail in checks:
            severity_color = (
                Fore.RED
                if detail.check_metadata.Severity == "critical"
                else (
                    Fore.YELLOW
                    if detail.check_metadata.Severity == "severe"
                    else Fore.WHITE
                )
            )
            severity = severity_color + detail.check_metadata.Severity + Style.RESET_ALL

            descr_width = Display.term_width - 110
            if descr_width < 30:
                descr_width = 30

            table.add_row(
                [
                    fill(detail.check_metadata.CheckTitle, width=30),
                    fill(detail.check_metadata.CheckID, width=20),
                    fill(detail.check_metadata.SubServiceName, width=20),
                    fill(",".join(detail.check_metadata.Categories), width=30),
                    fill(severity, width=20),
                    fill(detail.check_metadata.Description, width=descr_width),
                ],
                divider=True,
            )

        table_string = table.get_string()
        for field_name in table.field_names:
            table_string = table_string.replace(
                field_name,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                1,
            )
        print(table_string)

    @staticmethod
    def display_grouped_data(name: str, data: Dict[str, int]):
        table = Display.create_default_table([name, "Checks Count"], "l")

        for item, count in sorted(data.items()):
            table.add_row(
                [
                    item,
                    count,
                ],
            )

        print(table.get_string())

    @staticmethod
    def organize_results_by_resource(results):
        """Organize results by ResourceNamespace and ResourceName."""
        organized_results = defaultdict(lambda: defaultdict(list))
        for check_name, checks in results.items():
            for result in checks:
                resource_namespace = result.resource_namespace
                resource_name = result.resource_name
                organized_results[resource_namespace][resource_name].append(result)
        return organized_results

    @staticmethod
    def organize_results_by_check(results):
        """Organize results by CheckTitle."""
        organized_results = defaultdict(list)
        for check_name, checks in results.items():
            for result in checks:
                check_title = result.check_metadata.CheckTitle
                organized_results[check_title].append(result)
        return organized_results

    @staticmethod
    def display_sortby_object(results, llm_summary):
        headers = [
            "Resource Namespace",
            "Resource Name",
            "Check Title",
            "Status",
            "Severity",
        ]
        if llm_summary:
            headers.append("LLM Explanation")
        else:
            headers.append("Status Extended")

        table = PrettyTable(headers)
        # Set the table appearance to use solid lines for borders
        table.horizontal_char = "─"
        table.vertical_char = "|"
        table.junction_char = "─"
        table.border = True
        table.frame = True

        organized_results = Display.organize_results_by_resource(results)
        for resource_namespace, resources in organized_results.items():
            for resource_id, check_details in resources.items():
                for detail in check_details:
                    # Skip the detail if -f is enabled and
                    # the status is "PASS".
                    if Display.options.failing_only and detail.status == "PASS":
                        continue

                    severity = detail.check_metadata.Severity
                    if llm_summary and detail.llm_summary is not None:
                        status_extended = "🧠 " + detail.llm_summary
                    else:
                        status_extended = detail.status_extended

                    wrapped_title = textwrap.fill(
                        detail.check_metadata.CheckTitle, width=30
                    )
                    wrapped_status_extended = textwrap.fill(status_extended, width=60)

                    row = [
                        resource_namespace.ljust(20),
                        textwrap.fill(resource_id, width=20),
                        wrapped_title,
                        detail.status.center(10),
                        severity.center(10),
                        wrapped_status_extended,
                    ]
                    table.add_row(row, divider=True)

        # Then color the output
        table_string = table.get_string()
        for field_name in table.field_names:
            # Use exact match by adding word boundaries \b
            exact_match_pattern = r"\b{}\b".format(re.escape(field_name))

            # Replace the exact match of field_name with color formatting
            table_string = re.sub(
                exact_match_pattern,
                Fore.LIGHTBLUE_EX + Style.BRIGHT + field_name + Style.RESET_ALL,
                table_string,
                1,
            )
        table_output = (
            table_string.replace(
                "FAIL", Fore.RED + Style.BRIGHT + "FAIL" + Style.RESET_ALL
            )
            .replace("PASS", Fore.GREEN + Style.BRIGHT + "PASS" + Style.RESET_ALL)
            .replace(
                "critical",
                Fore.LIGHTRED_EX + Style.BRIGHT + "critical" + Style.RESET_ALL,
            )
            .replace(
                "severe",
                Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "severe" + Style.RESET_ALL,
            )
            .replace(
                "High",
                Fore.LIGHTYELLOW_EX + Style.BRIGHT + "High" + Style.RESET_ALL,
            )
            .replace("Low", Fore.LIGHTGREEN_EX + Style.BRIGHT + "Low" + Style.RESET_ALL)
        )
        print(table_output)

    @staticmethod
    def display_sortby_check(results, llm_summary):
        organized_results = Display.organize_results_by_check(results)
        for check_title, check_details in organized_results.items():
            statuses = [detail.status for detail in check_details]

            # Skip the check if -f is enabled and all checks passed.
            if Display.options.failing_only and all(
                status == "PASS" for status in statuses
            ):
                continue

            if all(status == "PASS" for status in statuses):
                print(Fore.WHITE + Style.BRIGHT + Fore.GREEN + f"✅ {check_title}")
                print()
            else:
                print(Fore.WHITE + Style.BRIGHT + Fore.RED + f"❌ {check_title}")
                Display.display_sort_by_check_table(check_details, llm_summary)
                print()

    @staticmethod
    def display_results_table(results, llm_summary=False, sort_by="object"):
        """Displays the results of the checks in a formatted table."""
        term_width = Display.term_width

        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'Checks Scan Report'.center(term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()
        if sort_by == "object":
            Display.display_sortby_object(results, llm_summary)
        elif sort_by == "check":
            Display.display_sortby_check(results, llm_summary)
        print("\n" + Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL)
        print(
            f"{Fore.YELLOW}"
            f"{Style.BRIGHT}"
            f"{'End of Scan Report'.center(term_width)}"
            f"{Style.RESET_ALL}"
        )
        print(Fore.YELLOW + Style.BRIGHT + "─" * term_width + Style.RESET_ALL + "\n")
        print()

    @staticmethod
    def debug_results_structure(results):
        unique_combinations = set()

        for result in results:
            sub_service = result.check_metadata.SubServiceName
            check_title = result.check_metadata.CheckTitle

            unique_combinations.add((sub_service, check_title))

        for combo in unique_combinations:
            print(combo)
