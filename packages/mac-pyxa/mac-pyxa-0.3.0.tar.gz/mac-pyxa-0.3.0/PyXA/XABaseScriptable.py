from enum import Enum
from typing import Union
import threading
import AppKit
import ScriptingBridge

from PyXA import XABase

import time

from .XAProtocols import XACloseable
from .XATypes import XARectangle


class XASBPrintable(XABase.XAObject):
    def __print_dialog(self, show_prompt: bool = True):
        """Displays a print dialog."""
        try:
            if self.xa_scel is not None:
                self.xa_scel.printWithProperties_(None)
            else:
                self.xa_elem.printWithProperties_(None)
        except:
            try:
                if self.xa_scel is not None:
                    self.xa_scel.print_withProperties_printDialog_(
                        self.xa_scel, None, show_prompt
                    )
                else:
                    self.xa_elem.print_withProperties_printDialog_(
                        self.xa_elem, None, show_prompt
                    )
            except:
                if self.xa_scel is not None:
                    self.xa_scel.print_printDialog_withProperties_(
                        self.xa_scel, show_prompt, None
                    )
                else:
                    self.xa_elem.print_printDialog_withProperties_(
                        self.xa_elem, show_prompt, None
                    )

    def print(self, properties: dict = None, print_dialog=None) -> XABase.XAObject:
        """Prints a document, window, or item.

        :return: A reference to the PyXA objects that called this method.
        :rtype: XABase.XAObject

        .. versionchanged:: 0.0.2
           Printing now initialized from a separate thread to avoid delaying main thread

        .. versionadded:: 0.0.1
        """
        print_thread = threading.Thread(
            target=self.__print_dialog, name="Print", daemon=True
        )
        print_thread.start()
        return self


class XASBApplication(XABase.XAApplication):
    """An application class for scriptable applications.

    .. seealso:: :class:`XABase.XAApplication`
    """

    class SaveOption(Enum):
        """Options for whether to save documents when closing them."""

        YES = XABase.OSType("yes ")  #: Save the file
        NO = XABase.OSType("no  ")  #: Do not save the file
        ASK = XABase.OSType(
            "ask "
        )  #: Ask user whether to save the file (bring up dialog)

    class PrintErrorHandling(Enum):
        """Options for how to handle errors while printing."""

        STANDARD = "lwst"  #: Standard PostScript error handling
        DETAILED = "lwdt"  #: Print a detailed report of PostScript errors

    def __init__(self, properties):
        super().__init__(properties)
        self.__xa_scel = None
        self.xa_wcls = XASBWindow

    @property
    def xa_scel(self) -> "ScriptingBridge.SBApplication":
        if self.__xa_scel is None:
            self.__xa_scel = ScriptingBridge.SBApplication.alloc().initWithURL_(
                self.xa_elem.bundleURL()
            )
        return self.__xa_scel

    @xa_scel.setter
    def xa_scel(self, xa_scel: "ScriptingBridge.SBObject"):
        self.__xa_scel = xa_scel

    @property
    def front_window(self) -> "XASBWindow":
        """The front window of the application."""
        return self._new_element(self.xa_scel.windows()[0], self.xa_wcls)

    def activate(self) -> "XASBApplication":
        """Activates the application.

        :return: The application object
        :rtype: XASBApplication

        .. versionadded:: 0.1.0.2
        """
        self.xa_scel.activate()
        return self

    def windows(self, filter: dict = None) -> "XASBWindowList":
        """Returns a list of windows, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned windows will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XASBWindowList

        .. versionadded:: 0.0.4
        """
        try:
            return self._new_element(self.xa_scel.windows(), XASBWindowList)
        except AttributeError:
            return self._new_element([], XASBWindowList)

    def set_property(self, property_name, value):
        if "_" in property_name:
            parts = property_name.split("_")
            titled_parts = [part.title() for part in parts[1:]]
            property_name = parts[0] + "".join(titled_parts)
        self.xa_scel.setValue_forKey_(value, property_name)


