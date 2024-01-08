""".. versionadded:: 0.0.2

Control the macOS Shortcuts application using JXA-like syntax.
"""
from typing import Any, Union, Any
from enum import Enum

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable


class XAShortcutsApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Shortcuts.app.

    .. versionadded:: 0.0.2
    """

    class ObjectType(Enum):
        """Types of objects that can be created using :func:`make`."""

        SHORTCUT = "shortcut"
        FOLDER = "folder"

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Shortcuts is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version number of Shortcuts.app."""
        return self.xa_scel.version()

    def run(self, shortcut: "XAShortcut", input: Any = None) -> Any:
        """Runs the shortcut with the provided input.

        :param shortcut: The shortcut to run
        :type shortcut: XAShortcut
        :param input: The input to pass to the shortcut, defaults to None
        :type input: Any, optional
        :return: The return value of the last action to execute
        :rtype: Any

        .. versionadded:: 0.0.4
        """
        return shortcut.run(input)

    def folders(self, filter: dict = None) -> "XAShortcutFolderList":
        """Returns a list of folders matching the given filter.

        :Example 1: Get all folders

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> print(app.folders())
        <<class 'PyXA.apps.Shortcuts.XAShortcutFolderList'>['Starter Shortcuts', 'Window Management', 'Dev Tools', ...]>

        :Example 2: Get the number of shortcuts contained in each folder

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> all_shortcuts = app.folders().shortcuts()
        >>> lengths = [len(ls) for ls in all_shortcuts]
        >>> print(lengths)
        [4, 3, 2, 15, 12, ...]

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutFolderList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.folders(), XAShortcutFolderList, filter)

    def shortcuts(self, filter: dict = None) -> "XAShortcutList":
        """Returns a list of shortcuts matching the given filter.

        :Example 1: Get all shortcuts

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> print(app.shortcuts())
        <<class 'PyXA.apps.Shortcuts.XAShortcutList'>['Combine Screenshots & Share', 'Travel plans', 'Paywall Bypasser via Facebook', 'Display Notification', 'Text Converter For iMessage', ...]>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_scel.shortcuts(), XAShortcutList, filter)

    def make(
        self,
        specifier: Union[str, "XAShortcutsApplication.ObjectType"],
        properties: Union[dict, None] = None,
        data: Any = None,
    ) -> XABase.XAObject:
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAShortcutsApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.3.0
        """
        if isinstance(specifier, XAShortcutsApplication.ObjectType):
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

        if specifier == "shortcut":
            return self._new_element(obj, XAShortcut)
        elif specifier == "folder":
            return self._new_element(obj, XAShortcutFolder)


class XAShortcutFolderList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of shortcuts folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folders's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAShortcutFolder, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_id(self, id: str) -> Union["XAShortcutFolder", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XAShortcutFolder", None]:
        return self.by_property("name", name)

    def shortcuts(self, filter: dict = None) -> list["XAShortcutList"]:
        ls = self.xa_elem.arrayByApplyingSelector_("shortcuts") or []
        return [self._new_element(x, XAShortcutList, filter) for x in ls.get()]

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each folder in the list.

        When the clipboard content is set to a list of shortcut folders, each folders's name is added to the clipboard.

        :return: The list of folder names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAShortcutFolder(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with folders of shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """A unique identifier for the folder."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name string for the folder."""
        return self.xa_elem.name()

    def shortcuts(self, filter: dict = None) -> "XAShortcutList":
        """Returns a list of shortcuts matching the given filter.

        :Example 1: Get all shortcuts in a folder

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> folder = app.folders()[0]
        >>> print(folder.shortcuts())
        <<class 'PyXA.apps.Shortcuts.XAShortcutList'>['Text Last Image', 'Shazam shortcut', 'Make QR Code', 'Music Quiz', ...]>

        :Example 2: Get a list of shortcut colors in a folder

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> folder = app.folders()[0]
        >>> print(folder.shortcuts().color())
        [<<class 'PyXA.XABase.XAColor'>r=0.21521323919296265, g=0.7715266942977905, b=0.32515448331832886, a=0.0>, <<class 'PyXA.XABase.XAColor'>r=0.2379034161567688, g=0.3681696951389313, b=0.7627069354057312, a=0.0>, ...]>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAShortcutList` instead of a default list.

        .. versionadded:: 0.0.2
        """
        return self._new_element(self.xa_elem.shortcuts(), XAShortcutList, filter)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the folder.

        When the clipboard content is set to a shortcut folder, the folders's name is added to the clipboard.

        :return: The name of the folder
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"

    def __eq__(self, other: "XAShortcutFolder"):
        if super().__eq__(other):
            return True

        return self.id == other.id


