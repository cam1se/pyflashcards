:github_url: https://github.com/flashcards/OpenFlashcards/tree/main/demos/python/sdk_wireless_camera_control

============
Installation
============

Stable release
--------------

To install Flashcards, run this command in your terminal:

.. code-block:: console

    $ pip install open-flashcards

This is the preferred method to install Flashcards, as it will always install the most recent stable release
from `PyPi <https://pypi.org/project/open-flashcards/>`_ .

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

The sources for Flashcards can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone https://github.com/flashcards/OpenFlashcards

Or download the `zip`_:

.. code-block:: console

    $ curl  -OL https://github.com/flashcards/OpenFlashcards/archive/refs/heads/main.zip

Once you have a copy of the source, you can install it:

First, enter the directory where the source code exists

.. code-block:: console

    $ cd OpenFlashcards/demos/python/sdk_wireless_camera_control

Then install the package

.. code-block:: console

    $ pip install .

.. _Github repo: https://github.com/flashcards/OpenFlashcards
.. _zip: https://github.com/flashcards/OpenFlashcards/archive/refs/heads/main.zip

For Developers
**************

The above installation will not install Flashcards in editable mode. If you want to modify the package, you
should install it as such:

.. code-block:: console

    $ pip install -r requirements-dev.txt -r requirements.txt