class XASBWindowList(XABase.XAList):
    """A wrapper around a list of windows.

    .. versionadded:: 0.0.5
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        super().__init__(properties, obj_class, filter)
        if obj_class is None or issubclass(self.xa_prnt.xa_wcls, obj_class):
            self.xa_ocls = self.xa_prnt.xa_wcls

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def bounds(self) -> list[XARectangle]:
        ls = self.xa_elem.arrayByApplyingSelector_("bounds") or []
        return [
            XARectangle(
                value.rectValue().origin.x,
                value.rectValue().origin.y,
                value.rectValue().size.width,
                value.rectValue().size.height,
            )
            for value in ls
        ]

    def closeable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("closeable") or [])

    def resizable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("resizable") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def zoomable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomable") or [])

    def zoomed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("zoomed") or [])

    def miniaturizable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("miniaturizable") or [])

    def miniaturized(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("miniaturized") or [])

    def by_name(self, name: str) -> Union["XASBWindow", None]:
        return self.by_property("name", name)

    def by_id(self, id: int) -> Union["XASBWindow", None]:
        return self.by_property("id", id)

    def by_index(self, index: int) -> Union["XASBWindow", None]:
        return self.by_property("index", index)

    def by_bounds(
        self, bounds: Union[tuple[int, int, int, int], XARectangle]
    ) -> Union["XASBWindow", None]:
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        return self.by_property("bounds", value)

    def by_closeable(self, closeable: bool) -> Union["XASBWindow", None]:
        return self.by_property("closeable", closeable)

    def by_resizable(self, resizable: bool) -> Union["XASBWindow", None]:
        return self.by_property("resizable", resizable)

    def by_visible(self, visible: bool) -> Union["XASBWindow", None]:
        return self.by_property("visible", visible)

    def by_zoomable(self, zoomable: bool) -> Union["XASBWindow", None]:
        return self.by_property("zoomable", zoomable)

    def by_zoomed(self, zoomed: bool) -> Union["XASBWindow", None]:
        return self.by_property("zoomed", zoomed)

    def by_miniaturizable(self, miniaturizable: bool) -> Union["XASBWindow", None]:
        return self.by_property("miniaturizable", miniaturizable)

    def by_miniaturized(self, miniaturized: bool) -> Union["XASBWindow", None]:
        return self.by_property("miniaturized", miniaturized)

    def collapse(self):
        """Collapses all windows in the list.

        .. versionadded:: 0.0.5
        """
        for window in self:
            while not window.miniaturized:
                window.collapse()
                time.sleep(0.01)

    def uncollapse(self):
        """Uncollapses all windows in the list.

        .. versionadded:: 0.1.1
        """
        for window in self:
            while window.miniaturized:
                window.uncollapse()
                time.sleep(0.01)

    def uncollapse(self):
        """Uncollapses all windows in the list.

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.uncollapse()

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of each window in the list.

        When the clipboard content is set to a list of windows, the name of each window is added to the clipboard.

        :return: A list of window names
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASBWindow(XABase.XAObject, XACloseable):
    def __init__(self, properties):
        super().__init__(properties)

        if self.xa_scel is None:
            parent = self.xa_prnt
            while not hasattr(parent, "xa_prcs"):
                parent = parent.xa_prnt

    def __getattr__(self, attr):
        attributes = [
            x
            for y in [
                cls.__dict__.keys()
                for cls in self.__class__.__mro__
                if cls.__name__ != "object"
            ]
            for x in y
        ]
        if attr in attributes:
            # If possible, use PyXA attribute
            return super().__getattribute__(attr)
        else:
            try:
                return self.xa_elem.__getattribute__(attr)
            except Exception as e:
                raise e

    @property
    def name(self) -> str:
        """The title of the window."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def id(self) -> int:
        """The unique identifier for the window."""
        return self.xa_elem.id()

    @property
    def index(self) -> int:
        """The index of the window, ordered front to back."""
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def bounds(self) -> XARectangle:
        """The bounding rectangle of the window."""
        rect = self.xa_elem.bounds()
        origin = rect.origin
        size = rect.size
        return XARectangle(origin.x, origin.y, size.width, size.height)

    @bounds.setter
    def bounds(self, bounds: Union[tuple[int, int, int, int], XARectangle]):
        x = bounds[0]
        y = bounds[1]
        w = bounds[2]
        h = bounds[3]
        value = AppKit.NSValue.valueWithRect_(AppKit.NSMakeRect(x, y, w, h))
        self.set_property("bounds", value)

    @property
    def closeable(self) -> bool:
        """Whether the window has a close button."""
        return self.xa_elem.closeable()

    @property
    def resizable(self) -> bool:
        """Whether the window can be resized."""
        return self.xa_elem.resizable()

    @property
    def visible(self) -> bool:
        """Whether the window is currently visible."""
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    @property
    def zoomable(self) -> bool:
        """Whether the window has a zoom button."""
        return self.xa_elem.zoomable()

    @property
    def zoomed(self) -> bool:
        """Whether the window is currently zoomed."""
        return self.xa_elem.zoomed()

    @zoomed.setter
    def zoomed(self, zoomed: bool):
        self.set_property("zoomed", zoomed)

    @property
    def miniaturizable(self) -> bool:
        """Whether the window can be miniaturized."""
        try:
            return self.xa_elem.miniaturizable()
        except Exception as e:
            print(e)

    @property
    def miniaturized(self) -> bool:
        """Whether the window is currently miniaturized."""
        try:
            return self.xa_elem.miniaturized()
        except Exception as e:
            print(e)

    @miniaturized.setter
    def miniaturized(self, miniaturized: bool):
        try:
            self.set_property("miniaturized", miniaturized)
        except Exception as e:
            print(e)

    def collapse(self) -> "XASBWindow":
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XASBWindow

        .. versionadded:: 0.0.4
        """
        try:
            self.set_property("miniaturized", True)
        except:
            try:
                self.set_property("minimized", True)
            except:
                self.set_property("collapsed", True)
        return self

    def uncollapse(self) -> "XASBWindow":
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XASBWindow

        .. versionadded:: 0.0.4
        """
        try:
            self.set_property("miniaturized", False)
        except:
            try:
                self.set_property("minimized", False)
            except:
                self.set_property("collapsed", False)
        return self

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the window.

        When the clipboard content is set to a window, the name of the window is added to the clipboard.

        :return: The name of the window
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
