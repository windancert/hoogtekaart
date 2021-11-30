import unittest

import numpy

import context
from slicer.slicer_utils import convert_data_slice_to_slices

class SlicerUtilTest(unittest.TestCase):
    def test_convert_data_slice_to_slices_wrong_type(self):
        for illegal in (None, [1, 2, 3], {"A": 1, "B": 2}, {1, 2, 3}, 1.0):
            self.assertRaises(TypeError, lambda:convert_data_slice_to_slices(illegal))

    def test_convert_data_slice_to_slices_wrong_value(self):
        for illegal in (numpy.zeros((2,2)), numpy.zeros((2,2,2))):
            self.assertRaises(ValueError, lambda:convert_data_slice_to_slices(illegal))

    def test_small_sequences(self):
        for mask, expected in (([1], [[(0,1)]]),
                               ([0], []),
                               ([0, 0], []),
                               ([0, 1], [[(1,1)]]),
                               ([1, 0], [[(0,1)]]),
                               ([1, 1], [[(0,1), (1,1)]])):
            array = self._create_array(mask)
            result = convert_data_slice_to_slices(array)
            self.assertEqual(expected, result)

    def test_ends(self):
        for mask, expected in (([1, 2, 3], [[(0,1), (1,2), (2,3)]]),
                               ([1, 0, 3], [[(0,1)], [(2,3)]]),
                               ([1, 2, 0], [[(0,1), (1,2)]]),
                               ([1, 0, 0], [[(0,1)]]),
                               ([0, 2, 3], [[(1,2), (2,3)]])):
            array = self._create_array(mask)
            result = convert_data_slice_to_slices(array)
            self.assertEqual(expected, result)

    def test_starts(self):
        for mask, expected in (([3, 2, 1], [[(0,3), (1,2), (2,1)]]),
                               ([3, 0, 1], [[(0,3)], [(2,1)]]),
                               ([0, 2, 1], [[(1,2), (2,1)]]),
                               ([0, 0, 1], [[(2,1)]]),
                               ([3, 2, 0], [[(0,3), (1,2)]])):
            array = self._create_array(mask)
            result = convert_data_slice_to_slices(array)
            self.assertEqual(expected, result)

    def test_longer_sequence(self):
        array = self._create_array([0, 1, 0, 0, 2, 2, 0, 0, 3, 3, 3, 0, 0, 0, 4])
        result = convert_data_slice_to_slices(array)
        self.assertEqual([[(1,1)], [(4,2), (5,2)], [(8,3), (9,3), (10,3)], [(14,4)]], result)

    def _create_array(self, mask):
        result = numpy.array(mask).astype(numpy.float32)
        result[result == 0] = numpy.nan
        return result

        