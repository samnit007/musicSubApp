from decimal import Decimal
import json
import boto3


def load_music(songs, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb')

    table = dynamodb.Table('music')
    for song in songs['songs']:
        title = song['title']
        artist = song['artist']
        year = int(song['year'])
        web_url = song['web_url']
        img_url = song['img_url']
        print("Adding musiv:", title)
        table.put_item(Item=song)


if __name__ == '__main__':
    with open("a2.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
        load_music(music_list)
