# In[ ]:
#  coding: utf-8

###### Searching and Downloading Google Images to the local disk ######

# Import Libraries
import sys
version = (3, 0)
cur_version = sys.version_info
if cur_version >= version:  # If the Current Version of Python is 3.0 or above
    import urllib.request
    from urllib.request import Request, urlopen
    from urllib.request import URLError, HTTPError
    from urllib.parse import quote
    import html
else:  # If the Current Version of Python is 2.x
    import urllib2
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urllib import quote
import time  # Importing the time library to check the time of code execution
import os
import argparse
import ssl
import datetime
import json
import re

# Taking command line arguments from users
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keywords', help='delimited list input', type=str, required=False)
parser.add_argument('-sk', '--suffix_keywords', help='comma separated additional words added to main keyword', type=str, required=False)
parser.add_argument('-l', '--limit', help='delimited list input', type=str, required=False)
parser.add_argument('-f', '--format', help='download images with specific format', type=str, required=False,
                    choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico'])
parser.add_argument('-u', '--url', help='search with google image URL', type=str, required=False)
parser.add_argument('-x', '--single_image', help='downloading a single image from URL', type=str, required=False)
parser.add_argument('-o', '--output_directory', help='download images in a specific directory', type=str, required=False)
parser.add_argument('-d', '--delay', help='delay in seconds to wait between downloading two images', type=str, required=False)
parser.add_argument('-c', '--color', help='filter on color', type=str, required=False,
                    choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
parser.add_argument('-ct', '--color_type', help='filter on color', type=str, required=False,
                    choices=['full-color', 'black-and-white', 'transparent'])
parser.add_argument('-r', '--usage_rights', help='usage rights', type=str, required=False,
                    choices=['labled-for-reuse-with-modifications','labled-for-reuse','labled-for-noncommercial-reuse-with-modification','labled-for-nocommercial-reuse'])
parser.add_argument('-s', '--size', help='image size', type=str, required=False,
                    choices=['large','medium','icon'])
parser.add_argument('-t', '--type', help='image type', type=str, required=False,
                    choices=['face','photo','clip-art','line-drawing','animated'])
parser.add_argument('-w', '--time', help='image age', type=str, required=False,
                    choices=['past-24-hours','past-7-days'])
parser.add_argument('-a', '--aspect_ratio', help='comma separated additional words added to keywords', type=str, required=False,
                    choices=['tall', 'square', 'wide', 'panoramic'])
parser.add_argument('-si', '--similar_images', help='downloads images very similar to the image URL you provide', type=str, required=False)
parser.add_argument('-ss', '--specific_site', help='downloads images that are indexed from a specific website', type=str, required=False)
parser.add_argument('-p', '--print_urls', default=False, help="Print the URLs of the images", action="store_true")
parser.add_argument('-ps', '--print_size', default=False, help="Print the size of the images on disk", action="store_true")
parser.add_argument('-m', '--metadata', default=False, help="Print the metadata of the image", action="store_true")
parser.add_argument('-e', '--extract_metadata', default=False, help="Dumps all the logs into a text file", action="store_true")
parser.add_argument('-st', '--socket_timeout', default=False, help="Connection timeout waiting for the image to download", type=float)
parser.add_argument('-th', '--thumbnail', default=False, help="Downloads image thumbnail along with the actual image", action="store_true")
parser.add_argument('-la', '--language', default=False, help="Defines the language filter. The search results are authomatically returned in that language", type=str, required=False,
                    choices=['Arabic','Chinese (Simplified)','Chinese (Traditional)','Czech','Danish','Dutch','English','Estonian','Finnish','French','German','Greek','Hebrew','Hungarian','Icelandic','Italian','Japanese','Korean','Latvian','Lithuanian','Norwegian','Portuguese','Polish','Romanian','Russian','Spanish','Swedish','Turkish'])
parser.add_argument('-pr', '--prefix', default=False, help="A word that you would want to prefix in front of each image name", type=str, required=False)

args = parser.parse_args()

#Initialization and Validation of user arguments
if args.keywords:
    search_keyword = [str(item) for item in args.keywords.split(',')]

#Additional words added to keywords
if args.suffix_keywords:
    suffix_keywords = [" " + str(sk) for sk in args.suffix_keywords.split(',')]
else:
    suffix_keywords = []

# Setting limit on number of images to be downloaded
if args.limit:
    limit = int(args.limit)
    if int(args.limit) >= 100:
        limit = 100
else:
    limit = 100

if args.url:
    current_time = str(datetime.datetime.now()).split('.')[0]
    search_keyword = [current_time.replace(":", "_")]

if args.similar_images:
    current_time = str(datetime.datetime.now()).split('.')[0]
    search_keyword = [current_time.replace(":", "_")]

# If single_image or url argument not present then keywords is mandatory argument
if args.single_image is None and args.url is None and args.similar_images is None and args.keywords is None:
            parser.error('Keywords is a required argument!')

# If this argument is present, set the custom output directory
if args.output_directory:
    main_directory = args.output_directory
else:
    main_directory = "downloads"

# Set the delay parameter if this argument is present
if args.delay:
    try:
        delay_time = int(args.delay)
    except ValueError:
        parser.error('Delay parameter should be an integer!')
else:
    delay_time = 0

if args.print_urls:
    print_url = 'yes'
else:
    print_url = 'no'

if args.print_size:
    print_size = 'yes'
else:
    print_size = 'no'

#------ Initialization Complete ------#

# Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(req)
            except URLError:  # Handling SSL certificate failed
                context = ssl._create_unverified_context()
                response = urlopen(req, context=context)
            page = response.read()
            return page
        except:
            return "Page Not found"

#Correcting the escape characters for python2
def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF
    return invalid_escape.sub(replace_with_byte, brokenjson)


#Format the object in readable format
def format_object(object):
    formatted_object = {}
    formatted_object['image_format'] = object['ity']
    formatted_object['image_height'] = object['oh']
    formatted_object['image_width'] = object['ow']
    formatted_object['image_link'] = object['ou']
    formatted_object['image_description'] = object['pt']
    formatted_object['image_host'] = object['rh']
    formatted_object['image_source'] = object['ru']
    formatted_object['image_thumbnail_url'] = object['tu']
    return formatted_object

#function to download single image
def single_image():
    url = args.single_image
    try:
        os.makedirs(main_directory)
    except OSError as e:
        if e.errno != 17:
            raise
        pass
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
    response = urlopen(req, None, 10)
    image_name = str(url[(url.rfind('/')) + 1:])
    if '?' in image_name:
        image_name = image_name[:image_name.find('?')]
    if ".jpg" in image_name or ".gif" in image_name or ".png" in image_name or ".bmp" in image_name or ".svg" in image_name or ".webp" in image_name or ".ico" in image_name:
        output_file = open(main_directory + "/" + image_name, 'wb')
    else:
        output_file = open(main_directory + "/" + image_name + ".jpg", 'wb')
        image_name = image_name + ".jpg"

    data = response.read()
    output_file.write(data)
    response.close()
    print("completed ====> " + image_name)
    return

def similar_images():
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        try:
            searchUrl = 'https://www.google.com/searchbyimage?site=search&sa=X&image_url=' + args.similar_images
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

            req1 = urllib.request.Request(searchUrl, headers=headers)
            resp1 = urllib.request.urlopen(req1)
            content = str(resp1.read())
            l1 = content.find('AMhZZ')
            l2 = content.find('&', l1)
            urll = content[l1:l2]

            newurl = "https://www.google.com/search?tbs=sbi:" + urll + "&site=search&sa=X"
            req2 = urllib.request.Request(newurl, headers=headers)
            resp2 = urllib.request.urlopen(req2)
            # print(resp2.read())
            l3 = content.find('/search?sa=X&amp;q=')
            l4 = content.find(';', l3 + 19)
            urll2 = content[l3 + 19:l4]
            return urll2
        except:
            return "Cloud not connect to Google Images endpoint"
    else:  # If the Current Version of Python is 2.x
        try:
            searchUrl = 'https://www.google.com/searchbyimage?site=search&sa=X&image_url=' + args.similar_images
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

            req1 = urllib2.Request(searchUrl, headers=headers)
            resp1 = urllib2.urlopen(req1)
            content = str(resp1.read())
            l1 = content.find('AMhZZ')
            l2 = content.find('&', l1)
            urll = content[l1:l2]

            newurl = "https://www.google.com/search?tbs=sbi:" + urll + "&site=search&sa=X"
            #print newurl
            req2 = urllib2.Request(newurl, headers=headers)
            resp2 = urllib2.urlopen(req2)
            # print(resp2.read())
            l3 = content.find('/search?sa=X&amp;q=')
            l4 = content.find(';', l3 + 19)
            urll2 = content[l3 + 19:l4]
            return(urll2)
        except:
            return "Cloud not connect to Google Images endpoint"

#Building URL parameters
def build_url_parameters():
    if args.language:
        lang = "&lr="
        lang_param = {"Arabic":"lang_ar","Chinese (Simplified)":"lang_zh-CN","Chinese (Traditional)":"lang_zh-TW","Czech":"lang_cs","Danish":"lang_da","Dutch":"lang_nl","English":"lang_en","Estonian":"lang_et","Finnish":"lang_fi","French":"lang_fr","German":"lang_de","Greek":"lang_el","Hebrew":"lang_iw ","Hungarian":"lang_hu","Icelandic":"lang_is","Italian":"lang_it","Japanese":"lang_ja","Korean":"lang_ko","Latvian":"lang_lv","Lithuanian":"lang_lt","Norwegian":"lang_no","Portuguese":"lang_pt","Polish":"lang_pl","Romanian":"lang_ro","Russian":"lang_ru","Spanish":"lang_es","Swedish":"lang_sv","Turkish":"lang_tr"}
        lang_url = lang+lang_param[args.language]
    else:
        lang_url = ''

    built_url = "&tbs="
    counter = 0
    params = {'color':[args.color,{'red':'ic:specific,isc:red', 'orange':'ic:specific,isc:orange', 'yellow':'ic:specific,isc:yellow', 'green':'ic:specific,isc:green', 'teal':'ic:specific,isc:teel', 'blue':'ic:specific,isc:blue', 'purple':'ic:specific,isc:purple', 'pink':'ic:specific,isc:pink', 'white':'ic:specific,isc:white', 'gray':'ic:specific,isc:gray', 'black':'ic:specific,isc:black', 'brown':'ic:specific,isc:brown'}],
              'color_type':[args.color_type,{'full-color':'ic:color', 'black-and-white':'ic:gray','transparent':'ic:trans'}],
              'usage_rights':[args.usage_rights,{'labled-for-reuse-with-modifications':'sur:fmc','labled-for-reuse':'sur:fc','labled-for-noncommercial-reuse-with-modification':'sur:fm','labled-for-nocommercial-reuse':'sur:f'}],
              'size':[args.size,{'large':'isz:l','medium':'isz:m','icon':'isz:i'}],
              'type':[args.type,{'face':'itp:face','photo':'itp:photo','clip-art':'itp:clip-art','line-drawing':'itp:lineart','animated':'itp:animated'}],
              'time':[args.time,{'past-24-hours':'qdr:d','past-7-days':'qdr:w'}],
              'aspect_ratio':[args.aspect_ratio,{'tall':'iar:t','square':'iar:s','wide':'iar:w','panoramic':'iar:xw'}],
              'format':[args.format,{'jpg':'ift:jpg','gif':'ift:gif','png':'ift:png','bmp':'ift:bmp','svg':'ift:svg','webp':'webp','ico':'ift:ico'}]}
    for key, value in params.items():
        if value[0] is not None:
            ext_param = value[1][value[0]]
            # counter will tell if it is first param added or not
            if counter == 0:
                # add it to the built url
                built_url = built_url + ext_param
                counter += 1
            else:
                built_url = built_url + ',' + ext_param
                counter += 1
    built_url = lang_url+built_url
    return built_url

#building main search URL
def build_search_url(search_term,params):
    # check the args and choose the URL
    if args.url:
        url = args.url
    elif args.similar_images:
        keywordem = similar_images()
        url = 'https://www.google.com/search?q=' + keywordem + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    elif args.specific_site:
        url = 'https://www.google.com/search?q=' + quote(
            search_term) + 'site:' + args.specific_site + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    else:
        url = 'https://www.google.com/search?q=' + quote(
            search_term) + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    #print(url)
    return url

#measures the file size
def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        size = file_info.st_size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size

# make directories
def create_directories(main_directory, dir_name):
    dir_name_thumbnail = dir_name + " - thumbnail"
    # make a search keyword  directory
    try:
        if not os.path.exists(main_directory):
            os.makedirs(main_directory)
            time.sleep(0.2)
            path = str(dir_name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
            if args.thumbnail:
                sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                if not os.path.exists(sub_directory_thumbnail):
                    os.makedirs(sub_directory_thumbnail)
        else:
            path = str(dir_name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
            if args.thumbnail:
                sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                if not os.path.exists(sub_directory_thumbnail):
                    os.makedirs(sub_directory_thumbnail)
    except OSError as e:
        if e.errno != 17:
            raise
            # time.sleep might help here
        pass
    return


# Download Images
def download_image_thumbnail(image_url, image_format, main_directory, dir_name, count):
    if args.print_urls:
        print("Image URL: " + image_url)
    try:
        req = Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        try:
            # timeout time to download an image
            if args.socket_timeout:
                timeout = float(args.socket_timeout)
            else:
                timeout = 15
            response = urlopen(req, None, timeout)

            # keep everything after the last '/'
            image_name = str(image_url[(image_url.rfind('tbn')) + 4:])
            image_name = image_name.lower()
            # if no extension then add it
            # remove everything after the image name
            if image_format == "":
                image_name = image_name + ".jpg"
            else:
                image_name = image_name + "." + image_format

            #prefix name in image
            if args.prefix:
                prefix = args.prefix + " "
            else:
                prefix = ''

            path = main_directory + "/" + dir_name + " - thumbnail" + "/" + prefix + " " +  str(count) + ". " + image_name
            output_file = open(path, 'wb')
            data = response.read()
            output_file.write(data)
            response.close()

            # image size parameter
            if args.print_size:
                print("Image Size: " + str(file_size(path)))

            download_status = 'success'
            download_message = "Completed Image Thumbnail ====> " + prefix + str(count) + ". " + image_name

        except UnicodeEncodeError as e:
            download_status = 'fail'
            download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)

    except HTTPError as e:  # If there is any HTTPError
        download_status = 'fail'
        download_message = "HTTPError on an image...trying next one..." + " Error: " + str(e)

    except URLError as e:
        download_status = 'fail'
        download_message = "URLError on an image...trying next one..." + " Error: " + str(e)

    except ssl.CertificateError as e:
        download_status = 'fail'
        download_message = "CertificateError on an image...trying next one..." + " Error: " + str(e)

    except IOError as e:  # If there is any IOError
        download_status = 'fail'
        download_message = "IOError on an image...trying next one..." + " Error: " + str(e)
    return download_status, download_message


# Download Images
def download_image(image_url,image_format,main_directory,dir_name,count):
    if args.print_urls:
        print("Image URL: " + image_url)
    try:
        req = Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        try:
            # timeout time to download an image
            if args.socket_timeout:
                timeout = float(args.socket_timeout)
            else:
                timeout = 15
            response = urlopen(req, None, timeout)

            # keep everything after the last '/'
            image_name = str(image_url[(image_url.rfind('/')) + 1:])
            image_name = image_name.lower()
            # if no extension then add it
            # remove everything after the image name
            if image_format == "":
                image_name = image_name + "." + "jpg"
            else:
                image_name = image_name[:image_name.find(image_format) + 3]

            # prefix name in image
            if args.prefix:
                prefix = args.prefix + " "
            else:
                prefix = ''

            path = main_directory + "/" + dir_name + "/" + prefix + str(count) + ". " + image_name
            output_file = open(path, 'wb')
            data = response.read()
            output_file.write(data)
            response.close()

            #image size parameter
            if args.print_size:
                print("Image Size: " + str(file_size(path)))

            download_status = 'success'
            download_message = "Completed Image ====> " + prefix +  str(count) + ". " + image_name

        except UnicodeEncodeError as e:
            download_status = 'fail'
            download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)

    except HTTPError as e:  # If there is any HTTPError
        download_status = 'fail'
        download_message = "HTTPError on an image...trying next one..." + " Error: " + str(e)

    except URLError as e:
        download_status = 'fail'
        download_message = "URLError on an image...trying next one..." + " Error: " + str(e)

    except ssl.CertificateError as e:
        download_status = 'fail'
        download_message = "CertificateError on an image...trying next one..." + " Error: " + str(e)

    except IOError as e:  # If there is any IOError
        download_status = 'fail'
        download_message = "IOError on an image...trying next one..." + " Error: " + str(e)
    return download_status,download_message


# Finding 'Next Image' from the given raw page
def _get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('class="rg_meta notranslate">')
        start_object = s.find('{', start_line + 1)
        end_object = s.find('</div>', start_object + 1)
        object_raw = str(s[start_object:end_object])
        #####print(object_raw)
        #remove escape characters based on python version
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version: #python3
            object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
            final_object = json.loads(object_decode)
        else:  #python2
            final_object = (json.loads(repair(object_raw)))
        return final_object, end_object


# Getting all links with the help of '_images_get_next_image'
def _get_all_items(page,main_directory,dir_name,limit):
    items = []
    errorCount = 0
    i = 0
    count = 1
    while count < limit+1:
        object, end_content = _get_next_item(page)
        if object == "no_links":
            break
        else:
            #format the item for readability
            object = format_object(object)
            if args.metadata:
                print("\nImage Metadata" + str(object))

            items.append(object)  # Append all the links in the list named 'Links'

            #download the images
            download_status,download_message = download_image(object['image_link'],object['image_format'],main_directory,dir_name,count)
            print(download_message)
            if download_status == "success":

                # download image_thumbnails
                if args.thumbnail:
                    download_status, download_message_thumbnail = download_image_thumbnail(object['image_thumbnail_url'],object['image_format'],main_directory, dir_name, count)
                    print(download_message_thumbnail)

                count += 1
            else:
                errorCount += 1

            #delay param
            if args.delay:
                time.sleep(int(args.delay))

            page = page[end_content:]
        i += 1
    if count < limit:
        print("\n\nUnfortunately all " + str(
            limit) + " could not be downloaded because some images were not downloadable. " + str(
            count-1) + " is all we got for this search filter!")
    return items,errorCount


# Bulk Download
def bulk_download(search_keyword,suffix_keywords,limit,main_directory):
    # appending a dummy value to Suffix Keywords array if it is blank
    if len(suffix_keywords) == 0:
        suffix_keywords.append('')

    for sky in suffix_keywords:     # 1.for every suffix keywords
        i = 0
        while i < len(search_keyword):      # 2.for every main keyword
            iteration = "\n" + "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(search_keyword[i] + str(sky))
            print(iteration)
            print("Evaluating...")
            search_term = search_keyword[i] + sky
            dir_name = search_term + ('-' + args.color if args.color else '')   #sub-directory

            create_directories(main_directory,dir_name)     #create directories in OS

            params = build_url_parameters()     #building URL with params

            url = build_search_url(search_term,params)      #building main search url

            raw_html = (download_page(url))     #download page

            print("Starting Download...")
            items,errorCount = _get_all_items(raw_html,main_directory,dir_name,limit)    #get all image items and download images

            #dumps into a text file
            if args.extract_metadata:
                try:
                    if not os.path.exists("logs"):
                        os.makedirs("logs")
                except OSError as e:
                    print(e)
                text_file = open("logs/"+search_keyword[i]+".txt", "w")
                text_file.write(json.dumps(items, indent=4, sort_keys=True))
                text_file.close()

            i += 1
    return errorCount

#------------- Main Program -------------#
if args.single_image:       #Download Single Image using a URL
    single_image()
else:                       # or download multiple images based on keywords/keyphrase search
    t0 = time.time()  # start the timer
    errorCount = bulk_download(search_keyword,suffix_keywords,limit,main_directory)

    print("\nEverything downloaded!")
    print("Total Errors: " + str(errorCount) + "\n")
    t1 = time.time()  # stop the timer
    total_time = t1 - t0  # Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Total time taken: " + str(total_time) + " Seconds")
#--------End of the main program --------#

# In[ ]:
