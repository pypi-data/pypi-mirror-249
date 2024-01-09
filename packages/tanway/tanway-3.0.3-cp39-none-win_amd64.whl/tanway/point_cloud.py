"""Contains the PointCloud class."""
import numpy

import _tanway


class PointCloud:
    """Point cloud with x, y, z, intensity, distance, channel, angle, pulse laid out on a 2D grid.

    An instance of this class is a handle to a point cloud stored on the compute device memory.
    Use the method copy_data to copy point cloud data from the compute device to a numpy
    array in host memory. Several formats are available.
    """

    def __init__(self, impl):
        """Initialize PointCloud wrapper.

        This constructor is only used internally, and should not be called by the end-user.

        Args:
            impl: Reference to internal/back-end instance.

        Raises:
            TypeError: If argument does not match the expected internal class.
        """
        if not isinstance(impl, _tanway.PointCloud):
            raise TypeError(
                "Unsupported type for argument impl. Got {}, expected {}".format(
                    type(impl), _tanway.PointCloud
                )
            )
        self.__impl = impl

    def copy_data(self, data_format):
        """Copy point cloud data from native SDK to numpy array.

        Supported data formats:
        xyz: 
            ndarray(Height,Width,3) of float
        xyzi:   x,y,z,intensity
            ndarray(Height,Width,4) of float    
        xyzid:  x,y,z,intensity,distance
            ndarray(Height,Width,5) of float    
        xyzall: x,y,z,intensity,distance,channel,angle,pulse,echo,mirror,left_right,block,t_sec,t_usec
            ndarray(Height,Width,14) of float 
            
        Args:
            data_format: A string specifying the data to be copied

        Returns:
            A numpy array with the requested data.

        Raises:
            ValueError: if the requested data format does not exist
        """
        data_formats = {
            "xyz": _tanway.Array2DPointXYZ,
            "xyzi": _tanway.Array2DPointXYZI,
            "xyzid": _tanway.Array2DPointXYZID,
            "xyzall":_tanway.Array2DPointXYZALL,
        }
        try:
            data_format_class = data_formats[data_format]
        except KeyError as ex:
            raise ValueError(
                "Unsupported data format: {data_format}. Supported formats: {all_formats}".format(
                    data_format=data_format, all_formats=list(data_formats.keys())
                )
            ) from ex
        return numpy.array(data_format_class(self.__impl))

    @property
    def height(self):
        """Get the height of the point cloud (number of rows).

        Returns:
            A positive integer
        """
        return self.__impl.height()

    @property
    def width(self):
        """Get the width of the point cloud (number of columns).

        Returns:
            A positive integer
        """
        return self.__impl.width()
    
    @property
    def stamp(self):
        """Get the stamp of the point cloud.

        Returns:
            A positive integer
        """
        return self.__impl.stamp()
    
    @property
    def is_empty(self):
        return self.__impl.is_empty()
