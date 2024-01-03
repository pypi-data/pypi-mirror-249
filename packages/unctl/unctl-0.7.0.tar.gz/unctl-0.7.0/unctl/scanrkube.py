import rich
import asyncio
from kubernetes_asyncio import client, config

from kubernetes_asyncio.client import (
    AppsV1Api,
    AutoscalingV1Api,
    NetworkingV1Api,
    BatchV1Api,
    StorageV1Api,
)

from kubernetes_asyncio.client.rest import ApiException
from kubernetes_asyncio.client.api_client import ApiClient
from pydantic import ValidationError

from unctl.lib.checks.check_report import CheckReport
from unctl.lib.checks.check import Check
from unctl.lib.display import Display
from unctl.lib.llm.base import LanguageModel
from unctl.lib.llm.instructions import GROUP, INSTRUCTIONS
from unctl.lib.llm.session import LLMSessionKeeper
from unctl.lib.models.recommendations import GroupLLMRecommendation
from unctl.lib.models.remediations import FailureGroup


# Data Collection Module


class DataCollector:
    async def fetch_data(self):
        raise NotImplementedError


class KubernetesData:
    # keep parameters sorted alphabetically to avoid merge conflicts
    def __init__(
        self,
        configmaps,
        cronjobs,
        daemonsets,
        deployments,
        endpoints,
        hpas,
        ingress_classes,
        ingresses,
        nodes,
        pods,
        network_policies,
        pvcs,
        replicationControllers,
        replicaSets,
        secrets,
        services,
        statefulsets,
        storageClasses,
    ):
        self._configmaps = configmaps
        self._cronjobs = cronjobs
        self._daemonsets = daemonsets
        self._deployments = deployments
        self._endpoints = endpoints
        self._hpas = hpas
        self._ingress_classes = ingress_classes
        self._ingresses = ingresses
        self._nodes = nodes
        self._pods = pods
        self._network_policies = network_policies
        self._pvcs = pvcs
        self._replicationControllers = replicationControllers
        self._replicaSets = replicaSets
        self._secrets = secrets
        self._services = services
        self._statefulsets = statefulsets
        self._storageClasses = storageClasses

    def get_configmaps(self):
        return self._configmaps

    def get_cronjobs(self):
        return self._cronjobs

    def get_daemonsets(self):
        return self._daemonsets

    def get_deployments(self):
        return self._deployments

    def get_endpoints(self):
        return self._endpoints

    def get_hpas(self):
        return self._hpas

    def get_ingress_classes(self):
        return self._ingress_classes

    def get_ingresses(self):
        return self._ingresses

    def get_nodes(self):
        return self._nodes

    def get_pods(self):
        return self._pods

    def get_network_policies(self):
        return self._network_policies

    def get_pvcs(self):
        return self._pvcs

    def get_replication_controllers(self):
        return self._replicationControllers

    def get_replica_sets(self):
        return self._replicaSets

    def get_secrets(self):
        return self._secrets

    def get_services(self):
        return self._services

    def get_statefulsets(self):
        return self._statefulsets

    def get_storage_classes(self):
        return self._storageClasses


class KubernetesDataCollector(DataCollector):
    async def fetch_data(self):
        async def _fetch_items(awaitable):
            return (await awaitable).items

        # Load kube config
        await config.load_kube_config()

        try:
            async with ApiClient() as api:
                # Get an instance of the API class
                v1 = client.CoreV1Api(api)
                v1apps = AppsV1Api(api)
                v1autoscaling = AutoscalingV1Api(api)
                v1networking = NetworkingV1Api(api)
                v1storage = StorageV1Api(api)
                v1batch = BatchV1Api(api)

                hpas = _fetch_items(
                    v1autoscaling.list_horizontal_pod_autoscaler_for_all_namespaces()
                )
                tasks = {
                    "configmaps": _fetch_items(v1.list_config_map_for_all_namespaces()),
                    "cronjobs": _fetch_items(
                        v1batch.list_cron_job_for_all_namespaces()
                    ),
                    "daemonsets": _fetch_items(
                        v1apps.list_daemon_set_for_all_namespaces()
                    ),
                    "deployments": _fetch_items(
                        v1apps.list_deployment_for_all_namespaces()
                    ),
                    "endpoints": _fetch_items(v1.list_endpoints_for_all_namespaces()),
                    "hpas": hpas,
                    "ingress_classes": _fetch_items(v1networking.list_ingress_class()),
                    "ingresses": _fetch_items(
                        v1networking.list_ingress_for_all_namespaces()
                    ),
                    "network_policies": _fetch_items(
                        v1networking.list_network_policy_for_all_namespaces()
                    ),
                    "nodes": _fetch_items(v1.list_node(watch=False)),
                    "pods": _fetch_items(v1.list_pod_for_all_namespaces()),
                    "pvcs": _fetch_items(
                        v1.list_persistent_volume_claim_for_all_namespaces()
                    ),
                    "replicationControllers": _fetch_items(
                        v1.list_replication_controller_for_all_namespaces()
                    ),
                    "replicaSets": _fetch_items(
                        v1apps.list_replica_set_for_all_namespaces()
                    ),
                    "secrets": _fetch_items(v1.list_secret_for_all_namespaces()),
                    "services": _fetch_items(v1.list_service_for_all_namespaces()),
                    "statefulsets": _fetch_items(
                        v1apps.list_stateful_set_for_all_namespaces()
                    ),
                    "storageClasses": _fetch_items(v1storage.list_storage_class()),
                }
                results = dict(zip(tasks, await asyncio.gather(*tasks.values())))
                return KubernetesData(**results)

        except ApiException as api_exception:
            # Handle exceptions raised by Kubernetes API interactions
            print(f"An error occurred with the Kubernetes API: {api_exception.reason}")
            # print(api_exception.body)
            return None

        except Exception as general_exception:
            # A generic handler for all other exceptions
            print(f"An unexpected error occurred: {general_exception}")
            return None


