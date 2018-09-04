import sys
from cx_Freeze import setup, Executable
import requests
import os
from multiprocessing import Queue

build_exe_options = {
    "includes":
        [
        'os',
        'requests', 
        'json',
        'queue'
        ]
    }

base = None

executable = Executable(r"auto_checkin.py", base=base, icon = "auto_checkin.ico")

setup(
        name = "auto_checkin",
        version = "0.1",
        description = "blue.fun Check in",
        options = {'build_exe': build_exe_options},
        executables = [executable],
        author = "kevtyle",
    )