import fire
import os
import requests
import re
import subprocess
from distutils.util import strtobool

token = os.environ['QIITA_TOKEN']


def post(file):
    url = 'https://qiita.com/api/v2/items'
    pattern = re.compile('(.*)=(.*)')
    path = os.getcwd()
    item = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        header = lines[0:7]
        lines.append('\n'+'**'+path + '/'+file+'**')
        body = ''.join(lines[8:len(lines)])

        # タグ情報をパース
        for line in header:
            result = pattern.match(line)
            if result:
                if result.group(1) == 'tags':
                    item['tags'] = []
                    for tag in result.group(2).split(','):
                        item['tags'].append({'name': tag})
                elif result.group(1) == "private" or result.group(1) == "tweet":
                    if strtobool(result.group(2)):
                        item[result.group(1)] = True
                    else:
                        item[result.group(1)] = False
                else:
                    item[result.group(1)] = result.group(2)
        item['body'] = body

    headers = {'Authorization': 'Bearer {}'.format(token)}

    # タグにidがあれば，patchで記事を更新
    # なければ，postで新規投稿
    if item['id']:
        url = url+'/'+item['id']
        res = requests.patch(url, headers=headers, json=item)
    else:
        res = requests.post(url, headers=headers, json=item)
        # タグを更新
        write_tag(file, res.json()['id'])
    print((res.json()['url']))


def write_tag(file, id):
    with open(file, 'r') as f:
        lines = f.readlines()
    lines[5] = 'id='+str(id)+'\n'

    with open(file, 'w') as f:
        f.writelines(lines)


def template(file_name):
    with open(file_name+'.md', "w") as f:
        templates = """@@@
title=タイトル
private=true
tags=tag1,tag2
tweet=false
id=
@@@
"""
        f.write(templates)
        subprocess.call(['code', file_name+'.md'])


def show():
    print()


if __name__ == '__main__':
    fire.Fire({
        'post': post,
        'template': template,
        'show': show,
        'test': write_tag
    })
