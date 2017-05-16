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

To download keyword 'Taj mahal' and 'Pyramid of Giza'

    google-images-download download 'Taj Mahal' 'Pyramid of Giza'

Installation
------------

  git clone https://github.com/rachmadaniHaryono/google-images-download
  cd ./google_images_download
  python setup.py install

or using pip to install it directly from github

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
