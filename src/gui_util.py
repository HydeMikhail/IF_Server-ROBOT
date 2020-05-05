#!/usr/bin/env python3

'''
WPRI-IF Robot Control Software
Copyright (C) 2020  Mikhail Hyde

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import tkinter as tk


def man_prime(entry, poseSuper):
    '''
    Allows user to manually set the X-Axis Pose
    '''
    temp = float(entry.get())
    print('Moving to %d mm' % temp)
    poseSuper.positionxAxis(temp)


def gen_radio_buttons(poseSuper, inProfile, frame, var):
    '''
    Generates radio buttons for each channel in the
    given profile
    '''
    for key in inProfile.keys():
        but = tk.Radiobutton(frame, text=inProfile[key][1],
                             variable=var, value=key, borderwidth=1,
                             width=8, relief=tk.SOLID,
                             command=lambda: poseSuper.positionxAxis(inProfile[var][0]))
        but.grid(row=0, column=key)


def startup_msg():
    '''
    Displays important information in terminal
    during program startup.
    '''
    print(
        '''
Welcome to the Index Finger Control System

This system is designed to remotely activate the channels
of a rack unit. Simply select the channel that you would
like to activate, press the Prime button to position the
switch, then the Take button to activate the switching
mechanism. The GUI is designed so that only one command
can be executed at once. For example, you cannot Take while
the system in Priming.

#############################
##       X-AXIS LIMIT      ##
#############################

      5 <= xPose <= 495

Please do not exceed this limit when manually setting
the X Position.

#############################
##          BUTTONS        ##
#############################

Radio Buttons (Top Row) - Selects Channel
Prime - Positions Switching Mechanism as currently selected Channel
Take - Commands the switcher to extend and retract, activating the button
       at the current location.
Manual Prime - Sets the X-Position to the value inside the entry box
Calibrate - Causes the Switching Mechanism to move in a negative direction
            along the X-Axis until the origin is met. It will then move one
            rotation positively from the origin.

#############################
##           HELP          ##
#############################

This program will start every time a terminal is opened. Please close the GUI
to access the terminal. To disable automatic startup, delete:

    python3 ~/wpri-if/ui_app.py

from the last line of ~/.bashrc.


SYSTEM IS CALIBRATING! UI WILL OPEN ONCE FINISHED!
    '''
    )
