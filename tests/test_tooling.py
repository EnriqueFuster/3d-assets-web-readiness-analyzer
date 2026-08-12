import subprocess
from pathlib import Path

import pytest

from web_readiness_analyzer.errors import ToolExecutionError, ToolTimeoutError
from web_readiness_analyzer.tooling import run_validator


def test_maps_tool_timeout_to_domain_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def time_out(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

    monkeypatch.setattr(
        "web_readiness_analyzer.tooling.subprocess.run",
        time_out,
    )

    with pytest.raises(ToolTimeoutError, match="120-second limit"):
        run_validator(tmp_path / "input.glb", tmp_path / "report.json")


def test_maps_unsuccessful_tool_result_to_domain_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Result:
        returncode = 2
        stdout = ""
        stderr = "invalid asset"

    monkeypatch.setattr(
        "web_readiness_analyzer.tooling.subprocess.run",
        lambda *args, **kwargs: Result(),
    )

    with pytest.raises(
        ToolExecutionError,
        match="validate-glb.mjs failed with exit code 2: invalid asset",
    ):
        run_validator(tmp_path / "input.glb", tmp_path / "report.json")
