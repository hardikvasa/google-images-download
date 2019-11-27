from google_images_download import google_images_download
import os
import json
import time

from .test_google_images_download import silent_remove_of_file


def test_metadata():
    start_time = time.time()
    output_folder_path = os.path.join(os.path.realpath('.'), 'logs')

    keywords = ["Polar bears", "ほげ"]
    for keyword in keywords:
        argumnets = {
            "keywords": keyword,
            "limit": 5,
            "no_download": True,
            "extract_metadata": True
        }
        response = google_images_download.googleimagesdownload()
        response.download(argumnets)
        with open(os.path.join(output_folder_path, '{}.json'.format(keyword)), 'r') as fp:
            for item in json.load(fp):
                assert keyword.lower() in item['image_description'].lower()

    files_modified_after_test_started = [name for name in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, name)) and os.path.getmtime(os.path.join(output_folder_path, name)) > start_time]
    print(f"Cleaning up all files downloaded by test {__name__}...")
    for file in files_modified_after_test_started:
        if silent_remove_of_file(os.path.join(output_folder_path, file)):
            print(f"Deleted {os.path.join(output_folder_path, file)}")
        else:
            print(f"Failed to delete {os.path.join(output_folder_path, file)}")
