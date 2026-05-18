=============================
Troubleshooting Errors/Issues
=============================

Link to `GitHub repo <https://github.com/hardikvasa/google-images-download>`__

Link to `Documentation Homepage <https://google-images-download.readthedocs.io/en/latest/index.html>`__

SSL Errors
==========

If you do see SSL errors on Mac for Python 3,
please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’
and run the file.

googleimagesdownload: command not found
=======================================

While using the above commands, if you get ``Error: -bash: googleimagesdownload: command not found`` then you have to set the correct path variable.

To get the details of the repo, run the following command:

.. code-block:: bash

    $ pip show -f google_images_download 

you will get the result like this:

.. code-block:: bash

	Location: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages
	Files:
	  ../../../bin/googleimagesdownload

together they make: ``/Library/Frameworks/Python.framework/Versions/2.7/bin`` which you need add it to the path:

.. code-block:: bash
	
    $ export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin"


[Errno 13] Permission denied creating directory 'downloads'
===========================================================

When you run the command, it downloads the images in the current directory (the directory from where you are running the command). If you get permission denied error for creating the `downloads directory`, then move to a directory in which you have the write permission and then run the command again.


Permission denied while installing the library
==============================================

On MAC and Linux, when you get permission denied when installing the library using pip, try doing a user install.

.. code-block:: bash
	
    $ pip install google_images_download --user

You can also run pip install as a superuser with ``sudo pip install google_images_download`` but it is not generally a good idea because it can cause issues with your system-level packages.


Installing the chromedriver (with Selenium)
===========================================

If you would want to download more than 100 images per keyword, then you will need to install 'selenium' library along with 'chromedriver' extension.

If you have pip-installed the library or had run the setup.py file, Selenium would have automatically installed on your machine. You will also need Chrome browser on your machine. For chromedriver:

`Download the correct chromedriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`__ based on your operating system.

On **Windows** or **MAC** if for some reason the chromedriver gives you trouble, download it under the current directory and run the command.

On windows however, the path to chromedriver has to be given in the following format:

``C:\\complete\\path\\to\\chromedriver.exe``

On **Linux** if you are having issues installing google chrome browser, refer to this `CentOS or Amazon Linux Guide <https://intoli.com/blog/installing-google-chrome-on-centos/>`__
or `Ubuntu Guide <https://askubuntu.com/questions/510056/how-to-install-google-chrome in documentation>`__

For **All the operating systems** you will have to use '--chromedriver' or '-cd' argument to specify the path of
chromedriver that you have downloaded in your machine.

If on any rare occasion the chromedriver does not work for you, try downgrading it to a lower version.


urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
==============================================

`Reference to this issue <https://github.com/hardikvasa/google-images-download/issues/140>`__

Use the below command to install the SSL certificate on your machine.

.. code-block:: bash
	
	cd /Applications/Python\ 3.7/
	./Install\ Certificates.command
