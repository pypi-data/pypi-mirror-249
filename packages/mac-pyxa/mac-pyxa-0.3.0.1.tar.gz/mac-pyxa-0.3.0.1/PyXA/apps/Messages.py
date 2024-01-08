""".. versionadded:: 0.0.1

Control the macOS Messages application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Union

import AppKit

from PyXA import XABase
from PyXA import XAEvents
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable


class XAMessagesApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Messages.app

    .. seealso:: :class:`XAMessagesChat`, :class:`XAMessagesFileTransfer`, :class:`XAMessagesParticipant`, :class:`XAMessagesAccount`

    .. versionadded:: 0.0.1
    """

    class ServiceType(Enum):
        """Options for services types supported by Messages.app."""

        SMS = XABase.OSType("ssms")
        IMESSAGE = XABase.OSType("sims")

    class MessageDirection(Enum):
        """Options for the direction of a message."""

        INCOMING = XABase.OSType("FTic")
        OUTGOING = XABase.OSType("FTog")

    class TransferStatus(Enum):
        """Options for the transfer stage/status of a message."""

        PREPARING = XABase.OSType("FTsp")
        WAITING = XABase.OSType("FTsw")
        TRANSFERRING = XABase.OSType("FTsg")
        FINALIZING = XABase.OSType("FTsz")
        FINISHED = XABase.OSType("FTsf")
        FAILED = XABase.OSType("FTse")

    class ConnectionStatus(Enum):
        """Options for the connection status of Messages.app to message transfer servers."""

        DISCONNECTING = XABase.OSType("dcng")
        CONNECTED = XABase.OSType("conn")
        CONNECTING = XABase.OSType("cong")
        DISCONNECTED = XABase.OSType("dcon")

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAMessagesWindow

    @property
    def name(self) -> str:
        """The name of the application.

        .. versionadded:: 0.0.1
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Messages is the active application.

        .. versionadded:: 0.0.1
        """
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of Messages.app.

        .. versionadded:: 0.0.1
        """
        return self.xa_scel.version()

    def send(self, message: str, chat: "XAMessagesChat"):
        """Sends a message to the specified chat.

        :param message: The message to send
        :type message: str
        :param chat: The chat to send the message to
        :type chat: XAMessagesChat

        :Example 1:

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> friend = messages.participants().by_full_name("Example Person")
        >>> chat = messages.chats().by_participants([friend])
        >>> messages.send("Testing 1 2 3", chat)

        .. versionadded:: 0.0.4
        """
        self.xa_scel.send_to_(message, chat)

    def print(self, object: XABase.XAObject, show_dialog: bool = True):
        self.xa_scel.print_withProperties_printDialog_(
            object.xa_elem, None, show_dialog
        )

    def documents(self, filter: Union[dict, None] = None) -> "XAMessagesDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.documents(), XAMessagesDocumentList, filter
        )

    def chats(self, filter: Union[dict, None] = None) -> "XAMessagesChatList":
        """Returns a list of chats, as PyXA objects, matching the given filter.

        :Example 1: List all chats

        >>> import PyXA
        >>> app = PyXA.Application("Messages")
        >>> print(app.chats())
        <<class 'PyXA.apps.Messages.XAMessagesChatList'>['iMessage;-;+11234567891', 'SMS;-;+12234567891', ...]

        :Example 2: List the names of all named chats

        >>> import PyXA
        >>> app = PyXA.Application("Messages")
        >>> print(app.chats().name())
        ['PyXA Group', 'Dev Chat']

        :Example 3: List the information, including participants, of every chat

        >>> import PyXA
        >>> app = PyXA.Application("Messages")
        >>> chats = app.chats()
        >>> for chat in chats:
        >>>     print("\\n")
        >>>     print("Name:", chat.name)
        >>>     print("ID:", chat.id)
        >>>     print("Account:", chat.account)
        >>>     print("Participants:", chat.participants())
        Name: None
        ID: iMessage;-;+11234567891
        Account: <PyXA.apps.Messages.XAMessagesAccount object at 0x10871e100>
        Participants: <<class 'PyXA.apps.Messages.XAMessagesParticipantList'>['+1 (123) 456-7891']>
        ...

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.chats(), XAMessagesChatList, filter)

    def participants(
        self, filter: Union[dict, None] = None
    ) -> "XAMessagesParticipantList":
        """Returns a list of participants, as PyXA objects, matching the given filter.

        :Example 1: List all participants

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.participants())
        <<class 'PyXA.apps.Messages.XAMessagesParticipantList'>['+1 (888) 888-8888', 'Example Person', 'Another Person', ...]>

        :Example 2: Get a participant by full name

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.participants().by_full_name("Example Person"))
        <<class 'PyXA.apps.Messages.XAMessagesParticipant'>Example Person>

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.participants(), XAMessagesParticipantList, filter
        )

    def accounts(self, filter: Union[dict, None] = None) -> "XAMessagesAccountList":
        """Returns a list of accounts, as PyXA objects, matching the given filter.

        :Example 1: Print a list of all accounts

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.accounts())
        <<class 'PyXA.apps.Messages.XAMessagesAccountList'>[<ServiceType.IMESSAGE: 1936289139>, <ServiceType.SMS: 1936289139>, <ServiceType.IMESSAGE: 1936289139>]>

        :Example 2: Get an account by its ID

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.accounts().by_id("BEC519EA-DD88-5574-BDB9-C48486D3111B"))
        <PyXA.apps.Messages.XAMessagesAccount object at 0x126de2340>

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_scel.accounts(), XAMessagesAccountList, filter)

    def file_transfers(
        self, filter: Union[dict, None] = None
    ) -> "XAMessagesFileTransferList":
        """Returns a list of file transfers, as PyXA objects, matching the given filter.

        :Example 1: List all file transfers

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.file_transfers())
        <<class 'PyXA.apps.Messages.XAMessagesFileTransferList'>['at_0_8BEC6B47-3B43-4D14-87C1-221C2BDED01C', 'at_0_9C0DC423-F6AB-4A98-8532-1C4D250160CD', ...]>

        :Example 2: Get a file transfer by filename

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.file_transfers().by_name("Example1.png")
        <<class 'PyXA.apps.Messages.XAMessagesFileTransfer'>Example1.png>

        :Example 3: List the file paths of file transfers

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.file_transfers().file_path())
        [file:///Users/exampleuser/Library/Messages/Attachments/de/14/at_0_8BEC6B47-3B43-4D14-87C1-221C2BDED01C/Example1.png, file:///Users/exampleuser/Library/Messages/Attachments/c4/04/at_0_9C0DC423-F6AB-4A98-8532-1C4D250160CD/Example2.jpg, ...]

        :Example 4: Get the first PNG file transfer

        >>> import PyXA
        >>> messages = PyXA.Application("Messages")
        >>> print(messages.file_transfers().containing("name", "png"))
        <<class 'PyXA.apps.Messages.XAMessagesFileTransfer'>Example1.png>

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            [x for x in self.xa_scel.fileTransfers()],
            XAMessagesFileTransferList,
            filter,
        )


class XAMessagesWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Messages windows.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The title of the window.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        """The unique identifier for the window.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        """The index of the window in the front-to-back ordering.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """The bounding rectangle of the window.

        .. versionadded:: 0.0.4
        """
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return (origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: tuple[int, int, int, int]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        """Whether the window has a close button.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.closeable()

    @property
    def miniaturizable(self) -> bool:
        """Whether the window can be minimized.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.miniaturizable()

    @property
    def miniaturized(self) -> bool:
        """Whether the window is currently minimized.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.miniaturized()

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        self.set_property("miniaturized", miniaturized)

    @property
    def resizable(self) -> bool:
        """Whether the window can be resized.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        """Whether the window is currently visible.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        """Whether the window can be zoomed.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        """Whether the window is currently zoomed.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def document(self) -> "XAMessagesDocument":
        return self._new_element(self.xa_elem.document(), XAMessagesDocument)


