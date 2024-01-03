import asyncio
import json
from abc import abstractmethod
from collections import OrderedDict
import subprocess
from tempfile import NamedTemporaryFile
from typing import Literal

from dataclasses import dataclass, field
from re import findall

from pydantic import ValidationError

from unctl.lib.llm.base import LLMExceededMessageLengthError, LanguageModel, LLMAPIError
from unctl.lib.llm.session import LLMSessionKeeper
from unctl.lib.models.checks import CheckMetadataModel
from unctl.lib.models.recommendations import LLMRecommendation


@dataclass
class CheckReport:
    """Contains the Check's finding information."""

    check_metadata: CheckMetadataModel

    _recommendation: LLMRecommendation | None = None
    _session_keeper: LLMSessionKeeper | None = None

    status: Literal["PASS", "FAIL"] | None = None
    status_extended: str = ""
    module: str = ""

    _executed_cmd: OrderedDict[str, str] = field(default_factory=OrderedDict)

    def __init__(self, metadata):
        self.check_metadata = CheckMetadataModel.model_validate_json(metadata)
        self._executed_cmd = OrderedDict()

    def _fill_tmpl_cmd(self, cmd: str):
        # TODO: switch to proper template tool
        for p in _find_substrings(cmd):
            if getattr(self, p) is None or len(getattr(self, p)) == 0:
                print(f"Error: {p} is None for {self.object_id}")
                break
            cmd = cmd.replace("{{" + p + "}}", self.__dict__[p])

        if len(_find_substrings(cmd)) != 0:
            print(f"Error: {cmd} has unresolved parameters for {self.object_id}")
            return None

        return cmd

    async def init_llm_session(self, llm: LanguageModel):
        """Initializes AI LLM component"""
        self._session_keeper = LLMSessionKeeper(llm=llm)
        await self._session_keeper.init_session(data=self.cmd_output_messages)

    async def execute_commands(self, cmds: list[str]):
        """Execute commands"""
        result = OrderedDict()

        for cmd in cmds:
            if cmd == "":
                continue

            # when commands coming from LLM or user it can contain
            # mixed quotation and making subprocess to fail,
            # writing it into script file will solve the problem
            cli_output = await _exec_wrapped_bash_cmd(cmd=cmd)
            self._executed_cmd[cmd] = cli_output
            result[cmd] = cli_output

        return result

    async def execute_diagnostics(self):
        """Execute check and builtin diagnostics commands"""
        if self.check_cmd is not None:
            self._executed_cmd[self.check_cmd] = await _exec_cmd(self.check_cmd)

        for diagnostic_cmd in self.diagnostics_cmds:
            self._executed_cmd[diagnostic_cmd] = await _exec_cmd(diagnostic_cmd)

    async def send_to_llm(self, outputs: OrderedDict[str, str]):
        if self.is_llm_disabled:
            return

        errors = OrderedDict()

        for cmd, output in outputs.items():
            # sending data to LLM may fail,
            # but we still want to return output and error
            try:
                await self._session_keeper.push_info(
                    f"After command {cmd} got output: {output}"
                )
            except LLMAPIError as e:
                errors[cmd] = e.message
            except LLMExceededMessageLengthError:
                errors[cmd] = (
                    "Output is above maximum length.\n"
                    "Please update command to make output shorter "
                    "or reduce it manually."
                )

        return errors

    async def log_recommendation(self, failed_objects: list[str]):
        name = self.unique_name
        status = self.status_extended
        check_name = self.check_metadata.CheckTitle

        print(f"\n❌ Failed {check_name}: {name} ({status})")
        if self._recommendation is None:
            print(f"🤯 LLM failed to analyze {name} check {check_name}")
            return

        diags = "> " + "\n> ".join(self.diagnosis_options)
        print(f"💬  Summary:\n{self.llm_summary.rstrip()}")
        print(f"🛠️  Diagnostics: \n{diags}")

        fix_steps = self.fix_options
        fix = "> " + "\n> ".join(fix_steps)
        print(f"🛠️  Remediation: \n{fix}")

        related_failining_objects = [
            item
            for item in self.related_objects
            if item in failed_objects and item != name
        ]

        if len(related_failining_objects) > 0:
            print(
                f"⚙️ Related objects: {json.dumps(related_failining_objects, indent=2)}"
            )

    async def get_next_steps(self, message: str | None = None):
        """Get set of commands to diagnose and fix problems"""
        if self._session_keeper is None:
            return self._recommendation

        try:
            recommendation = await self._session_keeper.request_llm_recommendation(
                message=message
            )

            try:
                self._recommendation = LLMRecommendation.model_validate_json(
                    recommendation
                )
            except ValidationError:
                return LLMRecommendation(
                    summary=f"Failed to parse openai response. {recommendation}"
                )

            return self._recommendation
        except LLMAPIError as e:
            return LLMRecommendation(summary=e.message)

    @property
    def check_cmd(self):
        return self._fill_tmpl_cmd(self.check_metadata.Cli)

    @property
    def diagnostics_cmds(self) -> list[str]:
        diagnostics_cmds = []
        for cmd in self.check_metadata.DiagnosticClis:
            diagnostic_cmd = self._fill_tmpl_cmd(cmd)
            if diagnostic_cmd is not None:
                diagnostics_cmds.append(diagnostic_cmd)

        return diagnostics_cmds

    @property
    def cmd_output_messages(self):
        messages: list[str] = []
        for cmd, output in self._executed_cmd.items():
            messages.append(
                f"""After running command "{cmd}" got output:
                    {output}"""
            )

        return messages

    @property
    def fix_options(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.fixes or []

    @property
    def related_objects(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.objects or []

    @property
    def diagnosis_options(self) -> list[str]:
        if self._recommendation is None:
            return []

        return self._recommendation.diagnostics or []

    @property
    def llm_summary(self) -> str:
        if self._recommendation is None:
            return "LLM is disabled."

        return self._recommendation.summary or "Analysis empty or hasn't been made"

    @property
    def passed(self):
        return self.status == "PASS"

    @property
    def is_llm_disabled(self):
        return self._recommendation is None

    @property
    @abstractmethod
    def display_object(self) -> str:
        """Returns object to display"""

    @property
    @abstractmethod
    def display_row(self) -> list[str]:
        """Returns row to display"""

    @property
    @abstractmethod
    def object_id(self) -> str:
        """Returns identifier of failed object"""

    @property
    @abstractmethod
    def object_name(self) -> str:
        """Returns name of failed object"""

    @property
    @abstractmethod
    def unique_name(self) -> str:
        """Returns unique name of failed object"""


async def _exec_wrapped_bash_cmd(cmd: str):
    with NamedTemporaryFile(mode="w+t") as script:
        script.write("#!/bin/bash\n")
        script.write(cmd)
        script.flush()
        return await _exec_cmd(f"bash {script.name}")


async def _exec_cmd(cmd: str):
    if cmd == "":
        return

    command = cmd.split()

    proc = await asyncio.create_subprocess_exec(
        *command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    stdout, stderr = await proc.communicate()

    if stderr:
        decoded_stderr = stderr.decode("utf-8")
        print(f"Error(executing command({cmd}) stderr: {decoded_stderr}")
        return f"stderr: {decoded_stderr}"

    return stdout.decode("utf-8")


def _find_substrings(input_str) -> list[str]:
    # Regular expression pattern for matching substrings within double curly braces
    pattern = r"\{\{([^}]+)\}\}"
    matches = findall(pattern, input_str)
    return matches if len(matches) > 0 else []
