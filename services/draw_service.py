import numpy as np
import math
import cv2

from puffyCV._version import __version__
from services.logging_service import initialize_logging

log = initialize_logging()
pi = np.pi

global board_resolution
global projection_coefficient
global projection_center_point
board_resolution = 800
projection_coefficient = 2
projection_center_point = (int(board_resolution/2), int(board_resolution/2))


def draw_line(img, point1, point2, color, thickness):
    img = cv2.line(img, point1, point2, color, thickness)
    return img


def draw_rectangle(img, top_left, bottom_right, color, thickness):
    img = cv2.rectangle(img, top_left, bottom_right, color, thickness)
    return img


def draw_circle(img, center_coord, radius, color, thickness):
    img = cv2.circle(img, center_coord, radius, color, thickness)
    return img


def draw_banner():
    banner =  "\n"
    banner += "██████╗ ██╗   ██╗███████╗███████╗██╗   ██╗ ██████╗██╗   ██╗\n"
    banner += "██╔══██╗██║   ██║██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝██║   ██║   by Patrick Hener\n"
    banner += "██████╔╝██║   ██║█████╗  █████╗   ╚████╔╝ ██║     ██║   ██║   patrickhener@gmx.de\n"
    banner += "██╔═══╝ ██║   ██║██╔══╝  ██╔══╝    ╚██╔╝  ██║     ╚██╗ ██╔╝   Version: {}, 2019-2020\n".\
        format(__version__)
    banner += "██║     ╚██████╔╝██║     ██║        ██║   ╚██████╗ ╚████╔╝    http://puffycv.rtfd.io/\n"
    banner += "╚═╝      ╚═════╝ ╚═╝     ╚═╝        ╚═╝    ╚═════╝  ╚═══╝\n"
    banner += "\n"
    return banner


class Board(object):
    """
    Class to draw dartboard and projections of recognised throws
    """
    def __init__(self, frame_size, img=None):
        """
        :param frame_size: Size of the frame drawn for dartboard projection
        :type frame_size: int
        """
        self.frame_size = frame_size
        if img:
            self.img = img
        else:
            self.img = np.zeros((self.frame_size, self.frame_size, 3), np.uint8)
        self.text_font = cv2.FONT_HERSHEY_SIMPLEX
        self.line_type = cv2.LINE_AA
        self.text_color = (255, 255, 255)
        self.line_color = (255, 255, 255)
        self.text_scale = 1

    def draw_line(self, point1, point2, color, thickness):
        self.img = cv2.line(self.img, point1, point2, color, thickness)

    def draw_rectangle(self, top_left, bottom_right, color, thickness):
        self.img = cv2.rectangle(self.img, top_left, bottom_right, color, thickness)

    def draw_circle(self, center_coord, radius, color, thickness):
        self.img = cv2.circle(self.img, center_coord, radius, color, thickness)

    def draw_string(self, string, text_coords):
        self.img = cv2.putText(self.img, string, text_coords, self.text_font, self.text_scale, self.text_color, 2,
                               self.line_type)

    def projection_draw_throw(self, poi_coord):
        self.img = cv2.circle(self.img, poi_coord, 1, (255, 0, 0), 1)

    def projection_draw_line(self, point1, point2, color, thickness):
        self.img = cv2.line(self.img, point1, point2, color, thickness)

    def projection_prepare(self):
        """
        Draws the dartboard
        :returns: img object
        """
        # Draw the circles of the board
        self.draw_circle(projection_center_point, projection_coefficient * 7, self.line_color, 1)
        self.draw_circle(projection_center_point, projection_coefficient * 17, self.line_color, 1)
        self.draw_circle(projection_center_point, projection_coefficient * 95, self.line_color, 1)
        self.draw_circle(projection_center_point, projection_coefficient * 105, self.line_color, 1)
        self.draw_circle(projection_center_point, projection_coefficient * 160, self.line_color, 1)
        self.draw_circle(projection_center_point, projection_coefficient * 170, self.line_color, 1)

        # Draw segment lines
        for i in range(0, 360, 9):
            segment_point1 = (
                    round(projection_center_point[0] + math.cos(pi/10 * i - pi/20) * projection_coefficient * 170),
                    round(projection_center_point[1] + math.sin(pi/10 * i - pi/20) * projection_coefficient * 170)
            )
            segment_point2 = (
                round(projection_center_point[0] + math.cos(pi/10 * i - pi/20) * projection_coefficient * 17),
                round(projection_center_point[1] + math.sin(pi/10 * i - pi/20) * projection_coefficient * 17)
            )
            self.draw_line(segment_point1, segment_point2, self.line_color, 1)

        # Put in the numbers around the board
        sectors = [
            11, 14, 9, 12, 5,
            20, 1, 18, 4, 13,
            6, 10, 15, 2, 17,
            3, 19, 7, 16, 8
        ]

        start_rad_sector = pi * -1
        rad_sector_step = pi * 0.1
        rad_sector = start_rad_sector
        for sector in sectors:
            self.draw_string(
                str(sector),
                (round(projection_center_point[0] - 20 + math.cos(rad_sector) * projection_coefficient * 190),
                 round(projection_center_point[1] + 10 + math.sin(rad_sector) * projection_coefficient * 190))
            )
            rad_sector += rad_sector_step

        return self.img