class XAMessagesDocumentList(XABase.XAList):
    """A wrapper around a list of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file") or [])

    def by_name(self, name: str) -> Union["XAMessagesDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XAMessagesDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> Union["XAMessagesDocument", None]:
        return self.by_property("file", file)


class XAMessagesDocument(XABase.XAObject):
    """A class for managing and interacting with documents in Messages.app.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The title of the document.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        """The location of the document on the disk, if one exists.

        .. versionadded:: 0.0.4
        """
        return self.xa_elem.file()


class XAMessagesChatList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of chats that employs fast enumeration techniques.

    All properties of chats can be called as methods on the wrapped list, returning a list containing each chat's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesChat, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def account(self) -> "XAMessagesAccountList":
        ls = self.xa_elem.arrayByApplyingSelector_("account") or []
        return self._new_element(ls, XAMessagesAccountList)

    def participants(self) -> list["XAMessagesParticipantList"]:
        ls = []
        for chat in self.xa_elem:
            ls.append(self._new_element(chat.participants(), XAMessagesParticipantList))
        return ls

    def by_id(self, id: str) -> "XAMessagesChat":
        return self.by_property("id", id)

    def by_name(self, name: str) -> "XAMessagesChat":
        return self.by_property("name", name)

    def by_account(self, account: "XAMessagesAccount") -> "XAMessagesChat":
        return self.by_property("account", account.xa_elem)

    def by_participants(
        self, participants: list["XAMessagesParticipant"]
    ) -> "XAMessagesChat":
        target_handles = [x.handle for x in participants]
        for chat in self.xa_elem:
            chat_participants = chat.participants()

            match = []
            for participant in chat_participants:
                if participant.handle() in target_handles:
                    match.append(participant)
                else:
                    match = []

            if len(match) == len(participants):
                return self._new_element(chat, XAMessagesChat)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each chat in the list.

        When the clipboard content is set to a list of chats, each chat's name is added to the clipboard.

        :return: The list of chat names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"


