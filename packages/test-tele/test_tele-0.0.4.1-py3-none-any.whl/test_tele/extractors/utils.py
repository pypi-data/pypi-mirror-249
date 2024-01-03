

async def clean_up_tags(query: str, modes: list = [], prefix: str = None):
    """Setting searching mode"""
    example_query = ".px sangonomiya kokomi loli no_ai no_tag safe"
    def_modes = ['no_tag']
    modes += def_modes
    current_modes = {}
    if prefix:
        query = query.strip().lower().replace(prefix, "").lstrip()
    keywords = query.split()

    for keyword in keywords:
        if keyword in modes:
            current_modes[keyword] = True
            query = query.replace(keyword, '')
        if keyword.isdigit():
            current_modes['illust_detail'] = True
        if 'no_inline' in keyword:
            current_modes['no_inline'] = True
            query = query.replace(keyword, '')
        if 'as_file' in keyword:
            if current_modes.get('no_inline'):
                current_modes['as_file'] = True
            query = query.replace(keyword, '')
        if 'limit:' in keyword:
            if current_modes.get('no_inline'):
                limit = keyword.split('limit:')[-1]
                current_modes['limit'] = limit
            query = query.replace(keyword, '')
        if 'offset:' in keyword:
            if current_modes.get('no_inline'):
                offset = keyword.split('offset:')[-1]
                current_modes['offset'] = offset
            query = query.replace(keyword, '')

    return current_modes, query.strip()