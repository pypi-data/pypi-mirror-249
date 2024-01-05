import Oasys.gRPC


# Metaclass for static properties and constants
class PartType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Part(Oasys.gRPC.OasysItem, metaclass=PartType):
    _props = {'elementType', 'include', 'index', 'label', 'material', 'model', 'title', 'type'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Part._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Part._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the parts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the parts in
        model : Model
            Model that all the parts will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the parts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the parts in
        model : Model
            Model that the flagged parts will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first part in the model (or None if there are no parts in the model)

        Parameters
        ----------
        model : Model
            Model to get first part in

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the parts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the parts will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Gets all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that all the parts are in

        Returns
        -------
        array
            Array of :py:class:`Part<Part>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Gets all of the parts in the model flagged with a defined flag

        Parameters
        ----------
        model : Model
            Model that the flagged parts are in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to get

        Returns
        -------
        array
            Array of :py:class:`Part<Part>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, label):
        """
        Returns the Part object for part in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get part in
        label : integer
            The LS-DYNA label for the part in the model

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Part object for part in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get part in
        index : integer
            The D3PLOT internal index in the model for part

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last part in the model (or None if there are no parts in the model)

        Parameters
        ----------
        model : Model
            Model to get last part in

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a part from the screen

        Returns
        -------
        Part
            Part object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects parts using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting parts

        Returns
        -------
        integer
            The number of parts selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of parts in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of parts
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the parts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the parts in
        model : Model
            Model that all the parts will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the parts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the parts in
        model : Model
            Model that the flagged parts will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the parts to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the parts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all parts will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the parts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the part in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the part in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the part is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the part is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a part

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Elements(self):
        """
        Returns a list containing the elements in the part

        Returns
        -------
        array
            Array of element objects
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Elements")

    def Flagged(self, flag):
        """
        Checks if the part is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the part

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Next(self):
        """
        Returns the next part in the model (or None if there is not one)

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous part in the model (or None if there is not one)

        Returns
        -------
        Part
            Part object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a part

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the part

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Unblank(self, window):
        """
        Unblanks the part in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the part in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

