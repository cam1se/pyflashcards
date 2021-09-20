:github_url: https://github.com/flashcards/OpenFlashcards/tree/main/demos/python/sdk_wireless_camera_control

================
QuickStart Guide
================

.. warning:: This section assumes you have successfully :ref:`installed<Installation>` the package.


Flashcards installs with several command line demos to demonstrate BLE and Wi-Fi. The source code for these example
can be found in `$INSTALL/demos` where $INSTALL can be found with:

.. code-block:: console

    $ pip show open-flashcards

All of the demos have command-line help via the `--help` parameter. They also all log to the console as well
as write a more detailed log to a file (this file can be set with the `--log` parameter). The detailed log
is very helpful for diagnosing BLE / WiFi inconsistencies.

Photo Demo
----------

The `photo` demo will discover a Flashcards camera, connect to it, take a photo, and then download the
photo to your local machine. To run, do:

.. code-block:: console

    $ flashcards-photo

For more information, do:

.. code-block:: console

    $ flashcards-photo --help
    usage: flashcards-photo [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT]

    Connect to a Flashcards camera, take a photo, then download it.

    optional arguments:
    -h, --help            show this help message and exit
    -i IDENTIFIER, --identifier IDENTIFIER
                            Last 4 digits of Flashcards serial number, which is the last 4 digits of the default
                            camera SSID. If not used, first discovered Flashcards will be connected to
    -l LOG, --log LOG     Location to store detailed log
    -o OUTPUT, --output OUTPUT
                            Where to write the photo to. If not set, write to 'photo.jpg'

