 <img src="https://storage.googleapis.com/ultralytics/logo/logoname1000.png" width="160">

# Introduction

This directory contains Bing image-scraping software forked from https://github.com/hardikvasa/google-images-download, and updated by Ultralytics LLC, and **is freely available for redistribution under the MIT license**. For more information please visit https://www.ultralytics.com.

# Requirements

Python 3.8 or later with all [requirements.txt](https://github.com/ultralytics/google-images-download/blob/master/requirements.txt) dependencies installed, including `selenium`. To install run:
```bash
$ pip install -r requirements.txt
```

# Install
```bash
$ git clone https://github.com/ultralytics/google-images-download
$ cd google-images-download
$ pip install -r requirements.txt
```

# Run

1. Install/update Chrome: https://www.google.com/chrome/

2. Install/update chromedriver: https://chromedriver.chromium.org/

3. Run. Download up to `--limit` images supplying either a `--url`:
 ```bash
$ python3 bing_scraper.py --url 'https://www.bing.com/images/search?q=flowers' --limit 10 --download --chromedriver /Users/glennjocher/Downloads/chromedriver
```

or `--search` terms. Images are saved to `./images`. Note that error-producing images may be skipped.
```bash
$ python bing_scraper.py --search 'honeybees on flowers' --limit 10 --download --chromedriver ./chromedriver

Searching for https://www.bing.com/images/search?q=honeybees%20on%20flowers
Downloading HTML... 3499588 elements: 30it [00:24,  1.21it/s]
Downloading images...
1/10 https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Apis_mellifera_Western_honey_bee.jpg/1200px-Apis_mellifera_Western_honey_bee.jpg 
2/10 https://berkshirefarmsapiary.files.wordpress.com/2013/07/imgp8415.jpg 
3/10 http://www.pestworld.org/media/561900/honey-bee-foraging-side-view.jpg 
4/10 https://www.gannett-cdn.com/-mm-/da6df33e2de11997d965f4d81915ba4d1bd4586e/c=0-248-3131-2017/local/-/media/2017/06/22/USATODAY/USATODAY/636337466517310122-GettyImages-610156450.jpg 
5/10 http://4.bp.blogspot.com/-b9pA6loDnsw/TY0GjKtyDCI/AAAAAAAAAD8/jHdZ5O40CeQ/s1600/bees.jpg 
6/10 https://d3i6fh83elv35t.cloudfront.net/static/2019/02/Honey_bee_Apis_mellifera_CharlesJSharpCC-1024x683.jpg 
7/10 http://www.fnal.gov/pub/today/images05/bee.jpg 
8/10 https://upload.wikimedia.org/wikipedia/commons/5/55/Honey_Bee_on_Willow_Catkin_(5419305106).jpg 
9/10 https://cdnimg.in/wp-content/uploads/2015/06/HoneyBeeW-1024x1024.jpg 
10/10 http://www.pouted.com/wp-content/uploads/2015/03/honeybee_06_by_wings_of_light-d3fhfg1.jpg 
Done with 0 errors in 37.1s. All images saved to /Users/glennjocher/PycharmProjects/google-images-download/images
```
<img src="https://user-images.githubusercontent.com/26833433/75287228-dcf2ca80-57ce-11ea-9557-cc13abaff453.jpg" width="">

# Cite

See https://github.com/hardikvasa/google-images-download.

## About Us

Ultralytics is a U.S.-based particle physics and AI startup with over 6 years of expertise supporting government, academic and business clients. We offer a wide range of vision AI services, spanning from simple expert advice up to delivery of fully customized, end-to-end production solutions, including:
- **Cloud-based AI** systems operating on **hundreds of HD video streams in realtime.**
- **Edge AI** integrated into custom iOS and Android apps for realtime **30 FPS video inference.**
- **Custom data training**, hyperparameter evolution, and model exportation to any destination.

For business inquiries and professional support requests please visit us at https://www.ultralytics.com. 

## Contact

**Issues should be raised directly in the repository.** For business inquiries or professional support requests please visit https://www.ultralytics.com or email Glenn Jocher at glenn.jocher@ultralytics.com. 
