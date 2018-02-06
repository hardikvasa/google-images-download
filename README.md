# :sunrise: Google Images Download
Python Script for 'searching' and 'downloading' hundreds of Google images to the local hard disk!

## Summary
This is a command line python program to search keywords/key-phrases on Google Images and then also optionally download one or more images to your computer. This is a small program which is ready-to-run, but still under development. Many more features will be added to it going forward.

## Compatability
This program is compatible with both the versions of python (2.x and 3.x). It is a download-and-run program with no changes to the file. You will just have to specify parameters through the command line.
___

## How to run the script?
1. Download this repository on your local hard drive
2. Open the terminal (for mac/linux OS) or command prompt (for windows OS) and browse to the location of the file 'google-images-download.py' on your local disk.
3. Type in one of the following command mentioned below

## Usage
`python3 google-images-download.py [Arguments...]` or `python google-images-download.py [Arguments...]`

### Arguments 

| Argument  | Short hand | Explanation |
| --- | :---: | --- |
|**keywords**| k | Denotes the words that you want to search for and the directory file name. |
|**limit** | l |Denotes number of images that you want to download.  |
|**color** | c |Denotes the color filter that you would want to apply to the images.|
|**url** | u |Allows you search by image. It downloads images from the google images link provided|
|**single_image** | s |Allows you to download one image if the complete URL of the image is provided|
|**output_directory** | o |Allows you specify the main directory name. If not specified, it will default to 'downloads'|
|**delay** | d |Time to wait between downloading two images|

**Note:** If `single_image` or `url` parameter is not present, then keywords is a mandatory parameter

## Examples
* If you have python 2.x version installed

`python google-images-download.py --keywords "Polar bears, baloons, Beaches" --limit 20`

* If you have python 3.x version installed

`python3 google-images-download.py --keywords "Polar bears, baloons, Beaches" --limit 20`

* To use the short hand command

`python google-images-download.py -k "Polar bears, baloons, Beaches" -l 20`

* To use color filters for the images

`python google-images-download.py -k "playground" -l 20 -c red`

* To use non-English keywords for image search

`python google-images-download.py -k "北极熊" -l 5`

* To download images from the google images link

`python google-images-download.py -k "sample" -u <google images page URL>`

* To save images in specific main directory (instead of in 'downloads')

`python google-images-download.py -k "boat" -o "boat_new"`

* To download one single image with the image URL

`python google-images-download.py --keywords "baloons" --single_image <URL of the images>`

===> The images would be downloaded in their own sub-directories inside the main directory (either the one you provided or in 'downloads') in the same folder as the python file that you run.

___

## SSL Errors
If you do see SSL errors on Mac for Python 3 please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’ and run the file.

## Contribute
Anyone is welcomed to contribute to this script. If you would like to make a change, open a pull request. For issues and discussion visit the [Issue Tracker](https://github.com/hardikvasa/google-images-download/issues)

## :exclamation::exclamation: Disclaimer
This program lets you download tons of images from Google. Please do not download any image without violating its copyright terms. Google Images is a search engine that merely indexes images and allows you to find them.  It does NOT produce its own images and, as such, it doesn't own copyright on any of them.  The original creators of the images own the copyrights.  

Images published in the United States are automatically copyrighted by their owners, even if they do not explicitly carry a copyright warning.  You may not reproduce copyright images without their owner's permission, except in "fair use" cases, or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits. Please be very careful before its usage!
