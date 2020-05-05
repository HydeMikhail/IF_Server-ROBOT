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

import time
import pigpio as gpio

iO = gpio.pi()


def set_outputs(pins):
    '''
    Takes list of GPIO pins (BCM) and sets them
    each as an output.
    '''
    for i in pins:
        iO.set_mode(i, gpio.OUTPUT)


class stepperA4988(object):
    '''
    Defines the State And Hardware Specs of
    a stepper motor
    '''

    def __init__(self, pins, step_res):

        set_outputs(pins)

        # Stepper Direction Pin
        self.dir_pin = pins[0]
        # Stepper Step Pin
        self.step_pin = pins[1]
        # Current Pose of Stepper in Steps
        self.current_step = 0

        # FULL STEP RESOLUTION
        if step_res == 'FULL':
            self.steps_per_rev = 200
            self.time_factor = 1
            iO.write(pins[4], 0)
            iO.write(pins[3], 0)
            iO.write(pins[2], 0)
        # HALF STEP RESOLUTION
        elif step_res == 'HALF':
            self.steps_per_rev = 400
            self.time_factor = 0.5
            iO.write(pins[4], 1)
            iO.write(pins[3], 0)
            iO.write(pins[2], 0)
        # QUARTER STEP RESOLUTION
        elif step_res == 'QURT':
            self.steps_per_rev = 800
            self.time_factor = 0.25
            iO.write(pins[4], 0)
            iO.write(pins[3], 1)
            iO.write(pins[2], 0)
        # EIGTH STEP RESOLUTION
        elif step_res == 'EGTH':
            self.steps_per_rev = 1600
            self.time_factor = 0.125
            iO.write(pins[4], 1)
            iO.write(pins[3], 1)
            iO.write(pins[2], 0)
        # SIXTEENTH STEP RESOLUTION
        elif step_res == 'SXTH':
            self.steps_per_rev = 3200
            self.time_factor = 0.0625
            iO.write(pins[4], 1)
            iO.write(pins[3], 1)
            iO.write(pins[2], 1)

    def plan_rotation(self, goalSteps):
        '''
        Determines the direction of the motor
        to achieve the desired position
        '''

        # Defines the magnitude of steps to acheive
        # desired position
        steps = goalSteps - self.current_step

        # POSITIVE MOTION CCW
        if steps > 0:
            iO.write(self.dir_pin, 0)
        # NEGATIVE MOTION CW
        else:
            iO.write(self.dir_pin, 1)
            steps *= -1

        return steps

    def step(self):
        '''
        One Step. Rotation and timing will be handled by the position
        supervisor.
        '''
        iO.write(self.step_pin, 1)
        iO.write(self.step_pin, 0)

    def manual_direction(self, direction):
        '''
        Method to manually dictate the direction of motor rotation
        '''
        if direction == 0:
            iO.write(self.dir_pin, 0)
        else:
            iO.write(self.dir_pin, 1)


class servo(object):
    '''
    Defines the state and hardware specs of the servo motor
    '''

    def __init__(self, logic_pin):
        self.logic_pin = logic_pin
        iO.set_servo_pulsewidth(logic_pin, 500)
        time.sleep(1)
        iO.set_servo_pulsewidth(logic_pin, 0)

    def extend(self):
        '''
        Rotates the servo to extend the activation
        mechanism
        '''
        iO.set_servo_pulsewidth(self.logic_pin, 925)

    def retract(self):
        '''
        Rotates the servo to retract the activation
        mechanism (ABSOLUTE 0 POSITION)
        '''
        iO.set_servo_pulsewidth(self.logic_pin, 500)

    def disable(self):
        '''
        Disables servo to avoid chattering while
        inactive.
        '''
        iO.set_servo_pulsewidth(self.logic_pin, 0)


class limitSwitch(object):
    '''
    Defines the state and hardware specs of the limit switch
    '''

    def __init__(self, logic_pin):
        self.logic_pin = logic_pin
        iO.set_mode(self.logic_pin, gpio.INPUT)

    def is_pressed(self):
        '''
        Checks the state of the limit switch. If high, the
        motor is at the X-Axis minor limit.
        '''
        return iO.read(self.logic_pin)
