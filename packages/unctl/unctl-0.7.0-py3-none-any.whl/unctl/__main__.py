from argparse import ArgumentParser
import sys
import asyncio
from textual.app import App

from unctl.config.config import load_config
from unctl.constants import CheckProviders
from unctl.interactive.remediation import RemediationApp

from unctl.lib.checks.loader import ChecksLoader

from unctl.lib.llm.base import LanguageModel
from unctl.lib.llm.assistant import OpenAIAssistant
from unctl.lib.display import Display

from unctl.scanrkube import JobDefinition, ResourceChecker, KubernetesDataCollector
from unctl.version import check, current
from unctl.list import load_checks, get_categories, get_services
from unctl.interactive.interactive import InteractiveApp

LLM_ANALYSIS_THRESHOLD = 10


def unctl_process_args():
    parser = ArgumentParser(prog="unctl")

    description = ""
    description = description + str("\n")
    description = description + str("\t  Welcome to unSkript CLI Interface \n")
    parser.description = description

    parser.add_argument(
        "-s",
        "--scan",
        help="Run a k8s scan",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--failing-only",
        help="Show only failing checks",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--diagnose",
        help="Run fixed diagnosis",
        action="store_true",
    )
    parser.add_argument(
        "-e",
        "--explain",
        help="Explain failures using AI",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--remediate",
        help="Create remediation plan",
        action="store_true",
    )
    parser.add_argument(
        "--no-interactive",
        default=False,
        help="Interactive mode is not allowed. Prompts will be skipped",
    )
    parser.add_argument(
        "--sort-by",
        choices=["object", "check"],
        default="object",
        help="Sort results by 'object' (default) or 'check'",
    ),
    parser.add_argument(
        "-c",
        "--checks",
        help="Filter checks by IDs",
        nargs="+",
    )
    parser.add_argument(
        "--categories",
        help="Filter checks by category",
        nargs="+",
        default=None,
    ),
    parser.add_argument(
        "--services",
        help="Filter checks by services",
        nargs="+",
        default=None,
    )
    parser.add_argument(
        "-l",
        "--list-checks",
        help="List available checks",
        action="store_true",
    )
    parser.add_argument(
        "--list-categories",
        help="List available categories",
        action="store_true",
    )
    parser.add_argument(
        "--list-services",
        help="List available services",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=current(),
    )
    parser.add_argument(
        "--config",
        help="Specify path to the unctl config file",
        nargs="+",
        default=None,
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return args


def prompt_interactive(options, app: App):
    if not options.no_interactive:
        choice = input("Do You want enter interactive mode to continue? (Y/n)\n> ")
        if choice != "n":
            app.run()


def unctl():
    # check version and notify if new version released
    check()

    options = unctl_process_args()
    # TODO: merge app_config and options. Options should have higher priority
    app_config = load_config(options.config)

    llm_helper: LanguageModel = None
    if options.explain or options.remediate:
        try:
            llm_helper = OpenAIAssistant()
        except Exception as e:
            sys.exit("Failed to initialize LLM: " + str(e))

    Display.init(options)

    if options.list_checks:
        checks_metadata = load_checks(
            provider="k8s",
            categories=options.categories,
            services=options.services,
            checks=options.checks,
        )
        Display.display_list_checks_table(checks_metadata)
        sys.exit()

    if options.list_categories:
        categories = get_categories(provider="k8s")
        Display.display_grouped_data("Category", categories)
        sys.exit()

    if options.list_services:
        services = get_services(provider="k8s")
        Display.display_grouped_data("Service", services)
        sys.exit()

    # Load the checks to be run
    loader = ChecksLoader()
    check_modules = loader.load_all(
        provider="k8s",
        categories=options.categories,
        services=options.services,
        checks=options.checks,
    )

    # Create a job definition
    job_definer = JobDefinition(check_modules)
    jobs = job_definer.generate_jobs()
    print("✅ Created jobs")

    # collect inventory
    collector = KubernetesDataCollector()
    print("✅ Collected Kubernetes data")

    # Run the checks
    app = ResourceChecker(
        collector=collector, checks=jobs, llm=llm_helper, provider=CheckProviders.K8S
    )
    interactive_app = InteractiveApp(
        app_config=app_config,
        provider=CheckProviders.K8S,  # TODO: get from options
        checker=app,
    )

    results = asyncio.run(app.execute())

    if not options.explain and not options.remediate:
        # explanations not needed: print and exit
        Display.display_results_table(results, sort_by=options.sort_by)
        prompt_interactive(options=options, app=interactive_app)
        return

    if len(app.failing_reports) > LLM_ANALYSIS_THRESHOLD:
        choice = input(
            f"unctl found {len(app.failing_reports)} failed items in your system. "
            "It will start sessions at LLM service for each of the item. "
            "Do You still want to use LLM to explain all the failures? (Y/n)\n> "
        )
        if choice == "n":
            Display.display_results_table(results, sort_by=options.sort_by)
            prompt_interactive(options=options, app=interactive_app)
            return

    # for each failure, print out the summary
    # and the recommendations
    print("\n\n🤔 Running diagnostic commands...\n")
    asyncio.run(app.diagnose())
    print("🤔 Analyzing results...\n")
    asyncio.run(app.analyze_results())

    Display.display_results_table(results, llm_summary=True, sort_by=options.sort_by)

    if not options.remediate:
        prompt_interactive(options=options, app=interactive_app)
        return

    if options.remediate:
        asyncio.run(app.find_dependencies())
        RemediationApp(
            app_config=app_config,
            provider=CheckProviders.K8S,  # TODO: get from options
            checker=app,
        ).run()

        return


if __name__ == "__main__":
    sys.exit(unctl())