class XAShortcutList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of shortcuts that employs fast enumeration techniques.

    All properties of shortcuts can be called as methods on the wrapped list, returning a list containing each shortcut's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAShortcut, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def subtitle(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subtitle") or [])

    def folder(self) -> XAShortcutFolderList:
        ls = self.xa_elem.arrayByApplyingSelector_("id") or []
        return self._new_element(ls, XAShortcutFolderList)

    def color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("color") or []
        return [XABase.XAColor(x) for x in ls]

    def icon(self) -> XABase.XAImageList:
        ls = self.xa_elem.arrayByApplyingSelector_("icon") or []
        return [XABase.XAImage(x) for x in ls]

    def accepts_input(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("acceptsInput") or [])

    def action_count(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("actionCount") or [])

    def by_id(self, id: str) -> Union["XAShortcut", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XAShortcut", None]:
        return self.by_property("name", name)

    def by_subtitle(self, subtitle: str) -> Union["XAShortcut", None]:
        return self.by_property("subtitle", subtitle)

    def by_folder(self, folder: XAShortcutFolder) -> Union["XAShortcut", None]:
        return self.by_property("folder", folder.xa_elem)

    def by_color(self, color: XABase.XAColor) -> Union["XAShortcut", None]:
        return self.by_property("color", color.xa_elem)

    def by_icon(self, icon: XABase.XAImage) -> Union["XAShortcut", None]:
        return self.by_property("icon", icon.xa_elem)

    def by_accepts_input(self, accepts_input: bool) -> Union["XAShortcut", None]:
        return self.by_property("acceptsInput", accepts_input)

    def by_action_count(self, action_count: int) -> Union["XAShortcut", None]:
        return self.by_property("actionCount", action_count)

    def get_clipboard_representation(
        self,
    ) -> list[Union[list[str], list[str], list[AppKit.NSImage]]]:
        """Gets a clipboard-codable representation of each shortcut in the list.

        When the clipboard content is set to a list of shortcuts, each shortcut's name, subtitle, and icon are added to the clipboard.

        :return: A list of each shortcut's name, subtitle, and icon
        :rtype: list[Union[list[str], list[str], list[AppKit.NSImage]]]

        .. versionadded:: 0.0.8
        """
        items = []
        names = self.name()
        subtitles = self.subtitle()
        icons = self.icon()
        for index, name in enumerate(names):
            items.append(name)
            items.append(subtitles[index])
            items.append(icons[index].xa_elem)
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAShortcut(XABaseScriptable.XASBPrintable, XAClipboardCodable):
    """A class for managing and interacting with shortcuts.

    .. seealso:: :class:`XAShortcutsApplication`

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the shortcut."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the shortcut."""
        return self.xa_elem.name()

    @property
    def subtitle(self) -> str:
        """The shortcut's subtitle."""
        return self.xa_elem.subtitle()

    @property
    def folder(self) -> XAShortcutFolder:
        """The folder that contains the shortcut."""
        return self._new_element(self.xa_elem.folder(), XAShortcutFolder)

    @property
    def color(self) -> XABase.XAColor:
        """The color of the short."""
        return XABase.XAColor(self.xa_elem.color())

    @property
    def icon(self) -> XABase.XAImage:
        """The shortcut's icon."""
        return XABase.XAImage(self.xa_elem.icon())

    @property
    def accepts_input(self) -> bool:
        """Whether the shortcut accepts input data."""
        return self.xa_elem.acceptsInput()

    @property
    def action_count(self) -> int:
        """The number of actions in the shortcut."""
        return self.xa_elem.actionCount()

    def run(self, input: Any = None) -> Any:
        """Runs the shortcut with the provided input.

        :param input: The input to pass to the shortcut, defaults to None
        :type input: Any, optional
        :return: The value returned when the shortcut executes
        :rtype: Any

        :Example 1: Run a shortcut without inputs

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> folder = app.folders().by_name("Dev Tools")
        >>> shortcut = folder.shortcuts().by_name("Show IP Address")
        >>> shortcut.run()

        :Example 2: Run a shortcut with text input

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> shortcut = app.shortcuts().by_name("Show Notification")
        >>> shortcut.run("Testing 1 2 3...")

        :Example 3: Run a shortcut with URL input

        >>> import PyXA
        >>> app = PyXA.Application("Shortcuts")
        >>> safari = PyXA.Application("Safari")
        >>> document = safari.document(0)
        >>> shortcut = app.shortcuts().by_name("Save URL as PDF")
        >>> shortcut.run(document.url)

        .. versionadded:: 0.0.2
        """
        if isinstance(input, XABase.XAObject):
            input = input.xa_elem
        return self.xa_elem.runWithInput_(input)

    def get_clipboard_representation(self) -> list[Union[str, str, AppKit.NSImage]]:
        """Gets a clipboard-codable representation of the shortcut.

        When the clipboard content is set to a shortcut, the shortcut's name, subtitle, and icon are added to the clipboard.

        :return: The shortcut's name, subtitle, and icon
        :rtype: list[Union[str, str, AppKit.NSImage]]

        .. versionadded:: 0.0.8
        """
        return [self.name, self.subtitle, self.icon.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ", id=" + str(self.id) + ">"

    def __eq__(self, other: "XAShortcut"):
        if super().__eq__(other):
            return True
        return self.id == other.id
