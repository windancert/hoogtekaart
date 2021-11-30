import math
import unittest

import context
from slicer.slicer import Slicer

class SlicerTeset(unittest.TestCase):
#     def test_slicer(self):
#         s = Slicer(r"../data/ahn_100.tif")
#         slices = s.generate_slices(100)

#         import matplotlib.pyplot as plt
#         f = plt.figure()
#         ax = f.add_subplot(111, projection="3d")
#         ax.set_axis_off()
#         for slice in slices:
#             x_values, y_values, z_values = zip(*slice)
# #            z_values = [_compress_z(z) for z in z_values]
#             ax.plot(x_values, y_values, zs=z_values, color='b')
#         plt.show(block=True)

    def test_slicer_3d(self):
        s = Slicer(r"../data/ahn_100.tif")

        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        # f = plt.figure()
        # ax = f.add_subplot(111)
        # ax.imshow(s.data)
        # plt.show(block=True)


        f = plt.figure()
        ax = f.add_subplot(111, projection="3d")
        ax.set_axis_off()

        # for slice in s.generate_slices(50, True):
        #     pc =Poly3DCollection([slice])
        #     import numpy
        #     color = numpy.random.rand(1,3)
        #     pc.set_facecolor('w')
        #     pc.set_edgecolor('w') 
        #     ax.add_collection3d(pc) 
            

        for slice in s.generate_slices(50):
            x_values, y_values, z_values = zip(*slice)
            ax.plot(x_values, y_values, zs=[_compress_z(z) for z in z_values], color='b')
        
        plt.show(block=True)

def _compress_z(z):
    if z > 0:
        return z/10
    return z