from google_images_download import google_images_download 

response = google_images_download.googleimagesdownload() 



def downloadimages(query):
    arguments = {"keywords": query,
                 "limit":1,
                 "print_urls":True,
                 "output_directory":"dataset",
                 "image_directory":"md5ldfkjldfkjasdflkjlsdfkaj",
                 "image_name":"test",
                 "no_numbering":True,
                 "silent_mode":True,
                }
    try:
        test = response.download(arguments)
        print(test)
    except FileNotFoundError: 
        pass
  
query = "المقدمة ابن خلدون"
downloadimages(query)