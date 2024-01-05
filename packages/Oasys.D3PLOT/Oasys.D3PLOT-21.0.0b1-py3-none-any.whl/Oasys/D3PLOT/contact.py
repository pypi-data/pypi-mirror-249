import Oasys.gRPC


# Metaclass for static properties and constants
class ContactType(type):
    _consts = {'SURFA', 'SURFB'}

    def __getattr__(cls, name):
        if name in ContactType._consts:
            return Oasys.D3PLOT._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Contact(Oasys.gRPC.OasysItem, metaclass=ContactType):
    _props = {'aNodes', 'aSegments', 'bNodes', 'bSegments', 'include', 'index', 'label', 'model', 'name', 'title', 'type'}


    def __del__(self):
        if not Oasys.D3PLOT._connection:
            return

        Oasys.D3PLOT._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Contact._props:
            return Oasys.D3PLOT._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Contact._props:
            Oasys.D3PLOT._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def BlankAll(window, model):
        """
        Blanks all of the contacts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the contacts in
        model : Model
            Model that all the contacts will be blanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankAll", window, model)

    def BlankFlagged(window, model, flag):
        """
        Blanks all of the contacts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the contacts in
        model : Model
            Model that the flagged contacts will be blanked in
        flag : Flag
            Flag (see AllocateFlag) set on the contacts to blank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "BlankFlagged", window, model, flag)

    def First(model):
        """
        Returns the first contact in the model (or None if there are no contacts in the model)

        Parameters
        ----------
        model : Model
            Model to get first contact in

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "First", model)

    def FlagAll(model, flag):
        """
        Flags all of the contacts in the model with a defined flag

        Parameters
        ----------
        model : Model
            Model that all the contacts will be flagged in
        flag : Flag
            Flag (see AllocateFlag) to set on the contacts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "FlagAll", model, flag)

    def GetAll(model):
        """
        Gets all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that all the contacts are in

        Returns
        -------
        array
            Array of :py:class:`Contact<Contact>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetAll", model)

    def GetFlagged(model, flag):
        """
        Gets all of the contacts in the model flagged with a defined flag

        Parameters
        ----------
        model : Model
            Model that the flagged contacts are in
        flag : Flag
            Flag (see AllocateFlag) set on the contacts to get

        Returns
        -------
        array
            Array of :py:class:`Contact<Contact>` objects
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFlagged", model, flag)

    def GetFromID(model, label):
        """
        Returns the Contact object for contact in model with label (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get contact in
        label : integer
            The LS-DYNA label for the contact in the model

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromID", model, label)

    def GetFromIndex(model, index):
        """
        Returns the Contact object for contact in model with index (or None if it does not exist)

        Parameters
        ----------
        model : Model
            Model to get contact in
        index : integer
            The D3PLOT internal index in the model for contact

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "GetFromIndex", model, index)

    def Last(model):
        """
        Returns the last contact in the model (or None if there are no contacts in the model)

        Parameters
        ----------
        model : Model
            Model to get last contact in

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Last", model)

    def Pick():
        """
        Allows the user to pick a contact from the screen

        Returns
        -------
        Contact
            Contact object or None if cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Pick")

    def Select(flag):
        """
        Selects contacts using an object menu

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to use when selecting contacts

        Returns
        -------
        integer
            The number of contacts selected or None if menu cancelled
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Select", flag)

    def Total(model):
        """
        Returns the total number of contacts in the model

        Parameters
        ----------
        model : Model
            Model to get total in

        Returns
        -------
        integer
            The number of contacts
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "Total", model)

    def UnblankAll(window, model):
        """
        Unblanks all of the contacts in the model

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the contacts in
        model : Model
            Model that all the contacts will be unblanked in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankAll", window, model)

    def UnblankFlagged(window, model, flag):
        """
        Unblanks all of the contacts in the model flagged with a defined flag

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the contacts in
        model : Model
            Model that the flagged contacts will be unblanked in
        flag : Flag
            Flag (see AllocateFlag) set on the contacts to unblank

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnblankFlagged", window, model, flag)

    def UnflagAll(model, flag):
        """
        Unsets a defined flag on all of the contacts in the model

        Parameters
        ----------
        model : Model
            Model that the defined flag for all contacts will be unset in
        flag : Flag
            Flag (see AllocateFlag) to unset on the contacts

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.classMethod(__class__.__name__, "UnflagAll", model, flag)



# Instance methods
    def Blank(self, window):
        """
        Blanks the contact in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to blank the contact in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blank", window)

    def Blanked(self, window):
        """
        Checks if the contact is blanked in a graphics window or not

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) in which to check if the contact is blanked

        Returns
        -------
        boolean
            True if blanked, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Blanked", window)

    def ClearFlag(self, flag):
        """
        Clears a flag on a contact

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to clear on the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "ClearFlag", flag)

    def Flagged(self, flag):
        """
        Checks if the contact is flagged or not

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to test on the contact

        Returns
        -------
        boolean
            True if flagged, False if not
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Flagged", flag)

    def GetNode(self, side, index):
        """
        Gets a node for a contact

        Parameters
        ----------
        side : constant
            The side of the contact to get the node for. Either Contact.SURFA or
            Contact.SURFB
        index : integer
            index of the node to get.
            0 <= index < aNodes for side SURFA
            0 <= index < bNodes for side SURFB

        Returns
        -------
        Node
            Node object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetNode", side, index)

    def GetSegment(self, side, index):
        """
        Gets a segment for a contact

        Parameters
        ----------
        side : constant
            The side of the contact to get the segment for. Either Contact.SURFA or
            Contact.SURFB
        index : integer
            index of the segment to get.
            0 <= index < aSegments for side SURFA
            0 <= index < bSegments for side SURFB

        Returns
        -------
        Segment
            Segment object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "GetSegment", side, index)

    def Next(self):
        """
        Returns the next contact in the model (or None if there is not one)

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Next")

    def Previous(self):
        """
        Returns the previous contact in the model (or None if there is not one)

        Returns
        -------
        Contact
            Contact object
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Previous")

    def SetFlag(self, flag):
        """
        Sets a flag on a contact

        Parameters
        ----------
        flag : Flag
            Flag (see AllocateFlag) to set on the contact

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "SetFlag", flag)

    def Unblank(self, window):
        """
        Unblanks the contact in a graphics window

        Parameters
        ----------
        window : GraphicsWindow
            GraphicsWindow) to unblank the contact in

        Returns
        -------
        None
            No return value
        """
        return Oasys.D3PLOT._connection.instanceMethod(self.__class__.__name__, self._handle, "Unblank", window)

