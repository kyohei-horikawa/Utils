import sys
import subprocess

url = 'https://www.google.com/search?q='
for i, word in enumerate(sys.argv):
    if i != 0:
        if i == 1:
            url += word
        else:
            url += '+'+word


subprocess.call(['open', url])
