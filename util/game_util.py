import numpy as np


def distance_between_points(point1, point2):
    return np.linalg.norm(point2 - point1)
