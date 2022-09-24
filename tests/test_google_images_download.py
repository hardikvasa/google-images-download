import argparse
from google_images_download import google_images_download
import os, errno
import time


def silent_remove_of_file(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
        return False
    return True


def test_download_images_to_default_location(arguments: dict):
    start_time = time.time()
    try:
        temp = arguments['output_folder']
    except KeyError:
        pass
    else:
        assert False, "This test checks download to default location yet an output folder was provided"

    output_folder_path = os.path.join(os.path.realpath('.'), 'downloads', '{}'.format(arguments['keywords']))
    if os.path.exists(output_folder_path):
        start_amount_of_files_in_output_folder = len([name for name in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, name)) and os.path.getctime(os.path.join(output_folder_path, name)) < start_time])
    else:
        start_amount_of_files_in_output_folder = 0

    response = google_images_download.googleimagesdownload()
    response.download(arguments)
    files_modified_after_test_started = [name for name in os.listdir(output_folder_path) if os.path.isfile(os.path.join(output_folder_path, name)) and os.path.getmtime(os.path.join(output_folder_path, name)) > start_time]
    end_amount_of_files_in_output_folder = len(files_modified_after_test_started)
    print(f"Files downloaded by test {__name__}:")
    for file in files_modified_after_test_started:
        print(os.path.join(output_folder_path, file))


    # assert end_amount_of_files_in_output_folder - start_amount_of_files_in_output_folder == argumnets['limit']
    assert end_amount_of_files_in_output_folder == arguments['limit']

    print(f"Cleaning up all files downloaded by test {__name__}...")
    for file in files_modified_after_test_started:
        if silent_remove_of_file(os.path.join(output_folder_path, file)):
            print(f"Deleted {os.path.join(output_folder_path, file)}")
        else:
            print(f"Failed to delete {os.path.join(output_folder_path, file)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keywords', type=str, help='delimited list input', default="Polar bears")
    parser.add_argument('-l', '--limit', type=int, help='delimited list input', default=101)
    parser.add_argument('-u', '--print_urls', action='store_true', help='print the URLs of the images')
    parser.add_argument('-c', '--chromedriver', type=str, help='path to chromedriver executable in your local machine', default='C:/Program Files (x86)/chromedriver/chromedriver.exe')
    args = parser.parse_args()
    print(f"testing with args: {args}")

    test_download_images_to_default_location(vars(args))
