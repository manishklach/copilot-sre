from __future__ import annotations

import shutil
import subprocess


def run_copilot(prompt: str) -> tuple[int, str]:
    executable = shutil.which("copilot")
    if executable is None:
        return 1, "Copilot CLI was not found on PATH. Install it or run without --run-copilot."

    completed = subprocess.run(
        [executable, "-p", prompt],
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout.strip() or completed.stderr.strip()
    return completed.returncode, output
