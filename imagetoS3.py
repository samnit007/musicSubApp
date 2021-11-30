import requests
import io
import boto3
from boto3.dynamodb.conditions import Key


def query_image(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')
    response = table.scan()
    return response['Items']


def upload_images():

    images_list = query_image()

    for image_url in images_list:

        url = image_url['img_url']
        image_name = url.split('/')[-1]

        try:
            s3_client = boto3.client('s3')
            response = requests.get(url)
            image = io.BytesIO(response.content)
            s3_client.upload_fileobj(image, 's3musicbucket', image_name)

        except Exception as e:
            print(f'Error in file upload {e}')


if __name__ == '__main__':

    upload_images()
