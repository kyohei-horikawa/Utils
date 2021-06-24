import os
import shutil
import sys
import subprocess

dir = sys.argv[-1]
paths = ['A', 'B', 'C', 'D', 'E', 'F']

os.mkdir(dir)
for path in paths:
    shutil.copyfile("./template/main.py", f"./{dir}/{path}.py")

subprocess.call(['touch', f',/{dir}/input.txt'])
