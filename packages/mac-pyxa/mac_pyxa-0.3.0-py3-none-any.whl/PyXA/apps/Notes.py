""".. versionadded:: 0.0.1

Control the macOS Notes application using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Union

import AppKit
from ScriptingBridge import SBElementArray

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from ..XAProtocols import (
    XACanOpenPath,
    XACanPrintPath,
    XAClipboardCodable,
    XADeletable,
    XAShowable,
)


class XANotesApplication(
    XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath
):
    """A class for interacting with Notes.app.

    .. seealso:: :class:`XANotesWindow`, :class:`XANote`, :class:`XANotesFolder`, :class:`XANotesAccount`

    .. versionchanged:: 0.0.3

       Added :func:`accounts`, :func:`attachments`, and related methods

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """Types of objects that can be created using :func:`make`."""

        NOTE = "note"
        ACCOUNT = "account"
        FOLDER = "folder"
        ATTACHMENT = "attachment"

    class FileFormat(Enum):
        NATIVE = OSType("item")  #: The native Notes format

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XANotesWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Notes is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version number of Notes.app."""
        return self.xa_scel.version()

    @property
    def default_account(self) -> "XANotesAccount":
        """The account that new notes are created in by default."""
        return self._new_element(self.xa_scel.defaultAccount(), XANotesAccount)

    @default_account.setter
    def default_account(self, default_account: "XANotesAccount"):
        self.set_property("defaultAccount", default_account.xa_elem)

    @property
    def selection(self) -> "XANoteList":
        """A list of currently selected notes."""
        return self._new_element(self.xa_scel.selection(), XANoteList)

    @selection.setter
    def selection(self, selection: Union["XANoteList", list["XANote"]]):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property("selection", selection)
        else:
            self.set_property("selection", selection.xa_elem)

    def open(self, file_ref: Union[XABase.XAPath, str]) -> "XANote":
        if isinstance(file_ref, XABase.XAPath):
            file_ref = file_ref.path

        super().open(file_ref)
        return self.notes()[0]

    def documents(self, filter: Union[dict, None] = None) -> "XANotesDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.documents(), XANotesDocumentList, filter)

    def notes(self, filter: Union[dict, None] = None) -> "XANoteList":
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        :Example 1: Retrieve the name of each note

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> print(app.notes().name())
        ['ExampleName1', 'ExampleName2', 'ExampleName3', ...]

        :Example 2: Retrieve notes by using a filter

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> print(app.notes().containing("name", "fancy"))
        [('ExampleName1', 'x-coredata://213D109C-B439-42A0-96EC-380DE31393E2/ICNote/p2964'), ('ExampleName11', 'x-coredata://213D109C-B439-42A0-96EC-380DE31393E2/ICNote/p2963'), ...]

        :Example 3: Iterate over each note

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> for note in app.notes():
        >>>     print(note.name)
        ExampleName1
        ExampleName2
        ExampleName3
        ...

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.notes(), XANoteList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XANotesFolderList":
        """Returns a list of Notes folders, as PyXA objects, matching the given filter.

        :Example 1: Retrieve the name of each folder

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> print(app.folders().name())
        ['ExampleFolder1', 'ExampleFolder2', 'ExampleFolder3', ...]

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesFolderList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.folders(), XANotesFolderList, filter)

    def accounts(self, filter: Union[dict, None] = None) -> "XANotesAccountList":
        """Returns a list of Notes accounts, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.accounts(), XANotesAccountList, filter)

    def attachments(self, filter: Union[dict, None] = None) -> "XANotesAttachmentList":
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.attachments(), XANotesAttachmentList, filter
        )

    def new_note(
        self,
        name: str = "New Note",
        body: Union[str, XABase.XAText] = "",
        folder: "XANotesFolder" = None,
    ) -> "XANote":
        """Creates a new note with the given name and body text in the given folder.
        If no folder is provided, the note is created in the default Notes folder.

        :param name: The name of the note, defaults to "New Note"
        :type name: str, optional
        :param body: The initial body text of the note, defaults to ""
        :type body: str, optional
        :param folder: The folder to create the new note in, defaults to None
        :type folder: XANotesFolder, optional
        :return: A reference to the newly created note.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.new_note("PyXA Notes", "Example text of new note.")
        >>> print(note)
        <<class 'PyXA.apps.Notes.XANote'>PyXA Notes, x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p3388>

        .. seealso:: :class:`XANote`, :func:`new_folder`

        .. versionadded:: 0.0.1
        """
        if folder is None:
            folder = self
        name = name.replace("\n", "<br />")

        if isinstance(body, str):
            body = body.replace("\n", "<br />")
        elif isinstance(body, XABase.XAText):
            body = body.text.replace("\n", "<br />")

        properties = {
            "body": f"<h1>{name}</h1><br />{body}",
        }
        note = self.make("note", properties)
        folder.notes().push(note)
        return folder.notes()[0]

    def new_folder(
        self, name: str = "New Folder", account: "XANotesAccount" = None
    ) -> "XANotesFolder":
        """Creates a new Notes folder with the given name.

        :param name: The name of the folder, defaults to "New Folder"
        :type name: str, optional
        :return: A reference to the newly created folder.
        :rtype: XANote

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> folder = app.new_folder("PyXA Notes Folder")
        >>> print(folder)
        <<class 'PyXA.apps.Notes.XANotesFolder'>PyXA Notes Folder, x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3389>

        .. seealso:: :class:`XANotesFolder`, :func:`new_note`

        .. versionadded:: 0.0.1
        """
        if account is None:
            account = self

        properties = {
            "name": name,
        }

        folder = self.make("folder", properties)
        account.folders().push(folder)
        return account.folders().by_name(name)

    def make(
        self,
        specifier: Union[str, "XANotesApplication.ObjectType"],
        properties: Union[dict, None] = None,
        data: Union[XABase.XAPath, str, None] = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XANotesApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new folder and add a new note to that folder

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> new_folder = app.make("folder", {"name": "Example Folder"})
        >>> new_note = app.make("note", {"name": "Example Note"})
        >>> app.folders().push(new_folder)
        >>> new_folder.notes().push(new_note)

        .. versionadded:: 0.0.3
        """
        if isinstance(specifier, XANotesApplication.ObjectType):
            specifier = specifier.value

        camelized_properties = {}

        if properties is None:
            properties = {}

        for key, value in properties.items():
            if key == "url":
                key = "URL"

            camelized_properties[XABase.camelize(key)] = value

        if isinstance(data, str):
            data = XABase.XAPath(data)

        if isinstance(data, XABase.XAPath):
            data = data.xa_elem

        obj = (
            self.xa_scel.classForScriptingClass_(specifier)
            .alloc()
            .initWithData_andProperties_(data, camelized_properties)
        )

        if specifier == "note":
            return self._new_element(obj, XANote)
        elif specifier == "account":
            return self._new_element(obj, XANotesAccount)
        elif specifier == "folder":
            return self._new_element(obj, XANotesFolder)
        elif specifier == "attachment":
            return self._new_element(obj, XANoteAttachment)


