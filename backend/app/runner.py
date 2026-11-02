"""Runs learner code by calling the `runner` service (a .NET 10 SDK container)."""
import os

import httpx

RUNNER_URL = os.getenv("RUNNER_URL", "http://runner:8080")


class RunnerUnavailable(Exception):
    pass


def run_code(code: str) -> tuple[bool, str]:
    """Compile and run `code`. Returns (ran without errors, compiler errors or program output)."""
    if not code.strip():
        return False, "Write some code in the editor, then click Run."
    try:
        res = httpx.post(f"{RUNNER_URL}/run", json={"code": code}, timeout=90)
        res.raise_for_status()
    except httpx.HTTPError as e:
        raise RunnerUnavailable(str(e)) from e
    body = res.json()
    return body["ok"], body["output"] or "(no output)"


def run_cli(session: str, command: str) -> tuple[bool, str, str]:
    """Run one terminal line in the learner's sandbox workspace. Returns (ok, output, prompt path)."""
    try:
        res = httpx.post(f"{RUNNER_URL}/cli", json={"session": session, "command": command}, timeout=120)
        res.raise_for_status()
    except httpx.HTTPError as e:
        raise RunnerUnavailable(str(e)) from e
    body = res.json()
    return body["ok"], body["output"], body["cwd"]


def _lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.strip().splitlines()]


def check_lab(code: str, spec: dict) -> tuple[bool, str]:
    """A lab passes when the program compiles, exits cleanly and prints the expected output."""
    ran, output = run_code(code)
    if not ran:
        return False, output
    expected = spec["expected_output"]
    if _lines(output) == _lines(expected):
        return True, output
    return False, f"✗ Output doesn't match.\n\nExpected:\n{expected}\n\nGot:\n{output}"
