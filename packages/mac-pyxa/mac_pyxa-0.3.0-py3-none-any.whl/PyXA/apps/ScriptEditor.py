""".. versionadded:: 0.0.9

Control Script Editor using JXA-like syntax.
"""

from typing import Literal, Union, Any
from enum import Enum

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable, XACloseable, XADeletable, XAPrintable


class XAScriptEditorItemList(XABase.XAList):
    """A wrapper around lists of Script Editor items that employs fast enumeration techniques.

    All properties of items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAScriptEditorItem
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def by_properties(self, properties: dict) -> "XAScriptEditorItem":
        return self.by_property("properties", properties)


class XAScriptEditorItem(XABase.XAObject):
    """An item in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All of the object's properties."""
        return self.xa_elem.properties()

    def exists(self) -> bool:
        """Verifies that an object exists.

        :return: True if the object exists.
        :rtype: bool

        .. versionadded:: 0.0.9
        """
        return self.xa_elem.exists()


class XAScriptEditorApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Script Editor.app.

    .. versionadded:: 0.0.9
    """

    class ObjectType(Enum):
        """Types of objects that can be created using :func:`make`."""

        DOCUMENT = "document"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAScriptEditorWindow

    @property
    def frontmost(self) -> bool:
        """Whether Script Editor is the active application."""
        return self.xa_scel.frontmost()

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of Script Editor.app."""
        return self.xa_scel.version()

    @property
    def selection(self) -> "XAScriptEditorSelectionObject":
        """The current selection."""
        return self._new_element(
            self.xa_scel.selection(), XAScriptEditorSelectionObject
        )

    @selection.setter
    def selection(self, selection: "XAScriptEditorSelectionObject"):
        self.set_property("selection", selection.xa_elem)

    def documents(self, filter: dict = None) -> "XAScriptEditorDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(
            self.xa_scel.documents(), XAScriptEditorDocumentList, filter
        )

    def classes(self, filter: dict = None) -> "XAScriptEditorObjectClassList":
        """Returns a list of classes, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(
            self.xa_scel.classes(), XAScriptEditorObjectClassList, filter
        )

    def languages(self, filter: dict = None) -> "XAScriptEditorLanguageList":
        """Returns a list of languages matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(
            self.xa_scel.languages(), XAScriptEditorLanguageList, filter
        )

    def make(
        self,
        specifier: Union[str, "XAScriptEditorApplication.ObjectType"],
        properties: Union[dict, None] = None,
        data: Any = None,
    ) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAScriptEditorApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.3.0
        """
        if isinstance(specifier, XAScriptEditorApplication.ObjectType):
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
            return self._new_element(obj, XAScriptEditorDocument)


class XAScriptEditorDocumentList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorDocument)

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def contents(self) -> "XAScriptEditorTextList":
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XAScriptEditorTextList)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def event_log(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("eventLog") or [])

    def language(self) -> "XAScriptEditorLanguageList":
        ls = self.xa_elem.arrayByApplyingSelector_("language") or []
        return self._new_element(ls, XAScriptEditorLanguageList)

    def selection(self) -> "XAScriptEditorSelectionObjectList":
        ls = self.xa_elem.arrayByApplyingSelector_("selection") or []
        return self._new_element(ls, XAScriptEditorSelectionObjectList)

    def text(self) -> "XAScriptEditorTextList":
        ls = self.xa_elem.arrayByApplyingSelector_("text") or []
        return self._new_element(ls, XAScriptEditorTextList)

    def by_modified(self, modified: bool) -> "XAScriptEditorDocument":
        return self.by_property("modified", modified)

    def by_name(self, name: str) -> "XAScriptEditorDocument":
        return self.by_property("name", name)

    def by_path(self, path: XABase.XAPath) -> "XAScriptEditorDocument":
        return self.by_property("path", path.xa_elem)

    def by_contents(self, contents: "XAScriptEditorText") -> "XAScriptEditorDocument":
        return self.by_property("contents", contents.xa_elem)

    def by_object_description(
        self, object_description: str
    ) -> "XAScriptEditorDocument":
        return self.by_property("objectDescription", object_description)

    def by_event_log(self, event_log: str) -> "XAScriptEditorDocument":
        return self.by_property("eventLog", event_log)

    def by_language(
        self, language: "XAScriptEditorLanguage"
    ) -> "XAScriptEditorDocument":
        return self.by_property("language", language.xa_elem)

    def by_selection(
        self, selection: "XAScriptEditorSelectionObject"
    ) -> "XAScriptEditorDocument":
        return self.by_property("selection", selection.xa_elem)

    def by_text(self, text: "XAScriptEditorText") -> "XAScriptEditorDocument":
        return self.by_property("text", text.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAScriptEditorDocument(
    XAScriptEditorItem, XACloseable, XADeletable, XAPrintable, XAClipboardCodable
):
    """A script document in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since it was last saved."""
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        """The document's name."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> XABase.XAPath:
        """The document's path."""
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: Union[XABase.XAPath, str]):
        if isinstance(path, XABase.XAPath):
            path = path.path
        self.set_property("path", path)

    @property
    def contents(self) -> XABase.XAText:
        """The contents of the document."""
        return self._new_element(self.xa_elem.contents(), XAScriptEditorText)

    @contents.setter
    def contents(self, contents: str):
        self.set_property("contents", contents)

    @property
    def object_description(self) -> str:
        """The description of the document."""
        return self.xa_elem.objectDescription()

    @object_description.setter
    def object_description(self, object_description: str):
        self.set_property("objectDescription", object_description)

    @property
    def event_log(self) -> str:
        """The event log of the document."""
        return self.xa_elem.eventLog().get()

    @property
    def language(self) -> "XAScriptEditorLanguage":
        """The scripting language."""
        return self._new_element(self.xa_elem.language(), XAScriptEditorLanguage)

    @language.setter
    def language(self, language: str):
        self.set_property("language", language)

    @property
    def selection(self) -> "XAScriptEditorSelectionObject":
        """The current selection."""
        return self._new_element(
            self.xa_elem.selection(), XAScriptEditorSelectionObject
        )

    @selection.setter
    def selection(self, selection: "XAScriptEditorSelectionObject"):
        self.set_property("selection", selection.xa_elem)

    @property
    def text(self) -> XABase.XAText:
        """The text of the document."""
        return self._new_element(self.xa_elem.text(), XAScriptEditorText)

    @text.setter
    def text(self, text: Union[str, XABase.XAText]):
        if isinstance(text, XABase.XAText):
            text = text.xa_elem
        self.set_property("text", text)

    def save(
        self,
        type: Literal["script", "script bundle", "application", "text"],
        path: Union[str, XABase.XAPath],
        run_only: bool = False,
        show_startup_screen: bool = False,
        stay_open: bool = False,
    ):
        """Saves the document as the specified file type.

        :param type: The file type in which to save the data
        :type type: Literal['script', 'script bundle', 'application', 'text']
        :param path: The file path in which to save the data
        :type path: Union[str, XABase.XAPath]
        :param run_only: Should the script be saved as Run-Only? If it is, you will not be able to edit the contents of the script again, defaults to False. (Applies to all script types except for "text")
        :type run_only: bool, optional
        :param show_startup_screen: Show the startup screen? Defaults to False. (Only applies to scripts saved as "application")
        :type show_startup_screen: bool, optional
        :param stay_open: Should the application remain open after it is launched? Defaults to False. (Only applies to scripts saved as "application")
        :type stay_open: bool, optional

        .. versionadded:: 0.0.9
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        self.xa_elem.saveAs_in_runOnly_startupScreen_stayOpen_(
            type, path.xa_elem, run_only, show_startup_screen, stay_open
        )

    def check_syntax(self):
        """Check the syntax of the document.

        .. versionadded:: 0.0.9
        """
        self.xa_elem.checkSyntax()

    def compile(self) -> bool:
        """Compile the script of the document.

        .. versionadded:: 0.0.9
        """
        return self.xa_elem.compile()

    def print(
        self, print_properties: Union[dict, None] = None, show_dialog: bool = True
    ) -> "XAPrintable":
        """Prints the object.

        Child classes of XAPrintable should override this method as necessary.

        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :return: A reference to the PyXA object that called this method.
        :rtype: XACanPrintPath

        .. versionadded:: 0.0.9
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.print_printDialog_withProperties_(
            self.xa_elem, show_dialog, print_properties
        )
        return self

    def get_clipboard_representation(self) -> list[Union[AppKit.NSURL, str]]:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a Script Editor document, the document's URL and source code are added to the clipboard.

        :return: The document's path and text content
        :rtype: list[Union[AppKit.NSURL, str]]

        .. versionadded:: 0.0.9
        """
        return [self.path.xa_elem, str(self.text)]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAScriptEditorWindow(XABaseScriptable.XASBWindow):
    """A window of Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> XAScriptEditorDocument:
        """The document currently displayed in the window."""
        return self._new_element(self.xa_elem.document(), XAScriptEditorDocument)

    @property
    def floating(self) -> bool:
        """Whether the window floats."""
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is the application's current modal window."""
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar."""
        return self.xa_elem.titled()


class XAScriptEditorObjectClassList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor classes that employs fast enumeration techniques.

    All properties of classes can be called as methods on the wrapped list, returning a list containing each class's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorObjectClass)


class XAScriptEditorObjectClass(XAScriptEditorItem):
    """A class in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAScriptEditorInsertionPointList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor insertion points that employs fast enumeration techniques.

    All properties of insertion points can be called as methods on the wrapped list, returning a list containing each insertion point's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorInsertionPoint)

    def contents(self) -> XAScriptEditorItemList:
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XAScriptEditorItemList)

    def by_contents(
        self, contents: XAScriptEditorItem
    ) -> "XAScriptEditorInsertionPoint":
        return self.by_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents()) + ">"


