# YouTube-Uploader-for-Reddit-Compilations-POC
This Project is a **Proof Of Concept** to prove one way of how Automated Compilation Channels work on Youtube.
Automatically Downloading Reddit Clips, merging them into compilations using FFMPEG and uploading them on Youtube using [Selenium](https://github.com/SeleniumHQ/selenium) ( + [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)).

> [!IMPORTANT]
> **PLEASE READ:** I uploaded this as a personal "archive" and to help others take ideas, Currently there are no Plans to Update or even Maintain this But at the end of this README i am gonna give some ideas to bypass possible issues.

## Simple workflow Diagram (2022-2023)
![Youtube Compilation Uploader](https://github.com/EvanLei-git/YouTube-Uploader-for-Reddit-Compilations-POC/assets/71707767/f43ad688-8e4a-44e3-b4bc-6052697365e8)

### Why did i not use Google's API to upload my videos?
I tried many times applying for a google api key from different accounts but after a week the api key wouldnt work, have issues or just be rejected.


## Manual Work:
1. Removing copyright claimed sections using youtube's editor.

2. Thumbnails - by finding random public image sites/drives or blog pages.

3. Video Titles will all be the same in all videos OR you can create a script to choose from a link of AI generated titles.(i edited them manually)

4. Profile Pictures. (AI generated)

5. Channel's ABOUT description. (AI generated)

6. Making videos PUBLIC. 

(6th can be done automatically but first the best idea would be to clean copyrighted parts instead of unlisting/privatizing videos which can ruin your algorithm)


## Testing Channel Showcase 

Channel Link: https://www.youtube.com/@Quirkitty/videos

[![image](https://github.com/EvanLei-git/YouTube-Uploader-for-Reddit-Compilations-POC/assets/71707767/852d4627-6ba7-4d23-a05f-34b73a609a61)](https://www.youtube.com/@Quirkitty/videos)


## Solution to some issues you will face:

* Use [pullpush.io](https://www.pullpush.io/) instead of Pushshift.io

> Because Pushshift.io is only available for mod accounts.

* Use [SeleniumBase](https://github.com/seleniumbase/SeleniumBase) instead of  undetected-chromedriver

> undetected-chromedriver is outdated, dev is rebuilding it from the ground up.(no deadline announced)

OR instead of building your own youtube autoclicker, there are a few **Ready to Use** Scripts you can use.

* [selenium_youtube](https://github.com/kkristof200/selenium_youtube) by kkristof200

* [youtube_uploader_selenium](https://github.com/linouk23/youtube_uploader_selenium) by linouk23

A different and more complicated way would be to use a **Portable browser** with a custom **Tampermonkey** script.
The script would communicate with a simple **Flask server** to send the videos' path and information like title, description...
While also achieving the autoclicking buttons part.

^ I would only recommend this if you are up for a challenge :)

