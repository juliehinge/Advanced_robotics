#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.nxtdevices import LightSensor, AnalogSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
import math 

class RobotController:
    def __init__(self, wheel_diameter, axle_track):
        self.ev3 = EV3Brick()
        self.ev3.speaker.beep()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.D)
        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter, axle_track)
        self.line_sensor = LightSensor(Port.S4)
        self.speed = -50
        self.robot.settings(straight_speed=self.speed)

        # For intersections
        self.right_sensor = ColorSensor(Port.S1)
        self.left_sensor = ColorSensor(Port.S2)
        self.threshold = 15
  


    def follow_line(self, directions: list):
        target = 8
        error = 0
        integral = 0
        kp = 0.1
        ki = 0
        kd = 0
        while True:
            value = self.line_sensor.reflection()
            self.ev3.screen.print(value, sep=' ', end='\n')

            error_old = error
            error = target - value
            integral = integral + error
            derivative = error - error_old

            steering = kp*error + ki*integral + kd*derivative

            self.robot.drive(self.speed, -steering)


            # For intersections
            left_value = self.left_sensor.reflection()
            right_value = self.right_sensor.reflection()
            
            if left_value < self.threshold or right_value < self.threshold:
                self.ev3.speaker.beep()
                self.robot.straight(-40)

                direction = directions.pop(0)

                if direction == 'left':
                    self.robot.settings(straight_speed=self.speed)
                    self.robot.turn(90)

                if direction == 'right':
                    self.robot.settings(straight_speed=self.speed)
                    self.robot.turn(-90)

                if direction == 'straight':
                    self.robot.settings(straight_speed=self.speed)
                    self.robot.straight(-10)
                
                if direction == 'reverse':
                    self.robot.settings(straight_speed=-self.speed)



robot_controller = RobotController(wheel_diameter=81, axle_track=160)
directions = []
with open('sokoban_robot_solution.txt', 'r') as file:
    directions = [line.rstrip() for line in file]

robot_controller.follow_line(directions)
