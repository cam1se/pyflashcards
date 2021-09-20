:github_url: https://github.com/flashcards/OpenFlashcards/tree/main/demos/python/sdk_wireless_camera_control

Flashcards Python SDK
=====================

.. figure:: https://raw.githubusercontent.com/flashcards/OpenFlashcards/main/docs/assets/images/logos/logo.png
    :alt: Flashcards Logo
    :width: 50%

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/
    :alt: MIT License

.. image:: https://img.shields.io/github/workflow/status/flashcards/OpenFlashcards/Python%20SDK%20Testing?label=Build%20and%20Test
    :target: https://github.com/flashcards/OpenFlashcards/actions/workflows/python_sdk_test.yml
    :alt: Build and Test

.. image:: https://img.shields.io/github/workflow/status/flashcards/OpenFlashcards/Python%20SDK%20Docs%20Build%20and%20Deploy?label=Docs
    :target: https://github.com/flashcards/OpenFlashcards/actions/workflows/python_sdk_deploy_docs.yml
    :alt: Build Docs

.. image:: https://img.shields.io/pypi/v/open-flashcards
    :target: https://pypi.org/project/open-flashcards/
    :alt: PyPI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black

.. image:: _static/coverage.svg
    :alt: Coverage

Summary
-------

Welcome to the Flashcards Python package documentation. This is a Python package that provides an
interface for the user to exercise the Flashcards Bluetooth Low Energy (BLE) and Wi-Fi API's.

This package implements the API as defined in the `Flashcards Specification <https://flashcards.github.io/OpenFlashcards/>`_ .
For more information on the API, see the relevant documentation:

- `BLE API <https://flashcards.github.io/OpenFlashcards/ble>`_
- `Wi-Fi API <https://flashcards.github.io/OpenFlashcards/wifi>`_


Features
--------

- Top-level Flashcards class interface to use both BLE / WiFi
- Cross-platform (tested on MacOS Big Sur, Windows 10, and Ubuntu 20.04)

    - BLE controller implemented using `bleak <https://pypi.org/project/bleak/>`_
    - Wi-Fi controller provided in the Flashcards package (loosely based on the `Wireless Library <https://pypi.org/project/wireless/>`_ )
- Supports all commands, settings, and statuses from the `Flashcards API <https://flashcards.github.io/OpenFlashcards/>`_
- Supports all versions of the Flashcards API
- Automatically handles connection maintenance:

    - manage camera ready / encoding
    - periodically sends keep alive signals
- Includes detailed logging for each module
- Includes demo scripts installed as command-line applications to show BLE and WiFi functionality such as:

    - Take a photo
    - Take a video
    - View the live stream
    - Log the battery

Getting Started
---------------

Here is a suggested procedure for getting acquainted with this package (it is the same as reading through
this document in order):

#. :ref:`Install<Installation>` the package
#. Try some of the :ref:`demos<QuickStart Guide>`
#. Implement your own example, perhaps starting with a demo, with :ref:`usage<Usage>` information
#. If you need more detailed implementation reference, see the Interface :ref:`documentation<Interfaces>`

.. toctree::
    :maxdepth: 4
    :caption: Contents:

    installation
    quickstart
    usage
    api
    contributing
    authors
    changelog
    future_work
