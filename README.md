# PHONETETHER

```
________________________________________________________________________________

     ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗████████╗███████╗████████╗██╗  ██╗███████╗██████╗ 
     ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝╚══██╔══╝██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
     ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗     ██║   █████╗     ██║   ███████║█████╗  ██████╔╝
     ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝     ██║   ██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
     ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║   ███████╗   ██║   ██║  ██║███████╗██║  ██║
     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                     
________________________________________________________________________________

     CONTROL ANDROID PHONE FROM LAPTOP | USB + WI-FI | LOW LATENCY

________________________________________________________________________________
```

## DESCRIPTION

PhoneTether is a complete Android phone control solution for laptop users. It provides low-latency screen mirroring, touch control, keyboard input, screenshot capture, and screen recording over both USB and Wi-Fi connections.

Built on ADB (Android Debug Bridge) and scrcpy, PhoneTether allows you to control your phone directly from your computer mouse and keyboard.

## INSTALLATION

### 1. Install ADB

```
LINUX:  $ sudo apt install adb
MAC:    $ brew install android-platform-tools
WIN:    Download from developer.android.com
```

### 2. Install SCRCPY

```
LINUX:  $ sudo apt install scrcpy
MAC:    $ brew install scrcpy
WIN:    Download from github.com/Genymobile/scrcpy
```

### 3. Install Python Library

```
$ pip install Pillow
```

### 4. Clone and Run

```
$ git clone https://github.com/saifulislaam/PhoneTether.git
$ cd PhoneTether
$ python3 phonetether.py
```

## PHONE SETUP (ONE TIME)

```
[1] SETTINGS > ABOUT PHONE > TAP BUILD NUMBER 7 TIMES
[2] SETTINGS > SYSTEM > DEVELOPER OPTIONS
[3] ENABLE USB DEBUGGING
[4] CONNECT USB CABLE
[5] ACCEPT RSA KEY ON PHONE
```

## USAGE

```
1. RUN: $ python3 phonetether.py

2. IN THE APPLICATION:
   > CLICK "REFRESH DEVICES"
   > CLICK "CONNECT USB"
   > CLICK "START MIRRORING"

3. CONTROL:
   > CLICK ON MIRROR WINDOW = TAP ON PHONE
   > USE KEYBOARD = TYPE TEXT
   > CTRL+H = HOME BUTTON
   > CTRL+B = BACK BUTTON
   > CTRL+S = SCREENSHOT
   > CTRL+R = START/STOP RECORDING
```

## OUTPUT FILES

```
screenshots/     screenshot_YYYYMMDD_HHMMSS.png
recordings/      recording_YYYYMMDD_HHMMSS.mp4
```

## LICENSE

MIT

## AUTHOR

saifulislaam

```
________________________________________________________________________________
```
