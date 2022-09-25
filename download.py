import sys
import os
from os.path import join
import requests

cwd = sys.path[0]

if not os.path.exists(join(cwd, "Attendance-CLI")):
    attPath = join(cwd, "Attendance-CLI")
    os.mkdir(attPath)

    url = "https://raw.githubusercontent.com/JAIDHEER007/Attendance-CLI/main/{programName}.py"
    programs = ["bots", "students", "checkAttnd", "dataVisualizers"]

    for program in programs:
        response = requests.request("GET", url.format(programName = program))

        if response.status_code != 200:
            print("Couldn't Get {programName}.py".format(programName = program))
        else:
            with open(join(attPath, '{programName}.py'.format(programName = program)), 'w', encoding = "utf-8") as fileHandle:
                fileHandle.write(response.text)
            print("Successfully downloaded {programName}.py".format(programName = program))

