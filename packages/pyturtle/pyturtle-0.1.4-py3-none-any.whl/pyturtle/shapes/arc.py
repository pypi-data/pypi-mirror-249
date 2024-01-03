from typing import Dict
import numpy.typing as npt
import numpy as np

from turtle import Turtle
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D

class T:
    def __init__(self, radian: float, step: int):
        self.radian = radian
        self.step = step
        self.value = radian / step

class Arc(Shape):
    # coordinates map a t_value (evenly spaced radians/steps)...
    # basically some weird fraction of a degree...
    # on the circle to a 2d point on cartesian coordinate system.
    #Step = int
    #Radian = float
    #Coordinates = Dict[T, Point2D]

    def __init__(
        self,
        turtle=None,
        #steps: Step = 100,
        steps=100,
        #coordinates: Coordinates = {},
        coordinates=None,
        #center: Point2D = Point2D(0, 0),
        center=None,
        radius: float = 10.0,
        #theta_start: Radian = 0,
        theta_start=0,
        theta_range=((2*np.pi)/8)
        #theta_range: Radian = ((2 * np.pi) / 8),
        #**kwargs
    ):
        super().__init__(turtle, steps, coordinates)
            #turtle, steps, **kwargs)
            #turtle, steps, color, coordinates)
        self.center = Point2D(0, 0) if center is None else center
        self.radius = radius
        self.theta_start = theta_start
        self.theta_range = theta_range

    # update coordinates for every step in the circle.
        for t in self._get_radians_lin_split():
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def _update_coordinates(self, t: T, x_cor: float, y_cor: float) -> None:
        """
        Parameters
        -------------
        t: T
        x_cor: float
            The x coordinate of the turtle at step int (T val 2 pi/steps).
        y_cor: float
            the y coodinate of the turtle at step int (T val 2 pi/steps).

        Notes:
            Recording the step will allow me to use simple logic, without
            math, to connect opposing points on the circle.

        updates coordinates of the turtle.
        """
        self.coordinates[t] = Point2D(x_cor, y_cor)

    def draw(self):
        """
        """
        for step, (t, point) in enumerate(self.coordinates.items()):
            if step == 0:
                self.turtle.penup()

            # x_cor = self.coordinates[t].x
            # y_cor = self.coordinates[t].y
            self.turtle.goto(point.x, point.y)
            self.turtle.pendown()

    def _get_radians_lin_split(self) -> npt.NDArray:
        """
        returns evenly spaced self.steps number of values over theta_range.
        """
        full_circle_lin_split = np.linspace(
            start=self.theta_start,
            # self.theta_start,
            stop=self.theta_range,
            # self.theta_range,
            num=self.steps,
        )
        # want to filter values so that all arcs and circles share
        # common radian mappings ( as opposed to using self.theta_start
        # and self.theta_range in start and stop.
        arc_lin_split = [
            theta
            for theta in full_circle_lin_split
            if theta >= self.theta_start and theta <= self.theta_range
        ]
        return arc_lin_split

    def _get_x_coordinate(self, t, rads=0) -> float:
        """
        converts polar to cartesian, returns x coordinate of turtle
        """
        return round(self.radius * np.cos(t + rads), 2) + self.center.x

    def _get_y_coordinate(self, t, rads=0) -> float:
        """
        convert polar to cartesian, returns y coordinate of turtle
        """
        return round(self.radius * np.sin(t + rads), 2) + self.center.y

    def get_slice():
        pass
    # def get_slice(self, step_num_one, step_num_two):
    #     """

    #     """
    #     slice_coordinates = {}
    #     t_in_arc_range = (t >= step_num_one and t <= step_num_two)
    #     for t in self._get_radians_lin_split():
    #         if t_in_arc_range:
    #             slice_coordinates[t] =
    #             for step, t in enumerate(self.coordinates.items())
        #         arc_coordinates[t] = {
        #             "x": self.coordinates[t]["x"],
        #             "y": self.coordinates[t]["y"],
        #         }
        # return arc_coordinates

    def get_random_slice(self):
        pass

    def translate_x(self, x_shift) -> None:
        """
        adds x_shift to x_coordinate of center to translate circle.
        a distance along x-axis x_shift length.
        """
        self.center.x = self.center.x + x_shift
        # update coordinates for every step in the circle.
        for t in self._get_radians_lin_split():
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def translate_y(self, y_shift) -> None:
        """
        adds y_shift to y_coordinate of center to translate circle
        a distance along y-axis y-shift length.
        """
        self.center.y = self.center.y + y_shift
        #self.center = (x_cor, self.center.y + y_shift)
        # update coordinates for every step in the circle.
        for t in self._get_radians_lin_split():
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def translate_xy(self, x_shift, y_shift) -> None:
        """
        shifts circle in both x and y direction.
        """
        self.center.x = self.center.x + x_shift
        self.center.y = self.center.y + y_shift
        # update coordinates for every step in the circle.
        for t in self._get_radians_lin_split():
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def rotate(self, rads) -> None:
        """
        rotates the circle so that the t-value mappings change
        """
        for t in self._get_radians_lin_split():
            x_cor = self._get_x_coordinate(t, rads)
            y_cor = self._get_y_coordinate(t, rads)
            self._update_coordinates(t, x_cor, y_cor)

    def set_center(self, x, y):
        self.center = Point2D(x, y)

    def set_radius(self, r):
        self.radius = r
        for t in enumerate(self._get_radians_lin_split()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)






