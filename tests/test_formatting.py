# -*- coding: utf-8 -*-
import os
import sys


def test_formatting_black():
    """
    Test all python code files are Black formatted
    """
    cmd = [
        sys.executable,
        "-m",
        "black",
        "--check",
        "-v",
        # Check all files under repo root
        os.path.join(os.path.dirname(__file__), ".."),
        "--exclude",
        r"'.*\/venv\/.*'",
    ]
    exit_code = os.system(" ".join(cmd))
    assert exit_code == 0
