import Oasys.gRPC


# Metaclass for static properties and constants
class ImageType(type):
    _consts = {'BMP', 'BMP8', 'BMP8C', 'GIF', 'JPEG', 'PNG', 'PNG8', 'PPM', 'SCREEN', 'X2', 'X4'}

    def __getattr__(cls, name):
        if name in ImageType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Image(Oasys.gRPC.OasysItem, metaclass=ImageType):


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Write(name, options=Oasys.gRPC.defaultArg):
        """
        Writes a static image file

        Parameters
        ----------
        name : string
            Filename for the image
        options : dict
            Optional. Dictionary containing options for writing image. Can be any of:

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Write", name, options)

