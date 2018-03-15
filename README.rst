Google Images Download
######################

Python Script for 'searching' and 'downloading' hundreds of Google images to the local hard disk!

Contents

.. contents:: :local:

Summary
=======

This is a command line python program to search keywords/key-phrases on Google Images
and then also optionally download one or more images to your computer.
This is a small program which is ready-to-run, but still under development.
Many more features will be added to it going forward.


Compatability
=============

This program is compatible with both the versions of python - 2.x and 3.x (recommended).
It is a download-and-run program with no changes to the file.
You will just have to specify parameters through the command line.

Installation
============

You can use **one of the below methods** to download and use this repository.

Using pip

.. code-block:: bash

    $ pip install google_images_download

Manually using CLI

.. code-block:: bash

    $ git clone https://github.com/hardikvasa/google-images-download.git
    $ cd google-images-download && sudo python setup.py install

Manually using UI

Go to the `repo on github <https://github.com/hardikvasa/google-images-download>`__ ==> Click on 'Clone or Download' ==> Click on 'Download ZIP' and save it on your local disk.
    
Usage
=====

If installed via pip or using CLI, use the following command:

.. code-block:: bash

    $ googleimagesdownload [Arguments...]

If downloaded via the UI, unzip the file downloaded, go to the 'google_images_download' directory and use one of the below commands:

.. code-block:: bash
    
    $ python3 google_images_download.py [Arguments...]
    OR
    $ python google_images_download.py [Arguments...]

Arguments
=========

