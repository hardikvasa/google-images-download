## Endless searching and downloading Repo 

The main process(collector) has to look for links and collect them, then the workers(download_worker) take care of the pool for the download. We need selenium to "scroll down" and get the hidden nodes. The process will run until keyboard interruption or if the items len in output folder rich the max value.

install selenium

`pip install selenium`

install geckodriver driver 
download driver
`wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz`
unpack driver
`tar -xvzf geckodriver*`
executable
`chmod +x geckodriver`
set path
`export PATH=$PATH:/path-to-extracted-file/geckodriver`


use scroll flag to define the scrolling range by pixel and the download-pool range

`python google-images-download.py --keywords "Neil Armstrong, nasa astronaut neil armstrong, apollo neil armstrong" --max 500 --scroll 200 --thread 6 --proxy ip:port --type face`

```
flyn@tron:~/git/google-images-download$ python3.5 google-images-download.py --keywords "new york, einstein" -m 20
Saving Files in /home/flyn/git/data/raw_downloaded_image/new york
Starting Download Process...
failed IOError on image  HTTP Error 404: Not Found
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/location_img-59-1224772867-148.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/Fotolia_66358333_XL-Empire-State-Building-1600x1067.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/ny-skyline.jpg
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/2185_hodesti_00_p_1024x768.jpg
failed IOError on image  HTTP Error 404: Not Found
failed IOError on image  HTTP Error 400: Bad Request
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/original.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/74445360.jpg
failed IOError on image  HTTP Error 404: Not Found
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/colourbox3530143.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/new-york.jpg%3Fquality%3D90%26strip%3Dall%26w%3D1200
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/NYC_Top_of_the_Rock_Pano.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/new-york-2.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/image.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/newyork_NationalGeographic_2328428.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/1428972217718.jpeg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/new_york_at_night_500x266.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/newyork-736x272.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/newyorkcitypass__large.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/rockefeller_aussicht2-1600x1067.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/image-1234600-860_poster_16x9-lfxm-1234600.jpg
collector end  <Process(Process-2, started)>
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/new-york-macys-thanksgiving-parade.jpg
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/time-square-new-york-city-istock-487537456-2.jpg
download_workers end 
Saving Files in /home/flyn/git/data/raw_downloaded_image/ einstein
Starting Download Process...
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/new york/these-will-be-the-10-hottest-new-york-city-neighborhoods-in-2016.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/220px-Einstein-formal_portrait-35.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/220px-Albert_Einstein_Head.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/albert-einstein.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/albert-einstein-1933340_960_720.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/vcvv.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/alberteinste.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/albert-einstein-1167031_960_720.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/GettyImages-114340267.jpeg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/einstein-inside_portrait_ART_1.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/1621895221-albert-einstein-marylin-monroe-1lelT7jvCoNG.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/9533_Albert-Einstein-steckt-die-Zunge-raus.jpg
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/rz062-albert-einstein.jpg
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/2-format6001.jpg%3FinIsFirst%3Dtrue
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/einstein.png
theard  Thread 3 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/007BE84200000258-5006473-Lost_note_Scientist_Albert_Einstein-a-3_1508706113357.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/einstein-und-die-relativitaetstheorie.jpg
theard  Thread 2 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/1200px-Einstein_1921_portrait2.jpg
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/einstein-albert-head-raw.jpg
theard  Thread 0 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/pxb_albert-einstein_.jpg
collector end  <Process(Process-8, started)>
theard  Thread 1 completed ====>  /home/flyn/git/data/raw_downloaded_image/ einstein/einstein-bild.jpg
failed IOError on image  HTTP Error 404: Not Found
download_workers end
```
