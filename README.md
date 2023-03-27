# WhatsApp Android Image Scraper

Basic script that downloads all images of a given WhatsApp chat using Android automation.

**Preview**

![Video](WAIS.gif)

## Description

**Note:** In its current state this script will not work "plug-and-play". It currently 
(barely) works for this niche use-case, but might be helpful for others to get a starting
point from.

This script uses Python and the **A**ndroid **D**ebug **B**ridge (ADB) to automatically download
all images within a given chat. It does this by emulating touch inputs (via ADB) and reading
the screen and locating text (via [Tesseract](https://github.com/tesseract-ocr/tesseract)).

The following steps have been implemented:

0. The newest (first) image of a given chat's gallery should be open.
1. Select the menu (using xy position)
1. Select "Share" (using OCR for "Share")
1. Select Dropbox (using OCR for "Dropbox")
1. Select "Add to Dropbox" (using OCR for "Add")
1. Select "Upload here" (using xy position)
    1. Check if image already exists and reupload if does (using OCR for "Replace")
1. Close Dropbox (using xy position)
1. Swipe to next image

## Getting Started

### Dependencies

The following external programs need to exist for this to run:
* ADB - to control the Android phone (I used [this XDA article](https://www.xda-developers.com/install-adb-windows-macos-linux/) to set up)
* python (>3.6)
* [Tesseract](https://github.com/tesseract-ocr/tesseract) - for OCR of screenshots
* [scrcpy](https://github.com/Genymobile/scrcpy) [Optional] - to mirror phone screen to computer

**Note:** I have only tested this on Linux, though no reason it should not work in MacOS/ Windows

### Installing

To install all dependencies run:

```bash
pip install -r requirements.txt
```

### Execute the script

* Ensure that your phone has been setup in developer mode and is setup to
use ADB
* [Optional] Start `scrcpy`
* Run the script and following the prompts on screen
    ```
    python wais.py
    ```


## Authors

[@OllieFritz](https://olliefritz.com/)

## To-dos
- [ ] Increase robustness of each step
- [ ] Refactor to make each step a combination of _Action_, _Collection_ and _Validation_.
- [ ] Make it more generally usable (if interest)

## Acknowledgments

Inspiration, code snippets, etc.
- [Pytesseract StackOverflow](https://stackoverflow.com/questions/71983792/how-to-paint-a-rectangle-over-words/71984673#71984673)
- [ADB install](https://www.xda-developers.com/install-adb-windows-macos-linux/)
- [PYIO Automate's video](https://www.youtube.com/watch?v=6cvGOiurzts)
- [Engineer Man's video](https://www.youtube.com/watch?v=Du__JfXqsAs)

Thank you to all of the above
