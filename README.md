 <img src="https://storage.googleapis.com/ultralytics/logo/logoname1000.png" width="160">

# Introduction

This directory contains Bing image-scraping software forked from https://github.com/hardikvasa/google-images-download, and updated by Ultralytics LLC, and **is freely available for redistribution under the MIT license**. For more information please visit https://www.ultralytics.com.

# Requirements

Python 3.7 or later with all of the `pip install -U -r requirements.txt` packages including:
- `selenium`

# Install
```bash
git clone https://github.com/ultralytics/bing_scraper
cd bing_scraper
pip install -U -r requirements.txt
```

# Use

1. Install or update Chrome: https://www.google.com/chrome/

2. Install chromedriver: https://chromedriver.chromium.org/

3. Search via URL for up to `--limit` images and download. Images are saved to `./images`.

```bash
$ python3 bing_scraper.py --url 'https://www.bing.com/images/search?q=flowers' --limit 10 --chromedriver /Users/glennjocher/Downloads/chromedriver

$ python3 bing_scraper.py --search 'honeybees on flowers' --limit 10 --chromedriver /Users/glennjocher/Downloads/chromedriver
```

4. Or search via terms:
<img src="https://user-images.githubusercontent.com/26833433/75074332-4792c600-54b0-11ea-8c98-22acf58ba8e7.jpg" width="">

```bash
$ python3 bing_scraper.py --search 'honeybees on flowers' --limit 10 --chromedriver /Users/glennjocher/Downloads/chromedriver
```

# Cite

[![DOI](https://zenodo.org/badge/242235660.svg)](https://zenodo.org/badge/latestdoi/242235660)

# Contact

**Issues should be raised directly in the repository.** For additional questions or comments please email Glenn Jocher at glenn.jocher@ultralytics.com or visit us at https://contact.ultralytics.com.
