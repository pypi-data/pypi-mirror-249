import Oasys.gRPC


# Metaclass for static properties and constants
class ShellType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Shell(Oasys.gRPC.OasysItem, metaclass=ShellType):
    _props = {'include', 'index', 'integrationPoints', 'label', 'material', 'model', 'part', 'type'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Shell._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Shell._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the shells in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the shells in
        model : Model
            Model that all the shells will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the shells in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the shells in
        model : Model
            Model that the flagged shells will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the shells to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first shell in the model (or None if there are no shells in the model)

        Parameters
        ----------
        model : Model
            Model to get first shell in

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the shells in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the shells will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Gets all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that all the shells are in

        Returns
        -------
        array
            Array of :py:class:`Shell<Shell>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Gets all of the shells in the model flagged with a defined flag

        Parameters
        ----------
        model : Model
            Model that the flagged shells are in
        flag : Flag
            Flag (see AllocateFlag) set on the shells to get

        Returns
        -------
        array
            Array of :py:class:`Shell<Shell>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, label):
        """
        Returns the Shell object for shell in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get shell in
        label : integer
            The LS-DYNA label for the shell in the model

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Shell object for shell in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get shell in
        index : integer
            The D3PLOT internal index in the model for shell

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last shell in the model (or None if there are no shells in the model)

        Parameters
        ----------
        model : Model
            Model to get last shell in

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a shell from the screen

        Returns
        -------
        Shell
            Shell object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects shells using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting shells

        Returns
        -------
        integer
            The number of shells selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of shells in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of shells
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def TotalDeleted(model):
        """
        Returns the total number of shells that have been deleted in a model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of shells that have been deleted
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "TotalDeleted", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the shells in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the shells in
        model : Model
            Model that all the shells will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the shells in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the shells in
        model : Model
            Model that the flagged shells will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the shells to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the shells in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all shells will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the shells

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the shell in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the shell in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the shell is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the shell is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a shell

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Deleted(self):
        """
        Checks if the shell has been deleted or not

        Returns
        -------
        boolean
            True if deleted, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Deleted")

    def Flagged(self, flag):
        """
        Checks if the shell is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the shell

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Next(self):
        """
        Returns the next shell in the model (or None if there is not one)

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous shell in the model (or None if there is not one)

        Returns
        -------
        Shell
            Shell object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a shell

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the shell

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Topology(self):
        """
        Returns the topology for the shell in the model

        Returns
        -------
        list
            list of Node objects
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Topology")

    def Unblank(self, window):
        """
        Unblanks the shell in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the shell in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

