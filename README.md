# Pie Menu Krita Plugin

Author: viksl

Github: https://github.com/viksl

Github for this project: https://github.com/viksl/kritapluginpiemenu

Krita version: 4.4.1

Licence:
- See file LICENSE

- GNU GENERAL PUBLIC LICENSE

- Version 3

- <https://www.gnu.org/licenses/>

Copyright: (C) viksl

Release Date: 19.12.2020

Version: 0.1

Default shortcut: ` + (Mouse left/middle button or Pen touch)

## 1/ Description:

  - Free plugin for Krita (<https://krita.org>)
  - Youtube video (<https://youtu.be/-rUf6Qz3nwU>)

Pie Menu plugin allows you to set up your own custom menu for a quick access of various tools and actions in Krita to streamline the whole painting process.

*Visuals*

![PieMenu1](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenu1.png)

![PieMenu2](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenu1.png)

*Settings:*

![PieMenuSettings](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenu1.png)

## 2/ Installation:

    Method A
     1. Download this plugin from:
        https://github.com/viksl/kritapluginpiemenu
        (on the right side there's a green button labeled Code, press it
        then click on Download ZIP)
    2. Open the zip file and locate file "kritapluginpiemenu.zip" inside
    3. Open Krita
    4. Inside Krita in the top menu: Tools - Scripts - Import Python Plugin...
    5. In the pop up window open the file "kritapluginpiemenu.zip" from step 2.
    6. Restart Krita


    Method B
    1. Download this plugin from:
        https://github.com/viksl/kritapluginpiemenu
        (on the right side there's a green button labeled Code, press it
        then click on Download ZIP)
    2. Open the zip file and locate file "kritapluginpiemenu.zip" inside
    3. Locate directory "kritapluginpiemenu", "kritapluginpiemenu.desktop"
        and "kritapluginpiemenu.action" file inside "kritapluginpiemenu" directory
    4. Copy the "kritapluginpiemenu.desktop" and the directory to pykrita directory
        located through: Open Krita, go to:
        Settings
            - Manage Resources...
                - Press the button Open Resource Folder
                (there you can find the pykrita directory)
    5. Copy "kritapluginpiemenu.action" to directory: Open Krita, go to:
        Settings
            - Manage Resources...
                - Press the button Open Resource Folder
                (there you can find the actions directory)
    6. Restart Krita
    7. Enable the plugin
        Settings
            - Configure Krita ...
                - Python Plugin Manager
                (Locate name Pie Menu and tick it to enable it)
                Press OK
    8. Restart Krita
    9. Setup your shortcut
        Settings
            - Configure Krita ...
                - Keyboard Shortcuts
                (Locate action: Scripts - Pie Menu)
                Change the shortcut to whatever you like
                (default shortcut is: `)

## 3/ How to use:

-   Settings

First set up your Pie Menu through krita's top menu: Tools - Scripts - Pie Menu Settings.
In settings you can:
1. Set the number of sections of the base menu
2. Assign actions to sections
3. Set any action as a submenu (opens a sub pie menu)

-   Use

1. Press the shortcut, press the left mouse button or use your pen on your tablet/screen to trigger the Pie menu.
2. Slide the cursor to an option in the menu.
3. Depending on type of action you have assigned in pie menu's settings the action:
    a. Gets triggered immediately
    b. Opens a submenu
    c. Gets triggered by releasing left mouse button or lifting the pen
4. If the action requires it you might need to move the pen around, for example:
    If the action is Brush Size then moving pen left and right changes the size of the brush

## 4/ Adjustments you can make if needed:

Check the video in section 1/.

## 5/ Known Issues
None (will be updated when something appears)

## 6/ Possible future updates
- New actions
Currently no plans, depends on what is needed through testing, feel free to let me know here:
