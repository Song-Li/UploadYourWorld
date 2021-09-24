#!/usr/bin/env python3
import sys

import src.commands as commands
from nubia import Nubia, Options
from src.uyw import UploadYourWorld

if __name__ == "__main__":
    shell = Nubia(
        name="UploadYourWorld",
        command_pkgs=commands,
        options=Options(
            persistent_history=False, auto_execute_single_suggestions=False
        ),
    )
    sys.exit(shell.run())