class XAMessagesChat(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with chats in Messages.app

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the chat.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the chat as it appears in the chat list.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.name() or ""

    @property
    def account(self) -> "XAMessagesAccount":
        """The account that is participating in the chat.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    def send(self, message):
        """Sends a message to the chat.

        _extended_summary_

        :param message: _description_
        :type message: _type_

        :Example 1: Send an SMS to a chat based on the chat ID

        >>> import PyXA
        >>> app = PyXA.Application("Messages")
        >>> chat = app.chats().by_id("SMS;-;+11234567891")
        >>> chat.send("Hello!")

        .. versionadded:: 0.0.4
        """
        self.xa_prnt.xa_prnt.send(message, self.xa_elem)

    def participants(
        self, filter: Union[dict, None] = None
    ) -> "XAMessagesParticipantList":
        """Returns a list of participants, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.participants(), XAMessagesParticipantList, filter
        )

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the chat.

        When the clipboard content is set to a chat, the chat's name is added to the clipboard.

        :return: The name of the chat
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.participants()) + ">"


class XAMessagesFileTransferList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of file transfers that employs fast enumeration techniques.

    All properties of file transfers can be called as methods on the wrapped list, returning a list containing each file transfer's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesFileTransfer, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def file_path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("filePath") or []
        return [XABase.XAPath(x) for x in ls]

    def direction(self) -> list[XAMessagesApplication.MessageDirection]:
        ls = [x.direction() for x in self.xa_elem]
        return [XAMessagesApplication.MessageDirection(x) for x in ls]

    def account(self) -> "XAMessagesAccountList":
        ls = [x.account() for x in self.xa_elem]
        return self._new_element(ls, XAMessagesAccountList)

    def participant(self) -> "XAMessagesParticipantList":
        ls = [x.participant() for x in self.xa_elem]
        return self._new_element(ls, XAMessagesParticipantList)

    def file_size(self) -> list[int]:
        return [x.fileSize() for x in self.xa_elem]

    def file_progress(self) -> list[int]:
        return [x.fileProgress() for x in self.xa_elem]

    def transfer_status(self) -> list[XAMessagesApplication.TransferStatus]:
        ls = [x.transferStatus() for x in self.xa_elem]
        try:
            return [XAMessagesApplication.TransferStatus(x) for x in ls]
        except ValueError:
            return [
                XAMessagesApplication.TransferStatus(XABase.OSType(x.stringValue()))
                for x in ls
            ]

    def started(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("started") or [])

    def by_id(self, id: str) -> "XAMessagesFileTransfer":
        return self.by_property("id", id)

    def by_name(self, name: str) -> "XAMessagesFileTransfer":
        return self.by_property("name", name)

    def by_file_path(self, file_path: XABase.XAPath) -> "XAMessagesFileTransfer":
        return self.by_property("filePath", file_path.xa_elem)

    def by_direction(
        self, direction: XAMessagesApplication.MessageDirection
    ) -> "XAMessagesFileTransfer":
        for x in self.xa_elem:
            if x.direction() == direction.value:
                return self._new_element(x, XAMessagesFileTransfer)

    def by_account(self, account: "XAMessagesAccount") -> "XAMessagesFileTransfer":
        return self.by_property("account", account.xa_elem)

    def by_participant(
        self, participant: "XAMessagesParticipant"
    ) -> "XAMessagesFileTransfer":
        return self.by_property("participant", participant.xa_elem)

    def by_file_size(self, file_size: int) -> "XAMessagesFileTransfer":
        return self.by_property("fileSize", file_size)

    def by_file_progress(self, file_progress: int) -> "XAMessagesFileTransfer":
        return self.by_property("fileProgress", file_progress)

    def by_transfer_status(
        self, transfer_status: XAMessagesApplication.TransferStatus
    ) -> "XAMessagesFileTransfer":
        for x in self.xa_elem:
            if x.transferStatus() == transfer_status.value:
                return self._new_element(x, XAMessagesFileTransfer)

    def by_started(self, started: bool) -> "XAMessagesFileTransfer":
        return self.by_property("started", started)

    def filter(
        self,
        filter: str,
        comparison_operation: Union[str, None] = None,
        value1: Union[Any, None] = None,
        value2: Union[Any, None] = None,
    ) -> XABase.XAList:
        substitutions = {
            "transfer status": "transferStatus",
            "file size": "fileSize",
            "file path": "filePath",
            "file progress": "fileProgress",
        }
        filter = substitutions.get(filter, filter)

        if isinstance(value1, XAMessagesApplication.MessageDirection) or isinstance(
            value1, XAMessagesApplication.TransferStatus
        ):
            value1 = XAEvents.event_from_str(XABase.unOSType(value1.value))
        return super().filter(filter, comparison_operation, value1, value2)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each file transfer in the list.

        When the clipboard content is set to a list of file transfers, each file transfer's file path URL is added to the clipboard.

        :return: The list of file path URLs
        :rtype: list[AppKit.NSURL]

        .. versionadded:: 0.0.8
        """
        items = []
        paths = self.file_path()
        for path in paths:
            items.append(path.xa_elem)
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAMessagesFileTransfer(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with file transfers in Messages.app

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the file transfer."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the file."""
        return self.xa_elem.name()

    @property
    def file_path(self) -> XABase.XAPath:
        """The local page to the file being transferred."""
        return XABase.XAPath(self.xa_elem.filePath())

    @property
    def direction(self) -> XAMessagesApplication.MessageDirection:
        """The direction that the file is being sent."""
        return XAMessagesApplication.MessageDirection(self.xa_elem.direction())

    @property
    def account(self) -> "XAMessagesAccount":
        """The account on which the file transfer is taking place."""
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    @property
    def participant(self) -> "XAMessagesParticipant":
        """The other participant in the file transfer."""
        return self._new_element(self.xa_elem.participant(), XAMessagesParticipant)

    @property
    def file_size(self) -> int:
        """The total size of the file transfer in bytes."""
        return self.xa_elem.fileSize()

    @property
    def file_progress(self) -> int:
        """The number of bytes that have been transferred."""
        return self.xa_elem.fileProgress()

    @property
    def transfer_status(self) -> XAMessagesApplication.TransferStatus:
        """The current status of the file transfer."""
        return XAMessagesApplication.TransferStatus(self.xa_elem.transferStatus())

    @property
    def started(self) -> datetime:
        """The date and time that the file transfer started."""
        return self.xa_elem.started()

    def get_clipboard_representation(self) -> list[AppKit.NSURL]:
        """Gets a clipboard-codable representation of the file transfer.

        When the clipboard content is set to a file transfer, the path of the file transfer is added to the clipboard.

        :return: The file path of the file transfer
        :rtype: list[AppKit.NSURL]

        .. versionadded:: 0.0.8
        """
        return [self.file_path.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAMessagesParticipantList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of participants that employs fast enumeration techniques.

    All properties of participants can be called as methods on the wrapped list, returning a list containing each participant's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesParticipant, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def account(self) -> "XAMessagesAccountList":
        ls = self.xa_elem.arrayByApplyingSelector_("account") or []
        return self._new_element(ls, XAMessagesAccountList)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def handle(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("handle") or [])

    def first_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("firstName") or [])

    def last_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("lastName") or [])

    def full_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullName") or [])

    def by_id(self, id: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("id", id)

    def by_account(
        self, account: "XAMessagesAccount"
    ) -> Union["XAMessagesParticipant", None]:
        for x in self:
            if x.account.xa_elem == account.xa_elem:
                return x
        return self.by_property("account", account.xa_elem)

    def by_name(self, name: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("name", name)

    def by_handle(self, handle: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("handle", handle)

    def by_first_name(self, first_name: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("firstName", first_name)

    def by_last_name(self, last_name: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("lastName", last_name)

    def by_full_name(self, full_name: str) -> Union["XAMessagesParticipant", None]:
        return self.by_property("fullName", full_name)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each participant in the list.

        When the clipboard content is set to a list of participants, each participant's full name is added to the clipboard.

        :return: The list of participant names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.full_name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAMessagesParticipant(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with chat participants in Messages.app

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the participant.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.id()

    @property
    def account(self) -> "XAMessagesAccount":
        """The account for the participant.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.account(), XAMessagesAccount)

    @property
    def name(self) -> str:
        """The name of the participant as it appears in the participant list

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.name() or ""

    @property
    def handle(self) -> str:
        """The participant's handle.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.handle() or ""

    @property
    def first_name(self) -> str:
        """The first name of the participant, taken from their contact card (if available).

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.firstName() or ""

    @property
    def last_name(self) -> str:
        """The last name of the participant, taken from their contact card (if available).

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.lastName() or ""

    @property
    def full_name(self) -> str:
        """The full name of the participant, taken from their contact card (if available).

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.fullName() or ""

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the participant.

        When the clipboard content is set to a participant, the full name of the participant is added to the clipboard.

        :return: The participant's full name
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.full_name

    def __repr__(self):
        return "<" + str(type(self)) + self.full_name + ">"


class XAMessagesAccountList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAMessagesAccount, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(
            self.xa_elem.get().arrayByApplyingSelector_("objectDescription") or []
        )

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def connection_status(self) -> list[XAMessagesApplication.ConnectionStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("connectionStatus") or []
        return [
            XAMessagesApplication.ConnectionStatus(XABase.OSType(x.stringValue()))
            for x in ls
        ]

    def service_type(self) -> list[XAMessagesApplication.ServiceType]:
        ls = [x.serviceType() for x in self.xa_elem]
        return [XAMessagesApplication.ServiceType(x) for x in ls]

    def by_id(self, id: str) -> Union["XAMessagesAccount", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XAMessagesAccount", None]:
        return self.by_property("objectDescription", object_description)

    def by_enabled(self, enabled: bool) -> Union["XAMessagesAccount", None]:
        return self.by_property("enabled", enabled)

    def by_connection_status(
        self, connection_status: XAMessagesApplication.ConnectionStatus
    ) -> Union["XAMessagesAccount", None]:
        for account in self.xa_elem:
            if account.connectionStatus() == connection_status.value:
                return self._new_element(account, XAMessagesAccount)

    def by_service_type(
        self, service_type: XAMessagesApplication.ServiceType
    ) -> Union["XAMessagesAccount", None]:
        for account in self.xa_elem:
            if account.serviceType() == service_type.value:
                return self._new_element(account, XAMessagesAccount)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each account in the list.

        When the clipboard content is set to a list of accounts, each account's object description is added to the clipboard.

        :return: The list of account descriptions
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.object_description()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.service_type()) + ">"


class XAMessagesAccount(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with accounts in Messages.app

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the account."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The name of the account as defined in the Account Preferences description field."""
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> bool:
        """Whether the account is currently enabled."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def connection_status(self) -> XAMessagesApplication.ConnectionStatus:
        """The connection status for the account."""
        return XAMessagesApplication.ConnectionStatus(self.xa_elem.connectionStatus())

    @property
    def service_type(self) -> XAMessagesApplication.ServiceType:
        """The type of service for the account."""
        return XAMessagesApplication.ServiceType(self.xa_elem.serviceType())

    def chats(self, filter: Union[dict, None] = None) -> XAMessagesChatList:
        """Returns a list of chats, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(self.xa_elem.chats(), XAMessagesChatList, filter)

    def participants(
        self, filter: Union[dict, None] = None
    ) -> XAMessagesParticipantList:
        """Returns a list of participants, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.participants(), XAMessagesParticipantList, filter
        )

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the account.

        When the clipboard content is set to an account, the name of the account is added to the clipboard.

        :return: The name of the account
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.object_description

    def __repr__(self):
        return "<" + str(type(self)) + str(self.service_type) + ">"
