from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '2.8.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='google_images_download',
    version=__version__,
    description="Python Script to download hundreds of images from 'Google Images'. It is a ready-to-run code! ",
    long_description=long_description,
    url='https://github.com/hardikvasa/google-images-download',
    download_url='https://github.com/hardikvasa/google-images-download/tarball/' + __version__,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='google images download save filter color image-search image-dataset image-scrapper image-gallery terminal command-line',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Hardik Vasa',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='hnvasa@gmail.com',
    entry_points={
        'console_scripts': [
            'googleimagesdownload = google_images_download.google_images_download:main'
        ]},

)
