import Oasys.gRPC


# Metaclass for static properties and constants
class ConstantType(type):
    _consts = {'X', 'Y', 'Z'}

    def __getattr__(cls, name):
        if name in ConstantType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Constant(Oasys.gRPC.OasysItem, metaclass=ConstantType):


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
