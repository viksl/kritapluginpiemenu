# Pie Menu Krita Plugin

Discontinued, life happened, but there's a better one us this: https://krita-artists.org/t/shortcut-composer-v1-4-2-plugin-for-pie-menus-multiple-key-assignment-mouse-trackers-and-more/55314

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

Version: 0.4

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
    2. Open Krita
    3. Inside Krita in the top menu: Tools - Scripts - Import Python Plugin...
    4. In the pop up window open the file "kritapluginpiemenu-main.zip" from step 1.
    5. Restart Krita


    Method B
    1. Download this plugin from:
        https://github.com/viksl/kritapluginpiemenu
        (on the right side there's a green button labeled Code, press it
        then click on Download ZIP)
    2. Open the zip file, go to "kritapluginpiemenu-main/plugin" directory
        and there locate:
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
5. Quit pie menu without triggering any action:
    a/ Press the shortcut again
    b/ If you already pressed left mouse button/pen then before releasing the shortcut key then just release the shortcut key

## 4/ Adjustments you can make if needed:

Check the video in section 1/

## 5/ Known Issues
- Possible issues with Steam version (since steam has overlays and deals with shortcuts)
More investigation needed
- Some applications which steal keyEvents from Krita might cause the pie menu to get stuck
in general for single use it shouldn't be a problem but this needs testing with
recording/streaming apps if they cause problems or not. I tested this with OBS on windows 10
and there were NO problems.
(no solution for now other than restarting Krita)

## 6/ Possible future updates
- New actions
- New sections
- Proper Default Menu
- Pie menu settings
I’ll be cleaning the code everywhere now when the plugin seems to be pretty stable which includes unifying settings properties/variables to a single entitty which will hopefulyl allow me to create a new settings section (separate) for the visuals of the pie menu - distances, size, colors, … to be changed real time in Krita
(Depends on what is needed through testing, wishes, ..., feel free to let me know through krita-artists.org)


## 7/ Version Notes
0.4
- Fixing several major bugs
*(error: NoneType list, NoneType eventController, menu getting stucked, ...)*
- Reworked gizmo
*Now part of PieMenu paint method, access to gizmo through custom actions as a mandatory argument*
- Added QTimer.singleShot(...) for all events and menu init to queue the menu at the end of the event queue
- Added QTimer.singleShot(10, ...) for ColorSelector else it breaks down with shortcuts
- Reworked how initialization of the pieMenu works with the shortcut
- Quitting menu now possible (2 ways):
*a/ Before pressing down mouse left button/pen -> press the shortcut again*
*b/ If mouse left button/pen pressed while shortcut held down -> release the shortcut*
- Added init method call to custom actions
*There are now three methods for every custom action instead of having 1 general purpose init method:*
*1st method called once (at the beginning): init method*
*2nd method repeated calls: callback*
*3rd method called once (at the end): resetCallback*
- QTimer.singleShot(...) for any action invocation (init, callback, resetCallback, krita's default actions)
- Simplified the EventController, it's also more sturdy (needs a code clean up though ;))
- Added new action category: ANIMATION
- Added 13 new actions to Animation category
- Added 3 new custom actions:
*Confirm Transform, Reset Transform, Reset Transform (deselect)*
*(ctrl + T / Transform has been in the action list since the beginning)*
*Reset transform (deselect) - resets transform (esc key) and deselects at the end*
- Added cursor to pieMenu (cursorOverride)

0.3
- Added offset to where a submenu appears to make triggering the inital tool (which invoked the submenu) more reliable
(especially with short quick hand movement)
- I've updated the video to reflect new categories for actions and simpler installation process.
- Top post now contains info about written instructions on the plugins website which are noted before the video itself,
there's also a note about the length of the video to make sure people know there's a faster method to get started if needed.
(check the krita-artist thread for the video and discussion about the plugin)

0.2
- MacOS confirmed working
- Update to installation instruction and change to the directory structure of the plugin for simpler installation
- actionsList now has categories for actions (customizable)
- Categories are listed in the actions list for better visual clarity
- Fixed isolate_active_layer action
- Moved Select Opaque to a different category Misc - > Layer

0.1
- First Release
