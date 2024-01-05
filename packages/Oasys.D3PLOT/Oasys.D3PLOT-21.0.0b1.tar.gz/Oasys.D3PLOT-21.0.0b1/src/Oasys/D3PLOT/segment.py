import Oasys.gRPC


# Metaclass for static properties and constants
class SegmentType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Segment(Oasys.gRPC.OasysItem, metaclass=SegmentType):
    _props = {'include', 'index', 'label', 'material', 'model', 'part', 'type'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Segment._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Segment._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the segments in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the segments in
        model : Model
            Model that all the segments will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the segments in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the segments in
        model : Model
            Model that the flagged segments will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the segments to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first segment in the model (or None if there are no segments in the model)

        Parameters
        ----------
        model : Model
            Model to get first segment in

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the segments in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the segments will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the segments

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Gets all of the segments in the model

        Parameters
        ----------
        model : Model
            Model that all the segments are in

        Returns
        -------
        array
            Array of :py:class:`Segment<Segment>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Gets all of the segments in the model flagged with a defined flag

        Parameters
        ----------
        model : Model
            Model that the flagged segments are in
        flag : Flag
            Flag (see AllocateFlag) set on the segments to get

        Returns
        -------
        array
            Array of :py:class:`Segment<Segment>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, label):
        """
        Returns the Segment object for segment in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get segment in
        label : integer
            The LS-DYNA label for the segment in the model

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Segment object for segment in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get segment in
        index : integer
            The D3PLOT internal index in the model for segment

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last segment in the model (or None if there are no segments in the model)

        Parameters
        ----------
        model : Model
            Model to get last segment in

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a segment from the screen

        Returns
        -------
        Segment
            Segment object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects segments using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting segments

        Returns
        -------
        integer
            The number of segments selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of segments in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of segments
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the segments in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the segments in
        model : Model
            Model that all the segments will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the segments in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the segments in
        model : Model
            Model that the flagged segments will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the segments to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the segments in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all segments will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the segments

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the segment in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the segment in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the segment is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the segment is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a segment

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the segment

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Flagged(self, flag):
        """
        Checks if the segment is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the segment

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def Next(self):
        """
        Returns the next segment in the model (or None if there is not one)

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous segment in the model (or None if there is not one)

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a segment

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the segment

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Topology(self):
        """
        Returns the topology for the segment in the model

        Returns
        -------
        list
            list of Node objects
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Topology")

    def Unblank(self, window):
        """
        Unblanks the segment in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the segment in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

