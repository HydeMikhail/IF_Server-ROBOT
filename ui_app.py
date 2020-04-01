#!/usr/bin/env python3

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

#############################################################################
#############################################################################
##                                                                         ##
##                         HELPER FUNCTIONS                                ##
##                                                                         ##
#############################################################################
#############################################################################

poseSuper = positionSupervisor([11, 12, 13, 31, 32], 'HALF', 18, 16)


def manTake():
    poseSuper.positionxAxis(int(e1.get()))


def generateRadioButtons(inProfile):
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

v = tk.IntVar()

generateRadioButtons(profile)

b1 = tk.Button(ptButtonFrame, text='Prime', height=2, width=15,
               font=helv36, command=lambda: poseSuper.positionxAxis(profile[v.get()][0]))
b1.grid(row=2, column=5, columnspan=2)
b2 = tk.Button(ptButtonFrame, text='Take', height=2, width=15,
               font=helv36, command=poseSuper.takeSwitch)
b2.grid(row=2, column=7, columnspan=2)

b3 = tk.Button(cButtonFrame, text='Calibrate', height=1, width=15,
               font=helv36, command=poseSuper.calibrate)
b3.grid(row=3, column=5, columnspan=3)

e1 = tk.Entry(eFrame)
e1.grid(row=3, column=2, columnspan=2)
but3 = tk.Button(eFrame, text='Manual Prime', height=1, width=10,
                 command=manTake)
but3.grid(row=3, column=5, columnspan=2)
l1 = tk.Label(eFrame, text='X-Axis Jog')
l1.grid(row=3, column=0)

root.mainloop()
