#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides a simple drawing library using matplotlib.

Functions:
- fill(c): Set the fill color for shapes.
- no_fill(): Disable filling shapes.
- stroke(c): Set the stroke color for shapes.
- no_stroke(): Disable stroking shapes.
- line_style(ls): Set the line style for lines and borders.
- line_width(lw): Set the line width for lines and borders.
- text_size(ts): Set the text size for text.
- text_color(tc): Set the text color for text.
- setup(): Set up the drawing environment.
- show(): Display the drawing.
- ellipse(x, y, w, h): Draw an ellipse.
- circle(x, y, r): Draw a circle.
- rect(x, y, w, h): Draw a rectangle.
- line(x1, y1, x2, y2): Draw a line.
- text(x, y, t): Draw text.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as pltp
import matplotlib.lines as pltl


class BasicPlot:
    """
    A simple drawing library using matplotlib.

    Functions:
    - fill(c): Set the fill color for shapes.
    - no_fill(): Disable filling shapes.
    - stroke(c): Set the stroke color for shapes.
    - no_stroke(): Disable stroking shapes.
    - line_style(ls): Set the line style for lines and borders.
    - line_width(lw): Set the line width for lines and borders.
    - text_size(ts): Set the text size for text.
    - text_color(tc): Set the text color for text.
    - setup(): Set up the drawing environment.
    - show(): Display the drawing.
    - ellipse(x, y, w, h): Draw an ellipse.
    - circle(x, y, r): Draw a circle.
    - rect(x, y, w, h): Draw a rectangle.
    - line(x1, y1, x2, y2): Draw a line.
    - text(x, y, t): Draw text.
    """

    def __init__(self) -> None:
        """
        Initialize the SimpleDraw object.
        """
        self.__current_fill_color = "w"
        self.__current_stroke_color = "k"
        self.__current_line_style = "-"
        self.__current_line_width = 1.0
        self.__current_text_color = "k"
        self.__current_text_size = 12

        self.__do_stroke = True
        self.__do_fill = True

    def fill(self, c):
        """
        Set the fill color for shapes.

        Args:
        - c: The fill color.
        """
        self.__do_fill = True
        self.__current_fill_color = c

    def no_fill(self):
        """
        Disable filling shapes.
        """
        self.__do_fill = False

    def stroke(self, c):
        """
        Set the stroke color for shapes.

        Args:
        - c: The stroke color.
        """
        self.__do_stroke = True
        self.__current_stroke_color = c

    def no_stroke(self):
        """
        Disable stroking shapes.
        """
        self.__do_stroke = False

    def line_style(self, ls):
        """
        Set the line style for lines and borders.

        Args:
        - ls: The line style.
        """
        self.__current_line_style = ls

    def line_width(self, lw):
        """
        Set the line width for lines and borders.

        Args:
        - lw: The line width.
        """
        self.__current_line_width = lw

    def text_size(self, ts):
        """
        Set the text size for text.

        Args:
        - ts: The text size.
        """
        self.__current_text_size = ts

    def text_color(self, tc):
        """
        Set the text color for text.

        Args:
        - tc: The text color.
        """
        self.__current_text_color = tc

    def setup(self):
        """
        Set up the drawing environment.
        """
        plt.axes()
        plt.gcf().patch.set_facecolor("lightgray")
        plt.axis("off")

    def show(self):
        """
        Display the drawing.
        """
        plt.axis("scaled")
        plt.show()

    def ellipse(self, x, y, w, h):
        """
        Draw an ellipse.

        Args:
        - x: The x-coordinate of the center of the ellipse.
        - y: The y-coordinate of the center of the ellipse.
        - w: The width of the ellipse.
        - h: The height of the ellipse.
        """
        if self.__do_stroke:
            ellipse = pltp.Ellipse(
                (x, y),
                w,
                h,
                fc=self.__current_fill_color,
                fill=self.__do_fill,
                ec=self.__current_stroke_color,
                ls=self.__current_line_style,
                lw=self.__current_line_width,
            )
        else:
            ellipse = pltp.Ellipse(
                (x, y), w, h, fc=self.__current_fill_color, fill=self.__do_fill
            )
        plt.gca().add_patch(ellipse)

    def circle(self, x, y, r):
        """
        Draw a circle.

        Args:
        - x: The x-coordinate of the center of the circle.
        - y: The y-coordinate of the center of the circle.
        - r: The radius of the circle.
        """
        self.ellipse(x, y, r, r)

    def rect(self, x, y, w, h):
        """
        Draw a rectangle.

        Args:
        - x: The x-coordinate of the top-left corner of the rectangle.
        - y: The y-coordinate of the top-left corner of the rectangle.
        - w: The width of the rectangle.
        - h: The height of the rectangle.
        """
        if self.__do_stroke:
            rect = pltp.Rectangle(
                (x, y),
                w,
                h,
                fc=self.__current_fill_color,
                fill=self.__do_fill,
                ec=self.__current_stroke_color,
                ls=self.__current_line_style,
                lw=self.__current_line_width,
            )
        else:
            rect = pltp.Rectangle(
                (x, y), w, h, fc=self.__current_fill_color, fill=self.__do_fill
            )

        plt.gca().add_patch(rect)

    def line(self, x1, y1, x2, y2):
        """
        Draw a line.

        Args:
        - x1: The x-coordinate of the starting point of the line.
        - y1: The y-coordinate of the starting point of the line.
        - x2: The x-coordinate of the ending point of the line.
        - y2: The y-coordinate of the ending point of the line.
        """
        line = pltl.Line2D(
            (x1, x2),
            (y1, y2),
            c=self.__current_stroke_color,
            ls=self.__current_line_style,
            lw=self.__current_line_width,
        )
        plt.gca().add_line(line)

    def text(self, x, y, t):
        """
        Draw text.

        Args:
        - x: The x-coordinate of the starting point of the text.
        - y: The y-coordinate of the starting point of the text.
        - t: The text to be drawn.
        """
        plt.gca().text(
            x, y, t, color=self.__current_text_color, fontsize=self.__current_text_size
        )


