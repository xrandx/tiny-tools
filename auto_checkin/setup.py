import sys
from cx_Freeze import setup, Executable
import requests
import os
from multiprocessing import Queue
import time
from requests.packages import urllib3


build_exe_options = {
    "includes":
        [
        'os',
        'requests', 
        'json',
        'queue',
        'urllib3',
        'time'
        ]
    }

base = None

executable = Executable(r"auto_checkin.py", base=base, icon = "auto_checkin.ico")

setup(
        name = "auto_checkin",
        version = "0.3",
        description = "blue.fun Check in",
        options = {'build_exe': build_exe_options},
        executables = [executable],
        author = "kevtyle",
    )