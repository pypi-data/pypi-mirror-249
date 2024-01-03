from turtle import Turtle
import numpy as np
from pyturtle.shapes.arc import Arc
from pyturtle.shapes.point import Point2D

class Circle(Arc):
    def __init__(self, turtle: Turtle, steps: int=100, coordinates={}, center = Point2D(0, 0), radius: float=10.0, theta_start=0, theta_range=2*np.pi):
        super().__init__(turtle, steps, coordinates, center, radius, theta_start, theta_range)
