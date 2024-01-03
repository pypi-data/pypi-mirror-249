import os
import json
import requests

from PIL import Image
from pysaucenao import SauceNao


sauce = SauceNao(api_key='6c2e6af3fa0b1b76971067efb5ab633c5c3ec2bf', priority=[5, 9, 25, 29, 38])


async def upload_image_imgbb(image):
    API = '5b622e78b088020f1f28ffbc0a12d540'

    url = 'https://api.imgbb.com/1/upload'
    params = {
        'expiration': 300,
        'key': API
    }
    files = {
        'image': image
    }

    response = requests.post(url, params=params, files=files)

    data = response.text
    parsed_data = json.loads(data)
    url_value = parsed_data["data"]["url"]
    return url_value


async def compress_image(image):
    with open(image, 'rb') as f:
        img = Image.open(f)
        
        # Convert to RGB mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        compressed_image_path = os.path.splitext(image)[0] + '_compressed.jpg'
        img.save(compressed_image_path, format='JPEG', quality=5)

        with open(compressed_image_path, 'rb') as f:
            return await upload_image_imgbb(f)


async def reverse_image_search():
    results = await sauce.from_url(compress_image('image.jpg'))

    for result in results:
        print(result.similarity )    # 96.07
        print(result.index      )    # Pixiv
        print(result.thumbnail  )    # Returns a temporary signed URL; not suitable for permanent hotlinking
        print(result.title      )    # なでなでするにゃ
        print(result.author_name)    # おーじ茶＠3日目I-03b
        print(result.author_url )    # https://www.pixiv.net/member.php?id=122233
        print(result.url        )    # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=66106354
        print(result.source_url )    # Same as url for Pixiv results, but returns the linked original source URL for Booru entries

