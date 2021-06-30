from parse import parse
import os
import requests
import subprocess
import fire

token = os.environ['QIITA_TOKEN']
editor = os.environ['QIITA_EDITOR']
team_url = os.environ['QIITA_TEAM_URL']


def post(file):
    url = 'https://qiita.com/api/v2/items'
    headers = {'Authorization': f'Bearer {token}'}

    item = parse(file)

    # タグにidがあれば，patchで記事を更新
    # なければ，postで新規投稿
    if item['id']:
        url = f"{url}/{item['id']}"
        res = requests.patch(url, headers=headers, json=item)
    else:
        res = requests.post(url, headers=headers, json=item)
        # タグを更新
        write_id(file, res.json()['id'])
    print(res.json()['url'])
    subprocess.call(['open', res.json()['url']])


def team(file):
    url = f'https://{team_url}.qiita.com/api/v2/items'
    headers = {'Authorization': f'Bearer {token}'}

    item = parse(file)

    # タグにidがあれば，patchで記事を更新
    # なければ，postで新規投稿
    if item['id']:
        url = f"{url}/{item['id']}"
        res = requests.patch(url, headers=headers, json=item)
    else:
        res = requests.post(url, headers=headers, json=item)
        # タグを更新
        write_id(file, res.json()['id'])
    print(res.json()['url'])
    subprocess.call(['open', res.json()['url']])


def write_id(file, id):
    with open(file, 'r') as f:
        lines = f.readlines()
    lines[5] = f"id={str(id)}\n"

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
    print('team_url:', team_url)
    print('\n')
    print("If you haven't set your token or editor, \
you can set like this in config.fish")
    print('set -Ux QIITA_TOKEN xxxxxxxx')
    print('set -Ux QIITA_EDITOR code')
    print('set -Ux QIITA_TEAM_URL xxxxxxxx')


if __name__ == '__main__':
    fire.Fire({
        'post': post,
        'team': team,
        'template': template,
        'show': show,
    })