__basic_plot = BasicPlot()


def fill(c):
    """
    Set the fill color for shapes.

    Args:
    - c: The fill color.
    """
    __basic_plot.fill(c)


def no_fill():
    """
    Disable filling shapes.
    """
    __basic_plot.no_fill()


def stroke(c):
    """
    Set the stroke color for shapes.

    Args:
    - c: The stroke color.
    """
    __basic_plot.stroke(c)


def no_stroke():
    """
    Disable stroking shapes.
    """
    __basic_plot.no_stroke()


def line_style(ls):
    """
    Set the line style for lines and borders.

    Args:
    - ls: The line style.
    """
    __basic_plot.line_style(ls)


def line_width(lw):
    """
    Set the line width for lines and borders.

    Args:
    - lw: The line width.
    """
    __basic_plot.line_width(lw)


def text_size(ts):
    """
    Set the text size for text.

    Args:
    - ts: The text size.
    """
    __basic_plot.text_size(ts)


def text_color(tc):
    """
    Set the text color for text.

    Args:
    - tc: The text color.
    """
    __basic_plot.text_color(tc)


def setup():
    """
    Set up the drawing environment.
    """
    __basic_plot.setup()


def show():
    """
    Display the drawing.
    """
    __basic_plot.show()


def ellipse(x, y, w, h):
    """
    Draw an ellipse.

    Args:
    - x: The x-coordinate of the center of the ellipse.
    - y: The y-coordinate of the center of the ellipse.
    - w: The width of the ellipse.
    - h: The height of the ellipse.
    """
    __basic_plot.ellipse(x, y, w, h)


def circle(x, y, r):
    """
    Draw a circle.

    Args:
    - x: The x-coordinate of the center of the circle.
    - y: The y-coordinate of the center of the circle.
    - r: The radius of the circle.
    """
    __basic_plot.circle(x, y, r)


def rect(x, y, w, h):
    """
    Draw a rectangle.

    Args:
    - x: The x-coordinate of the top-left corner of the rectangle.
    - y: The y-coordinate of the top-left corner of the rectangle.
    - w: The width of the rectangle.
    - h: The height of the rectangle.
    """
    __basic_plot.rect(x, y, w, h)


def line(x1, y1, x2, y2):
    """
    Draw a line.

    Args:
    - x1: The x-coordinate of the starting point of the line.
    - y1: The y-coordinate of the starting point of the line.
    - x2: The x-coordinate of the ending point of the line.
    - y2: The y-coordinate of the ending point of the line.
    """
    __basic_plot.line(x1, y1, x2, y2)


def text(x, y, t):
    """
    Draw text.

    Args:
    - x: The x-coordinate of the starting point of the text.
    - y: The y-coordinate of the starting point of the text.
    - t: The text to be drawn.
    """
    __basic_plot.text(x, y, t)

if __name__ == "__main__":

    setup()
    fill("lightblue")
    stroke("darkblue")
    line_style("--")
    line_width(3.0)
    rect(0, 0, 100, 100)
    fill("lightgreen")
    stroke("darkgreen")
    line_style("-")
    line_width(1.0)
    ellipse(50, 50, 100, 50)
    fill("lightyellow")
    stroke("yellow")
    line_style("-.")
    line_width(2.0)
    circle(50, 50, 50)
    text(50, 50, "Hello, world!")
    show()