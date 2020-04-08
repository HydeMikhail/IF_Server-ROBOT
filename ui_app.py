#!/usr/bin/env python3

'''
Main GUI Script
'''

#############################################################################
#############################################################################
##                                                                         ##
##                           IMPORTS                                       ##
##                                                                         ##
#############################################################################
#############################################################################

import tkinter as tk
from tkinter import font as tkFont

from src.position_supervisor import positionSupervisor
from profiles.wpri_server import profile

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

####    X-AXIS LIMIT    ####

      5 <= xPose <= 495

Please do not exceed this limit when manually setting
the X Position.

#############################
##                         ##
##          BUTTONS        ##
##                         ##
#############################

Radio Buttons (Top Row) - Selects Channel
Prime - Positions Switching Mechanism as currently selected Channel
Take - Commands the switcher to extend and retract, activating the button
       at the current location.
Manual Prime - Sets the X-Position to the value inside the entry box
Calibrate - Causes the Switching Mechanism to move in a negative direction
            along the X-Axis until the origin is met. It will then move one
            rotation positively from the origin.

This program will start every time a terminal is opened. Please close the GUI
to access the terminal. To disable automatic startup, delete:

    python3 ~/wpri-if/ui_app.py

from the last line of ~/.bashrc.


SYSTEM IS CALIBRATING! UI WILL OPEN ONCE FINISHED!
'''
)

#############################################################################
#############################################################################
##                                                                         ##
##                         HELPER FUNCTIONS                                ##
##                                                                         ##
#############################################################################
#############################################################################

poseSuper = positionSupervisor([17, 18, 27, 6, 12], 'HALF', 12, 23)


def manPrime():
    '''
    Allows user to manually set the X-Axis Pose
    '''
    temp = int(e1.get())
    print('Moving to %d mm' % temp)
    poseSuper.positionxAxis(temp)


def generateRadioButtons(inProfile):
    '''
    Generates radio buttons for each channel in the
    given profile
    '''
    for key in inProfile.keys():
        but = tk.Radiobutton(radioFrame, variable=v, value=key)
        but.grid(row=1, column=key)
        l = tk.Label(radioFrame, text=inProfile[key][1])
        l.grid(row=2, column=key)

#############################################################################
#############################################################################
##                                                                         ##
##                        TKINTER STRUCTURE                                ##
##                                                                         ##
#############################################################################
#############################################################################


initChoice = input('Would you like to start the IF_Controller UI? [Y/n]   ')

if initChoice.lower() == 'y':
    root = tk.Tk(className='WPRI-IF ::: Server Controller')
    root.geometry('900x350')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    radioFrame = tk.Frame(root)
    radioFrame.grid(row=0, column=0, rowspan=2, sticky='')

    ptButtonFrame = tk.Frame(root)
    ptButtonFrame.grid(row=2, column=0, rowspan=4, sticky='')

    cButtonFrame = tk.Frame(root)
    cButtonFrame.grid(row=8, column=0, rowspan=4, sticky='')

    eFrame = tk.Frame(root)
    eFrame.grid(row=6, column=0, columnspan=4)

    helv36 = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)

    v = tk.IntVar(value=1)

    generateRadioButtons(profile)

    b1 = tk.Button(ptButtonFrame, text='Prime', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID,
                   command=lambda: poseSuper.positionxAxis(profile[v.get()][0]))
    b1.grid(row=2, column=5, columnspan=2)
    b2 = tk.Button(ptButtonFrame, text='Take', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID,
                   command=poseSuper.takeSwitch)
    b2.grid(row=2, column=7, columnspan=2)

    b3 = tk.Button(cButtonFrame, text='Calibrate', height=1, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID,
                   command=lambda: poseSuper.calibrate(profile[1][0]))
    b3.grid(row=3, column=5, columnspan=3)

    e1 = tk.Entry(eFrame)
    e1.grid(row=3, column=2, columnspan=2)
    but3 = tk.Button(eFrame, text='Manual Prime', height=1, width=10, borderwidth=2,
                     relief=tk.SOLID, command=manPrime)
    but3.grid(row=3, column=5, columnspan=2)
    l1 = tk.Label(eFrame, text='X-Axis Jog')
    l1.grid(row=3, column=0)

    poseSuper.calibrate(profile[1][0])

    root.mainloop()