class XANoteList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of notes.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANote, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def body(self) -> list[str]:
        return [note.body for note in self]

    def plaintext(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("plaintext") or [])

    def creation_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def password_protected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("passwordProtected") or [])

    def shared(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared") or [])

    def container(self) -> "XANotesFolderList":
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XANotesFolderList)

    def attachments(self) -> "XANotesAttachmentList":
        ls = self.xa_elem.arrayByApplyingSelector_("attachments") or []
        return self._new_element(ls, XANotesAttachmentList)

    def by_name(self, name: str) -> "XANote":
        return self.by_property("name", name)

    def by_id(self, id: str) -> "XANote":
        return self.by_property("id", id)

    def by_body(self, body: str) -> "XANote":
        return self.by_property("body", body)

    def by_plaintext(self, plaintext: str) -> "XANote":
        return self.by_property("plaintext", plaintext)

    def by_creation_date(self, creation_date: datetime) -> "XANote":
        for note in self.xa_elem:
            if note.creationDate() == creation_date:
                return self._new_element(note, XANote)

    def by_modification_date(self, modification_date: datetime) -> "XANote":
        for note in self.xa_elem:
            if note.modificationDate() == modification_date:
                return self._new_element(note, XANote)

    def by_password_protected(self, password_protected: bool) -> "XANote":
        return self.by_property("passwordProtected", password_protected)

    def by_shared(self, shared: bool) -> "XANote":
        return self.by_property("shared", shared)

    def by_container(self, container: "XANotesFolder") -> "XANote":
        for note in self.xa_elem:
            if note.container().get() == container.xa_elem.get():
                return self._new_element(note, XANote)

    def show_separately(self) -> "XANoteList":
        """Shows each note in the list in a separate window.

        :Example 1: Show the currently selected notes in separate windows

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> notes = app.selection.show_separately()

        .. versionadded:: 0.0.4
        """
        for note in self.xa_elem:
            note.showSeparately_(True)
        return self

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each note in the list.

        When the clipboard content is set to a list of notes, the plaintext of each note is added to the clipboard.

        :return: A list of note plaintext representations
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.plaintext()

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self.xa_elem)) + ">"


