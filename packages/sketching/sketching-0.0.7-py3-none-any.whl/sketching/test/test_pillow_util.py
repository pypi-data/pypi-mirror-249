import os
import pathlib
import unittest

import PIL.ImageFont

import sketching.pillow_util
import sketching.shape_struct


class PillowUtilTests(unittest.TestCase):

    def test_make_arc_image(self):
        result = sketching.pillow_util.make_arc_image(
            10,
            20,
            3,
            4,
            1.5,
            1.6,
            True,
            True,
            (100, 100, 100),
            (200, 200, 200),
            7
        )
        self.assertEqual(result.get_x(), 3)
        self.assertEqual(result.get_y(), 13)
        self.assertEqual(result.get_width(), 17)
        self.assertEqual(result.get_height(), 18)
        self.assertIsNotNone(result.get_image())
    
    def test_make_shape_image_lines(self):
        shape = sketching.shape_struct.Shape(50, 100)
        shape.add_line_to(150, 200)
        shape.end()
        result = sketching.pillow_util.make_shape_image(
            shape,
            True,
            True,
            (100, 100, 100),
            (200, 200, 200),
            1
        )
        self.assertEqual(result.get_x(), 49)
        self.assertEqual(result.get_y(), 99)
        self.assertEqual(result.get_width(), 102)
        self.assertEqual(result.get_height(), 102)
        self.assertIsNotNone(result.get_image())
    
    def test_make_shape_image_bezier(self):
        shape = sketching.shape_struct.Shape(50, 100)
        shape.add_bezier_to(60, 110, 140, 190, 150, 200)
        shape.end()
        result = sketching.pillow_util.make_shape_image(
            shape,
            True,
            True,
            (100, 100, 100),
            (200, 200, 200),
            1
        )
        self.assertEqual(result.get_x(), 49)
        self.assertEqual(result.get_y(), 99)
        self.assertEqual(result.get_width(), 102)
        self.assertEqual(result.get_height(), 102)
        self.assertIsNotNone(result.get_image())
    
    def test_make_text_image(self):
        font_path = os.path.join(
            pathlib.Path(__file__).parent.absolute(),
            'IBMPlexMono-Regular.ttf'
        )
        result = sketching.pillow_util.make_text_image(
            20,
            20,
            'test',
            PIL.ImageFont.truetype(font_path, 10),
            True,
            True,
            (100, 100, 100),
            (200, 200, 200),
            7,
            'ms'
        )
        self.assertEqual(result.get_x(), 1)
        self.assertEqual(result.get_y(), 6)
        self.assertEqual(result.get_width(), 52)
        self.assertEqual(result.get_height(), 35)
        self.assertIsNotNone(result.get_image())
