# Class Launch Automator by Shaheer Sarfaraz

## Features

-   Open Zoom classes fully automatically based on time

-   Enter class details like the meeting code, the password and the time

-   Any number of classes can be present in the file and they will be opened at their respective time

## Format Of The Document

-   All file names are highlighted like `this`

-   File and folder names are mentioned relative to the folder you extract after downloading the `.zip` file

## Installation

-   Follow [this](https://github.com/DaKheera47/scheduled-class-launcher/archive/refs/heads/master.zip) link and download the .zip file

-   Extract the files to any folder (always keep them in the same folder structure)

-   See available features in the `build` folder

-   You may create a shortcut of any of these files

## Pre-requisites

-   Install Python from [here](https://www.python.org/downloads/)
-   Ensure that you tick the "Add Python 3.9 to PATH" option

-   Reopen any Command Prompt windows after installing Python
-   Open a `cmd` window in the same directory as the extracted files

## One Time Installation

-   Navigate to the installed folder and pressing the shortcut `alt + d` on your keyboard
-   Now, enter `cmd` without pressing anything else
-   A black Command Prompt window should show up
-   Paste this command in the black window: `pip install -r requirements.txt`
-   Wait for the installation to finish, after which you'll will be able to use the files in the `build` folder

## Required Zoom Settings

-   The "Automatically join audio by computer when joining a meeting" checkbox in the Zoom Audio settings must be unticked.
-   You must be logged in to a Google Account before starting any of the files in the `build` folder

## Reference for files in the `build` folder

### `manualClassLauncher.bat`

-   Can choose class to launch by yourself

-   All classes will be listed from `classes.yaml`

### `scheduledClassLauncher.bat`

-   Keeps checking for classes in the background, in a black `cmd` window, that can be minimized

-   Will check for classes in `classes.yaml` every minute

-   Will join class on its time automatically

## Frequently Asked Questions

#### How to add or remove classes?

-   Open the `classes.yaml` file found in the `config` folder in any text editor of your preference. Notepad is a quick and easy solution.

-   The format is available in the file in the form of comments

-   Relaunch the program to see your changes reflected

## Limitations

-   Only Windows 10 is supported. Other operating systems might work, but use at your own discretion

### Contact Me

-   Discord: `ShaheerSarfaraz#1532`
