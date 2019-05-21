===============
Input Arguments
===============

Link to `GitHub repo <https://github.com/hardikvasa/google-images-download>`__

Link to `Documentation Homepage <https://google-images-download.readthedocs.io/en/latest/index.html>`__

+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| Argument          | Short hand  | Description                                                                                                                   |
+===================+=============+===============================================================================================================================+
| config_file       | cf          | You can pass the arguments inside a config file. This is an alternative to passing arguments on the command line directly.    |
|                   |             |                                                                                                                               |
|                   |             | Please refer to the                                                                                                           |
|                   |             | `config file format <https://github.com/hardikvasa/google-images-download/blob/master/README.rst#config-file-format>`__ below |
|                   |             |                                                                                                                               |
|                   |             | * If 'config_file' argument is present, the program will use the config file and command line arguments will be discarded     |
|                   |             | * Config file can only be in **JSON** format                                                                                  |
|                   |             | * Please refrain from passing invalid arguments from config file. Refer to the below arguments list                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
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
| prefix_keywords   | pk          | Denotes additional words added before main keyword while making the search query.                                             |
|                   |             |                                                                                                                               |
|                   |             | The final search query would be: <prefix keyword> <keyword>                                                                   |
|                   |             |                                                                                                                               |
|                   |             | So, for example, if the keyword is 'car' and prefix_keyword is 'red,yellow,blue', it will search and download images for      |
|                   |             | 'red car', 'yellow car' and 'blue car' individually                                                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| suffix_keywords   | sk          | Denotes additional words added after main keyword while making the search query.                                              |
|                   |             |                                                                                                                               |
|                   |             | The final search query would be: <keyword> <suffix keyword>                                                                   |
|                   |             |                                                                                                                               |
|                   |             | So, for example, if the keyword is 'car' and suffix_keyword is 'red,yellow,blue', it will search and download images for      |
|                   |             | 'car red', 'car yellow' and 'car blue' individually                                                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| limit             | l           | Denotes number of images that you want to download.                                                                           |
|                   |             |                                                                                                                               |
|                   |             | You can specify any integer value here. It will try and get all the images that it finds in the google image search page.     |
|                   |             |                                                                                                                               |
|                   |             | If this value is not specified, it defaults to 100.                                                                           |
|                   |             |                                                                                                                               |
|                   |             | **Note**: In case of occasional errors while downloading images, you could get less than 100 (if the limit is set to 100)     |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| related_images    | ri          | This argument downloads a ton of images related to the keyword you provided.                                                  |
|                   |             |                                                                                                                               |
|                   |             | Google Images page returns list of related keywords to the keyword you have mentioned in the query. This tool downloads       |
|                   |             | images from each of those related keywords based on the limit you have mentioned in your query                                |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--related_images' or '-ri' in your query.                                    |
|                   |             |                                                                                                                               |
|                   |             | **Note:**  This argument can download hundreds or thousands of additional images so please use this carefully.                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| format            | f           | Denotes the format/extension of the image that you want to download.                                                          |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: jpg, gif, png, bmp, svg, webp, ico, raw`                                                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| color             | co          | Denotes the color filter that you want to apply to the images.                                                                |
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
|                   |             | * `labeled-for-reuse-with-modifications`,                                                                                     |
|                   |             | * `labeled-for-reuse`,                                                                                                        |
|                   |             | * `labeled-for-noncommercial-reuse-with-modification`,                                                                        |
|                   |             | * `labeled-for-nocommercial-reuse`                                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| size              | s           | Denotes the relative size of the image to be downloaded.                                                                      |
|                   |             |                                                                                                                               |
|                   |             | `Possible values: large, medium, icon, >400*300, >640*480, >800*600, >1024*768, >2MP, >4MP, >6MP, >8MP, >10MP,                |
|                   |             | >12MP, >15MP, >20MP, >40MP, >70MP`                                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| exact_size        | es          | You can specify the exact size/resolution of the images                                                                       |
|                   |             |                                                                                                                               |
|                   |             | This value of this argument can be specified as ``<integer,integer>`` where the fist integer stands for width of the image    |
|                   |             | and the second integer stands for the height of the image. For example, ``-es 1024,786``                                      |
|                   |             |                                                                                                                               |
|                   |             | **Note**: You cannot specify both 'size' and 'exact_size' arguments in the same query. You can only give one of them.         |
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
|                   |             | `Possible values: past-24-hours, past-7-days, past-month, past-year`                                                          |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| time_range        | wr          | Denotes the time range for which you want to search the images                                                                |
|                   |             |                                                                                                                               |
|                   |             | The value of this parameter should be in the following format '{"time_min":"MM/DD/YYYY","time_max":"MM/DD/YYYY"}'             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| delay             | d           | Time to wait between downloading two images                                                                                   |
|                   |             |                                                                                                                               |
|                   |             | Time is to be specified in seconds. But you can have sub-second times by using decimal points.                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| url               | u           | Allows you search by image when you have the URL from the Google Images page.                                                 |
|                   |             | It downloads images from the google images link provided                                                                      |
|                   |             |                                                                                                                               |
|                   |             | If you are searching an image on the browser google images page, simply grab the browser URL and paste it in this parameter   |
|                   |             | It will download all the images seen on that page.                                                                            |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| single_image      | x           | Allows you to download one image if the complete (absolute) URL of the image is provided                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| output_directory  | o           | Allows you specify the main directory name in which the images are downloaded.                                                |
|                   |             |                                                                                                                               |
|                   |             | If not specified, it will default to 'downloads' directory. This directory is located in the path from where you run this code|
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><image_directory><images>``                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| image_directory   | i           | This lets you specify a directory inside of the main directory (output_directory) in which the images will be saved           |
|                   |             |                                                                                                                               |
|                   |             | If not specified, it will default to the name of the keyword.                                                                 |
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><image_directory><images>``                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_directory      | n           | This option allows you download images directly in the main directory (output_directory) without an image_directory           |
|                   |             |                                                                                                                               |
|                   |             | The directory structure would look like: ``<output_directory><images>``                                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| proxy             | px          | Allows you to specify proxy server setting for all your requests                                                              |
|                   |             |                                                                                                                               |
|                   |             | You can specify the proxy settings in 'IP:Port' format                                                                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| similar_images    | si          | Reverse Image Search or 'Search by Image' as it is referred to on Google.                                                     |
|                   |             |                                                                                                                               |
|                   |             | Searches and downloads images that are similar to the absolute image link/url you provide.                                    |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| specific_site     | ss          | Allows you to download images with keywords only from a specific website/domain name you mention.                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_urls        | p           | Print the URLs of the images on the console. These image URLs can be used for debugging purposes                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--print_urls' or '-p' in your query.                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_size        | ps          | Prints the size of the images on the console                                                                                  |
|                   |             |                                                                                                                               |
|                   |             | The size denoted the actual size of the image and not the size of the image on disk                                           |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--print_size' or '-ps' in your query.                                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| print_paths       | pp          | Prints the list of all the absolute paths of the downloaded images                                                            |
|                   |             |                                                                                                                               |
|                   |             | When calling the script from another python file, this list will be saved in a variable (as shown in the example below)       |
|                   |             |                                                                                                                               |
|                   |             | This argument also allows you to print the list on the console                                                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| metadata          | m           | Prints the metada of the image on the console.                                                                                |
|                   |             |                                                                                                                               |
|                   |             | This includes image size, origin, image attributes, description, image URL, etc.                                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--metadata' or '-m' in your query.                                           |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| extract_metadata  | e           | This option allows you to save metadata of all the downloaded images in a JSON file.                                          |
|                   |             |                                                                                                                               |
|                   |             | This file can be found in the ``logs/`` directory. The name of the file would be same as the keyword name                     |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--extract_metadata' or '-e' in your query.                                   |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| socket_timeout    | st          | Allows you to specify the time to wait for socket connection.                                                                 |
|                   |             |                                                                                                                               |
|                   |             | You could specify a higher timeout time for slow internet connection. The default value is 10 seconds.                        |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| thumbnail         | th          | Downloads image thumbnails corresponding to each image downloaded.                                                            |
|                   |             |                                                                                                                               |
|                   |             | Thumbnails are saved in their own sub-directories inside of the main directory.                                               |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--thumbnail' or '-th' in your query.                                         |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| thumbnail_only    | tho         | Downloads only thumbnails without downloading actual size images                                                              |
|                   |             |                                                                                                                               |
|                   |             | Thumbnails are saved in their own sub-directories inside of the main directory.                                               |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--thumbnail_only' or '-tho' in your query.                                   |
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
| chromedriver      | cd          | With this argument you can pass the path to the 'chromedriver'.                                                               |
|                   |             |                                                                                                                               |
|                   |             | The path looks like this: "path/to/chromedriver". In windows it will be "C:\\path\\to\\chromedriver.exe"                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| safe_search       | sa          | Searches for images with the Safe Search filter On                                                                            |
|                   |             |                                                                                                                               |
|                   |             | And this filter will be Off by default if you do not specify the safe_search argument                                         |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--safe_search' or '-sa' in your query.                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_numbering      | nn          | When you specify this argument, the script does not add ordered numbering as prefix to the images it downloads                |
|                   |             |                                                                                                                               |
|                   |             | If this argument is not specified, the images are numbered in order in which they are downloaded                              |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--no_numbering' or '-nn' in your query.                                      |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| offset            | of          | When you specify this argument, it will skip the offset number of links before it starts downloading images                   |
|                   |             |                                                                                                                               |
|                   |             | If this argument is not specified, the script will start downloading form the first link until the limit is reached           |
|                   |             |                                                                                                                               |
|                   |             | This argument takes integer. Make sure the value of this argument is less than the value of limit                             |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| save_source       | is          | Creates a text file with list of downloaded images along with their source page paths.                                        |
|                   |             |                                                                                                                               |
|                   |             | This argument takes a string, name of the text file.                                                                          |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| no_download       | nd          | Print the URLs on the console without downloading images or thumbnails. These image URLs can be used for other purposes       |
|                   |             |                                                                                                                               |
|                   |             | This argument does not take any value. Just add '--no-download' or '-nd' in your query.                                       |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| silent_mode       | sil         | Remains silent. Does not print notification messages on the terminal/command prompt.                                          |
|                   |             |                                                                                                                               |
|                   |             | This argument will override all the other print arguments (like print_urls, print_size, etc.)                                 |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| ignore_urls       | iu          | Skip downloading of images whose urls contain certain strings such as wikipedia.org                                           |
|                   |             |                                                                                                                               |
|                   |             | This argument takes a delimited set of values e.g. wikipedia.org,wikimedia.org                                                |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+
| help              | h           | show the help message regarding the usage of the above arguments                                                              |
+-------------------+-------------+-------------------------------------------------------------------------------------------------------------------------------+

**Note:** If ``single_image`` or ``url`` parameter is not present, then keywords is a mandatory parameter. No other parameters are mandatory.
