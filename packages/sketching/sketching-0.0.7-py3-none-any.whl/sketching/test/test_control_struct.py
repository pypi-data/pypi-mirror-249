import unittest

import sketching.control_struct


class ControlStructTest(unittest.TestCase):

    def test_button(self):
        button = sketching.control_struct.Button('test')
        self.assertEqual(button.get_name(), 'test')
