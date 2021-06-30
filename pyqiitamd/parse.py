import re
import os
from image import image_parse


def parse(file):

    image_parse(file)

    s = ''

    with open('image.md', 'r') as f:
        s = f.read()

    pattern = re.compile(
        r'@@@\n([\s\S]*?)\n@@@\n(.*)', re.MULTILINE | re.DOTALL)
    path = os.getcwd()

    res = pattern.findall(s)[0]
    header = res[0]
    body = res[1]
    body += f'\n**{path}/{file}**'

    item = {}
    for line in header.split('\n'):
        pattern = re.compile('(.*)=(.*)')
        res = re.match(pattern, line)
        key = res.group(1)
        value = res.group(2)

        if key == 'tags':
            item['tags'] = []
            for tag in value.split(','):
                item['tags'].append({'name': tag})
        elif value == "true":
            item[key] = True
        elif value == "false":
            item[key] = False
        else:
            item[key] = value

    item['body'] = body

    return item
