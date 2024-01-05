import unittest
import numpy as np
# from .context import geometron
import geometron.geometries as gg


class Curve2dTestCase(unittest.TestCase):
    def test_cclength2xz(self):
        known_points = [[0, 284], [58, 280], [152, 275], [217, 270], [228, 267], [305, 265], [340, 260], [374, 255],
                        [397, 250], [417, 245], [459, 240], [484, 245], [539, 250], [687, 245]]
        actual = gg.cclength2xz(known_points, np.linspace(0, 800, 81))[65][0]
        expected = 645.9384090750688
        self.assertAlmostEqual(actual, expected, places=12)
