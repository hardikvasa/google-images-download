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


Installation
------------

.. code:: bash

  git clone https://github.com/rachmadaniHaryono/google-images-download
  cd ./google-images-download
  python setup.py install

or using pip to install it directly from github

.. code:: bash

  pip install git+https://github.com/rachmadaniHaryono/google-images-download.git

Requirements
^^^^^^^^^^^^

- click
- requests


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