class XANotesDocumentList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of documents.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file") or [])

    def by_name(self, name: str) -> "XANotesDocument":
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> "XANotesDocument":
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> "XANotesDocument":
        return self.by_property("file", file)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, the name of each document is added to the clipboard.

        :return: A list of document names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XANotesAccountList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of accounts.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesAccount, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def upgraded(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("upgraded") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def default_folder(self) -> "XANotesFolderList":
        ls = self.xa_elem.arrayByApplyingSelector_("defaultFolder") or []
        return self._new_element(ls, XANotesFolderList)

    def notes(self) -> "XANoteList":
        ls = self.xa_elem.arrayByApplyingSelector_("notes") or []
        return self._new_element(ls, XANoteList)

    def folders(self) -> "XANotesFolderList":
        ls = self.xa_elem.arrayByApplyingSelector_("folders") or []
        return self._new_element(ls, XANotesFolderList)

    def by_name(self, name: str) -> "XANotesAccount":
        return self.by_property("name", name)

    def by_upgraded(self, upgraded: bool) -> "XANotesAccount":
        return self.by_property("upgraded", upgraded)

    def by_id(self, id: str) -> "XANotesAccount":
        return self.by_property("id", id)

    def by_default_folder(self, default_folder: "XANotesFolder") -> "XANotesAccount":
        return self.by_property("defaultFolder", default_folder.xa_elem)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each account in the list.

        When the clipboard content is set to a list of accounts, the name of each account is added to the clipboard.

        :return: A list of account names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesFolderList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of Notes folders.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANotesFolder, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def shared(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared") or [])

    def container(self) -> XANotesAccountList:
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XANotesAccountList)

    def folders(self) -> "XANotesFolderList":
        ls = self.xa_elem.arrayByApplyingSelector_("folders") or []
        return self._new_element(ls, XANotesFolderList)

    def notes(self) -> XANoteList:
        ls = self.xa_elem.arrayByApplyingSelector_("notes") or []
        return self._new_element(ls, XANoteList)

    def by_name(self, name: str) -> "XANotesFolder":
        return self.by_property("name", name)

    def by_id(self, id: str) -> "XANotesFolder":
        return self.by_property("id", id)

    def by_shared(self, shared: bool) -> "XANotesFolder":
        return self.by_property("shared", shared)

    def by_container(self, container: "XANotesAccount") -> "XANotesFolder":
        return self.by_property("container", container.xa_elem)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each folder in the list.

        When the clipboard content is set to a list of folders, the name of each folder is added to the clipboard.

        :return: A list of folder names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesAttachmentList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of attachments.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XANoteAttachment, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def content_identifier(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("contentIdentifier") or [])

    def creation_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def shared(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("shared") or [])

    def container(self) -> XANoteList:
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XANoteList)

    def by_name(self, name: str) -> Union["XANoteAttachment", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XANoteAttachment", None]:
        return self.by_property("id", id)

    def by_content_identifier(
        self, content_identifier: str
    ) -> Union["XANoteAttachment", None]:
        return self.by_property("contentIdentifier", content_identifier)

    def by_creation_date(self, creation_date: datetime) -> "XANoteAttachment":
        for attachment in self.xa_elem:
            if attachment.creationDate() == creation_date:
                return self._new_element(attachment, XANoteAttachment)

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XANoteAttachment", None]:
        for attachment in self.xa_elem:
            if attachment.modificationDate() == modification_date:
                return self._new_element(attachment, XANoteAttachment)

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union["XANoteAttachment", None]:
        if not isinstance(url, XABase.XAURL):
            url = XABase.XAURL(url)
        return self.by_property("URL", url.xa_elem)

    def by_shared(self, shared: bool) -> Union["XANoteAttachment", None]:
        return self.by_property("shared", shared)

    def by_container(self, container: "XANote") -> Union["XANoteAttachment", None]:
        for attachment in self.xa_elem:
            if attachment.container().get() == container.xa_elem.get():
                return self._new_element(attachment, XANoteAttachment)

    def save(self, directory: str) -> "XANotesAttachmentList":
        """Saves all attachments in the list in the specified directory.

        :param directory: The directory to store the saved attachments in
        :type directory: str
        :return: A reference to the attachment list object
        :rtype: XANotesAttachmentList

        :Example 1: Save the attachments in currently selected notes to the downloads folder

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> app.selection.attachments().save("/Users/exampleuser/Downloads/")

        .. versionadded:: 0.0.4
        """
        for attachment_ls in self.xa_elem:
            if isinstance(attachment_ls, SBElementArray):
                for attachment in attachment_ls:
                    url = AppKit.NSURL.alloc().initFileURLWithPath_(
                        directory + attachment.name()
                    )
                    attachment.saveIn_as_(
                        url, XANotesApplication.FileFormat.NATIVE.value
                    )
            else:
                url = AppKit.NSURL.alloc().initFileURLWithPath_(
                    directory + attachment_ls.name()
                )
                attachment_ls.saveIn_as_(
                    url, XANotesApplication.FileFormat.NATIVE.value
                )
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(list(zip(self.name(), self.id()))) + ">"


class XANotesWindow(XABaseScriptable.XASBWindow):
    """A window of Notes.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XANotesDocument":
        """The active document."""
        return self._new_element(self.xa_scel.document(), XANotesDocument)


class XANotesFolder(XABase.XAObject, XAClipboardCodable):
    """A class for interacting with Notes folders and their contents.

    .. seealso:: class:`XANote`

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the folder."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def id(self) -> str:
        """The unique identifier for the folder."""
        return str(self.xa_elem.id())

    @property
    def shared(self) -> bool:
        """Whether the folder is shared."""
        return self.xa_elem.shared()

    @property
    def container(self) -> "XANotesAccount":
        """The account the folder belongs to."""
        return self._new_element(self.xa_elem.container(), XANotesAccount)

    def show(self) -> "XANotesFolder":
        """Shows the folder in the main Notes window.

        :return: The folder object.
        :rtype: XANotesFolder

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def move_to(
        self, destination: Union["XANotesFolder", "XANotesAccount"]
    ) -> "XANotesFolder":
        """Moves the folder to the specified container.

        :return: The folder object.
        :rtype: XANotesFolder

        .. versionadded:: 0.2.0
        """
        self.xa_elem.moveTo_(destination.xa_elem)

    def delete(self):
        """Permanently deletes the folder.

        .. versionadded:: 0.2.0
        """
        self.xa_elem.delete()

    def folders(self, filter: Union[dict, None] = None) -> "XANotesFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of folders
        :rtype: XANotesFolderList

        .. versionadded:: 0.2.0
        """
        return self._new_element(self.xa_elem.folders(), XANotesFolderList, filter)

    def notes(self, filter: Union[dict, None] = None) -> "XANoteList":
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.notes(), XANoteList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the folder.

        When the clipboard content is set to a notes folder, the name of the folder is added to the clipboard.

        :return: The name of the notes folder
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"


class XANotesDocument(XABase.XAObject, XAClipboardCodable):
    """A class for interacting with documents in Notes.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the document."""
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since the last save."""
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        """The location of the document on the disk, if one exists."""
        return self.xa_elem.file()

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a document, the document's name is added to the clipboard.

        :return: The name of the document
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XANote(XABase.XAObject, XAClipboardCodable, XAShowable, XADeletable):
    """A class for interacting with notes in the Notes application.

    .. seealso:: :class:`XANotesFolder`

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the note (generally the first line of the body)."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def id(self) -> str:
        """The unique identifier for the note."""
        return str(self.xa_elem.id())

    @property
    def body(self) -> str:
        """The HTML content of the note."""
        return self.xa_elem.body()

    @body.setter
    def body(self, body: str):
        self.set_property("body", body)

    @property
    def plaintext(self) -> str:
        """The plaintext content of the note."""
        return self.xa_elem.plaintext()

    @plaintext.setter
    def plaintext(self, plaintext: set):
        self.set_property("plaintext", plaintext)

    @property
    def creation_date(self) -> datetime:
        """The date and time the note was created."""
        return self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        """The date and time the note was last modified."""
        return self.xa_elem.modificationDate()

    @property
    def password_protected(self) -> bool:
        """Whether the note is password protected."""
        return self.xa_elem.passwordProtected()

    @property
    def shared(self) -> bool:
        """Whether the note is shared."""
        return self.xa_elem.shared()

    @property
    def container(self) -> XANotesFolder:
        """The folder that the note is in."""
        return self._new_element(self.xa_elem.container(), XANotesFolder)

    def show(self) -> "XANote":
        """Shows the note in the main Notes window.

        :return: A reference to the note object
        :rtype: XANote

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> "XANote":
        """Shows the note in a separate window.

        :return: A reference to the note object
        :rtype: XANote

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(True)
        return self

    def attachments(self, filter: Union[dict, None] = None) -> "XANotesAttachmentList":
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter attachments by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of attachments
        :rtype: XANotesAttachmentList

        :Example 1: List all attachments of a note

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[-4]
        >>> print(note.attachments())
        <<class 'PyXA.apps.Notes.XANotesAttachmentList'>[('Example.pdf, 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICAttachment/p526')]>

        :Example 2: Save the attachments of a note to the Downloads folder

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> print(note.attachments().save("/Users/exampleuser/Downloads/"))

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesAttachmentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_elem.attachments(), XANotesAttachmentList, filter
        )

    def move_to(self, folder: "XANotesFolder") -> "XANote":
        """Moves the note to the specified folder.

        :param folder: The folder to move the note to
        :type folder: XANotesFolder
        :return: A reference to the note object
        :rtype: XANote

        .. versionadded:: 0.0.4
        """
        self.xa_elem.moveTo_(folder.xa_elem)
        return self

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the note.

        When the clipboard content is set to a note, the plaintext representation of the note is added to the clipboard.

        :return: The plaintext representation of the note
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.plaintext

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ", " + str(self.id) + ">"


