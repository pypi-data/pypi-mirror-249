from test_tele.extractors.utils import *


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[my_dict] = []
    
    for elemen in gallery_dl_result:
        if elemen[0] == 3:
            my_dict = {}
            my_dict['img_url'] = elemen[1]
            my_dict['id_file'] = str(elemen[2]['file']['md5'])
            my_dict['id'] = str(elemen[2]['id'])
            my_dict['extension'] = elemen[2]['extension']
            my_dict['category'] = elemen[2]['category']
            my_dict['width'] = elemen[2]['file']['width']
            my_dict['height'] = elemen[2]['file']['height']
            my_dict['artist'] = await get_tags(elemen[2]['tags']['artist']) if 'artist' in elemen[2]['tags'] else "AI"
            my_dict['thumbnail'] = elemen[2]['preview']['url']
            my_dict['tags'] = await get_tags(elemen[2]['tags']['general'], 40)
            lists.append(my_dict)
    return lists


async def set_url(query: str) -> str:
    base_url = "https://e621.net/posts?tags="
    url = str(query).strip().lower().replace(".fur", "").lstrip()

    if "-ai" in url:
        url = url.replace("-ai", '')
        base_url = base_url.replace("e621.net", "e6ai.net")

    # Default = my little pony
    url = "my_little_pony+-penis" if url == "" else url.replace(" ", '+')
    return f"{base_url}{url}"


async def get_fur_file(callb_query:str):
    website, file_name = callb_query.split(",")
    modified_string = "{}/{}/{}".format(file_name[:2], file_name[2:4], file_name)
    return f"https://static1.{website}.net/data/{modified_string}"

