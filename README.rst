Google Images Download
======================

Python Script for 'searching' and 'downloading' hundreds of Google images to the local hard disk!

Summary
-------

This is a command line python program to search keywords/key-phrases on Google Images
and then also optionally download one or more images to your computer.
This is a small program which is ready-to-run, but still under development.
Many more features will be added to it going forward.

Compatability
-------------

This program is compatible with both the versions of python (2.x and 3.x).
It is a download-and-run program with no changes to the file.
You will just have to specify parameters through the command line.

Installation
------------

**Using pip:**

::

    $ pip install google_images_download

**Manually:**

::

    $ git clone https://github.com/hardikvasa/google-images-download.git
    $ cd google-images-download && sudo python setup.py install

Usage
-----

::

    $ googleimagesdownload [Arguments...]

Arguments
~~~~~~~~~

+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument         | Short hand  | Description                                                                                                                   |
+==================+=============+===============================================================================================================================+
| keywords         | k           | Denotes the keywords/key phrases you want to search for and the directory file name.                                          |
|                  |             |                                                                                                                               |
|                  |             | Tips:                                                                                                                         |
|                  |             |                                                                                                                               |
|                  |             | * If you simply type the keyword, Google will best try to match it                                                            |
|                  |             | * If you want to search for exact phrase, you can wrap the keywords in double quotes ("")                                     |
|                  |             | * If you want to search to contain either of the words provided, use **OR** between the words.                                |
|                  |             | * If you want to explicitly not want a specific word use a minus sign before the word (-)                                     |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| suffix_keywords  | sk          | Denotes additional words added after main keyword while making the search query.                                              |
|                  |             |                                                                                                                               |
|                  |             | Useful when you have multiple suffix keywords for one keyword.                                                                |
|                  |             |                                                                                                                               |
|                  |             | The final search query would be: <keyword> <suffix keyword>                                                                   |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| limit            | l           | Denotes number of images that you want to download.                                                                           |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| format           | f           | Denotes the format/extension that you want to download.                                                                       |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: jpg, gif, png, bmp, svg, webp, ico`                                                                         |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color            | c           | Denotes the color filter that you want to apply to the images.                                                                |
|                  |             |                                                                                                                               |
|                  |             | `Possible values`:                                                                                                            |
|                  |             |                                                                                                                               |
|                  |             | `red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown`                                             |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color_type       | ct          | Denotes the color type you want to apply to the images.                                                                       |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: full-color, black-and-white, transparent`                                                                   |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| usage_rights     | r           | Denotes the usage rights/licence under which the image is classified.                                                         |
|                  |             |                                                                                                                               |
|                  |             | `Possible values:`                                                                                                            |
|                  |             |                                                                                                                               |
|                  |             | * `labled-for-reuse-with-modifications`,                                                                                      |
|                  |             | * `labled-for-reuse`,                                                                                                         |
|                  |             | * `labled-for-noncommercial-reuse-with-modification`,                                                                         |
|                  |             | * `labled-for-nocommercial-reuse`                                                                                             |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| size             | s           | Denotes the relative size of the image to be downloaded.                                                                      |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: large, medium, icon`                                                                                        |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| aspect_ratio     | a           | Denotes the aspect ration of images to download.                                                                              |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: tall, square, wide, panoramic`                                                                              |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| type             | t           | Denotes the type of image to be downloaded.                                                                                   |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: face,photo,clip-art,line-drawing,animated`                                                                  |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time             | w           | Denotes the time the image was uploaded/indexed.                                                                              |
|                  |             |                                                                                                                               |
|                  |             | `Possible values: past-24-hours, past-7-days`                                                                                 |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| delay            | d           | Time to wait between downloading two images                                                                                   |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| url              | u           | Allows you search by image. It downloads images from the google images link provided                                          |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| single_image     | x           | Allows you to download one image if the complete URL of the image is provided                                                 |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| output_directory | o           | Allows you specify the main directory name. If not specified, it will default to 'downloads'                                  |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| similar_images   | si          | Reverse Image Search.                                                                                                         |
|                  |             |                                                                                                                               |
|                  |             | Searches and downloads images that are similar to the image link/url you provide.                                             |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| specific_site    | ss          | Allows you to download images with keywords only from a specific website/domain name you mention as indexed in Google Images. |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_urls       | p           | Print the URLs of the imageson the console. These image URLs can be used for debugging purposes                               |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help             | h           | show the help message regarding the usage of the above arguments                                                              |
+------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+

**Note:** If ``single_image`` or ``url`` parameter is not present, then keywords is a mandatory parameter. No other parameters are mandatory.

Examples
--------

- Simple examples

``googleimagesdownload --keywords "Polar bears, baloons, Beaches" --limit 20``

-  Using Suffix Keywords allows you to specify words after the main
   keywords. For example if the ``keyword = car`` and
   ``suffix keyword = 'red,blue'`` then it will first search for
   ``car red`` and then ``car blue``

``googleimagesdownload --k "car" -sk 'red,blue,white' -l 10``

-  To use the short hand command

``googleimagesdownload -k "Polar bears, baloons, Beaches" -l 20``

-  To download images with specific image extension/format

``googleimagesdownload --keywords "logo" --format svg``

-  To use color filters for the images

``googleimagesdownload -k "playground" -l 20 -c red``

-  To use non-English keywords for image search

``googleimagesdownload -k "北极熊" -l 5``

-  To download images from the google images link

``googleimagesdownload -k "sample" -u <google images page URL>``

-  To save images in specific main directory (instead of in 'downloads')

``googleimagesdownload -k "boat" -o "boat_new"``

-  To download one single image with the image URL

``googleimagesdownload --keywords "baloons" --single_image <URL of the images>``

-  To download images with size and type constrains

``googleimagesdownload --keywords "baloons" --size medium --type animated``

-  To download images with specific usage rights

``googleimagesdownload --keywords "universe" --usage_rights labled-for-reuse``

-  To download images with specific color type

``googleimagesdownload --keywords "flowers" --color_type black-and-white``

-  To download images with specific aspect ratio

``googleimagesdownload --keywords "universe" --aspect_ratio panoramic``

-  To download images which are similar to the image in the image URL that you provided (Reverse Image search).

``python3 pr.py -si <image url> -l 10``

-  To download images from specific website or domain name for a given keyword

``googleimagesdownload --keywords "universe" --specific_site example.com``

===> The images would be downloaded in their own sub-directories inside the main directory
(either the one you provided or in 'downloads') in the same folder you are in.

--------------

SSL Errors
----------

If you do see SSL errors on Mac for Python 3,
please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’
and run the file.

Contribute
----------

Anyone is welcomed to contribute to this script.
If you would like to make a change, open a pull request.
For issues and discussion visit the
`Issue Tracker <https://github.com/hardikvasa/google-images-download/issues>`__.

The aim of this repo is to keep it simple, stand-alone, backward compatible and 3rd party dependency proof.

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
