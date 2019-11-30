downloads_directory = "downloads"

google_search = 'https://www.google.com/search?q='

user_agent = ("Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 "
              "(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17")
user_agent_3 = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

args_list = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords",
             "limit", "format", "color", "color_type", "usage_rights", "size",
             "exact_size", "aspect_ratio", "type", "time", "time_range", "delay", "url", "single_image",
             "output_directory", "image_directory", "no_directory", "proxy", "similar_images", "specific_site",
             "print_urls", "print_size", "print_paths", "metadata", "extract_metadata", "socket_timeout",
             "thumbnail", "thumbnail_only", "language", "prefix", "chromedriver", "related_images", "safe_search",
             "no_numbering", "offset", "no_download", "save_source", "silent_mode", "ignore_urls"]

lang_param = {
    "Arabic": "lang_ar",
    "Chinese (Simplified)": "lang_zh-CN",
    "Chinese (Traditional)": "lang_zh-TW",
    "Czech": "lang_cs",
    "Danish": "lang_da",
    "Dutch": "lang_nl",
    "English": "lang_en",
    "Estonian": "lang_et",
    "Finnish": "lang_fi",
    "French": "lang_fr",
    "German": "lang_de",
    "Greek": "lang_el",
    "Hebrew": "lang_iw ",
    "Hungarian": "lang_hu",
    "Icelandic": "lang_is",
    "Italian": "lang_it",
    "Japanese": "lang_ja",
    "Korean": "lang_ko",
    "Latvian": "lang_lv",
    "Lithuanian": "lang_lt",
    "Norwegian": "lang_no",
    "Portuguese": "lang_pt",
    "Polish": "lang_pl",
    "Romanian": "lang_ro",
    "Russian": "lang_ru",
    "Spanish": "lang_es",
    "Swedish": "lang_sv",
    "Turkish": "lang_tr"
}

color_params = {
    'red': 'ic:specific,isc:red',
    'orange': 'ic:specific,isc:orange',
    'yellow': 'ic:specific,isc:yellow',
    'green': 'ic:specific,isc:green',
    'teal': 'ic:specific,isc:teel',
    'blue': 'ic:specific,isc:blue',
    'purple': 'ic:specific,isc:purple',
    'pink': 'ic:specific,isc:pink',
    'white': 'ic:specific,isc:white',
    'gray': 'ic:specific,isc:gray',
    'black': 'ic:specific,isc:black',
    'brown': 'ic:specific,isc:brown'
}

color_type_params = {
    'full-color': 'ic:color',
    'black-and-white': 'ic:gray',
    'transparent': 'ic:trans',
}

usage_rights_params = {
    'labeled-for-reuse-with-modifications': 'sur:fmc',
    'labeled-for-reuse': 'sur:fc',
    'labeled-for-noncommercial-reuse-with-modification': 'sur:fm',
    'labeled-for-nocommercial-reuse': 'sur:f',
}

size_params = {
    'large': 'isz:l',
    'medium': 'isz:m',
    'icon': 'isz:i',
    '>400*300': 'isz:lt,islt:qsvga',
    '>640*480': 'isz:lt,islt:vga',
    '>800*600': 'isz:lt,islt:svga',
    '>1024*768': 'visz:lt,islt:xga',
    '>2MP': 'isz:lt,islt:2mp',
    '>4MP': 'isz:lt,islt:4mp',
    '>6MP': 'isz:lt,islt:6mp',
    '>8MP': 'isz:lt,islt:8mp',
    '>10MP': 'isz:lt,islt:10mp',
    '>12MP': 'isz:lt,islt:12mp',
    '>15MP': 'isz:lt,islt:15mp',
    '>20MP': 'isz:lt,islt:20mp',
    '>40MP': 'isz:lt,islt:40mp',
    '>70MP': 'isz:lt,islt:70mp',
}

type_params = {
    'face': 'itp:face',
    'photo': 'itp:photo',
    'clipart': 'itp:clipart',
    'line-drawing': 'itp:lineart',
    'animated': 'itp:animated'
}

time_params = {
    'past-24-hours': 'qdr:d',
    'past-7-days': 'qdr:w',
    'past-month': 'qdr:m',
    'past-year': 'qdr:y',
}

aspect_ratio_params = {
    'tall': 'iar:t',
    'square': 'iar:s',
    'wide': 'iar:w',
    'panoramic': 'iar:xw',
}

format_params = {
    'jpg': 'ift:jpg',
    'gif': 'ift:gif',
    'png': 'ift:png',
    'bmp': 'ift:bmp',
    'svg': 'ift:svg',
    'webp': 'webp',
    'ico': 'ift:ico',
    'raw': 'ift:craw'
}
