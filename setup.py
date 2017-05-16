"""setup."""
import setuptools

setuptools.setup(
    name="google_images_download",
    version="0.1.0",
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
        'click>=6.7',
        'requests>=2.14.2',
        'fake-useragent==0.1.7',
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
            'google-images-download = google_images_download.__main__:cli'
        ]
    },
)
