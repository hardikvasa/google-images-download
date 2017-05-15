"""Searching and Downloading Google Images/Image Links."""

# Import Libraries

import time  # Importing the time library to check the time of code execution
import argparse
try:
    from urllib2 import urlopen, Request, URLError, HTTPError
except ImportError:
    from urllib.request import urlopen, Request, URLError, HTTPError  # For 3.6.X Python

from fake_useragent import UserAgent

# ########## Edit From Here ###########

# This list is used to search keywords.
# You can edit this list to search for google images of your choice.
# You can simply add and remove elements of the list.

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '-s', '--list', nargs='+', help='Search keywords for google image search', required=True)
args = parser.parse_args()
search_keyword = args.list

# This list is used to further add suffix to your search term.
# Each element of the list will help you download 100 images.
# First element is blank,
# which denotes that no suffix is added to the search keyword of the above list.
# You can edit the list by adding/deleting elements from it.
# So if the first element of the search_keyword is 'Australia' and
# the second element of keywords is 'high resolution',
# then it will search for 'Australia High Resolution'
keywords = [' high resolution']


# ########## End of Editing ###########


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


# ############# Main Program ############
t0 = time.time()  # start the timer

# Download Image Links
i = 0
while i < len(search_keyword):
    items = []
    iteration = "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(search_keyword[i])
    print(iteration)
    print("Evaluating...")
    search_keywords = search_keyword[i]
    search = search_keywords.replace(' ', '%20')
    j = 0
    while j < len(keywords):
        pure_keyword = keywords[j].replace(' ', '%20')
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'  # NOQA
        raw_html = (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    # print ("Image Links = "+str(items))
    print("Total Image Links = " + str(len(items)))
    print("\n")
    i = i + 1

# # This allows you to write all the links into a test file.
# This text file will be created in the same directory as your code.
# You can comment out the below 3 lines to stop writing the output to the text file.
# info = open('output.txt', 'a')  # Open the text file called database.txt
# Write the title of the page
# info.write(str(i) + ': ' + str(search_keyword[i - 1]) + ": " + str(items) + "\n\n\n")
# info.close()  # Close the file

t1 = time.time()  # stop the timer
# Calculating the total time required to crawl, find and download all the links of 60,000 images
total_time = t1 - t0
print("Total time taken: " + str(total_time) + " Seconds")
print("Starting Download...")

# To save imges to the same directory
# IN this saving process we are just skipping the URL if there is any error

k = 0
errorCount = 0
while (k < len(items)):
    ua = UserAgent()
    try:
        req = Request(items[k], headers={
            "User-Agent": ua.firefox})
        response = urlopen(req)
        output_file = open(str(k + 1) + ".jpg", 'wb')
        data = response.read()
        output_file.write(data)
        response.close()

        print("completed ====> " + str(k + 1))

        k = k + 1

    except IOError:  # If there is any IOError

        errorCount += 1
        print("IOError on image " + str(k + 1))
        k = k + 1

    except HTTPError as e:  # If there is any HTTPError

        errorCount += 1
        print("HTTPError" + str(k))
        k = k + 1

    except URLError as e:

        errorCount += 1
        print("URLError " + str(k))
        k = k + 1

print("\n")
print("All are downloaded")
print("\n" + str(errorCount) + " ----> total Errors")

# ----End of the main program ----#
