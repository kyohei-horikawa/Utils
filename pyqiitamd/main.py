import fire
import os
import requests
import re
import subprocess
from distutils.util import strtobool

token = os.environ['QIITA_TOKEN']
editor = os.environ['QIITA_EDITOR']


def post(file):
    url = 'https://qiita.com/api/v2/items'
    headers = {'Authorization': 'Bearer {}'.format(token)}

    item = parse(file)

    # タグにidがあれば，patchで記事を更新
    # なければ，postで新規投稿
    if item['id']:
        url = url+'/'+item['id']
        res = requests.patch(url, headers=headers, json=item)
    else:
        res = requests.post(url, headers=headers, json=item)
        # タグを更新
        write_id(file, res.json()['id'])
    print(res.json()['url'])
    subprocess.call(['open', res.json()['url']])


def team(file):
    url = 'https://nishitani.qiita.com/api/v2/items'
    headers = {'Authorization': 'Bearer {}'.format(token)}

    item = parse(file)

    # タグにidがあれば，patchで記事を更新
    # なければ，postで新規投稿
    if item['id']:
        url = url+'/'+item['id']
        res = requests.patch(url, headers=headers, json=item)
    else:
        res = requests.post(url, headers=headers, json=item)
        # タグを更新
        write_id(file, res.json()['id'])
    print(res.json())
    subprocess.call(['open', res.json()['url']])


def parse(file):
    pattern = re.compile('(.*)=(.*)')
    path = os.getcwd()
    item = {}
    with open(file, 'r') as f:
        lines = f.readlines()
        header = lines[0:7]  # タグは1-7行目と決めうち(要改善)
        lines.append('\n'+'**'+path + '/'+file+'**')
        body = ''.join(lines[8:len(lines)])

        # タグ情報をパース(もっと賢くやりたい，要改善)
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

        return item


def write_id(file, id):
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
    print('token:', token)
    print('editor:', editor)
    print('\n')
    print("If you haven't set your token or editor, \
you can set like this in config.fish")
    print('set -Ux QIITA_TOKEN xxxxxxxx')
    print('set -Ux QIITA_EDITOR code')


if __name__ == '__main__':
    fire.Fire({
        'post': post,
        'team': team,
        'template': template,
        'show': show,
    })
