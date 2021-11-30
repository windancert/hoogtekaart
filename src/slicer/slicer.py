from PIL import Image
import numpy

from slicer.slicer_utils import convert_data_slice_to_slices

class Slicer:
    def __init__(self, filename):
        image = Image.open(filename)
        self.__data = self.__post_process(image)

    @property
    def data(self):
        return self.__data

    def generate_slices(self, pitch, include_corners=False):
        result = []
        for y, data_slice in self.__generate_data_slices(pitch):
            slices = convert_data_slice_to_slices(data_slice)
            threed_slices = [[(x,y,z) for x,z in s] for s in slices]
            if include_corners:
                threed_slices = [s + [(s[-1][0], y, -1000), (s[0][0], y, -1000)] for s in threed_slices]
            result.extend(threed_slices)
        return result

    def __generate_data_slices(self, pitch):
        N = self.__data.shape[0]
        for i in range(0, N, pitch):
            yield N-i, self.__data[i, :]

    def __post_process(self, image):
        array = numpy.array(image)
        float_array = array.astype(numpy.float32)
        float_array[float_array == float_array.min()] = numpy.nan
        return float_array
