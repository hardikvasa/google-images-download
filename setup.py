"""setup."""
import setuptools

setuptools.setup(
    name="google_images_download",
    version="0.2.0",
    url="https://github.com/rachmadaniHaryono/google-images-download",

    author="Hardik Vasa",
    author_email="hnvasa@gmail.com",

    description="Download hundreds of images from google images",
    long_description=open('README.rst').read(),
    keywords="google image downloader",
    license="MIT",

    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=[
        'beautifulsoup4>=4.6.0',
        'click>=6.7',
        'fake-useragent==0.1.7',
        'requests>=2.14.2',
        'Send2Trash>=1.3.0',
        'structlog>=17.2.0',
    ],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],

    entry_points={
        'console_scripts': [
            'google-images-download = google_images_download.__main__:cli',
            'google-images-download-server = google_images_download.server:cli'
        ]
    },
)
