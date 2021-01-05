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
from src.constants import pulleyDiam, maxTime
from src.hardware import stepperA4988, servo, limitSwitch


def _linear_to_steps(linearPose, stepsPerRev):
    '''
    Take a desired linear position as input and converts it
    to a step magnitude for the stepper motor
    '''
    return int(linearPose / (pulleyDiam / stepsPerRev))  # Integer Number of Steps


def _acc_profile(current_step, pathMag, minTime):
    '''
    Calulates discrete time intervals to genearate
    acceleration and deceleration in X-Axis motion.
    '''

    # Slowest time interval
    disTime = maxTime

    # When Stepper is in first revolution
    if current_step < 400:
        disTime = maxTime - (current_step
                             * ((maxTime - minTime) / 400))

    # When Stepper is in last revolution
    elif current_step > pathMag - 400:
        disTime = maxTime - ((pathMag - current_step)
                             * ((maxTime - minTime) / 400))

    # Between First and Last Rev (MAX SPEED)
    else:
        disTime = minTime

    return disTime


class positionSupervisor(object):
    '''
    Handles positioning and calibration of Index Finger System.

    X-Axis (Stepper Motor) - Linear Position on Ball Screw
    Z-Axis (Servo Motor)   - Extends and Retracts Index Finger
    Origin (Limit Switch)  - Marks the 0 of the X-Axis for Cal
    '''

    def __init__(self, stepperPins, resolution, servoPin, limitPin):
        self.x_axis = stepperA4988(stepperPins, resolution)
        self.z_axis = servo(servoPin)
        self.origin = limitSwitch(limitPin)

    def _move_until(self):
        while True:
            self.x_axis.manual_direction(1)
            if self.origin.is_pressed():
                self.x_axis.current_step = 0
                time.sleep(0.25)
                break

            self.x_axis.step()
            time.sleep(0.0005)

    def positionx_axis(self, linearPose):
        '''
        Positions the x_axis at a given linear pose
        '''

        print('Moving to button at %d' % linearPose)
        print('\n')

        goalSteps = _linear_to_steps(linearPose, self.x_axis.steps_per_rev)
        pathMag = self.x_axis.plan_rotation(goalSteps)
        stepMag = pathMag

        while stepMag > 0:

            self.x_axis.step()
            stepMag -= 1
            time.sleep((_acc_profile(pathMag - stepMag, pathMag, 0.001))
                       * self.x_axis.time_factor)

        self.x_axis.current_step = goalSteps

    def take_swtich(self):
        '''
        Action for taking the button at the current pose.
        '''
        print('Activating Channel \n')
        self.z_axis.extend()
        time.sleep(0.6)
        self.z_axis.retract()
        time.sleep(0.6)
        self.z_axis.disable()

    def calibrate(self, initPose):
        '''
        Routine for calibrating the X-Axis. Returns
        to origin then positions at button 1
        '''
        print('Calibrating\n')
        self._move_until()
        self.positionx_axis(initPose)

    def home(self):
        '''
        Routine for returning Carrier to home position
        '''
        print('Homing\n')
        self._move_until()
        self.positionx_axis(5)

    def update_res(self, stepperPins, update, servoPin, limitPin):
        '''
        Allows user to update the step resolution, dynamically

        Remembers current step and steps per rev before change
        for appropriate adjustment.
        '''
        tempStep = self.x_axis.current_step
        tempRotDiv = self.x_axis.steps_per_rev
        self.__init__(stepperPins, update, servoPin, limitPin)
        self.x_axis.current_step = tempStep * (self.x_axis.steps_per_rev / tempRotDiv)
        print('Updated Resolution to %s'%update)

if __name__ == '__main__':
    possup = positionSupervisor([5, 6, 13, 15, 26], 'HALF', 4, 17)
    possup.take_swtich()
