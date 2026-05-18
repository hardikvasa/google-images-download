=====
Usage
=====

Link to `GitHub repo <https://github.com/hardikvasa/google-images-download>`__

Link to `Documentation Homepage <https://google-images-download.readthedocs.io/en/latest/index.html>`__

Using the library from Command Line Interface
=============================================

If installed via pip or using CLI, use the following command:

.. code-block:: bash

    $ googleimagesdownload [Arguments...]

If downloaded via the UI, unzip the file downloaded, go to the 'google_images_download' directory and use one of the below commands:

.. code-block:: bash

    $ python3 google_images_download.py [Arguments...]
    OR
    $ python google_images_download.py [Arguments...]


Using the library from another python file
==========================================

If you would want to use this library from another python file, you could use it as shown below:

.. code-block:: python

    from google_images_download import google_images_download

    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({<Arguments...>})