import os, subprocess
from subprocess import Popen, PIPE

from gitSecureFileReader import GitSecureFileReader


session = subprocess.Popen(['sh', './gitSearch.sh'], stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()
# print(stdout)
# print("File location using os.getcwd():", os.getcwd())

if stderr:
    print(13, stderr)
    raise Exception("Error "+str(stderr))
else:
    output = stdout.decode().split('\n')
    if len(output) > 3:
        last_outputs = output[:-2]
        files_changes = []
        current_dir = os.getcwd()
        for last_output in last_outputs:
            last_output = last_output.split('|')[0].replace(' ', '')
            gcfr = GitSecureFileReader(f'{current_dir}/{last_output}')
            gcfr.detect_secret_keys()