import os
import re

import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from tqdm import tqdm


def download_uri(uri, dir='./'):
    with open(dir + uri.split('/')[-1], 'wb') as f:
        f.write(requests.get(uri, stream=True).content)


def download_baidu(word):
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    pic_url = re.findall('"objURL":"(.*?)",', requests.get(url).text, re.S)

    i = 0
    for each in pic_url:
        print(pic_url)
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('exception')
            continue

        string = 'pictures' + word + '_' + str(i) + '.jpg'
        fp = open(string, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1


def download_google(word):
    # url = 'https://www.google.com/search?q=' + word + '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    url = 'https://www.bing.com/images/search?q=' + word
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    links = soup.find_all('a', {'class': 'thumb'})

    for link in links:
        link = link.get('href')
        s = "curl -s -L -o '%s' '%s'" % (link.split('/')[-1], link)
        os.system(s)


def get_html():
    url = 'http://www.dermnet.com/dn2/allJPG3/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    links = soup.find_all('a')

    dir = './images/dermnet/'
    for link in tqdm(links, total=len(links)):
        link = url + link.get('href')
        f = dir + link.split('/')[-1]
        if not os.path.exists(f):
            s = "curl -s -L -o '%s' '%s'" % (f, link)
            os.system(s)


def organize_folders():
    url = 'http://www.dermnet.com/dn2/allJPG3/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    links = soup.find_all('a')

    dir = './images/dermnet/'
    for link in tqdm(links, total=len(links)):
        link = url + link.get('href')
        f = dir + link.split('/')[-1]
        if not os.path.exists(f):
            s = "curl -s -L -o '%s' '%s'" % (f, link)
            os.system(s)


if __name__ == '__main__':
    # word = input("Input key word: ")
    # download_baidu(word)
    download_google('honeybees')
