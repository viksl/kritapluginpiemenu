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

Release Date: 21.12.2020

Version: 0.2

Default shortcut: ` + (Mouse left/middle button or Pen touch)

## 1/ Description:

  - Free plugin for Krita (<https://krita.org>)
  - Youtube video (<https://youtu.be/BkhT7v-eOnE>)
  - Krita Artists thread (<https://krita-artists.org/t/plugin-pie-menu-v0-1/15888>)

Pie Menu plugin allows you to set up your own custom menu for a quick access of various tools and actions in Krita to streamline the whole painting process.

*Visuals*

![PieMenu1](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenu1.png)

![PieMenu2](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenu2.png)

*Settings:*

![PieMenuSettings](https://github.com/viksl/kritapluginpiemenu/blob/main/images/piemenusettings.png)

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
    2. Open the zip file and inside kritapluginpiemenu-main locate:
        - Directories "pykrita" and "actions"
    3. Copy both directories "pykrita" and "actions" to the resource directory
        located through: Open Krita, go to:
        Settings
            - Manage Resources...
                - Press the button "Open Resource Folder"
                (this opens the resource directory)
    4. If overwrite dialog appears during copying let it overwrite (Yes)
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

-   **Settings**

First set up your Pie Menu through krita's top menu: Tools - Scripts - Pie Menu Settings.
In settings you can:
1. Set the number of sections of the base menu
2. Assign actions to sections
3. Set any action as a submenu (opens a sub pie menu)
    -   Action with (c) at the end of its name cannot be used to open a submenu

-   **Use**

1. Press the shortcut, press the left mouse button or use your pen on your tablet/screen to trigger the Pie menu.
2. Slide the cursor to an option in the menu.
3. Depending on type of action you have assigned in pie menu's settings the action:
    a. Gets triggered immediately
    b. Opens a submenu
    c. Gets triggered by releasing left mouse button or lifting the pen
4. If the action requires it you might need to move the pen around, for example:
    If the action is Brush Size then moving pen left and right changes the size of the brush

## 4/ Adjustments you can make if needed:

Check the video in section 1/

## 5/ Known Issues
- Some applications which steal keyEvents from Krita might cause the pie menu to get stuck
in general for single use it shouldn't be a problem but this needs testing with
recording/streaming apps if they cause problems or not. I tested this with OBS on windows 10
and there we NO problems.
(no solution for now other than restarting Krita)

## 6/ Possible future updates
- New actions

(Depends on what is needed through testing, wishes, ..., feel free to let me know through krita-artists.org)

## 7/ Version Notes
0.1
- First Release

0.2
- MacOS confirmed working
- Update to installation instruction and change to the directory structure of the plugin for simpler installation
- actionsList now has categories for actions (customizable)
- Categories are listed in the actions list for better visual clarity