class XANoteAttachment(XABase.XAObject, XAClipboardCodable):
    """A class for interacting with attachments in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show` and :func:`show_separately`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the attachment."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the attachment."""
        return str(self.xa_elem.id())

    @property
    def content_identifier(self) -> str:
        """The content ID of the attachment in the note's HTML."""
        return self.xa_elem.contentIdentifier()

    @property
    def creation_date(self) -> datetime:
        """The date the attachment was created."""
        return self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        """The date the attachment was last modified."""
        return self.xa_elem.modificationDate()

    @property
    def url(self) -> Union[XABase.XAURL, None]:
        """The URL that the attachment represents, if any."""
        url = self.xa_elem.URL()
        if url is not None:
            return XABase.XAURL(url)

    @property
    def shared(self) -> bool:
        """Whether the attachment is shared."""
        return self.xa_elem.shared()

    @property
    def container(self) -> "XANote":
        """The note containing the attachment."""
        return self._new_element(self.xa_elem.container(), XANote)

    def show(self) -> "XANoteAttachment":
        """Shows the attachment in the main Notes window.

        :return: A reference to the attachment object
        :rtype: XANoteAttachment

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def show_separately(self) -> "XANoteAttachment":
        """Shows the attachment in a separate window.

        :return: A reference to the attachment object
        :rtype: XANoteAttachment

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(True)
        return self

    def save(self, directory: str) -> "XANoteAttachment":
        """Saves the attachment to the specified directory.

        :param directory: The directory to store the saved attachment in
        :type directory: str
        :return: A reference to the attachment object
        :rtype: XANoteAttachment

        .. versionadded:: 0.0.4
        """
        url = AppKit.NSURL.alloc().initFileURLWithPath_(directory + self.name)
        self.xa_elem.saveIn_as_(url, XANotesApplication.FileFormat.NATIVE.value)
        return self

    def delete(self):
        """Permanently deletes the attachment.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def get_clipboard_representation(
        self,
    ) -> Union[str, list[Union[AppKit.NSURL, str]]]:
        """Gets a clipboard-codable representation of the attachment.

        When the clipboard content is set to an attachment, the URL of the attachment (if one exists) and the attachment's name are added to the clipboard.

        :return: The URL and name of the attachment, or just the name of the attachment
        :rtype: list[Union[AppKit.NSURL, str]]

        .. versionadded:: 0.0.8
        """
        if self.url is None:
            return self.name
        return [self.url, self.name]

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"


class XANotesAccount(XABase.XAObject, XAClipboardCodable):
    """A class for interacting with accounts in the Notes application.

    .. versionchanged:: 0.0.3

       Added :func:`show`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the account."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def upgraded(self) -> bool:
        """Whether the account is upgraded."""
        return self.xa_elem.upgraded()

    @property
    def id(self) -> str:
        """The unique identifier of the account."""
        return str(self.xa_elem.id())

    @property
    def default_folder(self) -> "XANotesFolder":
        """The default folder for creating new notes."""
        return self._new_element(self.xa_elem.defaultFolder(), XANotesFolder)

    @default_folder.setter
    def default_folder(self, default_folder: "XANotesFolder"):
        self.set_property("defaultFolder", default_folder.xa_elem)

    def show(self) -> "XANotesAccount":
        """Shows the first folder belonging to the account.

        :return: A reference to the account object
        :rtype: XANotesAccount

        .. versionadded:: 0.0.3
        """
        self.xa_elem.showSeparately_(False)
        return self

    def notes(self, filter: Union[dict, None] = None) -> "XANoteList":
        """Returns a list of notes, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter notes by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of notes
        :rtype: XANoteList

        :Example 1: List all notes belonging to an account

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> account = app.accounts()[0]
        >>> print(account.notes())
        <<class 'PyXA.apps.Notes.XANoteList'>[('PyXA Stuff', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p3380'), ('Important Note', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICNote/p614'), ...]>

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANoteList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.notes(), XANoteList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XANotesFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of folders
        :rtype: XANotesFolderList

        :Example 1: List all folders belonging to an account

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> account = app.accounts()[0]
        >>> print(account.folders())
        <<class 'PyXA.apps.Notes.XANotesFolderList'>[('Imported Notes', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3104'), ('Notes', 'x-coredata://224D909C-B449-42B0-96EC-380EE22332E2/ICFolder/p3123'), ...]>

        .. versionchanged:: 0.0.3

           Now returns an object of :class:`XANotesFolderList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.folders(), XANotesFolderList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the account.

        When the clipboard content is set to an account, the account's name are added to the clipboard.

        :return: The name of the account
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", " + self.id + ">"
