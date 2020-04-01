#!/usr/bin/env python3

import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)


def setOutputs(pins):
    '''
    Sets list of pins to outputs
    '''
    for i in pins:
        gpio.setup(i, gpio.OUT)


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
            gpio.output(pins[2], gpio.LOW)
            gpio.output(pins[3], gpio.LOW)
            gpio.output(pins[4], gpio.LOW)
        # HALF STEP RESOLUTION
        elif step_res == 'HALF':
            self.stepsPerRev = 400
            self.timeFactor = 0.5
            gpio.output(pins[2], gpio.HIGH)
            gpio.output(pins[3], gpio.LOW)
            gpio.output(pins[4], gpio.LOW)
        # QUARTER STEP RESOLUTION
        elif step_res == 'QURT':
            self.stepsPerRev = 800
            self.timeFactor = 0.25
            gpio.output(pins[2], gpio.LOW)
            gpio.output(pins[3], gpio.HIGH)
            gpio.output(pins[4], gpio.LOW)
        # EIGTH STEP RESOLUTION
        elif step_res == 'EGTH':
            self.stepsPerRev = 1600
            self.timeFactor = 0.125
            gpio.output(pins[2], gpio.HIGH)
            gpio.output(pins[3], gpio.HIGH)
            gpio.output(pins[4], gpio.LOW)
        # SIXTEENTH STEP RESOLUTION
        elif step_res == 'SXTH':
            self.stepsPerRev = 3200
            self.timeFactor = 0.0625
            gpio.output(pins[2], gpio.HIGH)
            gpio.output(pins[3], gpio.HIGH)
            gpio.output(pins[4], gpio.HIGH)

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
            gpio.output(self.dirPin, gpio.HIGH)
        # NEGATIVE MOTION CW
        else:
            gpio.output(self.dirPin, gpio.LOW)
            steps *= -1

        return steps

    def step(self):
        '''
        One Step. Rotation and timing will be handled by the position
        supervisor.
        '''
        gpio.output(self.stepPin, gpio.HIGH)
        gpio.output(self.stepPin, gpio.LOW)

    def manualDirection(self, direction):
        '''
        Method to manually dictate the direction of motor rotation
        '''
        if direction == 0:
            gpio.output(self.dirPin, gpio.LOW)
        else:
            gpio.output(self.dirPin, gpio.HIGH)


class servo(object):
    '''
    Defines the state and hardware specs of the servo motor
    '''

    def __init__(self, logicPin):
        gpio.setup(logicPin, gpio.OUT)

        self.posePWM = gpio.PWM(logicPin, 50)
        self.posePWM.start(2.5)


class limitSwitch(object):
    '''
    Defines the state and hardware specs of the limit switch
    '''

    def __init__(self, logicPin):
        self.logicPin = logicPin
        gpio.setup(self.logicPin, gpio.IN)

    def isPressed(self):
        '''
        Checks the state of the limit switch. If high, the
        motor is at the X-Axis minor limit.
        '''
        return gpio.input(self.logicPin)


if __name__ == '__main__':
    serv = servo(18)
    while True:
        cmd = input('Enter Pose: ')
        if cmd == 'end':
            break

        if cmd == 'e':
            serv.extend()

        if cmd == 'r':
            serv.retract()
