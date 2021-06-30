import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('qiita-kyohei-horikawa')

bucket.upload_file('image2.png', 'image3.png', ExtraArgs={
                   "ContentType": "image/jpeg", 'ACL': 'public-read'})
