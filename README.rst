google-images-download
======================

.. image:: https://travis-ci.org/rachmadaniHaryono/google-images-download.png
   :target: https://travis-ci.org/rachmadaniHaryono/google-images-download
   :alt: Latest Travis CI build status

Download hundreds of images from google images

This is a Python program to search keywords/key-phrases on Google Images
and then also optionally download all Images. 


Usage
-----

.. image:: https://github.com/rachmadaniHaryono/google-images-download/raw/master/res/screenshot.png
   :target: https://github.com/rachmadaniHaryono/google-images-download
   :alt: Screenshot

Download command have following option:

.. code:: bash

  Usage: google-images-download download [OPTIONS] [SEARCH_KEYWORDS]...

  Options:
    --keywords TEXT           Additional keyword input.
    -nc, --no-clobber         Skip downloads that would download to existing files (overwriting them)
    --download-limit INTEGER  Download limit. set 0 for no limit.
    --requests-delay INTEGER  Delay between requests(seconds). set 0 for no delay.
    --filename-format [basename|sha256]
                              Filename format of the url. default: basename
    --help                    Show this message and exit.

To download keyword 'Taj mahal' and 'Pyramid of Giza'

.. code:: bash

  google-images-download download 'Taj Mahal' 'Pyramid of Giza'

To download keyword 'Taj mahal' and 'Pyramid of Giza' with additional keyword 'high resolution'

.. code:: bash

  google-images-download download 'Taj Mahal' 'Pyramid of Giza'  --keywords 'high resolution'
  # this will search 'Taj Mahal high resolution' and 'Pyramid of Giza high resolution'

Starting from version 0.3.0 filename format flag added.
The downloaded image will be renamed based on available filename format
such as the file's sha256 checksum

.. code:: bash

  google-images-download download 'Taj Mahal' --filename-format sha256
  # this will download `Taj Mahal` pic and renamed it based on sha256 checksum

Starting from version 0.2.0 it also can search similar picture from the file. To do that do the following:

.. code:: bash

  google-images-download search filename.jpg
  # this willl open google image to search image similar to 'filename.jpg'


Usage as server for Hydrus (alpha)
----------------------------------

1. Run server with following command

.. code:: bash

  google-images-download-server run -d -p 5001 -t

It will run on debug and threaded mode on port 5001

2. choose which booru mode to install in Hydrus:

Simple google image search

.. code:: yaml

  !Booru
  _advance_by_page_num: true
  _image_data: '[link]'
  _image_id: null
  _name: gid_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/?query=%tags%&page=%index%
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

Google simlar image search

.. code:: yaml

  !Booru
  _advance_by_page_num: false
  _image_data: '[link]'
  _image_id: null
  _name: gid_similar_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/f/?file_path=%tags%&search_type=1
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

Google image size search

.. code:: yaml

  !Booru
  _advance_by_page_num: false
  _image_data: '[link]'
  _image_id: null
  _name: gid_size_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/f/?file_path=%tags%&search_type=2
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

Google image size search without cache

.. code:: yaml

  !Booru
  _advance_by_page_num: false
  _image_data: '[link]'
  _image_id: null
  _name: gid_size(dc)_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/f/?file_path=%tags%&search_type=2&disable_cache=y
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

Google simlar image search from image url

.. code:: yaml

  !Booru
  _advance_by_page_num: false
  _image_data: '[link]'
  _image_id: null
  _name: gid_size_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/f/?url=%tags%&search_type=1
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

Google image size search from image url

.. code:: yaml

  !Booru
  _advance_by_page_num: false
  _image_data: '[link]'
  _image_id: null
  _name: gid_size_booru
  _search_separator: +
  _search_url: http://127.0.0.1:5001/f/?url=%tags%&search_type=2
  _tag_classnames_to_namespaces: {tag-page-url: gid page url, tag-picture-subtitle: gid
      subtitle, tag-picture-title: gid title, tag-query: gid query, tag-site: gid site,
    tag-site-title: gid site title}
  _thumb_classname: thumb

3. Search the image. For similar image search and size image search you need to input image path.


Installation
------------

.. code:: bash

  git clone https://github.com/rachmadaniHaryono/google-images-download
  cd ./google-images-download
  pip install .
  # to install package needed for server
  pip install .[server]

or using pip to install it directly from github

.. code:: bash

  pip install git+https://github.com/rachmadaniHaryono/google-images-download.git

Compatibility
-------------
This program is now compatible with python 3.x and tested under version 3.5.
It is a download-and-run program with couple of changes
like the keywords for which you want to search and download images.

Status
------
This is a small program which is ready-to-run, but still under development.
Many more features will be added to it shortly.
Also looking for collaborator.

Disclaimer
----------
This program lets you download tons of images from Google.
Please do not download any image without violating its copyright terms.
Google Images is a search engine that merely indexes images and allows you to find them.
It does NOT produce its own images and, as such, it doesn't own copyright on any of them.
The original creators of the images own the copyrights.

Images published in the United States are automatically copyrighted by their owners,
even if they do not explicitly carry a copyright warning.
You may not reproduce copyright images without their owner's permission,
except in "fair use" cases,
or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits.
Please be very careful before its usage!

Licence
-------
MIT LICENSE

Authors
-------
- Hardik Vasa (@hardikvasa)
- rytoj (@rytoj)
- Rachmadani Haryono (@rachmadaniHaryono)

`google_images_download` was written by `Hardik Vasa <hnvasa@gmail.com>`_.
