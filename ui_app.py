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
from tkinter import font as tkFont

#from src.position_supervisor import positionSupervisor
from src.gui_util import generateRadioButtons, manPrime, startupMsg
from profiles.wpri_server import profile

#poseSuper = positionSupervisor([5, 6, 13, 19, 26], 'EGTH', 4, 17)

initChoice = input('Would you like to start the IF_Controller UI? [Y/n]   ')

if initChoice.lower() == 'y':

    startupMsg()

    # Main Window Config
    root = tk.Tk(className='WPRI-IF ::: Server Controller')
    root.geometry('900x350')
    root.grid_rowconfigure(0, weight=1, uniform='tom')
    root.grid_columnconfigure(0, weight=1, uniform='fred')

    # Define frames
    radioFrame = tk.Frame(root)
    radioFrame.grid(row=0, column=0, rowspan=2, columnspan=len(profile.keys()), sticky='')

    ptButtonFrame = tk.Frame(root)
    ptButtonFrame.grid(row=2, column=0, rowspan=4, sticky='W')

    cButtonFrame = tk.Frame(root)
    cButtonFrame.grid(row=2, column=0, rowspan=4, sticky='E')

    eFrame = tk.Frame(root)
    eFrame.grid(row=2, column=0, columnspan=4)

    # Defining font
    helv36 = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)

    # Tkinter Variables
    v = tk.IntVar(value=1)
    c = tk.StringVar(root)
    choices = ['FULL', 'HALF', 'QURT', 'EGTH', 'SXTH']
    c.set('EGTH')

    # Generate Control Buttons
    generateRadioButtons(profile, radioFrame, v)

    b1 = tk.Button(ptButtonFrame, text='Position', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID)#,command=lambda: poseSuper.positionxAxis(profile[v.get()][0]))
    b1.grid(row=2, column=1, columnspan=2, ipadx=2, ipady=2)
    b2 = tk.Button(ptButtonFrame, text='Take', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID)#,command=poseSuper.takeSwitch)
    b2.grid(row=4, column=1, columnspan=2, ipadx=2, ipady=2)

    b3 = tk.Button(cButtonFrame, text='Calibrate', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID)#,command=lambda: poseSuper.calibrate(profile[1][0]))
    b3.grid(row=2, column=1, columnspan=3, ipadx=2, ipady=2)
    b4 = tk.Button(cButtonFrame, text='Home', height=2, width=15,
                   font=helv36, borderwidth=2, relief=tk.SOLID) #,command=poseSuper.home)
    b4.grid(row=4, column=1, columnspan=3, ipadx=2, ipady=2)

    # Generate Manual Priming Controls
    e1 = tk.Entry(eFrame)
    e1.grid(row=3, column=2, columnspan=2, ipadx=2, ipady=2)
    but3 = tk.Button(eFrame, text='Manual Position', height=1, width=12, borderwidth=2,
                     relief=tk.SOLID) #, command=lambda: manPrime(e1, poseSuper))
    but3.grid(row=3, column=5, columnspan=2, ipadx=2, ipady=2)
    l1 = tk.Label(eFrame, text='X-Axis Jog')
    l1.grid(row=3, column=0, ipadx=2, ipady=2)

    m1 = tk.OptionMenu(eFrame, c, *choices)
    m1.grid(row=7, column=2, columnspan=2, ipadx=2, ipady=2)
    l2 = tk.Label(eFrame, text='Select Resolution')
    l2.grid(row=7, column=0, ipadx=2, ipady=2)
    but4 = tk.Button(eFrame, text='Change Res', height=1, width=12, borderwidth=2,
                     relief=tk.SOLID)
    but4.grid(row=7, column=5, columnspan=2, ipadx=2, ipady=2)

    # Calibrate
    #poseSuper.calibrate(profile[1][0])

    # Start UI
    root.mainloop()
