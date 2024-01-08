""".. versionadded:: 0.0.1

Control the macOS TextEdit application using JXA-like syntax.
"""

from time import sleep
from typing import Any, Union
from enum import Enum

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import (
    XACanOpenPath,
    XACanPrintPath,
    XAClipboardCodable,
    XACloseable,
    XAPrintable,
)


class XATextEditApplication(
    XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath
):
    """A class for managing and interacting with TextEdit.app.

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """Types of objects that can be created with :func:`make`."""

        DOCUMENT = "document"
        WINDOW = "window"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATextEditWindow

    @property
    def frontmost(self) -> bool:
        """Whether TextEdit is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of the TextEdit application."""
        return self.xa_scel.version()

    def open(self, path: str) -> "XATextEditDocument":
        super().open(path)
        return self.front_window.document

    def print(
        self,
        file: Union[str, AppKit.NSURL, "XATextEditDocument"],
        print_properties: dict = None,
        show_prompt: bool = True,
    ):
        """Prints a TextEdit document.

        :param file: The document or path to a document to print
        :type file: Union[str, AppKit.NSURL, XATextEditDocument]
        :param print_properties: Settings to print with or to preset in the print dialog, defaults to None
        :type print_properties: dict, optional
        :param show_prompt: Whether to show the print dialog, defaults to True
        :type show_prompt: bool, optional

        :Example 1: Printing a document with print properties

        >>> import PyXA
        >>> from datetime import datetime, timedelta
        >>> app = PyXA.Application("TextEdit")
        >>> doc = app.documents()[0]
        >>> print_time = datetime.now() + timedelta(minutes=1)
        >>> properties = {
        >>>     "copies": 3,
        >>>     "collating": False,
        >>>     "startingPage": 1,
        >>>     "endingPage": 10,
        >>>     "pagesAcross": 3,
        >>>     "pagesDown": 3,
        >>>     "requestedPrintTime": print_time,
        >>>     "errorHandling": app.PrintErrorHandling.DETAILED.value,
        >>>     "faxNumber": "",
        >>>     "targetPrinter": ""
        >>> }
        >>> app.print(doc, print_properties=properties)

        .. versionadded:: 0.0.3
        """
        if isinstance(file, str):
            file = AppKit.NSURL.alloc().initFileURLWithPath_(file)
        elif isinstance(file, XATextEditDocument):
            file = file.path.xa_elem
        self.xa_scel.print_printDialog_withProperties_(
            file, show_prompt, print_properties
        )

    def documents(self, filter: dict = None) -> "XATextEditDocumentList":
        """Returns a list of documents matching the filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have
        :type filter: dict
        :return: The list of documents
        :rtype: list[XATextEditDocument]

        :Example 1: Listing all documents

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> print(list(app.documents()))
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Current Document.txt>, <<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document.txt>, ...]

        :Example 2: List documents after applying a filter

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> print(list(app.documents({"name": "Another Document.txt"})))
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document.txt>]

        :Example 3: List all paragraphs, words, and characters in all currently open documents

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> documents = app.documents()
        >>> print("Paragraphs:", documents.paragraphs())
        >>> print("Words:", documents.words())
        >>> print("Characters:", documents.characters())
        Paragraphs: [This is note 1
        , This is note 2
        , This is note 3
        ]
        Words: [This, is, note, 1, This, is, note, 2, This, is, note, 3]
        Characters: [T, h, i, s,  , i, s, , n, o, t, e,  , 1,
        , T, h, i, s, , i, s, , n, o, t, e, , 2,
        , T, h, i, s, , i, s, , n, o, t, e, , 3,
        ]

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XATextEditDocumentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(
            self.xa_scel.documents(), XATextEditDocumentList, filter
        )

    def new_document(
        self,
        name: Union[str, None] = "Untitled.txt",
        text: Union[str, None] = "",
        location: Union[str, None] = None,
    ) -> "XATextEditDocument":
        """Creates a new document with the given name and initializes it with the supplied text. If no location is provided, the document file is created in the user's Documents folder.

        :param name: The name (including file extension) of the document, defaults to "Untitled.txt"
        :type name: Union[str, None], optional
        :param text: The initial text of the document, defaults to ""
        :type text: Union[str, None], optional
        :param location: The containing folder of the new document, defaults to None.
        :type location: Union[str, None]
        :return: A reference to the newly created document.
        :rtype: XATextEditDocument

        :Example 1: Create a new document with a name and initial body content

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> doc = app.new_document("New.txt", "Example text")
        >>> print(doc.properties)
        {
            modified = 0;
            name = "New.txt";
            objectClass = "<NSAppleEventDescriptor: 'docu'>";
            path = "/Users/exampleuser/Documents/New.txt";
            text = "Example text";
        }

        .. seealso:: :class:`XATextEditDocument`

        .. versionadded:: 0.0.1
        """
        if location is None:
            location = (
                AppKit.NSFileManager.alloc()
                .homeDirectoryForCurrentUser()
                .relativePath()
                + "/Documents/"
                + name
            )
        else:
            if not location.endswith("/"):
                location = location + "/"
            location = location + name
        new_doc = self.make("document", {"name": name, "text": text, "path": location})
        doc = self.documents().push(new_doc)
        return doc

    def make(
        self,
        specifier: Union[str, "XATextEditApplication.ObjectType"],
        properties: dict,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XATextEditApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to initialize the object with, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new document and push it onto the list of documents

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> properties = {
        >>>     "name": "Example.txt",
        >>>     "path": "/Users/exampleuser/Downloads/Example.txt",
        >>>     "text": "Some example text"
        >>> }
        >>> new_doc = app.make("document", properties)
        >>> app.documents().push(new_doc)

        .. versionadded:: 0.0.3
        """
        if isinstance(specifier, XATextEditApplication.ObjectType):
            specifier = specifier.value

        if data is None:
            camelized_properties = {}

            if properties is None:
                properties = {}

            for key, value in properties.items():
                if key == "url":
                    key = "URL"

                camelized_properties[XABase.camelize(key)] = value

            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithProperties_(camelized_properties)
            )
        else:
            obj = (
                self.xa_scel.classForScriptingClass_(specifier)
                .alloc()
                .initWithData_(data)
            )

        if specifier == "document":
            return self._new_element(obj, XATextEditDocument)
        elif specifier == "window":
            return self._new_element(obj, XATextEditWindow)


class XATextEditWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit windows.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XATextEditDocument":
        """The active document."""
        doc_obj = self.xa_elem.document()
        return self._new_element(doc_obj, XATextEditDocument)

    @document.setter
    def document(self, document: "XATextEditDocument"):
        self.set_property("document", document.xa_elem)

    @property
    def floating(self) -> bool:
        """Whether the window floats."""
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is a modal window."""
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar."""
        return self.xa_elem.titled()


class XATextEditDocumentList(XABase.XATextDocumentList, XAClipboardCodable):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XATextEditDocument)

    def properties(self) -> list[dict]:
        raw_dicts = list(self.xa_elem.arrayByApplyingSelector_("properties") or [])
        return [
            {
                "modified": raw_dict["modified"],
                "name": raw_dict["name"],
                "class": "document",
                "path": XABase.XAPath(raw_dict["path"])
                if raw_dict["path"] is not None
                else None,
                "text": raw_dict["text"],
            }
            for raw_dict in raw_dicts
        ]

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def by_properties(self, properties: dict) -> Union["XABase.XATextDocument", None]:
        for document in self.xa_elem:
            doc_props = document.properties()
            conditions = [
                doc_props["modified"] == properties["modified"],
                doc_props["name"] == properties["name"],
                doc_props["path"]
                == (
                    properties["path"].path
                    if isinstance(properties["path"], XABase.XAPath)
                    else properties["path"]
                ),
                doc_props["text"] == properties["text"],
            ]
            if all(conditions):
                return self._new_element(document, self.xa_ocls)

    def by_path(
        self, path: Union[str, XABase.XAPath]
    ) -> Union["XATextEditDocument", None]:
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_name(self, name: str) -> Union["XATextEditDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XATextEditDocument", None]:
        return self.by_property("modified", modified)

    def prepend(self, text: str) -> "XATextEditDocumentList":
        """Inserts the provided text at the beginning of every document in the list.

        :param text: The text to insert.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        :Example 1: Prepend a string at the beginning of every open document

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> documents = app.documents()
        >>> documents.prepend("-- PyXA Notes --\\n\\n")

        .. seealso:: :func:`append`

        .. versionadded:: 0.0.4
        """
        for doc in self.xa_elem:
            old_text = doc.text().get()
            doc.setValue_forKey_(text + old_text, "text")
        return self

    def append(self, text: str) -> "XATextEditDocumentList":
        """Appends the provided text to the end of every document in the list.

        :param text: The text to append.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        :Example 1: Append a string at the end of every open document

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> documents = app.documents()
        >>> documents.append("\\n\\n-- End Of Notes --")

        .. seealso:: :func:`prepend`

        .. versionadded:: 0.0.4
        """
        for doc in self.xa_elem:
            old_text = doc.text().get()
            doc.setValue_forKey_(old_text + text, "text")
        return self

    def reverse(self) -> "XATextEditDocumentList":
        """Reverses the text of every document in the list.

        :return: A reference to the document object.
        :rtype: XATextDocument

        :Example 1: Reverse the text of every open document

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> documents = app.documents()
        >>> documents.reverse()

        .. versionadded:: 0.0.4
        """
        for doc in self.xa_elem:
            doc.setValue_forKey_(doc.text().get()[::-1], "text")
        return self

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, each documents's file URL and name are added to the clipboard.

        :return: A list of each document's file URL and name
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        texts = self.text()
        paths = self.path()
        for index, text in enumerate(texts):
            items.append(str(text))
            items.append(paths[index].xa_elem)
        return items

    def push(
        self, *documents: list["XATextEditDocument"]
    ) -> Union["XATextEditDocument", list["XATextEditDocument"], None]:
        """Appends the document to the list.

        .. versionadded:: 0.1.1
        """
        objects = []
        num_added = 0

        for document in documents:
            len_before = len(self.xa_elem)
            self.xa_elem.addObject_(document.xa_elem)
            len_after = len(self.xa_elem)

            if len_after == len_before:
                # Document wasn't added -- try force-getting the list before adding
                self.xa_elem.get().addObject_(document.xa_elem)

            if len_after > len_before:
                num_added += 1
                objects.append(
                    self._new_element(
                        self.xa_elem.objectAtIndex_(0).get(), self.xa_ocls
                    )
                )

        if num_added == 1:
            return objects[0]

        if num_added == 0:
            return None

        return objects

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XATextEditDocument(
    XABase.XATextDocument, XAPrintable, XAClipboardCodable, XACloseable
):
    """A class for managing and interacting with TextEdit documents.

    .. versionchanged:: 0.0.2

       Added :func:`close`, :func:`save`, and :func:`copy`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document."""
        raw_dict = self.xa_elem.properties()
        return {
            "path": XABase.XAPath(raw_dict["path"]),
            "name": raw_dict["name"],
            "modified": raw_dict["modified"],
            "text": self._new_element(raw_dict["text"], XABase.XAText),
        }

    @properties.setter
    def properties(self, properties: dict[str, Any]):
        if "path" in properties:
            path = properties["path"]
            if isinstance(path, str):
                path = XABase.XAPath(path)
            self.set_property("path", path.xa_elem)

        if "name" in properties:
            self.set_property("name", properties["name"])

        if "text" in properties:
            # Assume provided text is a string
            text = properties["text"]
            if isinstance(properties["text"], XABase.XAText):
                # Provided text is actually an XAObject
                text = text.xa_elem
            self.set_property("text", text)

    @property
    def path(self) -> XABase.XAPath:
        """The path at which the document is stored."""
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: XABase.XAPath):
        self.set_property("path", path.xa_elem)

    @property
    def name(self) -> str:
        """The name of the document, including the file extension."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since the last save."""
        return self.xa_elem.modified()

    def print(
        self, print_properties: Union[dict, None] = None, show_dialog: bool = True
    ) -> "XATextEditDocument":
        """Prints the document.

        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :return: The document object
        :rtype: XATextEditDocument

        .. versionadded:: 0.0.8
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.print_printDialog_withProperties_(
            self.xa_elem, show_dialog, print_properties
        )
        return self

    def save(self, file_path: Union[str, XABase.XAPath, None] = None):
        """Saves the document.

        If a file path is provided, TextEdit will attempt to create a new file at the target location and of the specified file extension. If no file path is provided, and the document does not have a current path on the disk, a save dialog for the document will open.

        :param file_path: The path to save the document at, defaults to None
        :type file_path: str, optional

        :Example 1: Save all currently open documents

        >>> import PyXA
        >>> app = PyXA.Application("TextEdit")
        >>> for doc in app.documents():
        >>>     doc.save()

        .. versionadded:: 0.0.2
        """
        if file_path is not None:
            if isinstance(file_path, str):
                file_path = XABase.XAPath(file_path)
            self.xa_elem.saveAs_in_(None, file_path.xa_elem)
        else:
            url = self.path.xa_elem
            print(url)
            self.xa_elem.saveAs_in_(None, url)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a document, the documents's file URL and body text are added to the clipboard.

        :return: The document's file URL and body text
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [str(self.text), self.path.xa_elem]

    def __repr__(self):
        try:
            return "<" + str(type(self)) + self.name + ">"
        except AttributeError:
            return "<" + str(type(self)) + str(self.xa_elem) + ">"