class XAScriptEditorInsertionPoint(XAScriptEditorItem):
    """An insertion point between two objects in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def contents(self) -> XAScriptEditorItem:
        return self._new_element(self.xa_elem.contents(), XAScriptEditorItem)

    @contents.setter
    def contents(self, contents: XAScriptEditorItem):
        """The contents of the insertion point."""
        self.set_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem.contents().get()) + ">"


class XAScriptEditorTextList(XABase.XATextList):
    """A wrapper around lists of Script Editor texts that employs fast enumeration techniques.

    All properties of texts can be called as methods on the wrapped list, returning a list containing each text's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorText)

    def color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("color") or []
        return [XABase.XAColor(x) for x in ls]

    def font(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("font") or [])

    def size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def by_color(self, color: XABase.XAColor) -> "XAScriptEditorText":
        return self.by_property("color", color.xa_elem)

    def by_font(self, font: str) -> "XAScriptEditorText":
        return self.by_property("font", font)

    def by_size(self, size: int) -> "XAScriptEditorText":
        return self.by_property("size", size)


class XAScriptEditorText(XABase.XAText):
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def color(self) -> XABase.XAColor:
        """The color of the first character."""
        return XABase.XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: XABase.XAColor):
        self.set_property("color", color.xa_elem)

    @property
    def font(self) -> str:
        """The name of the font of the first character."""
        return self.xa_elem.font()

    @font.setter
    def font(self, font: str):
        self.set_property("font", font)

    @property
    def size(self) -> int:
        """The size in points of the first character."""
        return self.xa_elem.size()

    @size.setter
    def size(self, size: int):
        self.set_property("size", size)

    def insertion_points(
        self, filter: dict = None
    ) -> "XAScriptEditorInsertionPointList":
        """Returns a list of insertion points matching the given filter.

        .. versionadded:: 0.0.9
        """
        return self._new_element(
            self.xa_elem.insertionPoints(), XAScriptEditorInsertionPointList, filter
        )


