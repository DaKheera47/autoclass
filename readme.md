
# Class Launch Automator by Shaheer Sarfaraz

## Features

-   Open Zoom classes in a completely automated manner, based on class timings
-   Enter class details like the meeting code and the password of the meeting automatically
-   Any number of classes can be launched automatically at their scheduled timings
-   Support for different timings on Friday

## Format Of The Document

-   All proper names are highlighted like `this`

## Installation

-   Follow [this](https://github.com/DaKheera47/scheduled-class-launcher/blob/master/build/installationFromScratch.bat) link and download the .bat file
-   Run the file by double clicking. Ignore all warnings by Windows, as this software is completely virus free
-   To ignore warnings click on "More info", and "Run anyway"
-   Will take considerable time, so be patient (~20 minutes on 16mbps internet)

## Required Zoom Settings

-   The "Automatically join audio by computer when joining a meeting" checkbox in the Zoom Audio settings must be unticked.

## Reference for files in the `build` folder

### `manualClassLauncher.bat`

-   Can choose class to launch by yourself
-   All classes will be listed from `classes.yaml`

### `scheduledClassLauncher.bat`

-   Keeps checking for classes in the background, in a black `cmd` window, that can be minimized
-   Will check for classes in `classes.yaml` every minute
-   Will join class on its time automatically

### `firstInstall.bat`

-   Installs all necessary programs needed for the program to work.
-   Installs Zoom (used for classes), OBS Studio (to record classes) & Python (the language of the program)
-   Will take considerable time, so be patient (~20 minutes on 16mbps internet)

### `installationFromScratch.bat`

-   Installs all necessary programs needed for the program to work.
-   Installs Zoom (used for classes), OBS Studio (to record classes) & Python (the language of the program)
-   Additionally, also downloads the source code to the same folder, and executes the `scheduledClassLauncher.bat`
-   Will take considerable time, so be patient (~20 minutes on 16mbps internet)

## Customizability

#### How to add or remove classes?

-   Open the `classes.yaml` file found in the `config` folder in any text editor of your preference. Notepad is a quick and easy solution.
-   The example format is available in the file
-   Relaunch the program to see your changes reflected

#### How to change configuration?

-   Open the `config.yaml` file found in the `config` folder in any text editor of your preference. Notepad is a quick and easy solution.
-   Format:
    -   `variableName`: [possible values] description
-   Variable's in configuration:
    -   `delayBetweenActions`: [number] changes the delay (in s) between every action that the computer will perform. Decreasing it will make the program faster, but will also result in more chances of failure. If you have a somewhat slow computer, you might want to increase this value
    -   `requireConfirmation`: [True/False] changes if the program will require confirmation before joining a class. A small window opens, which reveals an "OK" button, and a "Cancel" Button. Choosing "OK" will launch the class meeting
    -   `recordClasses`: [True/False] decides if you want to record a class by starting OBS Studio before the meeting
    -   `timeToRecordClass`: [number] decides how long you want the program to set the recording to be
-   Relaunch the program to see your changes reflected

## Limitations

-   Only Windows 10 & 11 is supported officially. Other operating systems might work, but use at your own discretion

### Contact Me

-   Discord: `ShaheerSarfaraz#1532`