# Main Application


class ResourceChecker:
    _check_reports: dict[str, list[CheckReport]]
    _failure_groups: list[FailureGroup]

    def __init__(
        self,
        collector: DataCollector,
        checks: list[Check],
        llm: LanguageModel,
        provider: str,
    ):
        self._check_reports = {}
        self._failure_groups = []
        self._llm = llm
        self._collector = collector
        self._checks = checks
        self._provider = provider
        self._check_reports = {}

    async def execute(self):
        data = await self._collector.fetch_data()
        if data is None:
            print("Failed to collect inventory")
            exit(1)

        total_checks = len(self._checks)
        completed_checks = 0

        # Display the progress bar header
        Display.display_progress_bar_header()

        for check in self._checks:
            if check.Enabled is False:
                continue

            check_reports = check.execute(data)

            self._check_reports[check.__class__.__name__] = check_reports
            completed_checks += 1
            Display.display_progress_bar(
                completed_checks / total_checks, check.CheckTitle
            )

            print()  # New line after the progress bar completion

        return self._check_reports

    async def diagnose(self):
        # TODO: could use concurrency here
        for check, reports in self._check_reports.items():
            for report in reports:
                if not report.passed:
                    await report.execute_diagnostics()

    async def analyze_results(self):
        batch_size = 10
        failing_items = self.failing_reports
        total_tasks = len(failing_items)
        for batch_start in range(0, total_tasks, batch_size):
            batch_end = min(batch_start + batch_size, total_tasks)
            tasks = [
                self._analyze_result(report=failed_item)
                for failed_item in failing_items[batch_start:batch_end]
            ]
            await asyncio.gather(*tasks)

    async def _analyze_result(self, report: CheckReport):
        # start an assisted troubleshooting session
        await report.init_llm_session(llm=self._llm)
        await report.get_next_steps()
        await report.log_recommendation(self.failing_objects)

        return report

    def _find_related_group(self, related_objects: list[str]):
        for group in self._failure_groups:
            for object in related_objects:
                if group.contains_object(object):
                    return group

    async def _append_to_existing_group(
        self,
        failure_report: CheckReport,
        group: FailureGroup,
        recommendation: GroupLLMRecommendation,
        related_reports: list[CheckReport],
    ):
        for related in related_reports:
            not_in_group = not group.contains_object(related.unique_name)

            if related.unique_name != failure_report.unique_name or not_in_group:
                for output in related.cmd_output_messages:
                    await group.session.push_info(output)

            if not_in_group:
                group.objects.append(related)
                print(f"\t❌ Added <{related.object_name}> to group <{group.title}>")

        recommendation = await self._request_group_recommendation(
            message=(
                "Provide complete analysis on provided data for all related objects.\n"
                "Figure out possible root cause.\n"
                "Sort object list from root causes to downstream failures."
            ),
            session=group.session,
        )

        if recommendation is None:
            return

        related_reports = group.objects.copy()

        related_reports = sorted(
            related_reports,
            key=lambda report: group.objects.index(report.unique_name)
            if report.unique_name in group.objects
            else float("inf"),
        )

        if group.title != recommendation.title:
            rich.print(
                f"\t⏩ Updated group context <{group.title}> ➱ "
                f"<{recommendation.title}>\n"
                f"\t[bold yellow]Summary:[/bold yellow] {group.summary}\n"
            )

        group.title = recommendation.title
        group.summary = recommendation.summary
        group.objects = related_reports

    async def _create_new_group(
        self,
        failure_report: CheckReport,
        session: LLMSessionKeeper,
        recommendation: GroupLLMRecommendation,
        related_reports: list[CheckReport],
    ):
        for related in related_reports:
            if related.unique_name != failure_report.unique_name:
                for output in related.cmd_output_messages:
                    await session.push_info(output)

        # request additional analysis only if found more that 1 object related to issue
        if len(related_reports) > 1:
            recommendation = await self._request_group_recommendation(
                message=(
                    "Provide complete analysis on provided data "
                    "for all related objects.\n"
                    "Figure out possible root cause.\n"
                    "Sort object list from root causes to downstream failures."
                ),
                session=session,
            )

            if recommendation is None:
                return

        self._failure_groups.append(
            FailureGroup(
                id=(
                    f"{failure_report.unique_name}"
                    f"-{failure_report.check_metadata.CheckID}"
                ),
                title=recommendation.title,
                summary=recommendation.summary,
                objects=related_reports,
                session=session,
            )
        )

        rich.print(
            f"❌ Created group for check <{failure_report.check_metadata.CheckTitle}> "
            f"and object <{failure_report.object_name}>\n"
            f"[bold yellow]Title:[/bold yellow] {recommendation.title}\n"
            f"[bold yellow]Summary:[/bold yellow] {recommendation.summary}\n"
            f"[bold yellow]Objects:[/bold yellow] {', '.join(recommendation.objects)}\n"
        )

    async def _find_report_deps(
        self, failure_report: CheckReport, failing_reports: list[CheckReport]
    ):
        session = LLMSessionKeeper(llm=self._llm)
        await session.init_session(data=failure_report.cmd_output_messages)

        group = await self._request_group_recommendation(
            message=(
                "Identify possible related objects only from "
                f"the pool: {', '.join(self.failing_objects)}.\n"
                "Related objects may be mentioned (even if partially) "
                "in the logs, error events, etc "
                f"and which may be possibly impacted by {failure_report.unique_name}"
            ),
            session=session,
        )

        related_reports = [
            report for report in failing_reports if report.unique_name in group.objects
        ]

        existing_group = self._find_related_group(related_objects=group.objects)
        if existing_group is not None:
            session = existing_group.session

        if existing_group is not None:
            await self._append_to_existing_group(
                failure_report=failure_report,
                group=existing_group,
                recommendation=group,
                related_reports=related_reports,
            )
        else:
            await self._create_new_group(
                failure_report=failure_report,
                session=session,
                recommendation=group,
                related_reports=related_reports,
            )

        return related_reports

    async def find_dependencies(self):
        print("🔀 Looking for dependencies between failures...\n")

        leftovers = self.failing_objects.copy()
        failing_reports = self.failing_reports.copy()

        for failure_report in failing_reports:
            if failure_report.unique_name not in leftovers:
                continue

            related_reports = await self._find_report_deps(
                failure_report=failure_report, failing_reports=failing_reports
            )

            for related in related_reports:
                if related.unique_name in leftovers:
                    leftovers.remove(related.unique_name)

    async def _request_group_recommendation(
        self, message: str, session: LLMSessionKeeper
    ):
        try:
            recommendation = await session.request_llm_recommendation(
                message=message,
                instructions=INSTRUCTIONS[self._provider][GROUP],
                polling_timeout=1,
            )

            return GroupLLMRecommendation.model_validate_json(recommendation)
        except ValidationError:
            print(f"Failed to parse group recommendation for {id}")

    @property
    def failing_reports(self) -> list[CheckReport]:
        failing = []
        for check_list in self._check_reports.values():
            failing.extend(item for item in check_list if not item.passed)

        return failing

    @property
    def failing_objects(self):
        items = self.failing_reports
        objects = list(set(item.unique_name for item in items))
        return objects

    @property
    def reports(self):
        return self._check_reports

    @property
    def failure_groups(self):
        groups = [item for item in self._failure_groups if item.failed_count > 1]
        other = [
            item.objects[0] for item in self._failure_groups if item.failed_count == 1
        ]
        sorted_groups = sorted(groups, key=lambda item: item.failed_count, reverse=True)

        sorted_groups.append(
            FailureGroup(
                id="other",
                title="Other",
                summary=(
                    "This group contains all the failures which "
                    "are not related to any other problem."
                ),
                objects=other,
                session=None,
            )
        )

        return sorted_groups


class JobDefinition:
    def __init__(self, check_modules):
        self.check_modules = check_modules

    def generate_jobs(self, suite_name=None):
        # TBD: this list should be generated based on the JSON file
        # Loads checks related to the suite specified
        # suite_path = os.path.join(self.checks_dir, suite_name)
        check_modules = self.check_modules

        jobs: list[Check] = []
        for module in check_modules:
            # Load only the checks
            if len(module.__package__.split(".")) < 4:
                continue

            # Extract class name from the module's file name
            class_name = module.__package__.split(".")[-1]

            # Instantiate the class named after the module
            check_class = getattr(module, class_name)

            # load the class
            check_instance = check_class()

            # Ensure that the execute method exists in the check class
            if hasattr(check_instance, "execute"):
                jobs.append(check_instance)

        return jobs
