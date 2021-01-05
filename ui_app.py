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

from src.position_supervisor import positionSupervisor
from src.gui_util import gen_buttons, man_prime, startup_msg
from profiles.wpri_server import profile

_poseSuper = positionSupervisor([5, 6, 13, 19, 26], 'EGTH', 4, 17)

_initChoice = input('Would you like to start the IF_Controller UI? [Y/n]   ')

if _initChoice.lower() == 'y':

    startup_msg()

    # Main Window Config
    root = tk.Tk(className='WPRI-IF ::: Server Controller')
    root.geometry('950x350')
    root.grid_rowconfigure(0, weight=1, uniform='tom')
    root.grid_columnconfigure(0, weight=1, uniform='fred')

    # Define frames
    radioFrame = tk.Frame(root)
    radioFrame.grid(row=0, column=0,
                    columnspan=8, sticky='')

    ptButtonFrame = tk.Frame(root)
    ptButtonFrame.grid(row=2, column=0, rowspan=4, sticky='W')

    cButtonFrame = tk.Frame(root)
    cButtonFrame.grid(row=2, column=0, rowspan=4, sticky='E')

    eFrame = tk.Frame(root)
    eFrame.grid(row=2, column=0, columnspan=4)

    # Defining font
    helv36 = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)

    # Tkinter Variables for Step Resolution
    c = tk.StringVar(root)
    choices = ['QURT', 'EGTH', 'SXTH']
    c.set('EGTH')

    # Generate Control Buttons
    gen_buttons(_poseSuper, profile, radioFrame)

    takeButton = tk.Button(ptButtonFrame, text='Take', height=2, width=15,
                           font=helv36, borderwidth=2, relief=tk.SOLID,
                           command=_poseSuper.take_swtich)
    takeButton.grid(row=4, column=1, columnspan=2, ipadx=2, ipady=2)

    calibrateButton = tk.Button(cButtonFrame, text='Calibrate', height=2, width=15,
                                font=helv36, borderwidth=2, relief=tk.SOLID,
                                command=lambda: _poseSuper.calibrate(profile[1][0]))
    calibrateButton.grid(row=2, column=1, columnspan=3, ipadx=2, ipady=2)
    homeButton = tk.Button(cButtonFrame, text='Home', height=2, width=15,
                           font=helv36, borderwidth=2, relief=tk.SOLID,
                           command=_poseSuper.home)
    homeButton.grid(row=4, column=1, columnspan=3, ipadx=2, ipady=2)

    # Generate Manual Priming Controls
    entry = tk.Entry(eFrame)
    entry.grid(row=3, column=2, columnspan=2, ipadx=2, ipady=2)
    manButton = tk.Button(eFrame, text='Manual Position', height=1, width=12,
                          borderwidth=2, relief=tk.SOLID,
                          command=lambda: man_prime(entry, _poseSuper))
    manButton.grid(row=3, column=5, columnspan=2, ipadx=2, ipady=2)
    label1 = tk.Label(eFrame, text='X-Axis Jog')
    label1.grid(row=3, column=0, ipadx=2, ipady=2)

    menu = tk.OptionMenu(eFrame, c, *choices)
    menu.grid(row=7, column=2, columnspan=2, ipadx=2, ipady=2)
    label2 = tk.Label(eFrame, text='Select Resolution')
    label2.grid(row=7, column=0, ipadx=2, ipady=2)
    resButton = tk.Button(eFrame, text='Change Res', height=1, width=12,
                          borderwidth=2, relief=tk.SOLID,
                          command=lambda: _poseSuper.update_res([5, 6, 13, 19, 26], c.get(), 4, 17))
    resButton.grid(row=7, column=5, columnspan=2, ipadx=2, ipady=2)

    # Calibrate
    _poseSuper.calibrate(profile[1][0])

    # Start UI
    root.mainloop()