+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument          | Short hand  | Description                                                                                                                   |
+===================+=============+===============================================================================================================================+
| keywords          | k           | Denotes the keywords/key phrases you want to search for. For more than one keywords, wrap it in single quotes.                |
|                   |             |                                                                                                                               |
|                   |             | Tips:                                                                                                                         |
|                   |             |                                                                                                                               |
|                   |             | * If you simply type the keyword, Google will best try to match it                                                            |
|                   |             | * If you want to search for exact phrase, you can wrap the keywords in double quotes ("")                                     |
|                   |             | * If you want to search to contain either of the words provided, use **OR** between the words.                                |
|                   |             | * If you want to explicitly not want a specific word use a minus sign before the word (-)                                     |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| keywords_from_file| kf          | Denotes the file name from where you would want to import the keywords.                                                       |
|                   |             |                                                                                                                               |
|                   |             | Add one keyword per line. Blank/Empty lines are truncated automatically.                                                      |
|                   |             |                                                                                                                               |
|                   |             | Only file types '.txt' or  '.csv' are allowed.                                                                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| suffix_keywords   | sk          | Denotes additional words added after main keyword while making the search query.                                              |
|                   |             |                                                                                                                               |
|                   |             | Useful when you have multiple suffix keywords for one keyword.                                                                |
|                   |             |                                                                                                                               |
|                   |             | The final search query would be: <keyword> <suffix keyword>                                                                   |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| limit             | l           | Denotes number of images that you want to download.                                                                           |
|                   |             |                                                                                                                               |
|                   |             | As of now you can select anything between 1 and 100. If this value is not specified, it defaults to 100.                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| format            | f           | Denotes the format/extension of the image that you want to download.                                                          |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: jpg, gif, png, bmp, svg, webp, ico`                                                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color             | c           | Denotes the color filter that you want to apply to the images.                                                                |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown`                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color_type        | ct          | Denotes the color type you want to apply to the images.                                                                       |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: full-color, black-and-white, transparent`                                                                   |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| usage_rights      | r           | Denotes the usage rights/licence under which the image is classified.                                                         |
|                   |             |                                                                                                                               |
|                   |             | `Possible values:`                                                                                                            |
|                   |             |                                                                                                                               |
|                   |             | * `labled-for-reuse-with-modifications`,                                                                                      |
|                   |             | * `labled-for-reuse`,                                                                                                         |
|                   |             | * `labled-for-noncommercial-reuse-with-modification`,                                                                         |
|                   |             | * `labled-for-nocommercial-reuse`                                                                                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| size              | s           | Denotes the relative size of the image to be downloaded.                                                                      |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP,                |
|                   |             | >12MP, >15MP, >20MP, >40MP, >70MP`                                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| aspect_ratio      | a           | Denotes the aspect ratio of images to download.                                                                               |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: tall, square, wide, panoramic`                                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| type              | t           | Denotes the type of image to be downloaded.                                                                                   |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: face, photo, clip-art, line-drawing, animated`                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time              | w           | Denotes the time the image was uploaded/indexed.                                                                              |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: past-24-hours, past-7-days`                                                                                 |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time_range        | wr          | Denotes the time range for which you want to search the images                                                                |
|                   |             |                                                                                                                               |
|                   |             | The value of this parameter should be in the following format '{"time_min":"MM/DD/YYYY","time_max":"MM/DD/YYYY"}'             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| delay             | d           | Time to wait between downloading two images                                                                                   |
|                   |             |                                                                                                                               |
|                   |             | Time is to be specified in seconds. But you can have sub-second times by using decimal points.                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| url               | u           | Allows you search by image URL. It downloads images from the google images link provided                                      |
|                   |             |                                                                                                                               |
|                   |             | If you are searching an image on the browser google images page, simply grab the browser URL and paste it in this parameter   |
|                   |             | It will download all the images seen on that page.                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| single_image      | x           | Allows you to download one image if the complete (absolute) URL of the image is provided                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| output_directory  | o           | Allows you specify the main directory name in which the images are downloaded.                                                |
|                   |             |                                                                                                                               |
|                   |             | If not specified, it will default to 'downloads' directory. This directory is located in the path from where you run this code|
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| similar_images    | si          | Reverse Image Search.                                                                                                         |
|                   |             |                                                                                                                               |
|                   |             | Searches and downloads images that are similar to the absolute image link/url you provide.                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| specific_site     | ss          | Allows you to download images with keywords only from a specific website/domain name you mention.                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_urls        | p           | Print the URLs of the images on the console. These image URLs can be used for debugging purposes                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_size        | ps          | Prints the size of the images on the console                                                                                  |
|                   |             |                                                                                                                               |
|                   |             | The size denoted the actual size of the image and not the size of the image on disk                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| metadata          | m           | Prints the metada of the image on the console.                                                                                |
|                   |             |                                                                                                                               |
|                   |             | This includes image size, origin, image attributes, description, image URL, etc.                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| extract_metadata  | e           | This option allows you to save metadata of all the downloaded images in a text file.                                          |
|                   |             |                                                                                                                               |
|                   |             | This file can be found in the ``logs/`` directory. The name of the file would be same as the keyword nam                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| socket_timeout    | st          | Allows you to specify the time to wait for socket connection.                                                                 |
|                   |             |                                                                                                                               |
|                   |             | You could specify a higher timeout time for slow internet connection. The default value is 15 seconds.                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| thumbnail         | th          | Downloads image thumbnails corresponding to each image downloaded.                                                            |
|                   |             |                                                                                                                               |
|                   |             | Thumbnails are saved in their own sub-directories inside of the main directory.                                               |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| language          | la          | Defines the language filter. The search results are automatically returned in that language                                   |
|                   |             |                                                                                                                               |
|                   |             | `Possible Values: Arabic, Chinese (Simplified), Chinese (Traditional), Czech, Danish, Dutch, English, Estonian. Finnish,      |
|                   |             | French, German, Greek, Hebrew, Hungarian, Icelandic, Italian, Japanese, Korean, Latvianm, Lithuanian, Norwegian, Portuguese,  |
|                   |             | Polish, Romanian, Russian, Spanish, Swedish, Turkish`                                                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| prefix            | pr          | A word that you would want to prefix in front of actual image name.                                                           |
|                   |             |                                                                                                                               |
|                   |             | This feature can be used to rename files for image identification purpose.                                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help              | h           | show the help message regarding the usage of the above arguments                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+

**Note:** If ``single_image`` or ``url`` parameter is not present, then keywords is a mandatory parameter. No other parameters are mandatory.

Examples
========

- Simple examples

.. code-block:: bash
    
    $ googleimagesdownload --keywords "Polar bears, baloons, Beaches" --limit 20

-  Using Suffix Keywords allows you to specify words after the main
   keywords. For example if the ``keyword = car`` and
   ``suffix keyword = 'red,blue'`` then it will first search for
   ``car red`` and then ``car blue``

.. code-block:: bash
    
    $ googleimagesdownload --k "car" -sk 'red,blue,white' -l 10

-  To use the short hand command

.. code-block:: bash
    
    $ googleimagesdownload -k "Polar bears, baloons, Beaches" -l 20

-  To download images with specific image extension/format

.. code-block:: bash
    
    $ googleimagesdownload --keywords "logo" --format svg

-  To use color filters for the images

.. code-block:: bash
    
    $ googleimagesdownload -k "playground" -l 20 -c red

-  To use non-English keywords for image search

.. code-block:: bash
    
    $ googleimagesdownload -k "北极熊" -l 5

-  To download images from the google images link

.. code-block:: bash
    
    $ googleimagesdownload -k "sample" -u <google images page URL>

-  To save images in specific main directory (instead of in 'downloads')

.. code-block:: bash
    
    $ googleimagesdownload -k "boat" -o "boat_new"

-  To download one single image with the image URL

.. code-block:: bash
    
    $ googleimagesdownload --keywords "baloons" --single_image <URL of the images>

-  To download images with size and type constrains

.. code-block:: bash
    
    $ googleimagesdownload --keywords "baloons" --size medium --type animated

-  To download images with specific usage rights

.. code-block:: bash
    
    $ googleimagesdownload --keywords "universe" --usage_rights labled-for-reuse

-  To download images with specific color type

.. code-block:: bash
    
    $ googleimagesdownload --keywords "flowers" --color_type black-and-white

-  To download images with specific aspect ratio

.. code-block:: bash
    
    $ googleimagesdownload --keywords "universe" --aspect_ratio panoramic

-  To download images which are similar to the image in the image URL that you provided (Reverse Image search).

.. code-block:: bash
    
    $ googleimagesdownload -si <image url> -l 10

-  To download images from specific website or domain name for a given keyword

.. code-block:: bash
    
    $ googleimagesdownload --keywords "universe" --specific_site example.com

===> The images would be downloaded in their own sub-directories inside the main directory
(either the one you provided or in 'downloads') in the same folder you are in.

--------------

Troubleshooting
===============

**## SSL Errors**

If you do see SSL errors on Mac for Python 3,
please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’
and run the file.

**## googleimagesdownload: command not found**

While using the above commands, if you get ``Error: -bash: googleimagesdownload: command not found`` then you have to set the correct path variable.

To get the details of the repo, run the following command:

.. code-block:: bash

    $ pip show -f google_images_download 

you will get the result like this:

.. code-block:: bash

	Location: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
	Files:
	  ../../../bin/googleimagesdownload

together they make: ``/Library/Frameworks/Python.framework/Versions/2.7/bin`` which you need add it to the path:

.. code-block:: bash
	
    $ export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin"


**## [Errno 13] Permission denied creating directory 'downloads'**

When you run the command, it downloads the images in the current directory (the directory from where you are running the command). If you get permission denied error for creating the `downloads directory`, then move to a directory in which you have the write permission and then run the command again.


**## Permission denied while installing the library**

On MAC and Linux, when you get permission denied when installing the library using pip, try doing a user install.

.. code-block:: bash
	
    $ pip install google_images_download --user

You can also run pip install as a superuser with ``sudo pip install google_images_download`` but it is not generally a good idea because it can cause issues with your system-level packages.

Structure
=========

Below diagram represents the code logic.

.. figure:: http://www.zseries.in/flow-chart.png
   :alt:

Contribute
==========

Anyone is welcomed to contribute to this script.
If you would like to make a change, open a pull request.
For issues and discussion visit the
`Issue Tracker <https://github.com/hardikvasa/google-images-download/issues>`__.

The aim of this repo is to keep it simple, stand-alone, backward compatible and 3rd party dependency proof.

Disclaimer
==========

This program lets you download tons of images from Google.
Please do not download or use any image that violates its copyright terms.
Google Images is a search engine that merely indexes images and allows you to find them.
It does NOT produce its own images and, as such, it doesn't own copyright on any of them.
The original creators of the images own the copyrights.

Images published in the United States are automatically copyrighted by their owners,
even if they do not explicitly carry a copyright warning.
You may not reproduce copyright images without their owner's permission,
except in "fair use" cases,
or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits.
Please be very careful before its usage!
