 <img src="https://storage.googleapis.com/ultralytics/logo/logoname1000.png" width="160">

# Introduction

This directory contains Bing image-scraping software forked from https://github.com/hardikvasa/google-images-download, and updated by Ultralytics LLC, and **is freely available for redistribution under the MIT license**. For more information please visit https://www.ultralytics.com.

# Requirements

Python 3.7 or later with all of the `pip install -U -r requirements.txt` packages including:
- `selenium`

# Install
```bash
git clone https://github.com/ultralytics/google-images-download
cd google-images-download
pip install -U -r requirements.txt
```

# Use

1. Install/update Chrome: https://www.google.com/chrome/

2. Install/update chromedriver: https://chromedriver.chromium.org/

3. Search via URL for up to `--limit` images supplying either `--url`:
 ```bash
$ python3 bing_scraper.py --url 'https://www.bing.com/images/search?q=flowers' --limit 10 --chromedriver /Users/glennjocher/Downloads/chromedriver
```

or `--search` terms. Images are saved to `./images`. Note that error-producing images may be skipped.
```bash
$ python3 bing_scraper.py --search 'honeybees on flowers' --limit 10 --chromedriver /Users/glennjocher/Downloads/chromedriver

Item no.: 1 --> Item name = 2020-02-25 12_53_58
Evaluating...
Getting you a lot of images. This may take a few moments...
Reached end of Page.
Starting Download...
Completed Image ====> 1.bigstock-Honey-Bee-on-a-flower-72446224.jpg
Completed Image ====> 2.maxresdefault.jpg
URLError on an image...trying next one... Error: HTTP Error 404: Not Found
Invalid or missing image format. Skipping...
Completed Image ====> 3.Bees-on-Sundance-Howard_Cheek-338275-620x413.jpg
URLError on an image...trying next one... Error: HTTP Error 404: Not Found
Completed Image ====> 4.bg-honeybees_pollinator-003.jpg
Completed Image ====> 5.dieselexhaus.jpg
Completed Image ====> 6.1-teamfindsgen.jpg
Completed Image ====> 7.HoneyBeeOnAsterFlower.jpg
Completed Image ====> 8.European_honey_bee_extracts_nectar.jpg
Completed Image ====> 9.Bee_in_appleflower.jpg
Completed Image ====> 10.525b1277a9b56bc7ed54052558288b82.jpg
Done with 3 errors in 24.6s. All images saved to /Users/glennjocher/PycharmProjects/google-images-download/images
```
<img src="https://user-images.githubusercontent.com/26833433/75287228-dcf2ca80-57ce-11ea-9557-cc13abaff453.jpg" width="">

# Cite

See https://github.com/hardikvasa/google-images-download.

# Contact

**Issues should be raised directly in the repository.** For additional questions or comments please email Glenn Jocher at glenn.jocher@ultralytics.com or visit us at https://contact.ultralytics.com.
