import re
import boto3
import os

pattern = '.*@image:(.*)'
s3 = boto3.resource('s3')
bucket = s3.Bucket(os.environ['QIITA_S3_BUCKET'])
region = os.environ['QIITA_S3_REGION']
client = boto3.client('s3')


def image_parse(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        res = re.match(pattern, line)
        if res:
            image_path = res.group(1)
            base_name = image_path.split('/')[-1]
            lines[i] = '![](' + image_upload(image_path, base_name) + ')'

    with open(file, 'w') as f:
        f.writelines(lines)


def image_upload(image_path, base_name):
    bucket.upload_file(image_path, base_name, ExtraArgs={
        "ContentType": "image/jpeg", 'ACL': 'public-read'})
    return f"https://{os.environ['QIITA_S3_BUCKET']}.s3.{region}.amazonaws.com/{base_name}"


image_parse('image.md')
