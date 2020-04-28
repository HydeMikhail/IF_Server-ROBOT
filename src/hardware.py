#!/usr/bin/env python3

import pigpio as gpio
import time

iO = gpio.pi()

def setOutputs(pins):
    '''
    Sets list of pins to outputs
    '''
    for i in pins:
        iO.set_mode(i, gpio.OUTPUT)


class stepperA4988(object):
    '''
    Defines the State And Hardware Specs of
    a stepper motor
    '''

    def __init__(self, pins, step_res):

        setOutputs(pins)

        # Stepper Direction Pin
        self.dirPin = pins[0]
        # Stepper Step Pin
        self.stepPin = pins[1]
        # Current Pose of Stepper in Steps
        self.currentStep = 0

        # FULL STEP RESOLUTION
        if step_res == 'FULL':
            self.stepsPerRev = 200
            self.timeFactor = 1
            iO.write(pins[2], 0)
            iO.write(pins[3], 0)
            iO.write(pins[4], 0)
        # HALF STEP RESOLUTION
        elif step_res == 'HALF':
            self.stepsPerRev = 400
            self.timeFactor = 0.5
            iO.write(pins[2], 1)
            iO.write(pins[3], 0)
            iO.write(pins[4], 0)
        # QUARTER STEP RESOLUTION
        elif step_res == 'QURT':
            self.stepsPerRev = 800
            self.timeFactor = 0.25
            iO.write(pins[2], 0)
            iO.write(pins[3], 1)
            iO.write(pins[4], 0)
        # EIGTH STEP RESOLUTION
        elif step_res == 'EGTH':
            self.stepsPerRev = 1600
            self.timeFactor = 0.125
            iO.write(pins[2], 1)
            iO.write(pins[3], 1)
            iO.write(pins[4], 0)
        # SIXTEENTH STEP RESOLUTION
        elif step_res == 'SXTH':
            self.stepsPerRev = 3200
            self.timeFactor = 0.0625
            iO.write(pins[2], 1)
            iO.write(pins[3], 1)
            iO.write(pins[4], 1)

    def planRotation(self, goalSteps):
        '''
        Determines the direction of the motor
        to achieve the desired position
        '''

        # Defines the magnitude of steps to acheive
        # desired position
        steps = goalSteps - self.currentStep

        # POSITIVE MOTION CCW
        if steps > 0:
            iO.write(self.dirPin, 0)
        # NEGATIVE MOTION CW
        else:
            iO.write(self.dirPin, 1)
            steps *= -1

        return steps

    def step(self):
        '''
        One Step. Rotation and timing will be handled by the position
        supervisor.
        '''
        iO.write(self.stepPin, 1)
        iO.write(self.stepPin, 0)

    def manualDirection(self, direction):
        '''
        Method to manually dictate the direction of motor rotation
        '''
        if direction == 0:
            iO.write(self.dirPin, 0)
        else:
            iO.write(self.dirPin, 1)


class servo(object):
    '''
    Defines the state and hardware specs of the servo motor
    '''

    def __init__(self, logicPin):
        self.logicPin = logicPin
        iO.set_servo_pulsewidth(logicPin, 500)
        time.sleep(0.8)
        iO.set_servo_pulsewidth(logicPin, 0)

    def extend(self):
        iO.set_servo_pulsewidth(self.logicPin, 2500)

    def retract(self):
        iO.set_servo_pulsewidth(self.logicPin, 500)

    def disable(self):
        iO.set_servo_pulsewidth(self.logicPin, 0)


class limitSwitch(object):
    '''
    Defines the state and hardware specs of the limit switch
    '''

    def __init__(self, logicPin):
        self.logicPin = logicPin
        iO.set_mode(self.logicPin, gpio.INPUT)

    def isPressed(self):
        '''
        Checks the state of the limit switch. If high, the
        motor is at the X-Axis minor limit.
        '''
        return iO.read(self.logicPin)
