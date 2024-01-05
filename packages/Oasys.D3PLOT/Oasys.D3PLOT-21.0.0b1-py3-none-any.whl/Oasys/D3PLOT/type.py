import Oasys.gRPC


# Metaclass for static properties and constants
class TypeType(type):
    _consts = {'BEAM', 'CONTACT', 'GROUP', 'MATERIAL', 'NODE', 'PART', 'SEGMENT', 'SET', 'SHELL', 'SOLID', 'TSHELL'}

    def __getattr__(cls, name):
        if name in TypeType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Type(Oasys.gRPC.OasysItem, metaclass=TypeType):


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
