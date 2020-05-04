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


def linearToSteps(linearPose, stepsPerRev):
    '''
    Take a desired linear position as input and converts it
    to a step magnitude for the stepper motor
    '''
    return int(linearPose / (pulleyDiam / stepsPerRev))  # Integer Number of Steps


def accProfile(currentStep, pathMag, minTime):
    '''
    Calulates discrete time intervals to genearate
    acceleration and deceleration in X-Axis motion.
    '''

    # Slowest time interval
    disTime = maxTime

    # When Stepper is in first revolution
    if currentStep < 400:
        disTime = maxTime - (currentStep
                             * ((maxTime - minTime) / 400))

    # When Stepper is in last revolution
    elif currentStep > pathMag - 400:
        disTime = maxTime - ((pathMag - currentStep)
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
        self.xAxis = stepperA4988(stepperPins, resolution)
        self.zAxis = servo(servoPin)
        self.origin = limitSwitch(limitPin)

    def _moveUntil(self):
        while True:
            self.xAxis.manualDirection(1)
            if self.origin.isPressed():
                self.xAxis.currentStep = 0
                time.sleep(0.25)
                break

            self.xAxis.step()
            time.sleep(0.0005)

    def positionxAxis(self, linearPose):
        '''
        Positions the xAxis at a given linear pose
        '''

        print('Moving to button at %d' % linearPose)
        print('\n')

        goalSteps = linearToSteps(linearPose, self.xAxis.stepsPerRev)
        pathMag = self.xAxis.planRotation(goalSteps)
        stepMag = pathMag

        while stepMag > 0:

            self.xAxis.step()
            stepMag -= 1
            time.sleep((accProfile(pathMag - stepMag, pathMag, 0.001))
                       * self.xAxis.timeFactor)

        self.xAxis.currentStep = goalSteps

    def takeSwitch(self):
        '''
        Action for taking the button at the current pose.
        '''
        self.zAxis.extend()
        time.sleep(0.6)
        self.zAxis.retract()
        time.sleep(0.6)
        self.zAxis.disable()

    def calibrate(self, initPose):
        '''
        Routine for calibrating the X-Axis. Returns
        to origin then positions at button 1
        '''
        print('Calibrating')
        self._moveUntil()
        self.positionxAxis(initPose)

    def home(self):
        '''
        Routine for returning Carrier to home position
        '''
        print('Going Home')
        self._moveUntil()
        self.positionxAxis(5)

    def updateRes(self, stepperPins, update, servoPin, limitPin):
        '''
        Allows user to update the step resolution, dynamically

        Remembers current step and steps per rev before change
        for appropriate adjustment.
        '''
        tempStep = self.xAxis.currentStep
        tempRotDiv = self.xAxis.stepsPerRev
        self.__init__(stepperPins, update, servoPin, limitPin)
        self.xAxis.currentStep = tempStep * (self.xAxis.stepsPerRev / tempRotDiv)

if __name__ == '__main__':
    possup = positionSupervisor([5, 6, 13, 15, 26], 'HALF', 4, 17)
    possup.takeSwitch()