class XAScriptEditorLanguageList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor languages that employs fast enumeration techniques.

    All properties of languages can be called as methods on the wrapped list, returning a list containing each language's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorLanguage)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def supports_compiling(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsCompiling") or [])

    def supports_recording(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("supportsRecording") or [])

    def by_object_description(
        self, object_description: str
    ) -> "XAScriptEditorLanguage":
        return self.by_property("objectDescription", object_description)

    def by_id(self, id: str) -> "XAScriptEditorLanguage":
        return self.by_property("id", id)

    def by_name(self, name: str) -> "XAScriptEditorLanguage":
        return self.by_property("name", name)

    def by_supports_compiling(
        self, supports_compiling: bool
    ) -> "XAScriptEditorLanguage":
        return self.by_property("supportsCompiling", supports_compiling)

    def by_supports_recording(
        self, supports_recording: bool
    ) -> "XAScriptEditorLanguage":
        return self.by_property("supportsRecording", supports_recording)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAScriptEditorLanguage(XAScriptEditorItem):
    """A scripting language in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_description(self) -> str:
        """The description of the language."""
        return self.xa_elem.objectDescription()

    @property
    def id(self) -> str:
        """The unique id of the language."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the language."""
        return self.xa_elem.name()

    @property
    def supports_compiling(self) -> bool:
        """Is the language compilable?"""
        return self.xa_elem.supportsCompiling()

    @property
    def supports_recording(self) -> bool:
        """Is the language recordable?"""
        return self.xa_elem.supportsRecording()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAScriptEditorSelectionObjectList(XAScriptEditorItemList):
    """A wrapper around lists of Script Editor selection objects that employs fast enumeration techniques.

    All properties of selection objects can be called as methods on the wrapped list, returning a list containing each selection objects's value for the property.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAScriptEditorSelectionObject)

    def character_range(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("characterRange") or [])

    def contents(self) -> XAScriptEditorItemList:
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XAScriptEditorItemList)

    def by_character_range(
        self, character_range: tuple[int, int]
    ) -> "XAScriptEditorSelectionObject":
        return self.by_property("characterRange", character_range)

    def by_contents(
        self, contents: XAScriptEditorItem
    ) -> "XAScriptEditorSelectionObject":
        return self.by_property("contents", contents.xa_elem)


class XAScriptEditorSelectionObject(XAScriptEditorItem):
    """The state of the current selection in Script Editor.app.

    .. versionadded:: 0.0.9
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def character_range(self) -> tuple[int, int]:
        """The range of characters in the selection."""
        return self.xa_elem.characterRange()

    @property
    def contents(self) -> XAScriptEditorItem:
        """The contents of the selection."""
        return self.xa_elem.contents().get()

    @contents.setter
    def contents(self, contents: XAScriptEditorItem):
        self.set_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents) + ">"
