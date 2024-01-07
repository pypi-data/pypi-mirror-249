from test_tele.extractors.utils import *


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[dict] = []
    
    if gallery_dl_result:
        for elemen in gallery_dl_result:
            if elemen[0] == 6:
                my_dict = {}
                my_dict['post_url'] = elemen[1]
                my_dict['id'] = str(elemen[2]['gid'])
                my_dict['title'] = str(elemen[2]['desc']).rsplit(' ', 1)[0]
                my_dict['thumbnail'] = elemen[2]['t_url']
                my_dict['sample_img'] = elemen[2]['t_url_460']
                lists.append(my_dict)
            elif elemen[0] == 3:
                my_dict = {}
                my_dict['img_url'] = elemen[1]
                my_dict['thumbnail'] = await get_thumbnail(elemen[1])
                my_dict['sample_img'] = my_dict['thumbnail'].replace("/300/", "/460/")
                my_dict['title'] = str(elemen[2]['title'])
                my_dict['id'] = str(elemen[2]['gallery_id'])
                my_dict['slug'] = str(elemen[2]['slug'])
                my_dict['models'] = await get_tags(elemen[2]['models'])
                my_dict['tags'] = await get_tags(elemen[2]['categories'])
                my_dict['extension'] = elemen[2]['extension']
                lists.append(my_dict)
    return lists


async def get_thumbnail(image_url: str) -> str:
    # https://cdni.pornpics.com/460/7/687/69235644/69235644_009_15ef.jpg
    url = image_url.split("/1280/")[-1]
    url, ext = url.split(".")
    return f"https://cdni.pornpics.com/300/{url}.{ext}"


async def set_url(query: str) -> str:
    url = str(query).strip().lower().replace(".rp", "").lstrip()

    if 'id:' in url:
        url = url.replace('id:', '')
        return f"https://www.pornpics.com/galleries/{url}"

    url = url.replace(' ', '+')
    return f"https://www.pornpics.com/?q={url}"


async def get_pp_file(url):
    return f"https://cdni.pornpics.com/1280/{url}"

