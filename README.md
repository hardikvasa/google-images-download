<br>
<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="320">

# Introduction

This directory contains Bing image-scraping software forked from https://github.com/hardikvasa/google-images-download, and updated by Ultralytics.

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

# Contribute

We love your input! Ultralytics open-source efforts would not be possible without help from our community. Please see our [Contributing Guide](https://docs.ultralytics.com/help/contributing) to get started, and fill out our [Survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to send us feedback on your experience. Thank you 🙏 to all our contributors!

<!-- SVG image from https://opencollective.com/ultralytics/contributors.svg?width=990 -->
<a href="https://github.com/ultralytics/yolov5/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/assets/raw/main/im/image-contributors.png" alt="Ultralytics open-source contributors"></a>

# License

Ultralytics offers two licensing options to accommodate diverse use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/licenses/) open-source license is ideal for students and enthusiasts, promoting open collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) file for more details.
- **Enterprise License**: Designed for commercial use, this license permits seamless integration of Ultralytics software and AI models into commercial goods and services, bypassing the open-source requirements of AGPL-3.0. If your scenario involves embedding our solutions into a commercial offering, reach out through [Ultralytics Licensing](https://ultralytics.com/license).

# Contact

For Ultralytics bug reports and feature requests please visit [GitHub Issues](https://github.com/ultralytics/xview-yolov3/issues), and join our [Discord](https://ultralytics.com/discord) community for questions and discussions!

<br>
<div align="center">
  <a href="https://github.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="3%" alt="Ultralytics GitHub"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.linkedin.com/company/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="3%" alt="Ultralytics LinkedIn"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://twitter.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="3%" alt="Ultralytics Twitter"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://youtube.com/ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="3%" alt="Ultralytics YouTube"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.tiktok.com/@ultralytics"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="3%" alt="Ultralytics TikTok"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://www.instagram.com/ultralytics/"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="3%" alt="Ultralytics Instagram"></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="3%" alt="space">
  <a href="https://ultralytics.com/discord"><img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="3%" alt="Ultralytics Discord"></a>
</div>
