#!/usr/bin/env python3
"""Searching and Downloading Google Images/Image Links."""

# Import Libraries

from os.path import basename
from urllib.parse import quote
import time  # Importing the time library to check the time of code execution
try:
    from urllib2 import urlopen, Request, URLError, HTTPError
except ImportError:
    from urllib.request import urlopen, Request, URLError, HTTPError  # For 3.6.X Python

from fake_useragent import UserAgent


def download_page(url):
    """Downloading entire Web Document (Raw Page Content)."""
    ua = UserAgent()
    headers = {'User-Agent': ua.firefox}
    req = Request(url, headers=headers)
    response = urlopen(req)
    page = str(response.read())
    return page


def _images_get_next_item(s):
    """Finding 'Next Image' from the given raw page."""
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


def _images_get_all_items(page):
    """Getting all links with the help of '_images_get_next_image'."""
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)  # Append all the links in the list named 'Links'
            time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


def main(search_keywords, keywords, download_limit, requests_delay):
    t0 = time.time()  # start the timer
    items = []
    # Download Image Links
    for i, search_keyword in enumerate(search_keywords):
        print("Item no.: {} --> Item name = {}".format(i + 1, search_keyword))
        print("Evaluating...")
        search = quote(search_keyword)
        if not keywords:
            url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'  # NOQA
            raw_html = (download_page(url))
            items = items + (_images_get_all_items(raw_html))

        for j, keyword in enumerate(keywords):
            pure_keyword = quote(keyword)
            url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'  # NOQA
            raw_html = (download_page(url))
            items = items + (_images_get_all_items(raw_html))

            # delay is required here
            if requests_delay == 0:
                time.sleep(0.1)
            else:
                time.sleep(requests_delay)

        print("Total Image Links = {}\n".format(len(items)))

    # # This allows you to write all the links into a test file.
    # This text file will be created in the same directory as your code.
    # You can comment out the below 3 lines to stop writing the output to the text file.
    # info = open('output.txt', 'a')  # Open the text file called database.txt
    # Write the title of the page
    # info.write(str(i) + ': ' + str(search_keyword[i - 1]) + ": " + str(items) + "\n\n\n")
    # info.close()  # Close the file

    t1 = time.time()  # stop the timer
    # Calculating the total time required to crawl,
    # find and download all the links of 60,000 images
    total_time = t1 - t0
    print("Total time taken: " + str(total_time) + " Seconds")
    print("Starting Download...")

    # To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error

    error_count = 0
    dl_counter = 0
    ua = UserAgent()
    for k, item in enumerate(items):
        if download_limit != 0 and dl_counter >= download_limit:
            break
        filename = basename(item)
        try:
            req = Request(item, headers={"User-Agent": ua.firefox})
            with urlopen(req) as response, \
                    open(filename, 'wb') as output_file:
                data = response.read()
                output_file.write(data)

            print("completed ====>{}".format(k + 1))
            dl_counter += 1

        except IOError:  # If there is any IOError
            error_count += 1
            print("IOError on image {}".format(k + 1))

        except HTTPError as e:  # If there is any HTTPError
            error_count += 1
            print("HTTPError {}".format(k + 1))

        except URLError as e:
            error_count += 1
            print("URLError {}".format(k + 1))

        if requests_delay != 0:
            time.sleep(requests_delay)

    print("\nAll url(s) are downloaded\n{} ----> total Errors".format(error_count))

    # ----End of the main program ----#
