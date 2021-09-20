# Flashcards Python SDK

<img alt="Flashcards Logo" src="https://raw.githubusercontent.com/flashcards/OpenFlashcards/main/docs/assets/images/logos/logo.png" width="50%" style="max-width: 500px;"/>

[![Build and Test](https://img.shields.io/github/workflow/status/flashcards/OpenFlashcards/Python%20SDK%20Testing?label=Build%20and%20Test)](https://github.com/flashcards/OpenFlashcards/actions/workflows/python_sdk_test.yml)
[![Build Docs](https://img.shields.io/github/workflow/status/flashcards/OpenFlashcards/Python%20SDK%20Docs%20Build%20and%20Deploy?label=Docs)](https://github.com/flashcards/OpenFlashcards/actions/workflows/python_sdk_deploy_docs.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/open-flashcards)](https://pypi.org/project/open-flashcards/)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/flashcards/OpenFlashcards/blob/main/LICENSE)

This is a Python package that provides an interface for the user to exercise the Flashcards Bluetooth Low
Energy (BLE) and Wi-Fi API's as well as install command line interfaces to take photos, videos, and view
the preview stream.

-   Free software: MIT license
-   Documentation: [View on Flashcards](https://flashcards.github.io/OpenFlashcards/python_sdk/)
-   View on [Github](https://github.com/flashcards/OpenFlashcards/tree/main/demos/python/sdk_wireless_camera_control)

## Documentation

> This README is only an overview of the package.

Complete documentation can be found on [Flashcards](https://flashcards.github.io/OpenFlashcards/python_sdk/)

## Installation

```console
    $ pip install open-flashcards
```

## Features

-   Top-level Flashcards class interface to use both BLE / WiFi
-   Cross-platform (tested on MacOS Big Sur, Windows 10, and Ubuntu 20.04)
    -   BLE implemented using [bleak](https://pypi.org/project/bleak/)
    -   Wi-Fi controller provided in the Flashcards package (loosely based on the [Wireless Library](https://pypi.org/project/wireless/)
-   Supports all commands, settings, and statuses from the [Flashcards API](https://flashcards.github.io/OpenFlashcards/)
-   Supports all versions of the Flashcards API
-   Automatically handles connection maintenance:
    -   manage camera ready / encoding
    -   periodically sends keep alive signals
- Includes detailed logging for each module
-   Includes demo scripts installed as command-line applications to show BLE and WiFi functionality
    -   Take a photo
    -   Take a video
    -   View the live stream
    -   Log the battery

## Usage

To automatically connect to Flashcards device via BLE and WiFI, set the preset, set video parameters, take a
video, and download all files:

```python
import time
from pyflashcards import Flashcards

with Flashcards() as flashcards:
    flashcards.ble_command.load_preset(flashcards.params.Preset.CINEMATIC)
    flashcards.ble_setting.resolution.set(flashcards.params.Resolution.RES_4K)
    flashcards.ble_setting.fps.set(flashcards.params.FPS.FPS_30)
    flashcards.ble_command.set_shutter(flashcards.params.Shutter.ON)
    time.sleep(2) # Record for 2 seconds
    flashcards.ble_command.set_shutter(flashcards.params.Shutter.OFF)

    # Download all of the files from the camera
    media_list = [x["n"] for x in flashcards.wifi_command.get_media_list()["media"][0]["fs"]]
    for file in media_list:
        flashcards.wifi_command.download_file(camera_file=file)
```

And much more!

## Demos

> Note! These demos can be found on [Github](https://github.com/flashcards/OpenFlashcards/tree/main/demos/python/sdk_wireless_camera_control/pyflashcards/demos)

Demos can be found in the installed package in the "demos" folder. They are installed as a CLI entrypoint
and can be run via:

```bash
$ flashcards-photo
```

```bash
$ flashcards-video
```

```bash
$ flashcards-stream
```

```bash
$ flashcards-log-battery
```

```bash
$ flashcards-log-battery
```

For more information on each, try running with help as such:

```bash
$ flashcards-photo --help

usage: flashcards-photo [-h] [-i IDENTIFIER] [-l LOG] [-o OUTPUT]

Connect to a Flashcards camera, take a photo, then download it.

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTIFIER, --identifier IDENTIFIER
                        Last 4 digits of Flashcards serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered Flashcards will be connected to
  -l LOG, --log LOG     Location to store detailed log
  -o OUTPUT, --output OUTPUT
                        Where to write the photo to. If not set, write to 'photo.jpg'
```
