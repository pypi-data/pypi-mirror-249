import Oasys.gRPC


# Metaclass for static properties and constants
class ComponentType(type):
    _consts = {'BEAM', 'IN_CORE', 'NODE', 'OTHER', 'RENAME', 'REPLACE', 'SCALAR', 'SOLID_SHELL_TSHELL', 'SVON', 'TENSOR', 'VECTOR'}

    def __getattr__(cls, name):
        if name in ComponentType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Component(Oasys.gRPC.OasysItem, metaclass=ComponentType):
    _props = {'component', 'dataType', 'dispose', 'location', 'name'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Component._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Component._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, name, component, data, options=Oasys.gRPC.defaultArg):
        handle = Oasys.D3PLOT._connection.constructor(self.__class__.__name__, name, component, data, options)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)
        """
        Creates a new user defined binary data component in D3PLOT

        Parameters
        ----------
        name : string
            Name for the component
        component : constant
            The type of component stored in the user defined binary component. Either Component.NODE,
            Component.BEAM, Component.SOLID_SHELL_TSHELL or
            Component.OTHER
        data : constant
            The type of data stored in the user defined binary component. Either Component.SCALAR,
            Component.TENSOR or Component.VECTOR
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        Model
            Model object
        """


# Static methods
    def First():
        """
        Returns the first user defined binary component in D3PLOT (or None if there are no components)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First")

    def GetFromID(number):
        """
        Returns the user defined binary component in D3PLOT by ID (or None if the component does not exist)

        Parameters
        ----------
        number : integer
            number of the component you want the Component object for

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", number)

    def GetFromName(name):
        """
        Returns the user defined binary component in D3PLOT by name (or None if the component does not exist)

        Parameters
        ----------
        name : string
            name of the component you want the Component object for

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromName", name)

    def Last():
        """
        Returns the last user defined binary component in D3PLOT (or None if there are no components)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last")

    def Total():
        """
        Returns the total number of user defined binary components in D3PLOT

        Returns
        -------
        integer
            Total number of user binary components
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total")



# Instance methods
    def Delete(self):
        """
        Deletes the next user defined binary data component.
        Do not use the component object after calling this method

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Delete")

    def GetData(self, item, options=Oasys.gRPC.defaultArg):
        """
        Returns the user defined binary data component for an item

        Parameters
        ----------
        item : Node|Beam|Shell|Solid|Tshell
            The Node, Beam, Shell, Solid or
            Tshell the data should be retrieved for
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        float|array
            The component data
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetData", item, options)

    def Next(self):
        """
        Returns the next user defined binary data component (or None if there is not one)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous user defined binary data component (or None if there is not one)

        Returns
        -------
        Component
            Component object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def PutData(self, item, data, options=Oasys.gRPC.defaultArg):
        """
        Sets the user defined binary data component for an item

        Parameters
        ----------
        item : Node|Beam|Shell|Solid|Tshell
            The Node, Beam, Shell, Solid or
            Tshell the data should be set for
        data : float|list
            The data to set. If the component data property is Component.SCALAR
            this will be a single value. If the component data property is Component.VECTOR
            this is a list with length 3. If the component data property is Component.TESNOR
            this is an array with length 6
        options : dict
            Optional. Dictionary containing extra information. Can contain any of:

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "PutData", item, data, options)

