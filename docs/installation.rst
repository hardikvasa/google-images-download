============
Installation
============

Link to `Documentation Homepage <https://google-images-download.readthedocs.io/en/latest/index.html>`__

You can use **one of the below methods** to download and use this repository.

Install using pip
-----------------

.. code-block:: bash

    $ pip install google_images_download


Manually install using CLI
--------------------------

.. code-block:: bash

    $ git clone https://github.com/hardikvasa/google-images-download.git
    $ cd google-images-download && sudo python setup.py install


Manually install using UI
-------------------------

Go to the `repo on github <https://github.com/hardikvasa/google-images-download>`__ ==> Click on 'Clone or Download' ==> Click on 'Download ZIP' and save it on your local disk.

Installing in virtualenv
-------------------------
It's a good practice to install the project in a virtual env, especially if you are working on multiple python project

.. code-block:: bash
    $ python3 -m venv google
    $ cd google
    $ source bin/activate
    (google) $ git clone git@github.com:vandanabhandari/google-images-download.git
    (google) $ cd google-images-download/
    (google) $ pip install google_images_download