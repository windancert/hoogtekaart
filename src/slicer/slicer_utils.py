import numpy

def convert_data_slice_to_slices(data_slice):
    if not isinstance(data_slice, numpy.ndarray):
        raise TypeError("convert_data_slice_to_slices only accepts numpy.ndarray")

    if data_slice.ndim != 1:
        raise ValueError("convert_data_slice_to_slices only accepts numpy.ndarray of dimension 1")
 
    data_is_nan = numpy.isnan(data_slice)
    data_is_valid = ~numpy.isnan(data_slice)
    previous_is_nan = numpy.concatenate(([True], data_is_nan[:-1]))
    next_is_nan = numpy.concatenate((data_is_nan[1:], [True]))
    start_of_valid = previous_is_nan & data_is_valid
    end_of_valid = data_is_valid & next_is_nan
    starts = numpy.where(start_of_valid)[0].tolist()
    ends = numpy.where(end_of_valid)[0].tolist()
    slices = [_create_points(s, e+1, data_slice) for s,e in zip(starts, ends)]

    return slices

def _create_points(start, end, data_slice):
    x_values = range(start, end)
    z_values = data_slice[start:end]
    return list(zip(x_values, z_values))