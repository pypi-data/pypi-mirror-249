import abc
import os
from turtle import Turtle
from pyturtle.shapes.point import Point2D

class Shape(metaclass=abc.ABCMeta):

    def __init__(
        self,
        turtle = None,
        steps = None,
        coordinates = None,
    ):
        self.turtle = Turtle() if turtle is None else turtle
        #step = len(coordinates)
        self.steps = 10 if steps is None else steps
        # key will depend on shape.
        self.coordinates = {} if coordinates is None else coordinates

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def translate_x(self, x_shift):
        pass

    @abc.abstractmethod
    def translate_y(self, y_shift):
        pass

    @abc.abstractmethod
    def translate_xy(self, x_shift, y_shift):
        pass

    @abc.abstractmethod
    def rotate(self, degrees):
        pass

    @abc.abstractmethod
    def get_slice(self, step_one, step_two):
        pass

    @abc.abstractmethod
    def get_random_slice(self):
        pass

    def _update_coordinate(self, key, value):
        self.coordinates[key] = value

    def get_coordinate(self, key):
        return self.coordinates[key]

    def get_coordinates(self):
        return self.coordinates

    def get_turtle(self):
        return self.turtle
