""".. versionadded:: 0.0.1

General classes and methods applicable to any PyXA object.
"""

import importlib
import math
import os
import random
import re
import sys
import threading
import time
from datetime import datetime, timedelta
from enum import Enum
from pprint import pprint
from typing import Any, Callable, Literal, Union

import macimg, macimg.filters, macimg.distortions, macimg.transforms, macimg.compositions

import AppKit
import Quartz
import requests
import ScriptingBridge
import DataDetection
import libdispatch
from bs4 import BeautifulSoup, element
from PyObjCTools import AppHelper

from PyXA.XAErrors import (
    ApplicationNotFoundError,
    InvalidPredicateError,
    AppleScriptError,
)
from PyXA.XAProtocols import XACanOpenPath, XAClipboardCodable, XAPathLike
from PyXA.XATypes import XADatetimeBlock

from .apps import application_classes


def OSType(s: str):
    return int.from_bytes(s.encode("UTF-8"), "big")


def unOSType(i: int):
    return i.to_bytes((i.bit_length() + 7) // 8, "big").decode()


def snakify(text: str) -> str:
    """Converts a string to snake case.

    :param text: The string to convert
    :type text: str
    :return: The snakeized string
    :rtype: str

    .. versionadded:: 0.3.0
    """
    return re.sub(r"([A-Z])", r"_\1", text).lower()


def camelize(text: str) -> str:
    """Converts a string to camel case.

    :param text: The string to convert
    :type text: str
    :return: The camelized string
    :rtype: str

    .. versionadded:: 0.3.0
    """
    parts = text.split("_")
    return parts[0] + "".join([part.title() for part in parts[1:]])


VERSION = "0.3.0"  #: The installed version of PyXA
supported_applications: list[str] = list(
    application_classes.keys()
)  #: A list of names of supported scriptable applications

workspace = None


###############
### General ###
###############
class XAObject:
    """A general class for PyXA scripting objects.

    .. seealso:: :class:`XABaseScriptable.XASBObject`

    .. versionadded:: 0.0.1
    """

    _xa_sevt = None
    _xa_estr = None
    _xa_wksp = None

    def __init__(self, properties: dict = None):
        """Instantiates a PyXA scripting object.

        :param properties: A dictionary of properties to assign to this object.
        :type properties: dict, optional

        .. versionchanged:: 0.0.3
           Removed on-the-fly creation of class attributes. All objects should concretely define their properties.

        .. versionadded:: 0.0.1
        """
        if properties is not None:
            self.xa_prnt = properties.get("parent", None)
            self.xa_elem = properties.get("element", None)
            self.xa_scel = properties.get("scriptable_element", None)
            self.xa_aref = properties.get("appref", None)

    @property
    def xa_wksp(self):
        return workspace

    @property
    def xa_sevt(self):
        if XAObject._xa_sevt is None:
            XAObject._xa_sevt = Application("System Events")
        return XAObject._xa_sevt

    @property
    def xa_estr(self):
        if XAObject._xa_estr is None:
            import EventKit

            XAObject._xa_estr = self._exec_suppresed(EventKit.EKEventStore.alloc().init)
        return XAObject._xa_estr

    def _exec_suppresed(self, f: Callable[..., Any], *args: Any) -> Any:
        """Silences unwanted and otherwise unavoidable warning messages.

        Taken from: https://stackoverflow.com/a/3946828

        :param f: The function to execute
        :type f: Callable[...]
        :param args: The parameters to pass to the specified function
        :type args: Any
        :raises error: Any exception that occurs while trying to run the specified function
        :return: The value returned by the specified function upon execution
        :rtype: Any

        .. versionadded:: 0.0.2
        """
        error = None
        value = None

        old_stderr = os.dup(sys.stderr.fileno())
        fd = os.open("/dev/null", os.O_CREAT | os.O_WRONLY)
        os.dup2(fd, sys.stderr.fileno())
        try:
            value = f(*args)
        except Exception as e:
            error = e
        os.dup2(old_stderr, sys.stderr.fileno())

        if error is not None:
            raise error
        return value

    def _new_element(
        self, obj: "AppKit.NSObject", obj_class: type = "XAObject", *args: list[Any]
    ) -> "XAObject":
        """Wrapper for creating a new PyXA object.

        :param folder_obj: The Objective-C representation of an object.
        :type folder_obj: NSObject
        :return: The PyXA representation of the object.
        :rtype: XAObject

        .. versionchannged:: 0.1.2

           Now returns `None` if no object is provided or if the object itself is `None`.

        .. versionadded:: 0.0.1
        """
        if obj is None:
            return None

        if obj_class is None:
            return obj

        properties = {
            "parent": self,
            "element": obj,
            "appref": getattr(self, "xa_aref", None),
        }
        return obj_class(properties, *args)

    def _spawn_thread(
        self,
        function: Callable[..., Any],
        args: Union[list[Any], None] = None,
        kwargs: Union[list[Any], None] = None,
        daemon: bool = True,
    ) -> threading.Thread:
        """Spawns a new thread running the specified function.

        :param function: The function to run in the new thread
        :type function: Callable[..., Any]
        :param args: Arguments to pass to the function
        :type args: list[Any]
        :param kwargs: Keyword arguments to pass to the function
        :type kwargs: list[Any]
        :param daemon: Whether the thread should be a daemon thread, defaults to True
        :type daemon: bool, optional
        :return: The thread object
        :rtype: threading.Thread

        .. versionadded:: 0.0.9
        """
        new_thread = threading.Thread(
            target=function, args=args or [], kwargs=kwargs or {}, daemon=daemon
        )
        new_thread.start()
        return new_thread

    def set_properties(self, properties: dict) -> "XAObject":
        """Updates the value of multiple properties of the scripting element associated with this object.

        :param properties: A dictionary defining zero or more property names and updated values as key-value pairs.
        :type properties: dict
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. deprecated:: 0.2.0

           Use :func:`set_property` instead.

        .. versionadded:: 0.0.1
        """
        property_dict = {}
        for key in properties:
            parts = key.split("_")
            titled_parts = [part.title() for part in parts[1:]]
            property_name = parts[0] + "".join(titled_parts)
            property_dict[property_name] = properties[key]
        self.xa_elem.setValuesForKeysWithDictionary_(property_dict)
        return self

    def set_property(self, property_name: str, value: Any) -> "XAObject":
        """Updates the value of a single property of the scripting element associated with this object.

        :param property: The name of the property to assign a new value to.
        :type property: str
        :param value: The value to assign to the specified property.
        :type value: Any
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        if "_" in property_name:
            parts = property_name.split("_")
            titled_parts = [part.title() for part in parts[1:]]
            property_name = parts[0] + "".join(titled_parts)
        self.xa_elem.setValue_forKey_(value, property_name)
        return self

    def exists(self) -> bool:
        """Returns true if the scripting object referenced by this PyXA object exists, false otherwise.

        :return: True if the scripting object exists
        :rtype: bool

        .. versionadded:: 0.2.2
        """
        return self.xa_elem.exists()

    def __eq__(self, other: "XAObject"):
        if other is None:
            return False

        if hasattr(self.xa_elem, "get"):
            return self.xa_elem.get() == other.xa_elem.get()

        if isinstance(other, list) or isinstance(other.xa_elem, AppKit.NSArray):
            return len(self.xa_elem) == len(other.xa_elem) and all(
                [x == y for x, y in zip(self.xa_elem, other.xa_elem)]
            )

        return self.xa_elem == other.xa_elem


class XAList(XAObject):
    """A wrapper around NSArray and NSMutableArray objects enabling fast enumeration and lazy evaluation of Objective-C objects.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self,
        properties: dict,
        object_class: type = None,
        filter: Union[dict, None] = None,
    ):
        """Creates an efficient wrapper object around a list of scriptable elements.

        :param properties: PyXA properties passed to this object for utility purposes
        :type properties: dict
        :param object_class: _description_, defaults to None
        :type object_class: type, optional
        :param filter: A dictionary of properties and values to filter items by, defaults to None
        :type filter: Union[dict, None], optional

        .. versionchanged:: 0.0.8
           The filter property is deprecated and will be removed in a future version. Use the :func:`filter` method instead.

        .. versionadded:: 0.0.3
        """
        super().__init__(properties)
        self.xa_ocls = object_class

        if not isinstance(self.xa_elem, AppKit.NSArray) and not isinstance(
            self.xa_elem, ScriptingBridge.SBElementArray
        ):
            self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(self.xa_elem)

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def by_property(self, property: str, value: Any) -> XAObject:
        """Retrieves the first element whose property value matches the given value, if one exists.

        :param property: The property to match
        :type property: str
        :param value: The value to match
        :type value: Any
        :return: The matching element, if one is found
        :rtype: XAObject

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> photo = app.media_items().by_property("id", "CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001")
        >>> print(photo)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001>

        .. versionadded:: 0.0.6
        """
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)

        if len(ls) == 0:
            return None

        try:
            obj = ls.firstObject()
        except AttributeError:
            # List object has no get method
            obj = ls.firstObject()

        return self._new_element(obj, self.xa_ocls)

    def _format_for_filter(self, filter, value1, value2=None):
        if "_" in filter and " " not in filter:
            parts = filter.split("_")
            filter = parts[0]
            if len(parts) > 1:
                for part in parts[1:]:
                    filter += part.title()

        return (filter, value1, value2)

    def map(self, function: Callable[[object], object]) -> "XAList":
        """Applies the given function to each element in the list and returns a new :class:`XAList` containing the results.

        This is most effective when the function does not access the element's properties, as this will cause the element to be fully dereferenced. In such cases, it is better (faster) to use subclass-specific fast-enumeration methods. Use this method to associate element references with other data, e.g. by wrapping each element in a dictionary.

        :param function: The function to apply to each element
        :type function: Callable[[object], object]
        :return: The new list containing the results of the function
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> notes = app.notes()
        >>> indexed_notes = notes.map(lambda element, index: {"element": element, "id": index})
        >>> print(indexed_notes[0])
        {'element': <<class 'PyXA.apps.Notes.XANote'>Example Note, x-coredata://314D805E-C349-42A0-96EC-380EE21392E2/ICNote/p9527>, 'id': 0}

        .. versionadded:: 0.3.0
        """
        new_arr = AppKit.NSMutableArray.alloc().initWithArray_(self.xa_elem)

        def apply_to_index(index):
            new_arr.replaceObjectAtIndex_withObject_(
                index, function(self._new_element(new_arr[index], self.xa_ocls), index)
            )

        queue = libdispatch.dispatch_get_global_queue(
            libdispatch.DISPATCH_QUEUE_PRIORITY_HIGH, 0
        )
        libdispatch.dispatch_apply(
            self.xa_elem.count(), queue, lambda i: apply_to_index(i)
        )

        return self._new_element(new_arr, XAList)

    def equalling(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value equals the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("TV")
        >>> print(app.tracks().equalling("playedCount", 0))
        <<class 'PyXA.apps.TV.XATVTrackList'>['Frozen', 'Sunshine', 'The Hunger Games: Mockingjay - Part 2', ...]>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_eq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def not_equalling(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value does not equal the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("TV")
        >>> print(app.tracks().not_equalling("playedCount", 0))
        <<class 'PyXA.apps.TV.XATVTrackList'>['The Avatar State', 'The Cave of Two Lovers', 'Return to Omashu', ...]>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_neq_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def containing(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value contains the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Reminders")
        >>> print(app.reminders().containing("name", "PyXA"))
        <<class 'PyXA.apps.Reminders.XARemindersReminderList'>['PyXA v0.1.0 release']>

        .. versionadded:: 0.0.6
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_contains_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def not_containing(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value does not contain the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Reminders")
        >>> print(app.reminders().not_containing("name", " "))
        <<class 'PyXA.apps.Reminders.XARemindersReminderList'>['Trash', 'Thing', 'Reminder', ...]>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        ls = XAPredicate.evaluate_with_format(
            self.xa_elem, f'NOT {property} CONTAINS "{value}"'
        )
        return self._new_element(ls, self.__class__)

    def beginning_with(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value begins with the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("System Events")
        >>> print(app.downloads_folder.files().beginning_with("name", "Example"))
        <<class 'PyXA.apps.SystemEvents.XASystemEventsFileList'>['Example.png', 'ExampleImage.png', ...]>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_begins_with_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def ending_with(self, property: str, value: str) -> "XAList":
        """Retrieves all elements whose property value ends with the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to search for
        :type value: str
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("System Events")
        >>> print(app.downloads_folder.files().ending_with("name", ".png"))
        <<class 'PyXA.apps.SystemEvents.XASystemEventsFileList'>['Example.png', 'Image.png', ...]>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_ends_with_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def greater_than(self, property: str, value: Union[int, float]) -> "XAList":
        """Retrieves all elements whose property value is greater than the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to compare against
        :type value: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> print(app.media_items().greater_than("altitude", 10000)[0].spotlight())
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=53B0F28E-0B39-446B-896C-484CD0DC2D3C/L0/001>

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_gt_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def less_than(self, property: str, value: Union[int, float]) -> "XAList":
        """Retrieves all elements whose property value is less than the given value.

        :param property: The property to match
        :type property: str
        :param value: The value to compare against
        :type value: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> app = PyXA.Application("Music")
        >>> tracks = app.tracks()
        >>> print(tracks.less_than("playedCount", 5).name())
        ['Outrunning Karma', 'Death of a Hero', '1994', 'Mind Is a Prison']

        .. versionadded:: 0.1.0
        """
        property, value, _ = self._format_for_filter(property, value)
        predicate = XAPredicate()
        predicate.add_lt_condition(property, value)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def between(
        self, property: str, value1: Union[int, float], value2: Union[int, float]
    ) -> "XAList":
        """Retrieves all elements whose property value is between the given values.

        :param property: The property to match
        :type property: str
        :param value1: The lower-end of the range to match
        :type value1: Union[int, float]
        :param value2: The upper-end of the range to match
        :type value2: Union[int, float]
        :return: The list of matching elements
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> from datetime import datetime, timedelta
        >>>
        >>> app = PyXA.Application("Calendar")
        >>> events = app.calendars()[3].events()
        >>> now = datetime.now()
        >>> print(events.between("startDate", now, now + timedelta(days=1)))
        <<class 'PyXA.apps.Calendar.XACalendarEventList'>['Capstone Meeting', 'Lunch with Dan']>

        .. versionadded:: 0.1.0
        """
        property, value1, value2 = self._format_for_filter(property, value1, value2)
        predicate = XAPredicate()
        predicate.add_gt_condition(property, value1)
        predicate.add_lt_condition(property, value2)
        ls = predicate.evaluate(self.xa_elem)
        return self._new_element(ls, self.__class__)

    def exists(self, property: str) -> "XAList":
        """Retrieves all elements whose specified property value exists.

        :param property: The property to check the existence of
        :type property: str
        :return: The list of matching elements
        :rtype: XAList

        .. versionadded:: 0.2.2
        """
        ls = [x for x in self.xa_elem if getattr(x, property)().exists()]
        return self._new_element(ls, self.__class__)

    def not_exists(self, property: str) -> "XAList":
        """Retrieves all elements whose specified property value does not exist.

        :param property: The property to check the non-existence of
        :type property: str
        :return: The list of matching elements
        :rtype: XAList

        .. versionadded:: 0.2.2
        """
        ls = [x for x in self.xa_elem if not getattr(x, property)().exists()]
        return self._new_element(ls, self.__class__)

    def filter(
        self,
        filter: str,
        comparison_operation: Union[str, None] = None,
        value1: Union[Any, None] = None,
        value2: Union[Any, None] = None,
    ) -> "XAList":
        """Filters the list by the given parameters.

        The filter may be either a format string, used to create an NSPredicate, or up to 4 arguments specifying the filtered property name, the comparison operation, and up to two values to compare against.

        :param filter: A format string or a property name
        :type filter: str
        :param comparison_operation: The symbol or name of a comparison operation, such as > or <, defaults to None
        :type comparison_operation: Union[str, None], optional
        :param value1: The first value to compare each list item's property value against, defaults to None
        :type value1: Union[Any, None], optional
        :param value2: The second value to compare each list item's property value against, defaults to None
        :type value2: Union[Any, None], optional
        :return: The filtered XAList object
        :rtype: XAList

        :Example 1: Get the last file sent by you (via this machine) in Messages.app

        >>> import PyXA
        >>> app = PyXA.Application("Messages")
        >>> last_file_transfer = app.file_transfers().filter("direction", "==", app.MessageDirection.OUTGOING)[-1]
        >>> print(last_file_transfer)
        <<class 'PyXA.apps.Messages.XAMessagesFileTransfer'>Test.jpg>

        :Example 2: Get the list of favorite photos/videos from Photos.app

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> favorites = app.media_items().filter("favorite", "==", True)
        >>> print(favorites)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItemList'>['CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001', 'EFEB7F37-8373-4972-8E43-21612F597185/L0/001', ...]>

        .. note::

           For properties that appear to be boolean but fail to return expected filter results, try using the corresponding 0 or 1 value instead.

        :Example 3: Provide a custom format string

        >>> import PyXA
        >>> app = PyXA.Application("Photos")
        >>> photo = app.media_items().filter("id == 'CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001'")[0]
        >>> print(photo)
        <<class 'PyXA.apps.PhotosApp.XAPhotosMediaItem'>id=CB24FE9F-E9DC-4A5C-A0B0-CC779B1CEDCE/L0/001>

        :Example 4: Get All Top-Level Playlists in Music.app

        >>> import PyXA
        >>> app = PyXA.Music()
        >>> top_level_playlists = app.playlists().filter("parent", "!exists")
        >>> print(top_level_playlists)

        .. versionadded:: 0.0.8
        """
        filter, value1, value2 = self._format_for_filter(filter, value1, value2)
        if comparison_operation.lower() == "exists":
            return self.exists(filter)
        elif comparison_operation.lower() in ["not exists", "!exists", "nonexistent"]:
            return self.not_exists(filter)
        if comparison_operation is not None and value1 is not None:
            predicate = XAPredicate()
            if comparison_operation in ["=", "==", "eq", "EQ", "equals", "EQUALS"]:
                predicate.add_eq_condition(filter, value1)
            elif comparison_operation in [
                "!=",
                "!==",
                "neq",
                "NEQ",
                "not equal to",
                "NOT EQUAL TO",
            ]:
                predicate.add_neq_condition(filter, value1)
            elif comparison_operation in [
                ">",
                "gt",
                "GT",
                "greater than",
                "GREATER THAN",
            ]:
                predicate.add_gt_condition(filter, value1)
            elif comparison_operation in ["<", "lt", "LT", "less than", "LESS THAN"]:
                predicate.add_lt_condition(filter, value1)
            elif comparison_operation in [
                ">=",
                "geq",
                "GEQ",
                "greater than or equal to",
                "GREATER THAN OR EQUAL TO",
            ]:
                predicate.add_geq_condition(filter, value1)
            elif comparison_operation in [
                "<=",
                "leq",
                "LEQ",
                "less than or equal to",
                "LESS THAN OR EQUAL TO",
            ]:
                predicate.add_leq_condition(filter, value1)
            elif comparison_operation in [
                "begins with",
                "beginswith",
                "BEGINS WITH",
                "BEGINSWITH",
            ]:
                predicate.add_begins_with_condition(filter, value1)
            elif comparison_operation in ["contains", "CONTAINS"]:
                predicate.add_contains_condition(filter, value1)
            elif comparison_operation in [
                "ends with",
                "endswith",
                "ENDS WITH",
                "ENDSWITH",
            ]:
                predicate.add_ends_with_condition(filter, value1)
            elif comparison_operation in ["between", "BETWEEN"]:
                predicate.add_between_condition(filter, value1, value2)
            elif comparison_operation in ["matches", "MATCHES"]:
                predicate.add_match_condition(filter, value1)

            filtered_list = predicate.evaluate(self.xa_elem)
            return super()._new_element(filtered_list, self.__class__)
        else:
            filtered_list = XAPredicate.evaluate_with_format(self.xa_elem, filter)
            return super()._new_element(filtered_list, self.__class__)

    def at(self, index: int) -> XAObject:
        """Retrieves the element at the specified index.

        :param index: The index of the desired element
        :type index: int
        :return: The PyXA-wrapped element object
        :rtype: XAObject

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem[index], self.xa_ocls)

    @property
    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.firstObject(), self.xa_ocls)

    @property
    def last(self) -> XAObject:
        """Retrieves the last element of the list as a wrapped PyXA object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.lastObject(), self.xa_ocls)

    def shuffle(self) -> "XAList":
        """Randomizes the order of objects in the list.

        :return: A reference to the shuffled XAList
        :rtype: XAList

        .. versionadded:: 0.0.3
        """
        try:
            self.xa_elem = self.xa_elem.shuffledArray()
        except AttributeError as e:
            try:
                random.shuffle(self.xa_elem)
            except TypeError:
                self.xa_elem = [x for x in self.xa_elem]
                random.shuffle(self.xa_elem)
                self.xa_elem = AppKit.NSArray.alloc().initWithArray_(self.xa_elem)
        return self

    def extend(self, ls: Union["XAList", list]):
        """Appends all elements of the supplied list to the end of this list.

        :param ls: _description_
        :type ls: Union[XAList, list]

        .. versionadded:: 0.1.1
        """
        arr1 = AppKit.NSMutableArray.alloc().initWithArray_(self.xa_elem)

        if isinstance(ls, XAList):
            ls = ls.xa_elem
        else:
            ls = AppKit.NSMutableArray.alloc().initWithArray_(ls)

        arr1.addObjectsFromArray_(ls)
        self.xa_elem = arr1

    def push(self, *elements: list[XAObject]) -> Union[XAObject, list[XAObject], None]:
        """Appends the object referenced by the provided PyXA wrapper to the end of the list.

        .. versionadded:: 0.0.3
        """
        objects = []
        num_added = 0

        for element in elements:
            len_before = len(self.xa_elem)
            self.xa_elem.addObject_(element.xa_elem)
            len_after = len(self.xa_elem)

            if len_after == len_before:
                # Object wasn't added -- try force-getting the list before adding
                self.xa_elem.get().addObject_(element.xa_elem)

            if len_after > len_before:
                num_added += 1
                objects.append(self[len_after - 1])

        if num_added == 1:
            return objects[0]

        if num_added == 0:
            return None

        return objects

    def insert(self, element: XAObject, index: int):
        """Inserts the object referenced by the provided PyXA wrapper at the specified index.

        .. versionadded:: 0.0.3
        """
        self.xa_elem.insertObject_atIndex_(element.xa_elem, index)

    def pop(self, index: int = -1) -> XAObject:
        """Removes the object at the specified index from the list and returns it.

        .. versionadded:: 0.0.3
        """
        removed = self.xa_elem.lastObject()
        self.xa_elem.removeLastObject()
        return self._new_element(removed, self.xa_ocls)

    def index(self, element: XAObject) -> int:
        """Returns the index of the first occurrence of the element in the list, or -1 if no such element exists in the list.

        .. versionadded:: 0.1.2
        """
        for index, item in enumerate(self.xa_elem):
            if item == element.xa_elem:
                return index

        for index, item in enumerate(self):
            if item == element:
                return index

        return -1

    def count(self, count_function: Callable[[object], bool]) -> int:
        """Counts the number of entries in the list for which the provided function is True.

        :param count_function: The function to check entries against
        :type count_function: Callable[[object], bool]
        :return: The number of entries for which the given function is True.
        :rtype: int

        .. versionadded:: 0.1.0
        """
        count = 0
        for index in range(len(self)):
            in_count = False
            try:
                in_count = count_function(self.xa_elem[index])
            except:
                # TODO: Add logging message here
                pass

            if not in_count:
                try:
                    in_count = count_function(self[index])
                except:
                    pass

            if in_count:
                count += 1
        return count

    def __getitem__(self, key: Union[int, slice]):
        if isinstance(key, slice):
            arr = AppKit.NSMutableArray.alloc().initWithArray_(
                [
                    self.xa_elem[index]
                    for index in range(key.start, key.stop, key.step or 1)
                ]
            )
            return self._new_element(arr, self.__class__)
        if key < 0:
            key = self.xa_elem.count() + key

        return self._new_element(self.xa_elem.objectAtIndex_(key), self.xa_ocls)

    def __len__(self):
        return len(self.xa_elem)

    def __reversed__(self):
        self.xa_elem = self.xa_elem.reverseObjectEnumerator().allObjects()
        return self

    def __iter__(self):
        return (
            self._new_element(object, self.xa_ocls)
            for object in self.xa_elem.objectEnumerator()
        )

    def __contains__(self, item):
        if isinstance(item, XAObject):
            item = item.xa_elem
        return item in self.xa_elem

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"


class XAApplicationList(XAList):
    """A wrapper around a list of applications.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAApplication, filter)

        if filter is not None:
            self.xa_elem = XAPredicate().from_dict(filter).evaluate(self.xa_elem)

    def first(self) -> XAObject:
        """Retrieves the first element of the list as a wrapped PyXA application object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(0)

    def last(self) -> XAObject:
        """Retrieves the last element of the list as a wrapped PyXA application object.

        :return: The wrapped object
        :rtype: XAObject

        .. versionadded:: 0.0.5
        """
        return self.__getitem__(-1)

    def pop(self, index: int = -1) -> XAObject:
        """Removes the application at the specified index from the list and returns it.

        .. versionadded:: 0.0.5
        """
        removed = self.xa_elem.lastObject()
        self.xa_elem.removeLastObject()
        app_name = removed["kCGWindowOwnerName"]
        return Application(app_name)

    def __getitem__(self, key: Union[int, slice]):
        """Retrieves the wrapped application object(s) at the specified key."""
        if isinstance(key, slice):
            arr = AppKit.NSArray.alloc().initWithArray_(
                [
                    self.xa_elem[index]
                    for index in range(key.start, key.stop, key.step or 1)
                ]
            )
            return self._new_element(arr, self.__class__)
        app_name = self.xa_elem[key]["kCGWindowOwnerName"]
        return Application(app_name)

    def bundle_identifier(self) -> list[str]:
        return [app.bundle_identifier for app in self]

    def bundle_url(self) -> list["XAURL"]:
        return [XAURL(app.bundle_url) for app in self]

    def executable_url(self) -> list["XAURL"]:
        return [XAURL(app.executable_url) for app in self]

    def launch_date(self) -> list[datetime]:
        return [app.launch_date for app in self]

    def localized_name(self) -> list[str]:
        return [x.get("kCGWindowOwnerName") for x in self.xa_elem]

    def process_identifier(self) -> list[str]:
        return [x.get("kCGWindowOwnerPID") for x in self.xa_elem]

    def by_bundle_identifier(
        self, bundle_identifier: str
    ) -> Union["XAApplication", None]:
        for app in self:
            if app.bundle_identifier == bundle_identifier:
                return app

    def by_bundle_url(
        self, bundle_url: Union["XAURL", str]
    ) -> Union["XAApplication", None]:
        if isinstance(bundle_url, str):
            bundle_url = XAURL(bundle_url)

        for app in self:
            if app.bundle_url.xa_elem == bundle_url.xa_elem:
                return app

    def by_executable_url(
        self, executable_url: Union["XAURL", str]
    ) -> Union["XAApplication", None]:
        if isinstance(executable_url, str):
            executable_url = XAURL(executable_url)

        for app in self:
            if app.executable_url.xa_elem == executable_url.xa_elem:
                return app

    def by_launch_date(self, launch_date: datetime) -> Union["XAApplication", None]:
        for app in self:
            if app.launch_date == launch_date:
                return app

    def by_localized_name(self, localized_name: str) -> Union["XAApplication", None]:
        for index, app in enumerate(self.xa_elem):
            if app.get("kCGWindowOwnerName") == localized_name:
                return self.__getitem__(index)

    def by_process_identifier(
        self, process_identifier: str
    ) -> Union["XAApplication", None]:
        for index, app in enumerate(self.xa_elem):
            if app.get("kCGWindowOwnerPID") == process_identifier:
                return self.__getitem__(index)

    def hide(self):
        """Hides all applications in the list.

        :Example 1: Hide all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.hide()

        .. seealso:: :func:`unhide`

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.hide()

    def unhide(self):
        """Unhides all applications in the list.

        :Example 1: Hide then unhide all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.hide()
        >>> apps.unhide()

        .. seealso:: :func:`hide`

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.unhide()

    def terminate(self):
        """Quits (terminates) all applications in the list. Synonymous with :func:`quit`.

        :Example 1: Terminate all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.terminate()

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.terminate()

    def quit(self):
        """Quits (terminates) all applications in the list. Synonymous with :func:`terminate`.

        :Example 1: Quit all visible running applications

        >>> import PyXA
        >>> apps = PyXA.running_applications()
        >>> apps.quit()

        .. versionadded:: 0.0.5
        """
        for app in self:
            app.terminate()

    def windows(self) -> "XAList":
        """Retrieves a list of every window belonging to each application in the list.

        Operations on the list of windows will specialized to scriptable and non-scriptable application window operations as necessary.

        :return: A list containing both scriptable and non-scriptable windows
        :rtype: XAList

        :Example:

        >>> import PyXA
        >>> windows = PyXA.running_applications().windows()
        >>> windows.collapse()
        >>> sleep(1)
        >>> windows.uncollapse()

        .. versionchanged 0.1.2

            Now returns an instance of :class:`PyXA.apps.SystemEvents.XASystemEventsWindowList`

        .. versionchanged:: 0.1.1

           Now returns an instance of :class:`XAWindowList` instead of :class:`XACombinedWindowList`.

        .. versionadded:: 0.0.5
        """
        return self.xa_sevt.processes().windows()

    def __iter__(self):
        return (
            Application(object["kCGWindowOwnerName"])
            for object in self.xa_elem.objectEnumerator()
        )

    def __contains__(self, item):
        if isinstance(item, XAApplication):
            return item.process_identifier in self.process_identifier()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.localized_name()) + ">"


class Application(XAObject):
    """A wrapper around a macOS application providing access to its scripting functionality.

    .. versionchanged:: 0.1.1

       Moved into the XABase module.

    .. versionadded:: 0.1.0
    """

    app_paths: list[str] = []  #: A list containing the path to each application

    def __init__(self, app_name: str):
        """Creates a new application object.

        :param app_name: The name of the target application
        :type app_name: str

        .. versionadded:: 0.1.0
        """
        # Elevate to XAApplication
        new_self = self.__get_application(app_name)
        self.__class__ = new_self.__class__
        self.__dict__.update(new_self.__dict__)

    def __xa_get_path_to_app(self, app_identifier: str) -> str:
        self.__xa_load_app_paths()
        candidate = None
        for path in self.app_paths:
            app_path_component = path.split("/")[-1][:-4]
            if (
                app_identifier.lower() == path.lower()
                or app_identifier.lower() == app_path_component.lower()
            ):
                return path

            if app_identifier.lower() in path.lower():
                candidate = path

        if candidate is not None:
            return candidate

        raise ApplicationNotFoundError(app_identifier)

    def __xa_load_app_paths(self):
        if self.app_paths == []:
            search = XASpotlight()
            search.predicate = "kMDItemContentType == 'com.apple.application-bundle'"
            search.run()
            self.app_paths = [x.path for x in search.results]

    def __get_application(self, app_identifier: str) -> "XAApplication":
        """Retrieves a PyXA application object representation of the target application without launching or activating the application.

        :param app_identifier: The name of the application to get an object of.
        :type app_identifier: str
        :return: A PyXA application object referencing the target application.
        :rtype: XAApplication

        .. versionadded:: 0.0.1
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()

        app_identifier_l = app_identifier.lower()

        def _match_open_app(obj, index, stop):
            res = obj.localizedName().lower() == app_identifier_l
            return res, res

        idx_set = workspace.runningApplications().indexesOfObjectsPassingTest_(
            _match_open_app
        )
        if idx_set.count() == 1:
            index = idx_set.firstIndex()
            app = workspace.runningApplications()[index]
            properties = {
                "parent": None,
                "element": app,
                "appref": app,
            }

            app_obj = application_classes.get(app_identifier_l, XAApplication)
            if isinstance(app_obj, tuple):
                module = importlib.import_module("PyXA.apps." + app_obj[0])
                app_class = getattr(module, app_obj[1], None)
                if app_class is not None:
                    application_classes[app_identifier_l] = app_class
                    app = app_class
                else:
                    raise NotImplementedError()

            # Check if the app is supported by PyXA
            app_ref = application_classes.get(app_identifier_l, XAApplication)(
                properties
            )
            return app_ref

        app_path = app_identifier
        if not app_identifier.startswith("/"):
            app_path = self.__xa_get_path_to_app(app_identifier)
        bundle = AppKit.NSBundle.alloc().initWithPath_(app_path)
        url = workspace.URLForApplicationWithBundleIdentifier_(
            bundle.bundleIdentifier()
        )

        config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
        config.setActivates_(False)
        config.setHides_(True)

        app_ref = None

        def _launch_completion_handler(app, _error):
            nonlocal app_ref
            properties = {
                "parent": None,
                "element": app,
                "appref": app,
            }

            app_obj = application_classes.get(app_identifier_l, None)
            if isinstance(app_obj, tuple):
                module = importlib.import_module("PyXA.apps." + app_obj[0])
                app_class = getattr(module, app_obj[1], None)
                if app_class is not None:
                    application_classes[app_identifier_l] = app_class
                    app = app_class
                else:
                    raise NotImplementedError()

            app_ref = application_classes.get(app_identifier_l, XAApplication)(
                properties
            )

        workspace.openApplicationAtURL_configuration_completionHandler_(
            url, config, _launch_completion_handler
        )
        while app_ref is None:
            time.sleep(0.01)
        return app_ref


def current_application() -> "XAApplication":
    """Retrieves a PyXA representation of the frontmost application.

    :return: A PyXA application object referencing the current application.
    :rtype: XAApplication

    .. versionchanged:: 0.1.1

       Moved into the XABase module.

    .. versionadded:: 0.0.1
    """
    global workspace
    if workspace is None:
        workspace = AppKit.NSWorkspace.sharedWorkspace()
    return Application(workspace.frontmostApplication().localizedName())


def running_applications(unique=True) -> list["XAApplication"]:
    """Gets PyXA references to all currently visible (not hidden or minimized) running applications whose app bundles are stored in typical application directories. Applications are ordered by their z-index, with the frontmost application first.

    :param unique: Whether to return only one instance of each application, defaults to True
    :type unique: bool, optional
    :return: A list of PyXA application objects.
    :rtype: list[XAApplication]

    :Example 1: Get the name of each running application

    >>> import PyXA
    >>> apps = PyXA.running_applications()
    >>> print(apps.localized_name())
    ['GitHub Desktop', 'Safari', 'Code', 'Terminal', 'Notes', 'Messages', 'TV']

    .. versionchanged:: 0.3.0

        Added the :attr:`unique` parameter.

    .. versionadded:: 0.0.1
    """
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID
    )
    ls = XAPredicate.evaluate_with_format(windows, "kCGWindowLayer == 0")

    # Filter list to unique applications
    if unique:
        app_names = []
        ls = [
            x
            for x in ls
            if x["kCGWindowOwnerName"] not in app_names
            and (app_names.append(x["kCGWindowOwnerName"]) or True)
        ]

    properties = {
        "element": ls,
    }
    arr = XAApplicationList(properties)
    return arr


SUPPORTED_BROWSERS = [
    "Safari",
    "Google Chrome",
    "Google Chrome Canary",
    "Google Chrome Beta",
    "Google Chrome Dev",
    "Chromium",
    "Brave Browser",
    "Brave Browser Dev",
    "Brave Browser Beta",
    "Brave Browser Nightly",
    "Microsoft Edge",
    "Microsoft Edge Beta",
    "Microsoft Edge Dev",
    "Microsoft Edge Canary",
    "Opera",
    "Opera Beta",
    "Opera Developer",
    "Opera GX",
    "Opera Neon",
    "Vivaldi",
    "Blisk",
    "Iridium",
    "Yandex",
    "Maxthon",
    "Maxthon Beta",
    "Arc",
    "OmniWeb",
]
"""Browsers supported by PyXA, i.e. having dedicated PyXA Application classes.
"""


def active_browser() -> "XAApplication":
    """Retrieves a PyXA representation of the most recently active browser application. The browser must have at least one open window. The browser must be one of the ones listed in :attr:`SUPPORTED_BROWSERS`.

    :return: A PyXA application object referencing the current browser application.
    :rtype: XAApplication

    .. versionadded:: 0.3.0
    """
    running_app_names = running_applications().localized_name()
    for browser in running_app_names:
        if browser in SUPPORTED_BROWSERS:
            return Application(browser)


class XAApplication(XAObject, XAClipboardCodable):
    """A general application class for both officially scriptable and non-scriptable applications.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.__xa_prcs = None

    @property
    def xa_apsc(self):
        import appscript

        return appscript.app(self.bundle_url.path())

    @property
    def xa_prcs(self):
        if self.__xa_prcs == None:
            processes = self.xa_sevt.processes()
            self.__xa_prcs = processes.by_displayed_name(self.xa_elem.localizedName())
        return self.__xa_prcs

    @property
    def bundle_identifier(self) -> str:
        """The bundle identifier for the application.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.bundleIdentifier()

    @property
    def bundle_url(self) -> str:
        """The file URL of the application bundle.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.bundleURL()

    @property
    def executable_url(self) -> str:
        """The file URL of the application's executable.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.executableURL()

    @property
    def frontmost(self) -> bool:
        """Whether the application is the active application.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.isActive()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        if frontmost is True:
            self.xa_elem.activateWithOptions_(
                AppKit.NSApplicationActivateIgnoringOtherApps
            )

    @property
    def launch_date(self) -> datetime:
        """The date and time that the application was launched.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.launchDate()

    @property
    def localized_name(self) -> str:
        """The application's name.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.localizedName()

    @property
    def owns_menu_bar(self) -> bool:
        """Whether the application owns the top menu bar.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.ownsMenuBar()

    @property
    def process_identifier(self) -> str:
        """The process identifier for the application instance.

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.processIdentifier()

    @property
    def icon(self) -> "XAImage":
        """The application's icon.

        .. versionadded:: 0.1.1
        """
        return XAImage(self.xa_elem.icon())

    def launch(self) -> "XAApplication":
        """Launches the application.

        :return: The application object.
        :rtype: XAApplication

        .. versionadded:: 0.1.1
        """
        config = AppKit.NSWorkspaceOpenConfiguration.alloc().init()
        config.setActivates_(False)
        config.setHides_(True)

        finished_launching = False

        def test(app, error):
            nonlocal finished_launching
            finished_launching = True

        self.xa_wksp.openApplicationAtURL_configuration_completionHandler_(
            self.bundle_url, config, test
        )

        while not finished_launching:
            time.sleep(0.05)

        return self

    def activate(self) -> "XAApplication":
        """Activates the application, bringing its window(s) to the front and launching the application beforehand if necessary.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        .. seealso:: :func:`terminate`, :func:`unhide`, :func:`focus`

        .. versionadded:: 0.0.1
        """
        if not self.xa_elem.isFinishedLaunching():
            self.launch()

        if self.xa_elem.isHidden():
            self.unhide()

        self.xa_elem.activateWithOptions_(
            AppKit.NSApplicationActivateAllWindows
            | AppKit.NSApplicationActivateIgnoringOtherApps
        )
        return self

    def terminate(self) -> "XAApplication":
        """Quits the application. Synonymous with quit().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.terminate()

        .. seealso:: :func:`quit`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def quit(self) -> "XAApplication":
        """Quits the application. Synonymous with terminate().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.quit()

        .. seealso:: :func:`terminate`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def hide(self) -> "XAApplication":
        """Hides all windows of the application.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.hide()

        .. seealso:: :func:`unhide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.hide()
        return self

    def unhide(self) -> "XAApplication":
        """Unhides (reveals) all windows of the application, but does not does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.unhide()

        .. seealso:: :func:`hide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.unhide()
        return self

    def focus(self) -> "XAApplication":
        """Hides the windows of all applications except this one.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.focus()

        .. seealso:: :func:`unfocus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
            if app.localizedName() != self.xa_elem.localizedName():
                app.hide()
            else:
                app.unhide()
        return self

    def unfocus(self) -> "XAApplication":
        """Unhides (reveals) the windows of all other applications, but does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.Application("Safari")
        >>> safari.unfocus()

        .. seealso:: :func:`focus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
            app.unhide()
        return self

    def _get_processes(self, processes):
        for process in self.xa_sevt.processes():
            processes.append(process)

    def windows(self, filter: dict = None) -> XAList:
        return self.xa_prcs.windows(filter)

    @property
    def front_window(self) -> XAObject:
        """The frontmost window of the application."""
        return self.xa_prcs.front_window

    def menu_bars(self, filter: dict = None) -> XAList:
        return self.xa_prcs.menu_bars(filter)

    def get_clipboard_representation(
        self,
    ) -> list[Union[str, "AppKit.NSURL", "AppKit.NSImage"]]:
        """Gets a clipboard-codable representation of the application.

        When the clipboard content is set to an application, three items are placed on the clipboard:
        1. The application's name
        2. The URL to the application bundle
        3. The application icon

        After copying an application to the clipboard, pasting will have the following effects:
        - In Finder: Paste a copy of the application bundle in the current directory
        - In Terminal: Paste the name of the application followed by the path to the application
        - In iWork: Paste the application name
        - In Safari: Paste the application name
        - In Notes: Attach a copy of the application bundle to the active note
        The pasted content may be different for other applications.

        :return: The clipboard-codable representation
        :rtype: list[Union[str, AppKit.NSURL, AppKit.NSImage]]

        .. versionadded:: 0.0.8
        """
        return [
            self.xa_elem.localizedName(),
            self.xa_elem.bundleURL(),
            self.xa_elem.icon(),
        ]

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
            # Otherwise, fall back to appscript
            return getattr(self.xa_apsc, attr)


######################
### PyXA Utilities ###
######################
class AppleScript:
    """A class for constructing and executing AppleScript scripts.

    .. versionadded:: 0.0.5
    """

    def __init__(self, script: Union[str, list[str], None] = None):
        """Creates a new AppleScript object.

        :param script: A string or list of strings representing lines of AppleScript code, or the path to a script plaintext file, defaults to None
        :type script: Union[str, list[str], None], optional

        .. versionadded:: 0.0.5
        """
        self.script: list[str]  #: The lines of AppleScript code contained in the script
        self.last_result: Any  #: The return value of the last execution of the script
        self.file_path: XAPath  #: The file path of this script, if one exists

        if isinstance(script, str):
            if script.startswith("/"):
                with open(script, "r") as f:
                    script = f.readlines()
            else:
                script_text = re.sub(r"[ \t]+", " ", script)
                script_text = re.sub(r"[\n\r]+", "\n", script_text)
                self.script = script_text.split("\n")
        elif isinstance(script, list):
            self.script = script
        elif script == None:
            self.script = []

    @property
    def last_result(self) -> Any:
        return self.__last_result

    @property
    def file_path(self) -> "XAPath":
        return self.__file_path

    def add(self, script: Union[str, list[str], "AppleScript"]):
        """Adds the supplied string, list of strings, or script as a new line entry in the script.

        :param script: The script to append to the current script string.
        :type script: Union[str, list[str], AppleScript]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript("tell application \"Safari\"")
        >>> script.add("print the document of window 1")
        >>> script.add("end tell")
        >>> script.run()

        .. versionadded:: 0.0.5
        """
        if isinstance(script, str):
            self.script.append(script)
        elif isinstance(script, list):
            self.script.extend(script)
        elif isinstance(script, AppleScript):
            self.script.extend(script.script)

    def insert(self, index: int, script: Union[str, list[str], "AppleScript"]):
        """Inserts the supplied string, list of strings, or script as a line entry in the script starting at the given line index.

        :param index: The line index to begin insertion at
        :type index: int
        :param script: The script to insert into the current script
        :type script: Union[str, list[str], AppleScript]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> script.insert(1, "activate")
        >>> script.run()

        .. versionadded:: 0.0.9
        """
        if isinstance(script, str):
            self.script.insert(index, script)
        elif isinstance(script, list):
            for line in script:
                self.script.insert(index, line)
                index += 1
        elif isinstance(script, AppleScript):
            for line in script.script:
                self.script.insert(index, line)
                index += 1

    def pop(self, index: int = -1) -> str:
        """Removes the line at the given index from the script.

        :param index: The index of the line to remove
        :type index: int
        :return: The text of the removed line
        :rtype: str

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.pop(1))
            get chats

        .. versionadded:: 0.0.9
        """
        return self.script.pop(index)

    def load(path: Union["XAPath", str]) -> "AppleScript":
        """Loads an AppleScript (.scpt) file as a runnable AppleScript object.

        :param path: The path of the .scpt file to load
        :type path: Union[XAPath, str]
        :return: The newly loaded AppleScript object
        :rtype: AppleScript

        :Example 1: Load and run a script

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.run())
        {
            'string': None,
            'int': 0,
            'bool': False,
            'float': 0.0,
            'date': None,
            'file_url': None,
            'type_code': 845507684,
            'data': {length = 8962, bytes = 0x646c6532 00000000 6c697374 000022f2 ... 6e756c6c 00000000 },
            'event': <NSAppleEventDescriptor: [ 'obj '{ ... } ]>
        }

        :Example 2: Load, modify, and run a script

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> script.pop(1)
        >>> script.insert(1, "activate")
        >>> script.run()

        .. versionadded:: 0.0.8
        """
        if isinstance(path, str):
            path = XAPath(path)
        script = AppKit.NSAppleScript.alloc().initWithContentsOfURL_error_(
            path.xa_elem, None
        )[0]
        script_text = re.sub(r"[ \t]+", " ", str(script.richTextSource().string()))
        script_text = re.sub(r"[\n\r]+", "\n", script_text)
        script = AppleScript(script_text.split("\n"))
        script.__file_path = path
        return script

    def save(self, path: Union["XAPath", str, None] = None):
        """Saves the script to the specified file path, or to the path from which the script was loaded.

        :param path: The path to save the script at, defaults to None
        :type path: Union[XAPath, str, None], optional

        :Example 1: Save the script to a specified path

        >>> import PyXA
        >>> script = PyXA.AppleScript(f\"\"\"
        >>>     tell application "Safari"
        >>>         activate
        >>>     end tell
        >>> \"\"\")
        >>> script.save("/Users/exampleUser/Downloads/Example.scpt")

        :Example 2: Load a script, modify it, then save it

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/steven/Downloads/Example.scpt")
        >>> script.insert(2, "delay 2")
        >>> script.insert(3, "set the miniaturized of window 1 to true")
        >>> script.save()

        .. versionadded:: 0.0.9
        """
        if path is None and self.file_path is None:
            print("No path to save script to!")
            return

        if isinstance(path, str):
            path = XAPath(path)

        script = ""
        for line in self.script:
            script += line + "\n"
        script = AppKit.NSAppleScript.alloc().initWithSource_(script)
        script.compileAndReturnError_(None)
        source = script.richTextSource().string()

        if path is not None:
            self.__file_path = path

        with open(self.file_path.xa_elem.path(), "w") as f:
            f.write(source)

    def parse_result_data(result: dict) -> list[tuple[str, str]]:
        """Extracts string data from an AppleScript execution result dictionary.

        :param result: The execution result dictionary to extract data from
        :type result: dict
        :return: A list of responses contained in the result structured as tuples
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> script = PyXA.AppleScript.load("/Users/exampleUser/Downloads/Test.scpt")
        >>> print(script.script)
        >>> result = script.run()
        >>> print(PyXA.AppleScript.parse_result_data(result))
        ['tell application "Messages"', '\\tget chats', 'end tell']
        [('ID', 'iMessage;-;+12345678910'), ('ID', 'iMessage;-;+12345678911'), ('ID', 'iMessage;-;example@icloud.com'), ...]

        .. versionadded:: 0.0.9
        """
        result = result["event"]
        response_objects = []
        num_responses = result.numberOfItems()
        for response_index in range(1, num_responses + 1):
            response = result.descriptorAtIndex_(response_index)

            data = ()
            num_params = response.numberOfItems()
            if num_params == 0:
                data = response.stringValue().strip()

            else:
                for param_index in range(1, num_params + 1):
                    param = response.descriptorAtIndex_(param_index).stringValue()
                    if param is not None:
                        data += (param.strip(),)
            response_objects.append(data)

        return response_objects

    def run(self, args: list = None, dry_run=False) -> Any:
        """Compiles and runs the script, returning the result.

        :param args: A list of arguments to pass to the script, defaults to None
        :type args: list, optional
        :param dry_run: Whether to compile and check the script without running it, defaults to False
        :type dry_run: bool, optional
        :return: The return value of the script.
        :rtype: Any

        :Example 1: Basic Script Execution

        >>> import PyXA
        >>> script = PyXA.AppleScript(f\"\"\"tell application "System Events"
        >>>     return 1 + 2
        >>> end tell
        >>> \"\"\")
        >>> print(script.run())
        {
            'string': '3',
            'int': 3,
            'bool': False,
            'float': 3.0,
            'date': None,
            'file_url': None,
            'type_code': 3,
            'data': {length = 4, bytes = 0x03000000},
            'event': <NSAppleEventDescriptor: 3>
        }

        :Example 2: Run Script With Arguments

        >>> import PyXA
        >>> script = PyXA.AppleScript(f\"\"\"on run argv
        >>>     set x to item 1 of argv
        >>>     set y to item 2 of argv
        >>>     return x + y
        >>> end run\"\"\")
        >>> print(script.run([5, 6]))
        {'
            string': '11',
            'int': 11,
            'bool': False,
            'float': 11.0,
            'date': None,
            'file_url': None,
            'type_code': 11,
            'data': {length = 4, bytes = 0x0b000000},
            'event': <NSAppleEventDescriptor: 11>
        }

        .. versionadded:: 0.0.5
        """
        script = ""
        for line in self.script:
            if line.startswith("on run "):
                argv_specifier = line.split("on run ")[1].strip()
                script += "on run" + "\n"

                if args is not None:
                    if type(args) is not list:
                        args = [args]

                    args = [str(x) for x in args]

                    script += (
                        "set " + argv_specifier + ' to {"' + '", "'.join(args) + '"}\n'
                    )
                else:
                    script += "set " + argv_specifier + " to {}\n"
            else:
                script += line + "\n"

        full_script = AppKit.NSAppleScript.alloc().initWithSource_(script)
        if dry_run:
            status = full_script.compileAndReturnError_(None)
            if status[1] is not None:
                raise AppleScriptError(status[1], script)
            return status[0]

        result = full_script.executeAndReturnError_(None)
        if result[1] is not None:
            raise AppleScriptError(result[1], script)

        result = result[0]
        string_result = result.stringValue()
        if string_result is not None:
            string_result = string_result.replace("\r", "\n")

        if result is not None:
            self.__last_result = {
                "string": string_result,
                "int": result.int32Value(),
                "bool": result.booleanValue(),
                "float": result.doubleValue(),
                "date": result.dateValue(),
                "file_url": result.fileURLValue(),
                "type_code": result.typeCodeValue(),
                "data": result.data(),
                "event": result,
            }
            return self.last_result

    def __repr__(self):
        return "<" + str(type(self)) + str(self.script) + ">"


class XAPredicate(XAObject, XAClipboardCodable):
    """A predicate used to filter arrays.

    .. versionadded:: 0.0.4
    """

    def __init__(self):
        self.keys: list[str] = []
        self.operators: list[str] = []
        self.values: list[str] = []

    def from_dict(self, ref_dict: dict) -> "XAPredicate":
        """Populates the XAPredicate object from the supplied dictionary.

        The predicate will use == for all comparisons.

        :param ref_dict: A specification of key, value pairs
        :type ref_dict: dict
        :return: The populated predicate object
        :rtype: XAPredicate

        .. versionadded:: 0.0.4
        """
        for key, value in ref_dict.items():
            self.keys.append(key)
            self.operators.append("==")
            self.values.append(value)
        return self

    def from_args(self, *args) -> "XAPredicate":
        """Populates the XAPredicate object from the supplied key, value argument pairs.

        The number of keys and values must be equal. The predicate will use == for all comparisons.

        :raises InvalidPredicateError: Raised when the number of keys does not match the number of values
        :return: The populated predicate object
        :rtype: XAPredicate

        .. versionadded:: 0.0.4
        """
        arg_num = len(args)
        if arg_num % 2 != 0:
            raise InvalidPredicateError(
                "The number of keys and values must be equal; the number of arguments must be an even number."
            )

        for index, value in enumerate(args):
            if index % 2 == 0:
                self.keys.append(value)
                self.operators.append("==")
                self.values.append(args[index + 1])
        return self

    def evaluate(self, target: Union["AppKit.NSArray", XAList]) -> "AppKit.NSArray":
        """Evaluates the predicate on the given array.

        :param target: The array to evaluate against the predicate
        :type target: AppKit.NSArray
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        placeholders = ["%@"] * len(self.values)
        expressions = [
            " ".join(expr) for expr in zip(self.keys, self.operators, placeholders)
        ]
        format = "( " + " ) && ( ".join(expressions) + " )"

        ls = []
        predicate = AppKit.NSPredicate.predicateWithFormat_(format, *self.values)

        try:
            # Not sure why this is necessary sometimes, but it is.
            ls = target_list.filteredArrayUsingPredicate_(
                AppKit.NSPredicate.predicateWithFormat_(str(predicate))
            )
        except ValueError:
            ls = target_list.filteredArrayUsingPredicate_(predicate)

        if isinstance(target, XAList):
            return target.__class__(
                {
                    "parent": target,
                    "element": ls,
                    "appref": self.xa_aref,
                }
            )
        return ls

    def evaluate_with_format(
        target: Union["AppKit.NSArray", XAList], fmt: str, *fmt_parameters
    ) -> "AppKit.NSArray":
        """Evaluates the specified array against a predicate with the given format.

        :param target: The array to filter
        :type target: AppKit.NSArray
        :param fmt: The format string for the predicate
        :type fmt: str
        :param fmt_parameters: The parameters for the format string
        :type fmt_parameters: Any
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionchanged:: 0.3.0

            Added the :attr:`fmt_parameters` parameter.

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        predicate = AppKit.NSPredicate.predicateWithFormat_argumentArray_(
            fmt, fmt_parameters
        )
        ls = target_list.filteredArrayUsingPredicate_(predicate)

        if isinstance(target, XAList):
            return target.__class__(
                {
                    "parent": target,
                    "element": ls,
                    "appref": AppKit.NSApplication.sharedApplication(),
                }
            )
        return ls

    def evaluate_with_dict(
        target: Union["AppKit.NSArray", XAList], properties_dict: dict
    ) -> "AppKit.NSArray":
        """Evaluates the specified array against a predicate constructed from the supplied dictionary.

        The predicate will use == for all comparisons.

        :param target: The array to filter
        :type target: AppKit.NSArray
        :param properties_dict: The specification of key, value pairs
        :type properties_dict: dict
        :return: The filtered array
        :rtype: AppKit.NSArray

        .. versionadded:: 0.0.4
        """
        target_list = target
        if isinstance(target, XAList):
            target_list = target.xa_elem

        fmt = ""
        for key, value in properties_dict.items():
            if isinstance(value, str):
                value = "'" + value + "'"
            fmt += f"( {key} == {value} ) &&"

        predicate = AppKit.NSPredicate.predicateWithFormat_(fmt[:-3])
        ls = target_list.filteredArrayUsingPredicate_(predicate)

        if isinstance(target, XAList):
            return target.__class__(
                {
                    "parent": target,
                    "element": ls,
                    "appref": AppKit.NSApplication.sharedApplication(),
                }
            )
        return ls

    # EQUAL
    def add_eq_condition(self, property: str, value: Any):
        """Appends an `==` condition to the end of the predicate format.

        The added condition will have the form `property == value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("==")
        self.values.append(value)

    def insert_eq_condition(self, index: int, property: str, value: Any):
        """Inserts an `==` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property == value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "==")
        self.values.insert(index, value)

    # NOT EQUAL
    def add_neq_condition(self, property: str, value: Any):
        """Appends a `!=` condition to the end of the predicate format.

        The added condition will have the form `property != value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("!=")
        self.values.append(value)

    def insert_neq_condition(self, index: int, property: str, value: Any):
        """Inserts a `!=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property != value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "!=")
        self.values.insert(index, value)

    # GREATER THAN OR EQUAL
    def add_geq_condition(self, property: str, value: Any):
        """Appends a `>=` condition to the end of the predicate format.

        The added condition will have the form `property >= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append(">=")
        self.values.append(value)

    def insert_geq_condition(self, index: int, property: str, value: Any):
        """Inserts a `>=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property >= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, ">=")
        self.values.insert(index, value)

    # LESS THAN OR EQUAL
    def add_leq_condition(self, property: str, value: Any):
        """Appends a `<=` condition to the end of the predicate format.

        The added condition will have the form `property <= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("<=")
        self.values.append(value)

    def insert_leq_condition(self, index: int, property: str, value: Any):
        """Inserts a `<=` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property <= value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "<=")
        self.values.insert(index, value)

    # GREATER THAN
    def add_gt_condition(self, property: str, value: Any):
        """Appends a `>` condition to the end of the predicate format.

        The added condition will have the form `property > value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append(">")
        self.values.append(value)

    def insert_gt_condition(self, index: int, property: str, value: Any):
        """Inserts a `>` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property > value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, ">")
        self.values.insert(index, value)

    # LESS THAN
    def add_lt_condition(self, property: str, value: Any):
        """Appends a `<` condition to the end of the predicate format.

        The added condition will have the form `property < value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("<")
        self.values.append(value)

    def insert_lt_condition(self, index: int, property: str, value: Any):
        """Inserts a `<` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property < value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "<")
        self.values.insert(index, value)

    # BETWEEN
    def add_between_condition(
        self, property: str, value1: Union[int, float], value2: Union[int, float]
    ):
        """Appends a `BETWEEN` condition to the end of the predicate format.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value1: The lower target value of the condition
        :type value1: Union[int, float]
        :param value2: The upper target value of the condition
        :type value2: Union[int, float]

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("BETWEEN")
        self.values.append([value1, value2])

    def insert_between_condition(
        self,
        index: int,
        property: str,
        value1: Union[int, float],
        value2: Union[int, float],
    ):
        """Inserts a `BETWEEN` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property BETWEEN [value1, value2]`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value1: The lower target value of the condition
        :type value1: Union[int, float]
        :param value2: The upper target value of the condition
        :type valu2e: Union[int, float]

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "BETWEEN")
        self.values.insert(index, [value1, value2])

    # BEGINSWITH
    def add_begins_with_condition(self, property: str, value: Any):
        """Appends a `BEGINSWITH` condition to the end of the predicate format.

        The added condition will have the form `property BEGINSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("BEGINSWITH")
        self.values.append(value)

    def insert_begins_with_condition(self, index: int, property: str, value: Any):
        """Inserts a `BEGINSWITH` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property BEGINSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "BEGINSWITH")
        self.values.insert(index, value)

    # ENDSWITH
    def add_ends_with_condition(self, property: str, value: Any):
        """Appends a `ENDSWITH` condition to the end of the predicate format.

        The added condition will have the form `property ENDSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("ENDSWITH")
        self.values.append(value)

    def insert_ends_with_condition(self, index: int, property: str, value: Any):
        """Inserts a `ENDSWITH` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property ENDSWITH value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "ENDSWITH")
        self.values.insert(index, value)

    # CONTAINS
    def add_contains_condition(self, property: str, value: Any):
        """Appends a `CONTAINS` condition to the end of the predicate format.

        The added condition will have the form `property CONTAINS value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("CONTAINS")
        self.values.append(value)

    def insert_contains_condition(self, index: int, property: str, value: Any):
        """Inserts a `CONTAINS` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property CONTAINS value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "CONTAINS")
        self.values.insert(index, value)

    # MATCHES
    def add_match_condition(self, property: str, value: Any):
        """Appends a `MATCHES` condition to the end of the predicate format.

        The added condition will have the form `property MATCHES value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.append(property)
        self.operators.append("MATCHES")
        self.values.append(value)

    def insert_match_condition(self, index: int, property: str, value: Any):
        """Inserts a `MATCHES` condition to the predicate format at the desired location, specified by index.

        The added condition will have the form `property MATCHES value`.

        :param property: A property of an object to check the condition against
        :type property: str
        :param value: The target value of the condition
        :type value: Any

        .. versionadded:: 0.0.4
        """
        self.keys.insert(index, property)
        self.operators.insert(index, "MATCHES")
        self.values.insert(index, value)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the predicate.

        When a predicate is copied to the clipboard, the string representation of the predicate is added to the clipboard.

        :return: The string representation of the predicate
        :rtype: str

        .. versionadded:: 0.0.8
        """
        placeholders = ["%@"] * len(self.values)
        expressions = [
            " ".join(expr) for expr in zip(self.keys, self.operators, placeholders)
        ]
        format = "( " + " ) && ( ".join(expressions) + " )"
        predicate = AppKit.NSPredicate.predicateWithFormat_(format, *self.values)
        return predicate.predicateFormat()


class XAURLList(XAList):
    """A list of URLs. Supports bulk operations.

    .. versionadded:: 0.1.2
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAURL, filter)

    def base_url(self) -> list[str]:
        return [url.base_url for url in self]

    def parameters(self) -> list[str]:
        return [url.parameters for url in self]

    def scheme(self) -> list[str]:
        return [url.scheme for url in self]

    def fragment(self) -> list[str]:
        return [url.fragment for url in self]

    def port(self) -> list[int]:
        return [url.port for url in self]

    def html(self) -> list[element.Tag]:
        return [url.html for url in self]

    def title(self) -> list[str]:
        return [url.title for url in self]

    def open(self):
        """Opens each URL in the list.

        .. versionadded:: 0.1.2
        """
        for url in self:
            url.open()

    def extract_text(self) -> list[list[str]]:
        """Extracts the visible text of each URL in the list.

        .. versionadded:: 0.1.2
        """
        ls = [url.extract_text() for url in self]
        return ls

    def extract_images(self) -> list[list["XAImage"]]:
        """Extracts the images of each URL in the list.

        .. versionadded:: 0.1.2
        """
        ls = [url.extract_images() for url in self]
        return ls


class XAURL(XAObject, XAClipboardCodable):
    """A URL using any scheme recognized by the system. This can be a file URL.

    .. versionadded:: 0.0.5
    """

    def __init__(self, url: Union[str, "AppKit.NSURL", "XAURL", "XAPath"]):
        super().__init__()
        self.soup: BeautifulSoup = None  #: The bs4 object for the URL, starts as None until a bs4-related action is made
        self.url: str  #: The string form of the URL

        if isinstance(url, list):
            # Elevate to XAURLList
            new_self = XAURLList(
                {"element": AppKit.NSArray.alloc().initWithArray_(url)}
            )
            self.__dict__ = new_self.__dict__
            self.__class__ = new_self.__class__
            self = new_self
            return

        if isinstance(url, dict):
            # Initialized via XAURLList
            url = url["element"]

        if isinstance(url, str):
            # URL-encode spaces
            url = url.replace(" ", "%20")

            if url.startswith("/"):
                # Prepend file scheme
                url = "file://" + url
            elif url.replace(".", "").isdecimal():
                # URL is an IP -- must add http:// prefix
                if ":" not in url:
                    # No port provided, add port 80 by default
                    url = "http://" + url + ":80"
                else:
                    url = "http://" + url
            elif "://" not in url:
                # URL is not currently valid, try prepending http://
                url = "http://" + url

            self.url = url
            url = AppKit.NSURL.alloc().initWithString_(url)
        elif isinstance(url, XAURL) or isinstance(url, XAPath):
            self.url = url.url
            url = url.xa_elem
        else:
            self.url = str(url)

        self.xa_elem = url

    @property
    def base_url(self) -> str:
        return self.xa_elem.host()

    @property
    def parameters(self) -> str:
        """The query parameters of the URL."""
        return self.xa_elem.query()

    @property
    def scheme(self) -> str:
        """The URI scheme of the URL."""
        return self.xa_elem.scheme()

    @property
    def fragment(self) -> str:
        """The fragment identifier following a # symbol in the URL."""
        return self.xa_elem.fragment()

    @property
    def port(self) -> int:
        """The port that the URL points to."""
        return self.xa_elem.port()

    @property
    def html(self) -> element.Tag:
        """The html of the URL."""
        if self.soup is None:
            self.__get_soup()
        return self.soup.html

    @property
    def title(self) -> str:
        """The title of the URL."""
        if self.soup is None:
            self.__get_soup()
        return self.soup.title.text

    def __get_soup(self):
        req = requests.get(str(self.xa_elem))
        self.soup = BeautifulSoup(req.text, "html.parser")

    def open(self):
        """Opens the URL in the appropriate default application.

        .. versionadded:: 0.0.5
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()
        workspace.openURL_(self.xa_elem)

    def extract_text(self) -> list[str]:
        """Extracts the visible text from the webpage that the URL points to.

        :return: The list of extracted lines of text
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        if self.soup is None:
            self.__get_soup()
        return self.soup.get_text().splitlines()

    def extract_images(self) -> list["XAImage"]:
        """Extracts all images from HTML of the webpage that the URL points to.

        :return: The list of extracted images
        :rtype: list[XAImage]

        .. versionadded:: 0.0.8
        """
        data = AppKit.NSData.alloc().initWithContentsOfURL_(
            AppKit.NSURL.URLWithString_(str(self.xa_elem))
        )
        image = AppKit.NSImage.alloc().initWithData_(data)

        if image is not None:
            image_object = XAImage(image, name=self.xa_elem.pathComponents()[-1])
            return [image_object]
        else:
            if self.soup is None:
                self.__get_soup()

            images = self.soup.findAll("img")
            image_objects = []
            for image in images:
                image_src = image["src"]
                if image_src.startswith("/"):
                    image_src = str(self) + str(image["src"])

                data = AppKit.NSData.alloc().initWithContentsOfURL_(
                    AppKit.NSURL.URLWithString_(image_src)
                )
                image = AppKit.NSImage.alloc().initWithData_(data)
                if image is not None:
                    image_object = XAImage(image)
                    image_objects.append(image_object)

            return image_objects

    def get_clipboard_representation(self) -> list[Union["AppKit.NSURL", str]]:
        """Gets a clipboard-codable representation of the URL.

        When the clipboard content is set to a URL, the raw URL data and the string representation of the URL are added to the clipboard.

        :return: The clipboard-codable form of the URL
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, str(self.xa_elem)]

    def __eq__(self, other: "XAURL"):
        if not isinstance(other, XAURL):
            return False

        if self.xa_elem == other.xa_elem:
            return True

        return self.url == other.url

    def __str__(self):
        return str(self.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"


class XAPath(XAObject, XAClipboardCodable):
    """A path to a file on the disk.

    .. versionadded:: 0.0.5
    """

    def __init__(self, path: Union[str, "AppKit.NSURL"]):
        super().__init__()
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_elem = path
        self.path = path.path()  #: The path string without the file:// prefix
        self.url = str(
            self.xa_elem
        )  #: The path string with the file:// prefix included

    @property
    def name(self) -> str:
        """The name of the file or folder at the path."""
        return self.xa_elem.lastPathComponent()

    def open(self):
        """Opens the file in its default application.

        .. versionadded: 0.0.5
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()
        workspace.openURL_(self.xa_elem)

    def show_in_finder(self):
        """Opens a Finder window showing the folder containing this path, with the associated file selected. Synonymous with :func:`select`.

        .. versionadded: 0.0.9
        """
        self.select()

    def select(self):
        """Opens a Finder window showing the folder containing this path, with the associated file selected. Synonymous with :func:`show_in_finder`.

        .. versionadded: 0.0.5
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()
        workspace.activateFileViewerSelectingURLs_([self.xa_elem])

    def get_clipboard_representation(self) -> list[Union["AppKit.NSURL", str]]:
        """Gets a clipboard-codable representation of the path.

        When the clipboard content is set to a path, the raw file URL data and the string representation of the path are added to the clipboard.

        :return: The clipboard-codable form of the path
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.xa_elem.path()]

    def __eq__(self, other: "XAPath"):
        if not isinstance(other, XAPath):
            return False

        if self.xa_elem == other.xa_elem:
            return True

        return self.path == other.path

    def __repr__(self):
        return "<" + str(type(self)) + str(self.xa_elem) + ">"


########################
### System Utilities ###
########################
class XAClipboard(XAObject):
    """A wrapper class for managing and interacting with the system clipboard.

    .. versionadded:: 0.0.5
    """

    def __init__(self):
        self.xa_elem = AppKit.NSPasteboard.generalPasteboard()

    @property
    def content(self) -> dict[str, list[Any]]:
        """The content of the clipboard."""
        info_by_type = {}
        for item in self.xa_elem.pasteboardItems():
            for item_type in item.types():
                info_by_type[item_type] = {
                    "data": item.dataForType_(item_type),
                    "properties": item.propertyListForType_(item_type),
                    "strings": item.stringForType_(item_type),
                }
        return info_by_type

    @content.setter
    def content(self, value: list[Any]):
        if not isinstance(value, list):
            value = [value]
        self.xa_elem.clearContents()
        for index, item in enumerate(value):
            if item == None:
                value[index] = ""
            elif isinstance(item, XAObject):
                if not isinstance(item, XAClipboardCodable):
                    print(item, "is not a clipboard-codable object.")
                    continue
                if (
                    isinstance(item.xa_elem, ScriptingBridge.SBElementArray)
                    and item.xa_elem.get() is None
                ):
                    value[index] = ""
                else:
                    content = item.get_clipboard_representation()
                    if isinstance(content, list):
                        value.pop(index)
                        value += content
                    else:
                        value[index] = content
            elif isinstance(item, int) or isinstance(item, float):
                value[index] = str(item)
        self.xa_elem.writeObjects_(value)

    def clear(self):
        """Clears the system clipboard.

        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()

    def get_strings(self) -> list[str]:
        """Retrieves string type data from the clipboard, if any such data exists.

        :return: The list of strings currently copied to the clipboard
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        items = []
        for item in self.xa_elem.pasteboardItems():
            string = item.stringForType_(AppKit.NSPasteboardTypeString)
            if string is not None:
                items.append(string)
        return items

    def get_urls(self) -> list["XAURL"]:
        """Retrieves URL type data from the clipboard, as instances of :class:`XAURL` and :class:`XAPath`, if any such data exists.

        :return: The list of file URLs and web URLs currently copied to the clipboard
        :rtype: list[XAURL]

        .. versionadded:: 0.0.8
        """
        items = []
        for item in self.xa_elem.pasteboardItems():
            url = None
            string = item.stringForType_(AppKit.NSPasteboardTypeURL)
            if string is None:
                string = item.stringForType_(AppKit.NSPasteboardTypeFileURL)
                if string is not None:
                    url = XAPath(XAURL(string).xa_elem)
            else:
                url = XAURL(string)

            if url is not None:
                items.append(url)
        return items

    def get_images(self) -> list["XAImage"]:
        """Retrieves image type data from the clipboard, as instances of :class:`XAImage`, if any such data exists.

        :return: The list of images currently copied to the clipboard
        :rtype: list[XAImage]

        .. versionadded:: 0.0.8
        """
        image_types = [
            AppKit.NSPasteboardTypePNG,
            AppKit.NSPasteboardTypeTIFF,
            "public.jpeg",
            "com.apple.icns",
        ]
        items = []
        for item in self.xa_elem.pasteboardItems():
            for image_type in image_types:
                if image_type in item.types():
                    img = XAImage(data=item.dataForType_(image_type))
                    items.append(img)
        return items

    def set_contents(self, content: list[Any]):
        """Sets the content of the clipboard

        :param content: A list of the content to add fill the clipboard with.
        :type content: list[Any]

        .. deprecated:: 0.0.8
           Set the :attr:`content` property directly instead.

        .. versionadded:: 0.0.5
        """
        self.xa_elem.clearContents()
        self.xa_elem.writeObjects_(content)


class XASpotlight(XAObject):
    """A Spotlight query for files on the disk.

    .. versionadded:: 0.0.9
    """

    def __init__(self, *query: list[Any]):
        self.query: list[Any] = query  #: The query terms to search
        self.timeout: int = (
            10  #: The amount of time in seconds to timeout the search after
        )
        self.predicate: Union[
            str, XAPredicate
        ] = None  #: The predicate to filter search results by
        self.results: list[XAPath]  #: The results of the search
        self.__results = None

        self.query_object = AppKit.NSMetadataQuery.alloc().init()
        nc = AppKit.NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(
            self, "_queryNotification:", None, self.query_object
        )

    @property
    def results(self) -> list["XAPath"]:
        if len(self.query) == 0 and self.predicate is None:
            return []
        self.run()
        total_time = 0
        while self.__results is None and total_time < self.timeout:
            AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                datetime.now() + timedelta(seconds=0.01)
            )
            total_time += 0.01
        if self.__results is None:
            return []
        return self.__results

    def run(self):
        """Runs the search.

        :Example:

        >>> import PyXA
        >>> from datetime import date, datetime, time
        >>> date1 = datetime.combine(date(2022, 5, 17), time(0, 0, 0))
        >>> date2 = datetime.combine(date(2022, 5, 18), time(0, 0, 0))
        >>> search = PyXA.XASpotlight(date1, date2)
        >>> print(search.results)
        [<<class 'PyXA.XAPath'>file:///Users/exampleUser/Downloads/>, <<class 'PyXA.XAPath'>file:///Users/exampleUser/Downloads/Example.txt>, ...]

        .. versionadded:: 0.0.9
        """
        if self.predicate is not None:
            # Search with custom predicate
            if isinstance(self.predicate, XAPredicate):
                self.predicate = self.predicate.get_clipboard_representation()
            self.__search_with_predicate(self.predicate)
        elif len(self.query) == 1 and isinstance(self.query[0], datetime):
            # Search date + or - 24 hours
            self.__search_by_date(self.query)
        elif (
            len(self.query) == 2
            and isinstance(self.query[0], datetime)
            and isinstance(self.query[1], datetime)
        ):
            # Search date range
            self.__search_by_date_range(self.query[0], self.query[1])
        elif all(
            isinstance(x, str) or isinstance(x, int) or isinstance(x, float)
            for x in self.query
        ):
            # Search matching multiple strings
            self.__search_by_strs(self.query)
        elif isinstance(self.query[0], datetime) and all(
            isinstance(x, str) or isinstance(x, int) or isinstance(x, float)
            for x in self.query[1:]
        ):
            # Search by date and string
            self.__search_by_date_strings(self.query[0], self.query[1:])
        elif (
            isinstance(self.query[0], datetime)
            and isinstance(self.query[1], datetime)
            and all(
                isinstance(x, str) or isinstance(x, int) or isinstance(x, float)
                for x in self.query[2:]
            )
        ):
            # Search by date range and string
            self.__search_by_date_range_strings(
                self.query[0], self.query[1], self.query[2:]
            )

        AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
            datetime.now() + timedelta(seconds=0.01)
        )

    def show_in_finder(self):
        """Shows the search in Finder. This might not reveal the same search results.

        .. versionadded:: 0.0.9
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()
        workspace.showSearchResultsForQueryString_(str(self.query))

    def __search_by_strs(self, terms: tuple[str]):
        expanded_terms = [x for y in terms for x in [y] * 3]
        format = (
            "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND "
            * len(terms)
        )
        self.__search_with_predicate(format[:-5], *expanded_terms)

    def __search_by_date(self, date: datetime):
        self.__search_with_predicate(
            f"((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@))",
            *[date - timedelta(hours=12), date + timedelta(hours=12)] * 5,
        )

    def __search_by_date_range(self, date1: datetime, date2: datetime):
        self.__search_with_predicate(
            f"((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@))",
            *[date1, date2] * 5,
        )

    def __search_by_date_strings(self, date: datetime, terms: tuple[str]):
        expanded_terms = [x for y in terms for x in [y] * 3]
        format = (
            "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND "
            * len(terms)
        )
        format += "(((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@)))"
        self.__search_with_predicate(
            format,
            *expanded_terms,
            *[date - timedelta(hours=12), date + timedelta(hours=12)] * 5,
        )

    def __search_by_date_range_strings(
        self, date1: datetime, date2: datetime, terms: tuple[str]
    ):
        expanded_terms = [x for y in terms for x in [y] * 3]
        format = (
            "((kMDItemDisplayName CONTAINS %@) OR (kMDItemTextContent CONTAINS %@) OR (kMDItemFSName CONTAINS %@)) AND "
            * len(terms)
        )
        format += "(((kMDItemContentCreationDate > %@) AND (kMDItemContentCreationDate < %@)) OR ((kMDItemContentModificationDate > %@) AND (kMDItemContentModificationDate < %@)) OR ((kMDItemFSCreationDate > %@) AND (kMDItemFSCreationDate < %@)) OR ((kMDItemFSContentChangeDate > %@) AND (kMDItemFSContentChangeDate < %@)) OR ((kMDItemDateAdded > %@) AND (kMDItemDateAdded < %@)))"
        self.__search_with_predicate(format, *expanded_terms, *[date1, date2] * 5)

    def __search_with_predicate(self, predicate_format: str, *args: list[Any]):
        predicate = AppKit.NSPredicate.predicateWithFormat_(predicate_format, *args)
        self.query_object.setPredicate_(predicate)
        self.query_object.startQuery()

    def _queryNotification_(self, notification):
        if notification.name() == AppKit.NSMetadataQueryDidFinishGatheringNotification:
            self.query_object.stopQuery()
            results = notification.object().results()
            self.__results = [
                XAPath(x.valueForAttribute_(AppKit.NSMetadataItemPathKey))
                for x in results
            ]


############
### Text ###
############
class XATextDocumentList(XAList, XAClipboardCodable):
    """A wrapper around lists of text documents that employs fast enumeration techniques.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XATextDocument
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        ls = self.xa_elem.arrayByApplyingSelector_("properties") or []
        return [dict(x) for x in ls]

    def text(self) -> "XATextList":
        ls = self.xa_elem.arrayByApplyingSelector_("text") or []
        return self._new_element(ls, XATextList)

    def by_properties(self, properties: dict) -> Union["XATextDocument", None]:
        return self.by_property("properties", properties)

    def by_text(self, text: str) -> Union["XATextDocument", None]:
        return self.by_property("text", text)

    def paragraphs(self) -> "XAParagraphList":
        ls = self.xa_elem.arrayByApplyingSelector_("paragraphs") or []
        return self._new_element([plist for plist in ls], XAParagraphList)

    def words(self) -> "XAWordList":
        ls = self.xa_elem.arrayByApplyingSelector_("words") or []
        return [self._new_element([plist for plist in ls], XAWordList)]

    def characters(self) -> "XACharacterList":
        ls = self.xa_elem.arrayByApplyingSelector_("characters") or []
        return [self._new_element([plist for plist in ls], XACharacterList)]

    def attribute_runs(self) -> "XAAttributeRunList":
        ls = self.xa_elem.arrayByApplyingSelector_("attributeRuns") or []
        return [self._new_element([plist for plist in ls], XAAttributeRunList)]

    def attachments(self) -> "XAAttachmentList":
        ls = self.xa_elem.arrayByApplyingSelector_("attachments") or []
        return [self._new_element([plist for plist in ls], XAAttachmentList)]

    def get_clipboard_representation(self) -> list[Union[str, "AppKit.NSURL"]]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of documents, each documents's file URL and name are added to the clipboard.

        :return: A list of each document's file URL and name
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [str(x) for x in self.text()]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.text()) + ">"


class XATextDocument(XAObject):
    """A class for managing and interacting with text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def text(self) -> "XAText":
        """The text of the document."""
        return self._new_element(self.xa_elem.text(), XAText)

    @text.setter
    def text(self, text: Union[str, "XAText"]):
        if isinstance(text, XAText):
            text = text.xa_elem
        self.set_property("text", text)

    def prepend(self, text: str) -> "XATextDocument":
        """Inserts the provided text at the beginning of the document.

        :param text: The text to insert.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`append`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = str(self.text)
        self.set_property("text", text + old_text)
        return self

    def append(self, text: str) -> "XATextDocument":
        """Appends the provided text to the end of the document.

        :param text: The text to append.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`prepend`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = str(self.text)
        self.set_property("text", old_text + text)
        return self

    def reverse(self) -> "XATextDocument":
        """Reverses the text of the document.

        :return: A reference to the document object.
        :rtype: XATextDocument

        .. versionadded:: 0.0.4
        """
        self.set_property("text", reversed(str(self.text)))
        return self

    def paragraphs(self, filter: dict = None) -> "XAParagraphList":
        return self.text.paragraphs(filter)

    def sentences(self, filter: dict = None) -> "XASentenceList":
        return self.text.sentences(filter)

    def words(self, filter: dict = None) -> "XAWordList":
        return self.text.words(filter)

    def characters(self, filter: dict = None) -> "XACharacterList":
        return self.text.characters(filter)

    def attribute_runs(self, filter: dict = None) -> "XAAttributeRunList":
        return self.text.attribute_runs(filter)

    def attachments(self, filter: dict = None) -> "XAAttachmentList":
        return self.text.attachments(filter)


class XATextList(XAList):
    """A wrapper around lists of text objects that employs fast enumeration techniques.

    .. versionadded:: 0.0.4
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAText
        super().__init__(properties, obj_class, filter)

    def paragraphs(self, filter: dict = None) -> "XAParagraphList":
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("paragraphs") or []
        else:
            ls = [x.xa_elem.split("\n") for x in self]
        ls = [
            paragraph
            for paragraphlist in ls
            for paragraph in paragraphlist
            if paragraph.strip() != ""
        ]
        return self._new_element(ls, XAParagraphList, filter)

    def sentences(self) -> "XASentenceList":
        ls = [x.sentences() for x in self]
        ls = [sentence for sentencelist in ls for sentence in sentencelist]
        return self._new_element(ls, XASentenceList)

    def words(self, filter: dict = None) -> "XAWordList":
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("words") or []
        else:
            ls = [x.xa_elem.split() for x in self]
        ls = [word for wordlist in ls for word in wordlist]
        return self._new_element(ls, XAWordList, filter)

    def characters(self, filter: dict = None) -> "XACharacterList":
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("characters") or []
        else:
            ls = [list(x.xa_elem) for x in self]
        ls = [character for characterlist in ls for character in characterlist]
        return self._new_element(ls, XACharacterList, filter)

    def attribute_runs(self, filter: dict = None) -> "XAAttributeRunList":
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("attributeRuns") or []
        ls = [
            attribute_run
            for attribute_run_list in ls
            for attribute_run in attribute_run_list
        ]
        return self._new_element(ls, XAAttributeRunList, filter)

    def attachments(self, filter: dict = None) -> "XAAttachmentList":
        ls = []
        if hasattr(self.xa_elem, "get"):
            ls = self.xa_elem.arrayByApplyingSelector_("attachments") or []
        ls = [attachment for attachment_list in ls for attachment in attachment_list]
        return self._new_element(ls, XAAttachmentList, filter)

    def __repr__(self):
        try:
            if isinstance(self.xa_elem[0], ScriptingBridge.SBObject):
                # List items will not resolved to text upon dereferencing the list; need to resolve items individually
                count = self.xa_elem.count()
                if count <= 500:
                    # Too many unresolved pointers, save time by just reporting the length
                    return (
                        "<"
                        + str(type(self))
                        + str([x.get() for x in self.xa_elem])
                        + ">"
                    )
                return (
                    "<" + str(type(self)) + "length: " + str(self.xa_elem.count()) + ">"
                )

            # List items will resolve to text upon dereferencing the list
            return "<" + str(type(self)) + str(self.xa_elem.get()) + ">"
        except:
            return "<" + str(type(self)) + str(list(self.xa_elem)) + ">"


class XAText(XAObject):
    """A class for managing and interacting with the text of documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        if isinstance(properties, dict):
            super().__init__(properties)
        elif isinstance(properties, str):
            super().__init__({"element": properties})

        self.text: str  #: The plaintext contents of the rich text
        self.color: XAColor  #: The color of the first character
        self.font: str  #: The name of the font of the first character
        self.size: int  #: The size in points of the first character

    @property
    def text(self) -> str:
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        else:
            return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        if isinstance(self.xa_elem, str):
            self.xa_elem = text
        else:
            self.set_property("text", text)

    @property
    def color(self) -> "XAColor":
        if isinstance(self.xa_elem, str):
            return None
        else:
            return XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: "XAColor"):
        if isinstance(self.xa_elem, str):
            self.color = color.xa_elem
        else:
            self.set_property("color", color.xa_elem)

    @property
    def font(self) -> str:
        if isinstance(self.xa_elem, str):
            return None
        else:
            return self.xa_elem.font()

    @font.setter
    def font(self, font: str):
        if isinstance(self.xa_elem, str):
            self.font = font
        else:
            self.set_property("font", font)

    @property
    def size(self) -> int:
        if isinstance(self.xa_elem, str):
            return 0
        else:
            return self.xa_elem.size()

    @size.setter
    def size(self, size: int):
        if isinstance(self.xa_elem, str):
            self.size = size
        else:
            self.set_property("size", size)

    def tag_parts_of_speech(
        self, unit: Literal["word", "sentence", "paragraph", "document"] = "word"
    ) -> list[tuple[str, str]]:
        """Tags each word of the text with its associated part of speech.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its part of speech
        :rtype: list[tuple[str, str]]

        :Example 1: Extract nouns from a text

        >>> import PyXA
        >>> text = PyXA.XAText("Here’s to the crazy ones. The misfits. The rebels.")
        >>> nouns = [pos[0] for pos in text.tag_parts_of_speech() if pos[1] == "Noun"]
        >>> print(nouns)
        ['ones', 'misfits', 'rebels']

        .. versionadded:: 0.1.0
        """
        import NaturalLanguage

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_(
            [NaturalLanguage.NLTagSchemeLexicalClass]
        )
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagged_pos = []

        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[
                token_range.location : token_range.location + token_range.length
            ]
            tagged_pos.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_(
            (0, len(str(self.xa_elem))),
            unit,
            NaturalLanguage.NLTagSchemeLexicalClass,
            NaturalLanguage.NLTaggerOmitPunctuation
            | NaturalLanguage.NLTaggerOmitWhitespace,
            apply_tags,
        )
        return tagged_pos

    def tag_languages(
        self, unit: Literal["word", "sentence", "paragraph", "document"] = "paragraph"
    ) -> list[tuple[str, str]]:
        """Tags each paragraph of the text with its language.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "paragraph"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each paragraph of the text and its language
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> text = PyXA.XAText("This is English.\\nQuesto è Italiano.\\nDas ist deutsch.\\nこれは日本語です。")
        >>> print(text.tag_languages())
        [('This is English.\\n', 'en'), ('Questo è Italiano.\\n', 'it'), ('Das ist deutsch.\\n', 'de'), ('これは日本語です。', 'ja')]

        .. versionadded:: 0.1.0
        """
        import NaturalLanguage

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_(
            [NaturalLanguage.NLTagSchemeLanguage]
        )
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagged_languages = []

        def apply_tags(tag, token_range, error):
            paragraph = str(self.xa_elem)[
                token_range.location : token_range.location + token_range.length
            ]
            if paragraph.strip() != "":
                tagged_languages.append((paragraph, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_(
            (0, len(str(self.xa_elem))),
            unit,
            NaturalLanguage.NLTagSchemeLanguage,
            NaturalLanguage.NLTaggerOmitPunctuation
            | NaturalLanguage.NLTaggerOmitWhitespace,
            apply_tags,
        )
        return tagged_languages

    def tag_entities(
        self, unit: Literal["word", "sentence", "paragraph", "document"] = "word"
    ) -> list[tuple[str, str]]:
        """Tags each word of the text with either the category of entity it represents (i.e. person, place, or organization) or its part of speech.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its entity category or part of speech
        :rtype: list[tuple[str, str]]

        :Example:

        >>> import PyXA
        >>> text = PyXA.XAText("Tim Cook is the CEO of Apple.")
        >>> print(text.tag_entities())
        [('Tim', 'PersonalName'), ('Cook', 'PersonalName'), ('is', 'Verb'), ('the', 'Determiner'), ('CEO', 'Noun'), ('of', 'Preposition'), ('Apple', 'OrganizationName')]

        .. versionadded:: 0.1.0
        """
        import NaturalLanguage

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_(
            [NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass]
        )
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagged_languages = []

        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[
                token_range.location : token_range.location + token_range.length
            ]
            if word_phrase.strip() != "":
                tagged_languages.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_(
            (0, len(str(self.xa_elem))),
            unit,
            NaturalLanguage.NLTagSchemeNameTypeOrLexicalClass,
            NaturalLanguage.NLTaggerOmitPunctuation
            | NaturalLanguage.NLTaggerOmitWhitespace,
            apply_tags,
        )
        return tagged_languages

    def tag_lemmas(
        self, unit: Literal["word", "sentence", "paragraph", "document"] = "word"
    ) -> list[tuple[str, str]]:
        """Tags each word of the text with its stem word.

        :param unit: The grammatical unit to divide the text into for tagging, defaults to "word"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each word of the text and its stem words
        :rtype: list[tuple[str, str]]

        :Example 1: Lemmatize each word in a text

        >>> import PyXA
        >>> text = PyXA.XAText("Here’s to the crazy ones. The misfits. The rebels.")
        >>> print(text.tag_lemmas())
        [('Here’s', 'here'), ('to', 'to'), ('the', 'the'), ('crazy', 'crazy'), ('ones', 'one'), ('The', 'the'), ('misfits', 'misfit'), ('The', 'the'), ('rebels', 'rebel')]

        :Example 2: Combine parts of speech tagging and lemmatization

        >>> import PyXA
        >>> text = PyXA.XAText("The quick brown fox tries to jump over the sleeping lazy dog.")
        >>> verbs = [pos[0] for pos in text.tag_parts_of_speech() if pos[1] == "Verb"]
        >>> for index, verb in enumerate(verbs):
        >>>     print(index, PyXA.XAText(verb).tag_lemmas())
        0 [('tries', 'try')]
        1 [('jump', 'jump')]
        2 [('sleeping', 'sleep')]

        .. versionadded:: 0.1.0
        """
        import NaturalLanguage

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_(
            [NaturalLanguage.NLTagSchemeLemma]
        )
        tagger.setString_(str(self.xa_elem))

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagged_lemmas = []

        def apply_tags(tag, token_range, error):
            word_phrase = str(self.xa_elem)[
                token_range.location : token_range.location + token_range.length
            ]
            if word_phrase.strip() != "":
                tagged_lemmas.append((word_phrase, tag))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_(
            (0, len(str(self.xa_elem))),
            unit,
            NaturalLanguage.NLTagSchemeLemma,
            NaturalLanguage.NLTaggerOmitPunctuation
            | NaturalLanguage.NLTaggerOmitWhitespace
            | NaturalLanguage.NLTaggerJoinContractions,
            apply_tags,
        )
        return tagged_lemmas

    def tag_sentiments(
        self,
        sentiment_scale: list[str] = None,
        unit: Literal["word", "sentence", "paragraph", "document"] = "paragraph",
    ) -> list[tuple[str, str]]:
        """Tags each paragraph of the text with a sentiment rating.

        :param sentiment_scale: A list of terms establishing a range of sentiments from most negative to most postive
        :type sentiment_scale: list[str]
        :param unit: The grammatical unit to divide the text into for tagging, defaults to "paragraph"
        :type unit: Literal["word", "sentence", "paragraph", "document"]
        :return: A list of tuples identifying each paragraph of the text and its sentiment rating
        :rtype: list[tuple[str, str]]

        :Example 1: Assess the sentiment of a string

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\\nBut this is great!")
        >>> print(text.tag_sentiments())
        [('This sucks.\\n', 'Negative'), ('But this is great!', 'Positive')]

        :Example 2: Use a custom sentiment scale

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\\nBut this is good!\\nAnd this is great!")
        >>> print(text.tag_sentiments(sentiment_scale=["Very Negative", "Negative", "Somewhat Negative", "Neutral", "Somewhat Positive", "Positive", "Very Positive"]))
        [('This sucks.\\n', 'Very Negative'), ('But this is good!\\n', 'Neutral'), ('And this is great!', 'Very Positive')]

        :Example 3: Use other tag units

        >>> import PyXA
        >>> text = PyXA.XAText("This sucks.\\nBut this is good!\\nAnd this is great!")
        >>> print(1, text.tag_sentiments())
        >>> print(2, text.tag_sentiments(unit="word"))
        >>> print(3, text.tag_sentiments(unit="document"))
        1 [('This sucks.\\n', 'Negative'), ('But this is good!\\n', 'Neutral'), ('And this is great!', 'Positive')]
        2 [('This', 'Negative'), ('sucks', 'Negative'), ('.', 'Negative'), ('But', 'Neutral'), ('this', 'Neutral'), ('is', 'Neutral'), ('good', 'Neutral'), ('!', 'Neutral'), ('And', 'Positive'), ('this', 'Positive'), ('is', 'Positive'), ('great', 'Positive'), ('!', 'Positive')]
        3 [('This sucks.\\nBut this is good!\\nAnd this is great!', 'Neutral')]

        .. versionadded:: 0.1.0
        """
        import NaturalLanguage

        if sentiment_scale is None or len(sentiment_scale) == 0:
            sentiment_scale = ["Negative", "Neutral", "Positive"]

        if unit == "word":
            unit = NaturalLanguage.NLTokenUnitWord
        elif unit == "sentence":
            unit = NaturalLanguage.NLTokenUnitSentence
        elif unit == "paragraph":
            unit = NaturalLanguage.NLTokenUnitParagraph
        elif unit == "document":
            unit = NaturalLanguage.NLTokenUnitDocument

        tagger = NaturalLanguage.NLTagger.alloc().initWithTagSchemes_(
            [NaturalLanguage.NLTagSchemeSentimentScore]
        )
        tagger.setString_(str(self.xa_elem))

        tagged_sentiments = []

        def apply_tags(tag, token_range, error):
            paragraph = str(self.xa_elem)[
                token_range.location : token_range.location + token_range.length
            ]
            if paragraph.strip() != "":
                # Map raw tag value to range length
                raw_value = float(tag or 0)
                scaled = (raw_value + 1.0) / 2.0 * (len(sentiment_scale) - 1)

                label = sentiment_scale[int(scaled)]
                tagged_sentiments.append((paragraph, label))

        tagger.enumerateTagsInRange_unit_scheme_options_usingBlock_(
            (0, len(str(self.xa_elem))),
            unit,
            NaturalLanguage.NLTagSchemeSentimentScore,
            0,
            apply_tags,
        )
        return tagged_sentiments

    def extract_urls(self) -> list["XAURL"]:
        """Gets a list of URLs in the text.

        :return: The list of URLs.
        :rtype: list[XAURL]

        .. versionadded:: 0.3.0
        """
        detector = AppKit.NSDataDetector.dataDetectorWithTypes_error_(
            AppKit.NSTextCheckingTypeLink, None
        )
        if detector[1] is not None:
            raise Exception("Error creating data detector")

        matches = detector[0].matchesInString_options_range_(
            self.xa_elem, 0, AppKit.NSMakeRange(0, len(self.xa_elem))
        )
        return [XAURL(match.URL()) for match in matches]

    def extract_dates(self) -> list["XADatetimeBlock"]:
        """Gets a list of dates and durations in the text.

        :return: The list of dates.
        :rtype: list[XADatetimeBlock]

        .. versionadded:: 0.3.0
        """
        detector = AppKit.NSDataDetector.dataDetectorWithTypes_error_(
            AppKit.NSTextCheckingTypeDate, None
        )
        if detector[1] is not None:
            raise Exception("Error creating data detector")

        matches = detector[0].matchesInString_options_range_(
            self.xa_elem, 0, AppKit.NSMakeRange(0, len(self.xa_elem))
        )
        return [XADatetimeBlock(match.date(), match.duration()) for match in matches]

    def extract_addresses(self):
        """Gets a list of addresses in the text.

        :return: The list of addresses.
        :rtype: list[XALocation]

        .. versionadded:: 0.3.0
        """
        import CoreLocation

        detector = AppKit.NSDataDetector.dataDetectorWithTypes_error_(
            AppKit.NSTextCheckingTypeAddress, None
        )
        if detector[1] is not None:
            raise Exception()

        matches = detector[0].matchesInString_options_range_(
            self.xa_elem, 0, AppKit.NSMakeRange(0, len(self.xa_elem))
        )
        address_dicts = [match.addressComponents() for match in matches]

        geocoder = CoreLocation.CLGeocoder.alloc().init()
        addresses = []

        def add_location(placemarks, error):
            nonlocal addresses
            if error is not None:
                raise Exception("Error creating data detector")

            if len(placemarks) > 0:
                addresses.append(
                    XALocation(
                        placemarks[0].location(),
                        placemarks[0].name(),
                        0,
                        0,
                        None,
                        0,
                        placemarks[0].postalAddress(),
                    )
                )

            if len(addresses) == len(address_dicts):
                AppHelper.stopEventLoop()

        for address_dict in address_dicts:
            address_string = ", ".join(
                [x for x in address_dict.values() if x is not None]
            )
            geocoder.geocodeAddressString_completionHandler_(
                address_string, add_location
            )

        AppHelper.runConsoleEventLoop()
        return addresses

    def extract_phone_numbers(self):
        """Gets a list of phone numbers in the text.

        :return: The list of phone numbers.
        :rtype: list[XAText]

        .. versionadded:: 0.3.0
        """
        detector = AppKit.NSDataDetector.dataDetectorWithTypes_error_(
            AppKit.NSTextCheckingTypePhoneNumber, None
        )
        if detector[1] is not None:
            raise Exception("Error creating data detector")

        matches = detector[0].matchesInString_options_range_(
            self.xa_elem, 0, AppKit.NSMakeRange(0, len(self.xa_elem))
        )
        return [XAText(match.phoneNumber()) for match in matches]

    def paragraphs(self, filter: dict = None) -> "XAParagraphList":
        """Gets a list of paragraphs in the text.

        :param filter: The properties and associated values to filter paragraphs by, defaults to None
        :type filter: dict, optional
        :return: The list of paragraphs
        :rtype: XAParagraphList

        :Example 1: Get paragraphs of a text string

        >>> import PyXA
        >>> string = \"\"\"This is the first paragraph.
        >>>
        >>> This is the second paragraph.\"\"\"
        >>> text = PyXA.XAText(string)
        >>> print(text.paragraphs())
        <<class 'PyXA.XAWordList'>['This is the first paragraph.', 'This is the second paragraph. Neat! Very cool.']>

        :Example 2: Get paragraphs of a Note

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.paragraphs())
        <<class 'PyXA.XAWordList'>['This is the first paragraph.', 'This is the second paragraph. Neat! Very cool.']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = [x for x in self.xa_elem.split("\n") if x.strip() != ""]
            return self._new_element(ls, XAWordList, filter)
        else:
            return self._new_element(self.xa_elem.paragraphs(), XAParagraphList, filter)

    def sentences(self) -> "XASentenceList":
        """Gets a list of sentences in the text.

        :return: The list of sentencnes
        :rtype: XASentenceList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.sentences())
        <<class 'PyXA.XASentenceList'>['This is the first paragraph.\\n', '\\n', 'This is the second paragraph. ', 'Neat! ', 'Very cool.']>

        .. versionadded:: 0.1.0
        """
        raw_string = self.xa_elem
        if hasattr(self.xa_elem, "get"):
            raw_string = self.xa_elem.get()

        sentences = []
        tokenizer = AppKit.NLTokenizer.alloc().initWithUnit_(
            AppKit.kCFStringTokenizerUnitSentence
        )
        tokenizer.setString_(raw_string)
        for char_range in tokenizer.tokensForRange_((0, len(raw_string))):
            start = char_range.rangeValue().location
            end = start + char_range.rangeValue().length
            sentences.append(raw_string[start:end])

        ls = AppKit.NSArray.alloc().initWithArray_(sentences)
        return self._new_element(sentences, XASentenceList)

    def words(self, filter: dict = None) -> "XAWordList":
        """Gets a list of words in the text.

        :return: The list of words
        :rtype: XAWordList

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.words())
        <<class 'PyXA.XAWordList'>['This', 'is', 'the', 'first', 'paragraph.', 'This', 'is', 'the', 'second', 'paragraph.', 'Neat!', 'Very', 'cool.']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = self.xa_elem.split()
            return self._new_element(ls, XAWordList, filter)
        else:
            return self._new_element(self.xa_elem.words(), XAWordList, filter)

    def characters(self, filter: dict = None) -> "XACharacterList":
        """Gets a list of characters in the text.

        :return: The list of characters
        :rtype: XACharacterList

        :Example 1: Get all characters in a text

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.characters())
        <<class 'PyXA.XACharacterList'>['T', 'h', 'i', 's', ' ', 'i', 's', ' ', 't', 'h', 'e', ' ', 'f', 'i', 'r', 's', 't', ' ', 'p', 'a', 'r', 'a', 'g', 'r', 'a', 'p', 'h', '.', '\\n', '\\n', 'T', 'h', 'i', 's', ' ', 'i', 's', ' ', 't', 'h', 'e', ' ', 's', 'e', 'c', 'o', 'n', 'd', ' ', 'p', 'a', 'r', 'a', 'g', 'r', 'a', 'p', 'h', '.', ' ', 'N', 'e', 'a', 't', '!', ' ', 'V', 'e', 'r', 'y', ' ', 'c', 'o', 'o', 'l', '.']>

        :Example 2: Get the characters of the first word in a text

        >>> import PyXA
        >>> app = PyXA.Application("Notes")
        >>> note = app.notes()[0]
        >>> text = PyXA.XAText(note.plaintext)
        >>> print(text.words()[0].characters())
        <<class 'PyXA.XACharacterList'>['T', 'h', 'i', 's']>

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            ls = list(self.xa_elem)
            return self._new_element(ls, XACharacterList, filter)
        else:
            return self._new_element(
                self.xa_elem.characters().get(), XACharacterList, filter
            )

    def attribute_runs(self, filter: dict = None) -> "XAAttributeRunList":
        """Gets a list of attribute runs in the text. For formatted text, this returns all sequences of characters sharing the same attributes.

        :param filter: The properties and associated values to filter attribute runs by, defaults to None
        :type filter: dict, optional
        :return: The list of attribute runs
        :rtype: XAAttributeRunList

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            return []
        else:
            return self._new_element(
                self.xa_elem.attributeRuns(), XAAttributeRunList, filter
            )

    def attachments(self, filter: dict = None) -> "XAAttachmentList":
        """Gets a list of attachments of the text.

        :param filter: The properties and associated values to filter attachments by, defaults to None
        :type filter: dict, optional
        :return: The list of attachments
        :rtype: XAAttachmentList

        .. versionadded:: 0.0.1
        """
        if isinstance(self.xa_elem, str):
            return []
        else:
            return self._new_element(
                self.xa_elem.attachments(), XAAttachmentList, filter
            )

    def __len__(self):
        return len(self.xa_elem.get())

    def __str__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())

    def __repr__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())


class XAParagraphList(XATextList):
    """A wrapper around lists of paragraphs that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAParagraph)


class XAParagraph(XAText):
    """A class for managing and interacting with paragraphs in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XASentenceList(XATextList):
    """A wrapper around lists of sentences that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASentence)


class XASentence(XAText):
    """A class for managing and interacting with sentences in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAWordList(XATextList):
    """A wrapper around lists of words that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAWord)


class XAWord(XAText):
    """A class for managing and interacting with words in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XACharacterList(XATextList):
    """A wrapper around lists of characters that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XACharacter)


class XACharacter(XAText):
    """A class for managing and interacting with characters in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAAttributeRunList(XATextList):
    """A wrapper around lists of attribute runs that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAttributeRun)


class XAAttributeRun(XAText):
    """A class for managing and interacting with attribute runs in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAAttachmentList(XATextList):
    """A wrapper around lists of text attachments that employs fast enumeration techniques.

    .. versionadded:: 0.0.5
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAttachment)


class XAAttachment(XAObject):
    """A class for managing and interacting with attachments in text documents.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAColorList(XATextList):
    """A wrapper around lists of colors that employs fast enumeration techniques.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAColor, filter)


class XAColor(macimg.Color, XAObject, XAClipboardCodable):
    def __init__(self, *args):
        super().__init__(*args)
        self.xa_elem = self._nscolor

    def get_clipboard_representation(self) -> "AppKit.NSColor":
        """Gets a clipboard-codable representation of the color.

        When the clipboard content is set to a color, the raw color data is added to the clipboard.

        :return: The raw color data
        :rtype: AppKit.NSColor

        .. versionadded:: 0.1.0
        """
        return self.xa_elem


class XALocation(XAObject):
    """A location with a latitude and longitude, along with other data.

    .. versionadded:: 0.0.2
    """

    current_location: "XALocation"  #: The current location of the device

    def __init__(
        self,
        raw_value=None,
        title: str = None,
        latitude: float = 0,
        longitude: float = 0,
        altitude: float = None,
        radius: int = 0,
        address: str = None,
    ):
        self.raw_value = raw_value  #: The raw CLLocation object
        self.title = title  #: The name of the location
        self.latitude = latitude  #: The latitude of the location
        self.longitude = longitude  #: The longitude of the location
        self.altitude = altitude  #: The altitude of the location
        self.radius = radius  #: The horizontal accuracy of the location measurement
        self.address = address  #: The address of the location

        import CoreLocation

        if self.raw_value is None:
            if latitude is not None and longitude is not None:
                self.raw_value = (
                    CoreLocation.CLLocation.alloc().initWithLatitude_longitude_(
                        latitude, longitude
                    )
                )
        else:
            self.latitude = self.raw_value.coordinate()[0]
            self.longitude = self.raw_value.coordinate()[1]
            self.altitude = self.raw_value.altitude()
            self.radius = self.raw_value.horizontalAccuracy()

    @property
    def raw_value(self):
        return self.__raw_value

    @raw_value.setter
    def raw_value(self, raw_value):
        self.__raw_value = raw_value
        if raw_value is not None:
            self.latitude = raw_value.coordinate()[0]
            self.longitude = raw_value.coordinate()[1]
            self.altitude = raw_value.altitude()
            self.radius = raw_value.horizontalAccuracy()

    @property
    def current_location(self) -> "XALocation":
        """The location of the user's computer."""
        self.raw_value = None
        self._spawn_thread(self.__get_current_location)
        while self.raw_value is None:
            time.sleep(0.01)
        return self

    def show_in_maps(self):
        """Shows the location in Maps.app.

        .. versionadded:: 0.0.6
        """
        XAURL(f"maps://?q={self.title},ll={self.latitude},{self.longitude}").open()

    def reverse_geocode(self) -> dict[str, str]:
        """Obtains reverse-geocode information from the location's latitude and longitude.

        :return: A dictionary containing the location's name, street address, locality, state, country, timezone, and notable features.
        :rtype: dict[str, str]

        :Example:

        >>> import PyXA
        >>> loc = PyXA.XALocation(latitude=44.460552, longitude=-110.82807)
        >>> print(loc.reverse_geocode())
        {'name': 'Old Faithful', 'street_number': None, 'street': 'Upper Geyser Basin Trail', 'sub_locality': None, 'locality': 'Alta', 'county': 'Teton County', 'state': 'WY', 'postal_code': '83414', 'country': 'United States', 'timezone': America/Denver (MST) offset -25200, 'notable_features': (
            "Old Faithful",
            "Yellowstone National Park"
        )}

        .. versionadded:: 0.1.1
        """
        self._placemark = None

        def get_place(place, error):
            if place is not None:
                self._placemark = place[0]
            AppHelper.stopEventLoop()

        import CoreLocation

        CoreLocation.CLGeocoder.alloc().init().reverseGeocodeLocation_completionHandler_(
            self.raw_value, get_place
        )
        AppHelper.runConsoleEventLoop()

        return {
            "name": self._placemark.name(),
            "street_number": self._placemark.subThoroughfare(),
            "street": self._placemark.thoroughfare(),
            "sub_locality": self._placemark.subLocality(),
            "locality": self._placemark.locality(),
            "county": self._placemark.subAdministrativeArea(),
            "state": self._placemark.administrativeArea(),
            "postal_code": self._placemark.postalCode(),
            "country": self._placemark.country(),
            "timezone": self._placemark.timeZone(),
            "notable_features": self._placemark.areasOfInterest(),
        }

    def __get_current_location(self):
        import CoreLocation

        location_manager = CoreLocation.CLLocationManager.alloc().init()
        old_self = self

        class CLLocationManagerDelegate(AppKit.NSObject):
            def locationManager_didUpdateLocations_(self, manager, locations):
                if locations is not None:
                    old_self.raw_value = locations[0]
                    AppHelper.stopEventLoop()

            def locationManager_didFailWithError_(self, manager, error):
                print(manager, error)

        location_manager.requestWhenInUseAuthorization()
        location_manager.setDelegate_(CLLocationManagerDelegate.alloc().init().retain())
        location_manager.requestLocation()

        AppHelper.runConsoleEventLoop()

    def __repr__(self):
        return (
            "<"
            + str(type(self))
            + (self.title + " " if self.title is not None else "")
            + str((self.latitude, self.longitude))
            + ">"
        )


class XAColorPickerStyle(Enum):
    """Options for which tab a color picker should display when first opened."""

    GRAYSCALE = AppKit.NSColorPanelModeGray
    RGB_SLIDERS = AppKit.NSColorPanelModeRGB
    CMYK_SLIDERS = AppKit.NSColorPanelModeCMYK
    HSB_SLIDERS = AppKit.NSColorPanelModeHSB
    COLOR_LIST = AppKit.NSColorPanelModeColorList
    COLOR_WHEEL = AppKit.NSColorPanelModeWheel
    CRAYONS = AppKit.NSColorPanelModeCrayon
    IMAGE_PALETTE = AppKit.NSColorPanelModeCustomPalette


class XAColorPicker(XAObject):
    """A class for creating and interacting with a color picker window.

    .. versionadded:: 0.0.5
    """

    def __init__(self, style: XAColorPickerStyle = XAColorPickerStyle.COLOR_WHEEL):
        super().__init__()
        self.style = style

    def display(self) -> XAColor:
        """Displays the color picker.

        :return: The color that the user selected
        :rtype: XAColor

        .. versionadded:: 0.0.5
        """
        panel = AppKit.NSColorPanel.sharedColorPanel()
        panel.setMode_(self.style.value)
        panel.setShowsAlpha_(True)

        def run_modal(panel):
            initial_color = panel.color()
            time.sleep(0.5)
            while panel.isVisible() and panel.color() == initial_color:
                time.sleep(0.01)
            AppKit.NSApp.stopModal()

        modal_thread = threading.Thread(
            target=run_modal, args=(panel,), name="Run Modal", daemon=True
        )
        modal_thread.start()

        AppKit.NSApp.runModalForWindow_(panel)
        return XAColor(panel.color())


class XADialog(XAObject):
    """A custom dialog window.

    .. versionadded:: 0.0.8
    """

    def __init__(
        self,
        text: str = "",
        title: Union[str, None] = None,
        buttons: Union[None, list[Union[str, int]]] = None,
        hidden_answer: bool = False,
        default_button: Union[str, int, None] = None,
        cancel_button: Union[str, int, None] = None,
        icon: Union[Literal["stop", "note", "caution"], None] = None,
        default_answer: Union[str, int, None] = None,
    ):
        super().__init__()
        self.text: str = text
        self.title: str = title
        self.buttons: Union[None, list[Union[str, int]]] = buttons or []
        self.hidden_answer: bool = hidden_answer
        self.icon: Union[str, None] = icon
        self.default_button: Union[str, int, None] = default_button
        self.cancel_button: Union[str, int, None] = cancel_button
        self.default_answer: Union[str, int, None] = default_answer

    def display(self) -> Union[str, int, None, list[str]]:
        """Displays the dialog, waits for the user to select an option or cancel, then returns the selected button or None if cancelled.

        :return: The selected button or None if no value was selected
        :rtype: Union[str, int, None, list[str]]

        .. versionadded:: 0.0.8
        """
        buttons = [x.replace("'", "") for x in self.buttons]
        buttons = str(buttons).replace("'", '"')

        default_button = str(self.default_button).replace("'", "")
        default_button_str = (
            'default button "' + default_button + '"'
            if self.default_button is not None
            else ""
        )

        cancel_button = str(self.cancel_button).replace("'", "")
        cancel_button_str = (
            'cancel button "' + cancel_button + '"'
            if self.cancel_button is not None
            else ""
        )

        icon_str = "with icon " + self.icon + "" if self.icon is not None else ""

        default_answer = str(self.default_answer).replace("'", '"')
        default_answer_str = (
            'default answer "' + default_answer + '"'
            if self.default_answer is not None
            else ""
        )

        script = AppleScript(
            f"""
        tell application "System Events"
            display dialog \"{self.text}\" with title \"{self.title}\" buttons {buttons} {default_button_str} {cancel_button_str} {icon_str} {default_answer_str} hidden answer {self.hidden_answer}
        end tell
        """
        )

        result = script.run()["event"]
        if result is not None:
            if result.numberOfItems() > 1:
                return [
                    result.descriptorAtIndex_(1).stringValue(),
                    result.descriptorAtIndex_(2).stringValue(),
                ]
            else:
                return result.descriptorAtIndex_(1).stringValue()


class XAMenu(XAObject):
    """A custom list item selection menu.

    .. versionadded:: 0.0.8
    """

    def __init__(
        self,
        menu_items: list[Any],
        title: str = "Select Item",
        prompt: str = "Select an item",
        default_items: Union[list[str], None] = None,
        ok_button_name: str = "Okay",
        cancel_button_name: str = "Cancel",
        multiple_selections_allowed: bool = False,
        empty_selection_allowed: bool = False,
    ):
        super().__init__()
        self.menu_items: list[
            Union[str, int]
        ] = menu_items  #: The items the user can choose from
        self.title: str = title  #: The title of the dialog window
        self.prompt: str = prompt  #: The prompt to display in the dialog box
        self.default_items: list[str] = (
            default_items or []
        )  #: The items to initially select
        self.ok_button_name: str = ok_button_name  #: The name of the OK button
        self.cancel_button_name: str = (
            cancel_button_name  #: The name of the Cancel button
        )
        self.multiple_selections_allowed: bool = (
            multiple_selections_allowed  #: Whether multiple items can be selected
        )
        self.empty_selection_allowed: bool = empty_selection_allowed  #: Whether the user can click OK without selecting anything

    def display(self) -> Union[str, int, bool, list[str], list[int]]:
        """Displays the menu, waits for the user to select an option or cancel, then returns the selected value or False if cancelled.

        :return: The selected value or False if no value was selected
        :rtype: Union[str, int, bool, list[str], list[int]]

        .. versionadded:: 0.0.8
        """
        menu_items = [x.replace("'", "") for x in self.menu_items]
        menu_items = str(menu_items).replace("'", '"')
        default_items = str(self.default_items).replace("'", '"')
        script = AppleScript(
            f"""
        tell application "System Events"
            choose from list {menu_items} with title \"{self.title}\" with prompt \"{self.prompt}\" default items {default_items} OK button name \"{self.ok_button_name}\" cancel button name \"{self.cancel_button_name}\" multiple selections allowed {self.multiple_selections_allowed} empty selection allowed {self.empty_selection_allowed}
        end tell
        """
        )
        result = script.run()["event"]
        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(desc.stringValue())
                return values
            else:
                if result.stringValue() == "false":
                    return False
                return result.stringValue()


class XAFilePicker(XAObject):
    """A file selection window.

    .. versionadded:: 0.0.8
    """

    def __init__(
        self,
        prompt: str = "Choose File",
        types: list[str] = None,
        default_location: Union[str, None] = None,
        show_invisibles: bool = False,
        multiple_selections_allowed: bool = False,
        show_package_contents: bool = False,
    ):
        super().__init__()
        self.prompt: str = prompt  #: The prompt to display in the dialog box
        self.types: list[
            str
        ] = types  #: The file types/type identifiers to allow for selection
        self.default_location: Union[
            str, None
        ] = default_location  #: The default file location
        self.show_invisibles: bool = (
            show_invisibles  #: Whether invisible files and folders are shown
        )
        self.multiple_selections_allowed: bool = (
            multiple_selections_allowed  #: Whether the user can select multiple files
        )
        self.show_package_contents: bool = (
            show_package_contents  #: Whether to show the contents of packages
        )

    def display(self) -> Union[XAPath, None]:
        """Displays the file chooser, waits for the user to select a file or cancel, then returns the selected file URL or None if cancelled.

        :return: The selected file URL or None if no file was selected
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """
        types = [x.replace("'", "") for x in self.types]
        types = str(types).replace("'", '"')
        types_str = "of type " + types if self.types is not None else ""

        default_location_str = (
            'default location "' + self.default_location + '"'
            if self.default_location is not None
            else ""
        )

        script = AppleScript(
            f"""
        tell application "System Events"
            choose file with prompt \"{self.prompt}\" {types_str}{default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """
        )
        result = script.run()["event"]

        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(XAPath(desc.fileURLValue()))
                return values
            else:
                return XAPath(result.fileURLValue())


class XAFolderPicker(XAObject):
    """A folder selection window.

    .. versionadded:: 0.0.8
    """

    def __init__(
        self,
        prompt: str = "Choose Folder",
        default_location: Union[str, None] = None,
        show_invisibles: bool = False,
        multiple_selections_allowed: bool = False,
        show_package_contents: bool = False,
    ):
        super().__init__()
        self.prompt: str = prompt  #: The prompt to display in the dialog box
        self.default_location: Union[
            str, None
        ] = default_location  #: The default folder location
        self.show_invisibles: bool = (
            show_invisibles  #: Whether invisible files and folders are shown
        )
        self.multiple_selections_allowed: bool = (
            multiple_selections_allowed  #: Whether the user can select multiple folders
        )
        self.show_package_contents: bool = (
            show_package_contents  #: Whether to show the contents of packages
        )

    def display(self) -> Union[XAPath, None]:
        """Displays the folder chooser, waits for the user to select a folder or cancel, then returns the selected folder URL or None if cancelled.

        :return: The selected folder URL or None if no folder was selected
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """

        default_location_str = (
            'default location "' + self.default_location + '"'
            if self.default_location is not None
            else ""
        )

        script = AppleScript(
            f"""
        tell application "System Events"
            choose folder with prompt \"{self.prompt}\" {default_location_str} invisibles {self.show_invisibles} multiple selections allowed {self.multiple_selections_allowed} showing package contents {self.show_package_contents}
        end tell
        """
        )
        result = script.run()["event"]
        if result is not None:
            if self.multiple_selections_allowed:
                values = []
                for x in range(1, result.numberOfItems() + 1):
                    desc = result.descriptorAtIndex_(x)
                    values.append(XAPath(desc.fileURLValue()))
                return values
            else:
                return XAPath(result.fileURLValue())


class XAApplicationPicker(XAObject):
    """An application selection window.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self,
        title: Union[str, None] = None,
        prompt: Union[str, None] = None,
        multiple_selections_allowed: bool = False,
    ):
        super().__init__()
        self.title: str = title  #: The dialog window title
        self.prompt: str = prompt  #: The prompt to be displayed in the dialog box
        self.multiple_selections_allowed: bool = multiple_selections_allowed  #: Whether to allow multiple items to be selected

    def display(self) -> str:
        """Displays the application chooser, waits for the user to select an application or cancel, then returns the selected application's name or None if cancelled.

        :return: The name of the selected application
        :rtype: str

        .. versionadded:: 0.0.8
        """

        script = AppleScript('tell application "System Events"')
        dialog_str = "choose application "
        if self.title is not None:
            dialog_str += f'with title "{self.title}" '
        if self.prompt is not None:
            dialog_str += f'with prompt "{self.prompt}"'
        dialog_str += f"multiple selections allowed {self.multiple_selections_allowed} "
        script.add(dialog_str)
        script.add("end tell")

        return script.run()["string"]


class XAFileNameDialog(XAObject):
    """A file name input window.

    .. versionadded:: 0.0.8
    """

    def __init__(
        self,
        prompt: str = "Specify file name and location",
        default_name: str = "New File",
        default_location: Union[str, None] = None,
    ):
        super().__init__()
        self.prompt: str = prompt  #: The prompt to display in the dialog box
        self.default_name: str = default_name  #: The default name for the new file
        self.default_location: Union[
            str, None
        ] = default_location  #: The default file location

    def display(self) -> Union[XAPath, None]:
        """Displays the file name input window, waits for the user to input a name and location or cancel, then returns the specified file URL or None if cancelled.

        :return: The specified file URL or None if no file name was inputted
        :rtype: Union[XAPath, None]

        .. versionadded:: 0.0.8
        """

        default_location_str = (
            'default location "' + self.default_location + '"'
            if self.default_location is not None
            else ""
        )

        script = AppleScript(
            f"""
        tell application "System Events"
            choose file name with prompt \"{self.prompt}\" default name \"{self.default_name}\" {default_location_str}
        end tell
        """
        )
        result = script.run()["event"]
        if result is not None:
            return XAPath(result.fileURLValue())


#############################
### System / Image Events ###
#############################
# ? Move into separate XAFileSystemBase.py file?
class XAEventsApplication(XACanOpenPath):
    """A base class for the System and Image events applications.

    .. versionadded:: 0.1.0
    """

    class Format(Enum):
        """Disk format options."""

        APPLE_PHOTO = OSType("dfph")
        APPLESHARE = OSType("dfas")
        AUDIO = OSType("dfau")
        HIGH_SIERRA = OSType("dfhs")
        ISO_9660 = OSType("fd96")
        MACOS_EXTENDED = OSType("dfh+")
        MACOS = OSType("dfhf")
        MSDOS = OSType("dfms")
        NFS = OSType("dfnf")
        PRODOS = OSType("dfpr")
        QUICKTAKE = OSType("dfqt")
        UDF = OSType("dfud")
        UFS = OSType("dfuf")
        UNKNOWN = OSType("df$$")
        WEBDAV = OSType("dfwd")


class XADiskItemList(XAList):
    """A wrapper around lists of disk items that employs fast enumeration techniques.

    All properties of disk items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, object_class=None
    ):
        if object_class is None:
            object_class = XADiskItem
        super().__init__(properties, object_class, filter)

    def busy_status(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("busyStatus") or [])

    def container(self) -> "XADiskItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XADiskItemList)

    def creation_date(self) -> list["datetime"]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def displayed_name(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def id(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def modification_date(self) -> list["datetime"]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def name(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def name_extension(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("nameExtension") or [])

    def package_folder(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("packageFolder") or [])

    def path(self) -> list["XAPath"]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XAPath(x) for x in ls]

    def physical_size(self) -> list["int"]:
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize") or [])

    def posix_path(self) -> list[XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("POSIXPath") or []
        return [XAPath(x) for x in ls]

    def size(self) -> list["int"]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def url(self) -> list["XAURL"]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XAURL(x) for x in ls]

    def visible(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def volume(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("volume") or [])

    def by_busy_status(self, busy_status: bool) -> Union["XADiskItem", None]:
        return self.by_property("busyStatus", busy_status)

    def by_container(self, container: "XADiskItem") -> Union["XADiskItem", None]:
        return self.by_property("container", container.xa_elem)

    def by_creation_date(self, creation_date: datetime) -> Union["XADiskItem", None]:
        return self.by_property("creationDate", creation_date)

    def by_displayed_name(self, displayed_name: str) -> Union["XADiskItem", None]:
        return self.by_property("displayedName", displayed_name)

    def by_id(self, id: str) -> Union["XADiskItem", None]:
        return self.by_property("id", id)

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XADiskItem", None]:
        return self.by_property("modificationDate", modification_date)

    def by_name(self, name: str) -> Union["XADiskItem", None]:
        return self.by_property("name", name)

    def by_name_extension(self, name_extension: str) -> Union["XADiskItem", None]:
        return self.by_property("nameExtension", name_extension)

    def by_package_folder(self, package_folder: bool) -> Union["XADiskItem", None]:
        return self.by_property("packageFolder", package_folder)

    def by_path(self, path: Union[XAPath, str]) -> Union["XADiskItem", None]:
        if isinstance(path, XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_physical_size(self, physical_size: int) -> Union["XADiskItem", None]:
        return self.by_property("physicalSize", physical_size)

    def by_posix_path(
        self, posix_path: Union[XAPath, str]
    ) -> Union["XADiskItem", None]:
        if isinstance(posix_path, XAPath):
            posix_path = posix_path.path
        return self.by_property("POSIXPath", posix_path)

    def by_size(self, size: int) -> Union["XADiskItem", None]:
        return self.by_property("size", size)

    def by_url(self, url: XAURL) -> Union["XADiskItem", None]:
        return self.by_property("URL", url.xa_elem)

    def by_visible(self, visible: bool) -> Union["XADiskItem", None]:
        return self.by_property("visible", visible)

    def by_volume(self, volume: str) -> Union["XADiskItem", None]:
        return self.by_property("volume", volume)

    def move_to(self, folder: Union[str, XAPath, "XAFolder"]) -> "XADiskItem":
        """Moves all disk items in the list to the specified location.

        :param folder: The folder location to move the items to
        :type folder: Union[str, XAPath, XAFolder]
        :return: The list of disk items
        :rtype: XADiskItem

        .. versionadded:: 0.2.1
        """
        if isinstance(folder, XAFolder):
            folder = folder.posix_path
        elif isinstance(folder, str):
            folder = XAPath(folder)

        for item in self.xa_elem.get():
            item.moveTo_(folder.xa_elem)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XADiskItem(XAObject, XAPathLike):
    """An item stored in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def busy_status(self) -> "bool":
        """Whether the disk item is busy.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.busyStatus()

    @property
    def container(self) -> "XADiskItem":
        """The folder or disk which has this disk item as an element.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.container(), XADiskItem)

    @property
    def creation_date(self) -> "datetime":
        """The date on which the disk item was created.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creationDate()

    @property
    def displayed_name(self) -> "str":
        """The name of the disk item as displayed in the User Interface.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.displayedName()

    @property
    def id(self) -> "str":
        """The unique ID of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def modification_date(self) -> "datetime":
        """The date on which the disk item was last modified.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.modificationDate()

    @property
    def name(self) -> "str":
        """The name of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def name_extension(self) -> "str":
        """The extension portion of the name.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.nameExtension()

    @property
    def package_folder(self) -> "bool":
        """Whether the disk item is a package.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.packageFolder()

    @property
    def path(self) -> "XAPath":
        """The file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAPath(self.xa_elem.path())

    @property
    def physical_size(self) -> "int":
        """The actual space used by the disk item on disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.physicalSize()

    @property
    def posix_path(self) -> XAPath:
        """The POSIX file system path of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAPath(self.xa_elem.POSIXPath())

    @property
    def size(self) -> "int":
        """The logical size of the disk item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.size()

    @property
    def url(self) -> "XAURL":
        """The URL of the disk item.

        .. versionadded:: 0.1.0
        """
        return XAURL(self.xa_elem.URL())

    @property
    def visible(self) -> "bool":
        """Whether the disk item is visible.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.visible()

    @property
    def volume(self) -> "str":
        """The volume on which the disk item resides.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.volume()

    def open(self) -> "XADiskItem":
        """Opens the item in its default application.

        :return: The item object
        :rtype: XADiskItem

        .. versionadded:: 0.1.1
        """
        self.xa_elem.open()
        return self

    def move_to(self, folder: Union[str, XAPath, "XAFolder"]) -> "XADiskItem":
        """Moves the disk item to the specified location.

        :param folder: The folder location to move the item to
        :type folder: Union[str, XAPath, XAFolder]
        :return: The disk item object
        :rtype: XADiskItem

        .. versionadded:: 0.2.1
        """
        if isinstance(folder, XAFolder):
            folder = folder.posix_path
        elif isinstance(folder, str):
            folder = XAPath(folder)

        self.xa_elem.moveTo_(folder.xa_elem)
        return self

    def get_path_representation(self) -> XAPath:
        return self.posix_path

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAAliasList(XADiskItemList):
    """A wrapper around lists of aliases that employs fast enumeration techniques.

    All properties of aliases can be called as methods on the wrapped list, returning a list containing each alias' value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAAlias)

    def creator_type(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def default_application(self) -> "XADiskItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication") or []
        return self._new_element(ls, XADiskItemList)

    def file_type(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def kind(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def product_version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion") or [])

    def short_version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion") or [])

    def stationery(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("stationery") or [])

    def type_identifier(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier") or [])

    def version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("version") or [])

    def by_creator_type(self, creator_type: str) -> Union["XAAlias", None]:
        return self.by_property("creatorType", creator_type)

    def by_default_application(
        self, default_application: "XADiskItem"
    ) -> Union["XAAlias", None]:
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> Union["XAAlias", None]:
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> Union["XAAlias", None]:
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> Union["XAAlias", None]:
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> Union["XAAlias", None]:
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> Union["XAAlias", None]:
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> Union["XAAlias", None]:
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> Union["XAAlias", None]:
        return self.by_property("version", version)


class XAAlias(XADiskItem):
    """An alias in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> "str":
        """The OSType identifying the application that created the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> "XADiskItem":
        """The application that will launch if the alias is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XADiskItem)

    @property
    def file_type(self) -> "str":
        """The OSType identifying the type of data contained in the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> "str":
        """The kind of alias, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> "str":
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> "str":
        """The short version of the application bundle referenced by the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> "bool":
        """Whether the alias is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> "str":
        """The type identifier of the alias.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> "str":
        """The version of the application bundle referenced by the alias (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()

    def aliases(self, filter: Union[dict, None] = None) -> "XAAliasList":
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> "XADiskItemList":
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> "XAFileList":
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> "XAFilePackageList":
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)


class XADiskList(XADiskItemList):
    """A wrapper around lists of disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XADisk)

    def capacity(self) -> list["float"]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity") or [])

    def ejectable(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable") or [])

    def format(self) -> list["XAEventsApplication.Format"]:
        ls = self.xa_elem.arrayByApplyingSelector_("format") or []
        return [XAEventsApplication.Format(OSType(x.stringValue())) for x in ls]

    def free_space(self) -> list["float"]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace") or [])

    def ignore_privileges(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("ignorePrivileges") or [])

    def local_volume(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume") or [])

    def server(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("server") or [])

    def startup(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("startup") or [])

    def zone(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("zone") or [])

    def by_capacity(self, capacity: float) -> Union["XADisk", None]:
        return self.by_property("capacity", capacity)

    def by_ejectable(self, ejectable: bool) -> Union["XADisk", None]:
        return self.by_property("ejectable", ejectable)

    def by_format(self, format: "XAEventsApplication.Format") -> Union["XADisk", None]:
        return self.by_property("format", format.value)

    def by_free_space(self, free_space: float) -> Union["XADisk", None]:
        return self.by_property("freeSpace", free_space)

    def by_ignore_privileges(self, ignore_privileges: bool) -> Union["XADisk", None]:
        return self.by_property("ignorePrivileges", ignore_privileges)

    def by_local_volume(self, local_volume: bool) -> Union["XADisk", None]:
        return self.by_property("localVolume", local_volume)

    def by_server(self, server: str) -> Union["XADisk", None]:
        return self.by_property("server", server)

    def by_startup(self, startup: bool) -> Union["XADisk", None]:
        return self.by_property("startup", startup)

    def by_zone(self, zone: str) -> Union["XADisk", None]:
        return self.by_property("zone", zone)


class XADisk(XADiskItem):
    """A disk in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def capacity(self) -> "float":
        """The total number of bytes (free or used) on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.capacity()

    @property
    def ejectable(self) -> "bool":
        """Whether the media can be ejected (floppies, CD's, and so on).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ejectable()

    @property
    def format(self) -> "XAEventsApplication.Format":
        """The file system format of the disk.

        .. versionadded:: 0.1.0
        """
        return XAEventsApplication.Format(self.xa_elem.format())

    @property
    def free_space(self) -> "float":
        """The number of free bytes left on the disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.freeSpace()

    @property
    def ignore_privileges(self) -> "bool":
        """Whether to ignore permissions on this disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.ignorePrivileges()

    @property
    def local_volume(self) -> "bool":
        """Whether the media is a local volume (as opposed to a file server).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.localVolume()

    @property
    def server(self) -> "str":
        """The server on which the disk resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.server()

    @property
    def startup(self) -> "bool":
        """Whether this disk is the boot disk.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.startup()

    @property
    def zone(self) -> "str":
        """The zone in which the disk's server resides, AFP volumes only.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.zone()

    def aliases(self, filter: Union[dict, None] = None) -> "XAAliasList":
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> "XADiskItemList":
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> "XAFileList":
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> "XAFilePackageList":
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fileOackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)


class XADomainList(XAList):
    """A wrapper around lists of domains that employs fast enumeration techniques.

    All properties of domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XADomain, filter)

    def id(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_id(self, id: str) -> Union["XADomain", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XADomain", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XADomain(XAObject):
    """A domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def application_support_folder(self) -> "XAFolder":
        """The Application Support folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationSupportFolder(), XAFolder)

    @property
    def applications_folder(self) -> "XAFolder":
        """The Applications folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.applicationsFolder(), XAFolder)

    @property
    def desktop_pictures_folder(self) -> "XAFolder":
        """The Desktop Pictures folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopPicturesFolder(), XAFolder)

    @property
    def folder_action_scripts_folder(self) -> "XAFolder":
        """The Folder Action Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folderActionScriptsFolder(), XAFolder)

    @property
    def fonts_folder(self) -> "XAFolder":
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAFolder)

    @property
    def id(self) -> "str":
        """The unique identifier of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.id()

    @property
    def library_folder(self) -> "XAFolder":
        """The Library folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.libraryFolder(), XAFolder)

    @property
    def name(self) -> "str":
        """The name of the domain.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.name()

    @property
    def preferences_folder(self) -> "XAFolder":
        """The Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAFolder)

    @property
    def scripting_additions_folder(self) -> "XAFolder":
        """The Scripting Additions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptingAdditionsFolder(), XAFolder)

    @property
    def scripts_folder(self) -> "XAFolder":
        """The Scripts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scriptsFolder(), XAFolder)

    @property
    def shared_documents_folder(self) -> "XAFolder":
        """The Shared Documents folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sharedDocumentsFolder(), XAFolder)

    @property
    def speakable_items_folder(self) -> "XAFolder":
        """The Speakable Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.speakableItemsFolder(), XAFolder)

    @property
    def utilities_folder(self) -> "XAFolder":
        """The Utilities folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.utilitiesFolder(), XAFolder)

    @property
    def workflows_folder(self) -> "XAFolder":
        """The Automator Workflows folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.workflowsFolder(), XAFolder)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAClassicDomainObject(XADomain):
    """The Classic domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def apple_menu_folder(self) -> "XAFolder":
        """The Apple Menu Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.appleMenuFolder(), XAFolder)

    @property
    def control_panels_folder(self) -> "XAFolder":
        """The Control Panels folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlPanelsFolder(), XAFolder)

    @property
    def control_strip_modules_folder(self) -> "XAFolder":
        """The Control Strip Modules folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.controlStripModulesFolder(), XAFolder)

    @property
    def desktop_folder(self) -> "XAFolder":
        """The Classic Desktop folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAFolder)

    @property
    def extensions_folder(self) -> "XAFolder":
        """The Extensions folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.extensionsFolder(), XAFolder)

    @property
    def fonts_folder(self) -> "XAFolder":
        """The Fonts folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.fontsFolder(), XAFolder)

    @property
    def launcher_items_folder(self) -> "XAFolder":
        """The Launcher Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.launcherItemsFolder(), XAFolder)

    @property
    def preferences_folder(self) -> "XAFolder":
        """The Classic Preferences folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.preferencesFolder(), XAFolder)

    @property
    def shutdown_folder(self) -> "XAFolder":
        """The Shutdown Items folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.shutdownFolder(), XAFolder)

    @property
    def startup_items_folder(self) -> "XAFolder":
        """The StartupItems folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.startupItemsFolder(), XAFolder)

    @property
    def system_folder(self) -> "XAFolder":
        """The System folder.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.systemFolder(), XAFolder)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)


class XAFileList(XADiskItemList):
    """A wrapper around lists of files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, object_class=None
    ):
        if object_class is None:
            object_class = XAFile
        super().__init__(properties, filter, object_class)

    def creator_type(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def default_application(self) -> "XADiskItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("defaultApplication") or []
        return self._new_element(ls, XADiskItemList)

    def file_type(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def kind(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def product_version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion") or [])

    def short_version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("shortVersion") or [])

    def stationery(self) -> list["bool"]:
        return list(self.xa_elem.arrayByApplyingSelector_("stationery") or [])

    def type_identifier(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("typeIdentifier") or [])

    def version(self) -> list["str"]:
        return list(self.xa_elem.arrayByApplyingSelector_("version") or [])

    def by_creator_type(self, creator_type: str) -> Union["XAFile", None]:
        return self.by_property("creatorType", creator_type)

    def by_default_application(
        self, default_application: "XADiskItem"
    ) -> Union["XAFile", None]:
        return self.by_property("defaultApplication", default_application.xa_elem)

    def by_file_type(self, file_type: str) -> Union["XAFile", None]:
        return self.by_property("fileType", file_type)

    def by_kind(self, kind: str) -> Union["XAFile", None]:
        return self.by_property("kind", kind)

    def by_product_version(self, product_version: str) -> Union["XAFile", None]:
        return self.by_property("productVersion", product_version)

    def by_short_version(self, short_version: str) -> Union["XAFile", None]:
        return self.by_property("shortVersion", short_version)

    def by_stationery(self, stationery: bool) -> Union["XAFile", None]:
        return self.by_property("stationery", stationery)

    def by_type_identifier(self, type_identifier: str) -> Union["XAFile", None]:
        return self.by_property("typeIdentifier", type_identifier)

    def by_version(self, version: str) -> Union["XAFile", None]:
        return self.by_property("version", version)


class XAFile(XADiskItem):
    """A file in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def creator_type(self) -> "str":
        """The OSType identifying the application that created the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.creatorType()

    @property
    def default_application(self) -> "XADiskItem":
        """The application that will launch if the file is opened.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.defaultApplication(), XADiskItem)

    @default_application.setter
    def default_application(self, default_application: XADiskItem):
        self.set_property("defaultApplication", default_application.xa_elem)

    @property
    def file_type(self) -> "str":
        """The OSType identifying the type of data contained in the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.fileType()

    @property
    def kind(self) -> "str":
        """The kind of file, as shown in Finder.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.kind()

    @property
    def product_version(self) -> "str":
        """The version of the product (visible at the top of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.productVersion()

    @property
    def short_version(self) -> "str":
        """The short version of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.shortVersion()

    @property
    def stationery(self) -> "bool":
        """Whether the file is a stationery pad.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stationery()

    @property
    def type_identifier(self) -> "str":
        """The type identifier of the file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.typeIdentifier()

    @property
    def version(self) -> "str":
        """The version of the file (visible at the bottom of the "Get Info" window).

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.version()


class XAFilePackageList(XAFileList):
    """A wrapper around lists of file packages that employs fast enumeration techniques.

    All properties of file packages can be called as methods on the wrapped list, returning a list containing each package's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFilePackage)


class XAFilePackage(XAFile):
    """A file package in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> "XAAliasList":
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> "XADiskItemList":
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> "XAFileList":
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> "XAFilePackageList":
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)


class XAFolderList(XADiskItemList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    All properties of folders can be called as methods on the wrapped list, returning a list containing each folder's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFolder)


class XAFolder(XADiskItem):
    """A folder in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    def aliases(self, filter: Union[dict, None] = None) -> "XAAliasList":
        """Returns a list of aliases, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.aliases(), XAAliasList, filter)

    def disk_items(self, filter: Union[dict, None] = None) -> "XADiskItemList":
        """Returns a list of disk items, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.diskItems(), XADiskItemList, filter)

    def files(self, filter: Union[dict, None] = None) -> "XAFileList":
        """Returns a list of files, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.files(), XAFileList, filter)

    def file_packages(self, filter: Union[dict, None] = None) -> "XAFilePackageList":
        """Returns a list of file packages, as PyXA objects, matching the given filter.

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.filePackages(), XAFilePackageList, filter)

    def folders(self, filter: Union[dict, None] = None) -> "XAFolderList":
        """Returns a list of folders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XAFolderList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.folders(), XAFolderList, filter)


class XALocalDomainObject(XADomain):
    """The local domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XANetworkDomainObject(XADomain):
    """The network domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XASystemDomainObject(XADomain):
    """The system domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAUserDomainObject(XADomain):
    """The user domain in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def desktop_folder(self) -> "XAFolder":
        """The user's Desktop folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.desktopFolder(), XAFolder)

    @property
    def documents_folder(self) -> "XAFolder":
        """The user's Documents folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.documentsFolder(), XAFolder)

    @property
    def downloads_folder(self) -> "XAFolder":
        """The user's Downloads folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.downloadsFolder(), XAFolder)

    @property
    def favorites_folder(self) -> "XAFolder":
        """The user's Favorites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.favoritesFolder(), XAFolder)

    @property
    def home_folder(self) -> "XAFolder":
        """The user's Home folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.homeFolder(), XAFolder)

    @property
    def movies_folder(self) -> "XAFolder":
        """The user's Movies folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.moviesFolder(), XAFolder)

    @property
    def music_folder(self) -> "XAFolder":
        """The user's Music folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.musicFolder(), XAFolder)

    @property
    def pictures_folder(self) -> "XAFolder":
        """The user's Pictures folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.picturesFolder(), XAFolder)

    @property
    def public_folder(self) -> "XAFolder":
        """The user's Public folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.publicFolder(), XAFolder)

    @property
    def sites_folder(self) -> "XAFolder":
        """The user's Sites folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sitesFolder(), XAFolder)

    @property
    def temporary_items_folder(self) -> "XAFolder":
        """The Temporary Items folder

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.temporaryItemsFolder(), XAFolder)


#############
### Media ###
#############
class XAImageList(XAList, XAClipboardCodable):
    """A wrapper around lists of images that employs fast enumeration techniques.

    .. deprecated:: 0.2.0

       Use :class:`XAImage` and its methods instead.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAImage
        super().__init__(properties, obj_class, filter)

        self.modified = False  #: Whether the list of images has been modified since it was initialized

    def __partial_init(self):
        images = [None] * self.xa_elem.count()

        def init_images(ref, index, stop):
            if isinstance(ref, str):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(XAPath(ref).xa_elem)
            elif isinstance(ref, ScriptingBridge.SBObject):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(
                    XAPath(ref.imageFile().POSIXPath()).xa_elem
                )
            elif isinstance(ref, XAObject):
                ref = AppKit.NSImage.alloc().initWithContentsOfURL_(
                    ref.image_file.posix_path.xa_elem
                )
            images[index] = ref

        self.xa_elem.enumerateObjectsUsingBlock_(init_images)
        return AppKit.NSMutableArray.alloc().initWithArray_(images)

    def __apply_filter(self, filter_block, *args):
        images = self.__partial_init()

        filtered_images = [None] * images.count()

        def filter_image(image, index, *args):
            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = filter_block(image, *args)
            filter.setValue_forKey_(img, "inputImage")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(
                Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2)
            )

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            filtered_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(filter_image, [image, index, *args])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(filtered_images)
        return self

    def file(self) -> list[XAPath]:
        return [x.file for x in self]

    def horizontal_stitch(self) -> "XAImage":
        """Horizontally stacks each image in the list.

        The first image in the list is placed at the left side of the resulting image.

        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return XAImage.horizontal_stitch(self)

    def vertical_stitch(self) -> "XAImage":
        """Vertically stacks each image in the list.

        The first image in the list is placed at the bottom side of the resulting image.

        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return XAImage.vertical_stitch(self)

    def additive_composition(self) -> "XAImage":
        """Creates a composition image by adding the color values of each image in the list.

        :param images: The images to add together
        :type images: list[XAImage]
        :return: The resulting image composition
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image_data = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            if isinstance(image, str):
                image = AppKit.NSImage.alloc().initWithContentsOfURL_(
                    XAPath(image).xa_elem
                )
            image_data[index] = Quartz.CIImage.imageWithData_(
                image.TIFFRepresentation()
            )

        current_composition = None
        while len(image_data) > 1:
            img1 = image_data.pop(0)
            img2 = image_data.pop(0)
            composition_filter = Quartz.CIFilter.filterWithName_(
                "CIAdditionCompositing"
            )
            composition_filter.setDefaults()
            composition_filter.setValue_forKey_(img1, "inputImage")
            composition_filter.setValue_forKey_(img2, "inputBackgroundImage")
            current_composition = composition_filter.outputImage()
            image_data.insert(0, current_composition)

        composition_rep = AppKit.NSCIImageRep.imageRepWithCIImage_(current_composition)
        composition = AppKit.NSImage.alloc().initWithSize_(composition_rep.size())
        composition.addRepresentation_(composition_rep)
        return XAImage(composition)

    def subtractive_composition(self) -> "XAImage":
        """Creates a composition image by subtracting the color values of each image in the list successively.

        :param images: The images to create the composition from
        :type images: list[XAImage]
        :return: The resulting image composition
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        image_data = [None] * self.xa_elem.count()
        for index, image in enumerate(self.xa_elem):
            if isinstance(image, str):
                image = AppKit.NSImage.alloc().initWithContentsOfURL_(
                    XAPath(image).xa_elem
                )
            image_data[index] = Quartz.CIImage.imageWithData_(
                image.TIFFRepresentation()
            )

        current_composition = None
        while len(image_data) > 1:
            img1 = image_data.pop(0)
            img2 = image_data.pop(0)
            composition_filter = Quartz.CIFilter.filterWithName_("CISubtractBlendMode")
            composition_filter.setDefaults()
            composition_filter.setValue_forKey_(img1, "inputImage")
            composition_filter.setValue_forKey_(img2, "inputBackgroundImage")
            current_composition = composition_filter.outputImage()
            image_data.insert(0, current_composition)

        composition_rep = AppKit.NSCIImageRep.imageRepWithCIImage_(current_composition)
        composition = AppKit.NSImage.alloc().initWithSize_(composition_rep.size())
        composition.addRepresentation_(composition_rep)
        return XAImage(composition)

    def edges(self, intensity: float = 1.0) -> "XAImageList":
        """Detects the edges in each image of the list and highlights them colorfully, blackening other areas of the images.

        :param intensity: The degree to which edges are highlighted. Higher is brighter. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIEdges")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def gaussian_blur(self, intensity: float = 10) -> "XAImageList":
        """Blurs each image in the list using a Gaussian filter.

        :param intensity: The strength of the blur effect, defaults to 10
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIGaussianBlur")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def reduce_noise(
        self, noise_level: float = 0.02, sharpness: float = 0.4
    ) -> "XAImageList":
        """Reduces noise in each image of the list by sharpening areas with a luminance delta below the specified noise level threshold.

        :param noise_level: The threshold for luminance changes in an area below which will be considered noise, defaults to 0.02
        :type noise_level: float
        :param sharpness: The sharpness of the resulting images, defaults to 0.4
        :type sharpness: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, noise_level, sharpness):
            filter = Quartz.CIFilter.filterWithName_("CINoiseReduction")
            filter.setDefaults()
            filter.setValue_forKey_(noise_level, "inputNoiseLevel")
            filter.setValue_forKey_(sharpness, "inputSharpness")
            return filter

        return self.__apply_filter(filter_block, noise_level, sharpness)

    def pixellate(self, pixel_size: float = 8.0) -> "XAImageList":
        """Pixellates each image in the list.

        :param pixel_size: The size of the pixels, defaults to 8.0
        :type pixel_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, pixel_size):
            filter = Quartz.CIFilter.filterWithName_("CIPixellate")
            filter.setDefaults()
            filter.setValue_forKey_(pixel_size, "inputScale")
            return filter

        return self.__apply_filter(filter_block, pixel_size)

    def outline(self, threshold: float = 0.1) -> "XAImageList":
        """Outlines detected edges within each image of the list in black, leaving the rest transparent.

        :param threshold: The threshold to use when separating edge and non-edge pixels. Larger values produce thinner edge lines. Defaults to 0.1
        :type threshold: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, threshold):
            filter = Quartz.CIFilter.filterWithName_("CILineOverlay")
            filter.setDefaults()
            filter.setValue_forKey_(threshold, "inputThreshold")
            return filter

        return self.__apply_filter(filter_block, threshold)

    def invert(self) -> "XAImageList":
        """Inverts the colors of each image in the list.

        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image):
            filter = Quartz.CIFilter.filterWithName_("CIColorInvert")
            filter.setDefaults()
            return filter

        return self.__apply_filter(filter_block)

    def sepia(self, intensity: float = 1.0) -> "XAImageList":
        """Applies a sepia filter to each image in the list; maps all colors of the images to shades of brown.

        :param intensity: The opacity of the sepia effect. A value of 0 will have no impact on the image. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CISepiaTone")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def vignette(self, intensity: float = 1.0) -> "XAImageList":
        """Applies vignette shading to the corners of each image in the list.

        :param intensity: The intensity of the vignette effect, defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIVignette")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def depth_of_field(
        self,
        focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None] = None,
        intensity: float = 10.0,
        focal_region_saturation: float = 1.5,
    ) -> "XAImageList":
        """Applies a depth of field filter to each image in the list, simulating a tilt & shift effect.

        :param focal_region: Two points defining a line within each image to focus the effect around (pixels around the line will be in focus), or None to use the center third of the image, defaults to None
        :type focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None]
        :param intensity: Controls the amount of distance around the focal region to keep in focus. Higher values decrease the distance before the out-of-focus effect starts. Defaults to 10.0
        :type intensity: float
        :param focal_region_saturation: Adjusts the saturation of the focial region. Higher values increase saturation. Defaults to 1.5 (1.5x default saturation)
        :type focal_region_saturation: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, focal_region, intensity, focal_region_saturation):
            if focal_region is None:
                center_top = Quartz.CIVector.vectorWithX_Y_(
                    image.size().width / 2, image.size().height / 3
                )
                center_bottom = Quartz.CIVector.vectorWithX_Y_(
                    image.size().width / 2, image.size().height / 3 * 2
                )
                focal_region = (center_top, center_bottom)
            else:
                point1 = Quartz.CIVector.vectorWithX_Y_(focal_region[0])
                point2 = Quartz.CIVector.vectorWithX_Y_(focal_region[1])
                focal_region = (point1, point2)

            filter = Quartz.CIFilter.filterWithName_("CIDepthOfField")
            filter.setDefaults()
            filter.setValue_forKey_(focal_region[0], "inputPoint0")
            filter.setValue_forKey_(focal_region[1], "inputPoint1")
            filter.setValue_forKey_(intensity, "inputRadius")
            filter.setValue_forKey_(focal_region_saturation, "inputSaturation")
            return filter

        return self.__apply_filter(
            filter_block, focal_region, intensity, focal_region_saturation
        )

    def crystallize(self, crystal_size: float = 20.0) -> "XAImageList":
        """Applies a crystallization filter to each image in the list. Creates polygon-shaped color blocks by aggregating pixel values.

        :param crystal_size: The radius of the crystals, defaults to 20.0
        :type crystal_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, crystal_size):
            filter = Quartz.CIFilter.filterWithName_("CICrystallize")
            filter.setDefaults()
            filter.setValue_forKey_(crystal_size, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, crystal_size)

    def comic(self) -> "XAImageList":
        """Applies a comic filter to each image in the list. Outlines edges and applies a color halftone effect.

        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image):
            filter = Quartz.CIFilter.filterWithName_("CIComicEffect")
            filter.setDefaults()
            return filter

        return self.__apply_filter(filter_block)

    def pointillize(self, point_size: float = 20.0) -> "XAImageList":
        """Applies a pointillization filter to each image in the list.

        :param crystal_size: The radius of the points, defaults to 20.0
        :type crystal_size: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, point_size):
            filter = Quartz.CIFilter.filterWithName_("CIPointillize")
            filter.setDefaults()
            filter.setValue_forKey_(point_size, "inputRadius")
            return filter

        return self.__apply_filter(filter_block, point_size)

    def bloom(self, intensity: float = 0.5) -> "XAImageList":
        """Applies a bloom effect to each image in the list. Softens edges and adds a glow.

        :param intensity: The strength of the softening and glow effects, defaults to 0.5
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIBloom")
            filter.setDefaults()
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def monochrome(self, color: XAColor, intensity: float = 1.0) -> "XAImageList":
        """Remaps the colors of each image in the list to shades of the specified color.

        :param color: The color of map each images colors to
        :type color: XAColor
        :param intensity: The strength of recoloring effect. Higher values map colors to darker shades of the provided color. Defaults to 1.0
        :type intensity: float
        :return: The resulting images after applying the filter
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        ci_color = Quartz.CIColor.alloc().initWithColor_(color.xa_elem)

        def filter_block(image, intensity):
            filter = Quartz.CIFilter.filterWithName_("CIColorMonochrome")
            filter.setDefaults()
            filter.setValue_forKey_(ci_color, "inputColor")
            filter.setValue_forKey_(intensity, "inputIntensity")
            return filter

        return self.__apply_filter(filter_block, intensity)

    def bump(
        self,
        center: Union[tuple[int, int], None] = None,
        radius: float = 300.0,
        curvature: float = 0.5,
    ) -> "XAImageList":
        """Adds a concave (inward) or convex (outward) bump to each image in the list at the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The radius of the bump in pixels, defaults to 300.0
        :type radius: float
        :param curvature: Controls the direction and intensity of the bump's curvature. Positive values create convex bumps while negative values create concave bumps. Defaults to 0.5
        :type curvature: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        bumped_images = [None] * images.count()

        def bump_image(image, index, center, radius, curvature):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(
                    image.size().width / 2, image.size().height / 2
                )
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CIBumpDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(radius, "inputRadius")
            filter.setValue_forKey_(curvature, "inputScale")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(
                Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2)
            )

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            bumped_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(
                bump_image, [image, index, center, radius, curvature]
            )

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(bumped_images)
        return self

    def pinch(
        self, center: Union[tuple[int, int], None] = None, intensity: float = 0.5
    ) -> "XAImageList":
        """Adds an inward pinch distortion to each image in the list at the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param intensity: Controls the scale of the pinch effect. Higher values stretch pixels away from the specified center to a greater degree. Defaults to 0.5
        :type intensity: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        pinched_images = [None] * images.count()

        def pinch_image(image, index, center, intensity):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(
                    image.size().width / 2, image.size().height / 2
                )
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CIPinchDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(intensity, "inputScale")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(
                Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2)
            )

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            pinched_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(
                pinch_image, [image, index, center, intensity]
            )

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(pinched_images)
        return self

    def twirl(
        self,
        center: Union[tuple[int, int], None] = None,
        radius: float = 300.0,
        angle: float = 3.14,
    ) -> "XAImageList":
        """Adds a twirl distortion to each image in the list by rotating pixels around the specified location within each image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
        :type radius: float
        :param angle: The angle of the twirl in radians, defaults to 3.14
        :type angle: float
        :return: The resulting images after applying the distortion
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        twirled_images = [None] * images.count()

        def twirl_image(image, index, center, radius, angle):
            if center is None:
                center = Quartz.CIVector.vectorWithX_Y_(
                    image.size().width / 2, image.size().height / 2
                )
            else:
                center = Quartz.CIVector.vectorWithX_Y_(center[0], center[1])

            img = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            filter = Quartz.CIFilter.filterWithName_("CITwirlDistortion")
            filter.setDefaults()
            filter.setValue_forKey_(img, "inputImage")
            filter.setValue_forKey_(center, "inputCenter")
            filter.setValue_forKey_(radius, "inputRadius")
            filter.setValue_forKey_(angle, "inputAngle")
            uncropped = filter.valueForKey_(Quartz.kCIOutputImageKey)

            # Crop the result to the original image size
            cropped = uncropped.imageByCroppingToRect_(
                Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2)
            )

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            twirled_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(
                twirl_image, [image, index, center, radius, angle]
            )

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(twirled_images)
        return self

    def auto_enhance(
        self,
        correct_red_eye: bool = False,
        crop_to_features: bool = False,
        correct_rotation: bool = False,
    ) -> "XAImageList":
        """Attempts to enhance each image in the list by applying suggested filters.

        :param correct_red_eye: Whether to attempt red eye removal, defaults to False
        :type correct_red_eye: bool, optional
        :param crop_to_features: Whether to crop the images to focus on their main features, defaults to False
        :type crop_to_features: bool, optional
        :param correct_rotation: Whether attempt perspective correction by rotating the images, defaults to False
        :type correct_rotation: bool, optional
        :return: The list of enhanced images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        enhanced_images = [None] * images.count()

        def enhance_image(image, index):
            ci_image = Quartz.CIImage.imageWithCGImage_(image.CGImage())

            options = {
                Quartz.kCIImageAutoAdjustRedEye: correct_red_eye,
                Quartz.kCIImageAutoAdjustCrop: crop_to_features,
                Quartz.kCIImageAutoAdjustLevel: correct_rotation,
            }

            enhancements = ci_image.autoAdjustmentFiltersWithOptions_(options)
            for filter in enhancements:
                filter.setValue_forKey_(ci_image, "inputImage")
                ci_image = filter.outputImage()

            # Crop the result to the original image size
            cropped = ci_image.imageByCroppingToRect_(
                Quartz.CGRectMake(0, 0, image.size().width * 2, image.size().height * 2)
            )

            # Convert back to NSImage
            rep = AppKit.NSCIImageRep.imageRepWithCIImage_(cropped)
            result = AppKit.NSImage.alloc().initWithSize_(rep.size())
            result.addRepresentation_(rep)
            enhanced_images[index] = result

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(enhance_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(enhanced_images)
        return self

    def flip_horizontally(self) -> "XAImageList":
        """Flips each image in the list horizontally.

        :return: The list of flipped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        flipped_images = [None] * images.count()

        def flip_image(image, index):
            flipped_image = AppKit.NSImage.alloc().initWithSize_(image.size())
            imageBounds = AppKit.NSMakeRect(
                0, 0, image.size().width, image.size().height
            )

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(image.size().width, 0)
            transform.scaleXBy_yBy_(-1, 1)

            flipped_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(
                imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0
            )
            flipped_image.unlockFocus()
            flipped_images[index] = flipped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(flip_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(flipped_images)
        return self

    def flip_vertically(self) -> "XAImageList":
        """Flips each image in the list vertically.

        :return: The list of flipped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()

        flipped_images = [None] * images.count()

        def flip_image(image, index):
            flipped_image = AppKit.NSImage.alloc().initWithSize_(image.size())
            imageBounds = AppKit.NSMakeRect(
                0, 0, image.size().width, image.size().height
            )

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(0, image.size().height)
            transform.scaleXBy_yBy_(1, -1)

            flipped_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(
                imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0
            )
            flipped_image.unlockFocus()
            flipped_images[index] = flipped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(flip_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(flipped_images)
        return self

    def rotate(self, degrees: float) -> "XAImageList":
        """Rotates each image in the list by the specified amount of degrees.

        :param degrees: The number of degrees to rotate the images by
        :type degrees: float
        :return: The list of rotated images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        sinDegrees = abs(math.sin(degrees * math.pi / 180.0))
        cosDegrees = abs(math.cos(degrees * math.pi / 180.0))

        images = self.__partial_init()

        rotated_images = [None] * images.count()

        def rotate_image(image, index):
            new_size = Quartz.CGSizeMake(
                image.size().height * sinDegrees + image.size().width * cosDegrees,
                image.size().width * sinDegrees + image.size().height * cosDegrees,
            )
            rotated_image = AppKit.NSImage.alloc().initWithSize_(new_size)

            imageBounds = Quartz.CGRectMake(
                (new_size.width - image.size().width) / 2,
                (new_size.height - image.size().height) / 2,
                image.size().width,
                image.size().height,
            )

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.translateXBy_yBy_(new_size.width / 2, new_size.height / 2)
            transform.rotateByDegrees_(degrees)
            transform.translateXBy_yBy_(-new_size.width / 2, -new_size.height / 2)

            rotated_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(
                imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0
            )
            rotated_image.unlockFocus()

            rotated_images[index] = rotated_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(rotate_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(rotated_images)
        return self

    def crop(
        self, size: tuple[int, int], corner: Union[tuple[int, int], None] = None
    ) -> "XAImageList":
        """Crops each image in the list to the specified dimensions.

        :param size: The dimensions to crop each image to
        :type size: tuple[int, int]
        :param corner: The bottom-left location to crom each image from, or None to use (0, 0), defaults to None
        :type corner: Union[tuple[int, int], None]
        :return: The list of cropped images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if corner is None:
            # No corner provided -- use (0,0) by default
            corner = (0, 0)

        images = self.__partial_init()

        cropped_images = [None] * images.count()

        def crop_image(image, index):
            cropped_image = AppKit.NSImage.alloc().initWithSize_(
                AppKit.NSMakeSize(size[0], size[1])
            )
            imageBounds = AppKit.NSMakeRect(
                corner[0], corner[1], image.size().width, image.size().height
            )

            cropped_image.lockFocus()
            image.drawInRect_(imageBounds)
            cropped_image.unlockFocus()
            cropped_images[index] = cropped_image

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(crop_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(cropped_images)
        return self

    def scale(
        self, scale_factor_x: float, scale_factor_y: Union[float, None] = None
    ) -> "XAImageList":
        """Scales each image in the list by the specified horizontal and vertical factors.

        :param scale_factor_x: The factor by which to scale each image in the X dimension
        :type scale_factor_x: float
        :param scale_factor_y: The factor by which to scale each image in the Y dimension, or None to match the horizontal factor, defaults to None
        :type scale_factor_y: Union[float, None]
        :return: The list of scaled images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if scale_factor_y is None:
            scale_factor_y = scale_factor_x

        images = self.__partial_init()

        scaled_images = [None] * self.xa_elem.count()

        def scale_image(image, index):
            scaled_image = AppKit.NSImage.alloc().initWithSize_(
                AppKit.NSMakeSize(
                    image.size().width * scale_factor_x,
                    image.size().height * scale_factor_y,
                )
            )
            imageBounds = AppKit.NSMakeRect(
                0, 0, image.size().width, image.size().height
            )

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.scaleXBy_yBy_(scale_factor_x, scale_factor_y)

            scaled_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(
                imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0
            )
            scaled_image.unlockFocus()
            scaled_images[index] = scaled_image

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(scale_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(scaled_images)
        return self

    def resize(self, width: int, height: Union[int, None] = None) -> "XAImageList":
        """Resizes each image in the list to the specified width and height.

        :param width: The width of the resulting images
        :type width: int
        :param height: The height of the resulting images, or None to maintain width:height proportions, defaults to None
        :type height: Union[int, None]
        :return: The list of scaled images
        :rtype: XAImageList

        .. versionadded:: 0.1.1
        """
        images = self.__partial_init()

        scaled_images = [None] * self.xa_elem.count()

        def scale_image(image, index):
            nonlocal height
            img_width = image.size().width
            img_height = image.size().height

            if height is None:
                height = img_height

            scaled_image = AppKit.NSImage.alloc().initWithSize_(
                AppKit.NSMakeSize(
                    img_width * width / img_width, img_height * height / img_height
                )
            )
            imageBounds = AppKit.NSMakeRect(
                0, 0, image.size().width, image.size().height
            )

            transform = AppKit.NSAffineTransform.alloc().init()
            transform.scaleXBy_yBy_(width / img_width, height / img_height)

            scaled_image.lockFocus()
            transform.concat()
            image.drawInRect_fromRect_operation_fraction_(
                imageBounds, Quartz.CGRectZero, AppKit.NSCompositingOperationCopy, 1.0
            )
            scaled_image.unlockFocus()
            scaled_images[index] = scaled_image

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(scale_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(scaled_images)
        return self

    def pad(
        self,
        horizontal_border_width: int = 50,
        vertical_border_width: int = 50,
        pad_color: Union[XAColor, None] = None,
    ) -> "XAImageList":
        """Pads each image in the list with the specified color; add a border around each image in the list with the specified vertical and horizontal width.

        :param horizontal_border_width: The border width, in pixels, in the x-dimension, defaults to 50
        :type horizontal_border_width: int
        :param vertical_border_width: The border width, in pixels, in the y-dimension, defaults to 50
        :type vertical_border_width: int
        :param pad_color: The color of the border, or None for a white border, defaults to None
        :type pad_color: Union[XAColor, None]
        :return: The list of padded images
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if pad_color is None:
            # No color provided -- use white by default
            pad_color = XAColor.white()

        images = self.__partial_init()

        padded_images = [None] * images.count()

        def pad_image(image, index):
            new_width = image.size().width + horizontal_border_width * 2
            new_height = image.size().height + vertical_border_width * 2
            color_swatch = pad_color.make_swatch(new_width, new_height)

            color_swatch.xa_elem.lockFocus()
            bounds = AppKit.NSMakeRect(
                horizontal_border_width,
                vertical_border_width,
                image.size().width,
                image.size().height,
            )
            image.drawInRect_(bounds)
            color_swatch.xa_elem.unlockFocus()
            padded_images[index] = color_swatch.xa_elem

        threads = [None] * images.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(pad_image, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(padded_images)
        return self

    def overlay_image(
        self,
        image: "XAImage",
        location: Union[tuple[int, int], None] = None,
        size: Union[tuple[int, int], None] = None,
    ) -> "XAImageList":
        """Overlays an image on top of each image in the list, at the specified location, with the specified size.

        :param image: The image to overlay on top of each image in the list
        :type image: XAImage
        :param location: The bottom-left point of the overlaid image in the results, or None to use the bottom-left point of each background image, defaults to None
        :type location: Union[tuple[int, int], None]
        :param size: The width and height of the overlaid image, or None to use the overlaid's images existing width and height, or (-1, -1) to use the dimensions of each background images, defaults to None
        :type size: Union[tuple[int, int], None]
        :return: The list of images with the specified image overlaid on top of them
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use the bottom-left point of the background image by default
            location = (0, 0)

        images = self.__partial_init()
        overlayed_images = [None] * images.count()

        def overlay_image(img, index, image, size, location):
            if size is None:
                # No dimensions provided -- use size of overlay image by default
                size = image.size
            elif size == (-1, -1):
                # Use remaining width/height of background image
                size = (img.size().width - location[0], img.size().height - location[1])
            elif size[0] == -1:
                # Use remaining width of background image + provided height
                size = (img.size().width - location[0], size[1])
            elif size[1] == -1:
                # Use remaining height of background image + provided width
                size = (size[1], img.size().width - location[1])

            img.lockFocus()
            bounds = AppKit.NSMakeRect(location[0], location[1], size[0], size[1])
            image.xa_elem.drawInRect_(bounds)
            img.unlockFocus()
            overlayed_images[index] = img

        threads = [None] * images.count()
        for index, img in enumerate(images):
            threads[index] = self._spawn_thread(
                overlay_image, [img, index, image, size, location]
            )

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(overlayed_images)
        return self

    def overlay_text(
        self,
        text: str,
        location: Union[tuple[int, int], None] = None,
        font_size: float = 12,
        font_color: Union[XAColor, None] = None,
    ) -> "XAImageList":
        """Overlays text of the specified size and color at the provided location within each image of the list.

        :param text: The text to overlay onto each image of the list
        :type text: str
        :param location: The bottom-left point of the start of the text, or None to use (5, 5), defaults to None
        :type location: Union[tuple[int, int], None]
        :param font_size: The font size, in pixels, of the text, defaults to 12
        :type font_size: float
        :param font_color: The color of the text, or None to use black, defaults to None
        :type font_color: XAColor
        :return: The list of images with the specified text overlaid on top of them
        :rtype: XAImageList

        .. versionadded:: 0.1.0
        """
        if location is None:
            # No location provided -- use (5, 5) by default
            location = (5, 5)

        if font_color is None:
            # No color provided -- use black by default
            font_color = XAColor.black()

        font = AppKit.NSFont.userFontOfSize_(font_size)
        images = self.__partial_init()
        overlayed_images = [None] * self.xa_elem.count()

        def overlay_text(image, index):
            textRect = Quartz.CGRectMake(
                location[0], 0, image.size().width - location[0], location[1]
            )
            attributes = {
                AppKit.NSFontAttributeName: font,
                AppKit.NSForegroundColorAttributeName: font_color.xa_elem,
            }

            image.lockFocus()
            AppKit.NSString.alloc().initWithString_(text).drawInRect_withAttributes_(
                textRect, attributes
            )
            image.unlockFocus()
            overlayed_images[index] = image

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(overlay_text, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        self.modified = True
        self.xa_elem = AppKit.NSMutableArray.alloc().initWithArray_(overlayed_images)
        return self

    def extract_text(self) -> list[str]:
        """Extracts and returns a list of all visible text in each image of the list.

        :return: The array of extracted text strings
        :rtype: list[str]

        :Example:

        >>> import PyXA
        >>> test = PyXA.XAImage("/Users/ExampleUser/Downloads/Example.jpg")
        >>> print(test.extract_text())
        ["HERE'S TO THE", 'CRAZY ONES', 'the MISFITS the REBELS', 'THE TROUBLEMAKERS', ...]

        .. versionadded:: 0.1.0
        """
        images = self.__partial_init()
        import Vision

        extracted_strings = [None] * self.xa_elem.count()

        def get_text(image, index):
            # Prepare CGImage
            ci_image = Quartz.CIImage.imageWithCGImage_(image.CGImage())
            context = Quartz.CIContext.alloc().initWithOptions_(None)
            img = context.createCGImage_fromRect_(ci_image, ci_image.extent())

            # Handle request completion
            image_strings = []

            def recognize_text_handler(request, error):
                observations = request.results()
                for observation in observations:
                    recognized_strings = observation.topCandidates_(1)[0].string()
                    image_strings.append(recognized_strings)

            # Perform request and return extracted text
            request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(
                recognize_text_handler
            )
            request_handler = (
                Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(img, None)
            )
            request_handler.performRequests_error_([request], None)
            extracted_strings[index] = image_strings

        threads = [None] * self.xa_elem.count()
        for index, image in enumerate(images):
            threads[index] = self._spawn_thread(get_text, [image, index])

        while any([t.is_alive() for t in threads]):
            time.sleep(0.01)

        return extracted_strings

    def show_in_preview(self):
        """Opens each image in the list in Preview.

        .. versionadded:: 0.1.0
        """
        for image in self:
            image.show_in_preview()

    def save(self, file_paths: list[Union[XAPath, str]]):
        """Saves each image to a file on the disk.

        :param file_path: The path at which to save the image file. Any existing file at that location will be overwritten, defaults to None
        :type file_path: Union[XAPath, str, None]

        .. versionadded:: 0.1.0
        """
        for index, image in enumerate(self):
            path = None
            if len(file_paths) > index:
                path = file_paths[index]
            image.save(path)

    def get_clipboard_representation(self) -> list["AppKit.NSImage"]:
        """Gets a clipboard-codable representation of each image in the list.

        When the clipboard content is set to a list of image, the raw data of each image is added to the clipboard. You can then

        :return: A list of media item file URLs
        :rtype: list[NSURL]

        .. versionadded:: 0.0.8
        """
        data = []
        for image in self.__partial_init():
            if image.TIFFRepresentation():
                data.append(image)
        return data


class XAImage(macimg.Image, XAObject, XAClipboardCodable):
    """A wrapper around NSImage with specialized automation methods.

    .. versionadded:: 0.0.2
    """

    def __init__(
        self,
        image_reference: Union[
            str, XAPath, "AppKit.NSURL", "AppKit.NSImage", None
        ] = None,
    ):
        match image_reference:
            case {"element": str(ref)}:
                image_reference = ref

            case {"element": XAImage() as image}:
                image_reference = image._nsimage

            case {"element": AppKit.NSImage() as image}:
                image_reference = image

            case XAPath() as path:
                image_reference = path.path

            case XAURL() as url:
                image_reference = url.url

            case XAObject():
                try:
                    image_reference = image_reference.get_image_representation()
                except AttributeError:
                    raise TypeError(
                        f"{str(type(image_reference))} does not implement the XAImageLike protocol."
                    )

        super().__init__(image_reference)

    @property
    def xa_elem(self):
        return self._nsimage

    def open(
        *images: Union[str, XAPath, list[Union[str, XAPath]]]
    ) -> Union["XAImage", XAImageList]:
        """Initializes one or more images from files.

        :param images: The image(s) to open
        :type images: Union[str, XAPath, list[Union[str, XAPath]]]
        :return: The newly created image object, or a list of image objects
        :rtype: Union[XAImage, XAImageList]

        .. versionadded:: 0.1.0
        """
        if len(images) == 1:
            images = images[0]

        if isinstance(images, list) or isinstance(images, tuple):
            return XAImageList({"element": images})
        else:
            return XAImage(images)

    def horizontal_stitch(images: Union[list["XAImage"], XAImageList]) -> "XAImage":
        """Horizontally stacks two or more images.

        The first image in the list is placed at the left side of the resulting image.

        :param images: The list of images to stitch together
        :type images: Union[list[XAImage], XAImageList]
        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.1
        """
        return macimg.compositions.HorizontalStitch().compose(*images)

    def vertical_stitch(images: Union[list["XAImage"], XAImageList]) -> "XAImage":
        """Vertically stacks two or more images.

        The first image in the list is placed at the bottom of the resulting image.

        :param images: The list of images to stitch together
        :type images: Union[list[XAImage], XAImageList]
        :return: The resulting image after stitching
        :rtype: XAImage

        .. versionadded:: 0.1.1
        """
        return macimg.compositions.VerticalStitch().compose(*images)

    def edges(self, intensity: float = 1.0) -> "XAImage":
        """Detects the edges in the image and highlights them colorfully, blackening other areas of the image.

        :param intensity: The degree to which edges are highlighted. Higher is brighter. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Edges(intensity).apply_to(self)

    def gaussian_blur(self, intensity: float = 10) -> "XAImage":
        """Blurs the image using a Gaussian filter.

        :param intensity: The strength of the blur effect, defaults to 10
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.GaussianBlur(intensity).apply_to(self)

    def reduce_noise(
        self, noise_level: float = 0.02, sharpness: float = 0.4
    ) -> "XAImage":
        """Reduces noise in the image by sharpening areas with a luminance delta below the specified noise level threshold.

        :param noise_level: The threshold for luminance changes in an area below which will be considered noise, defaults to 0.02
        :type noise_level: float
        :param sharpness: The sharpness of the resulting image, defaults to 0.4
        :type sharpness: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.NoiseReduction(noise_level, sharpness).apply_to(self)

    def pixellate(self, pixel_size: float = 8.0) -> "XAImage":
        """Pixellates the image.

        :param pixel_size: The size of the pixels, defaults to 8.0
        :type pixel_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Pixellate(pixel_size).apply_to(self)

    def outline(self, threshold: float = 0.1) -> "XAImage":
        """Outlines detected edges within the image in black, leaving the rest transparent.

        :param threshold: The threshold to use when separating edge and non-edge pixels. Larger values produce thinner edge lines. Defaults to 0.1
        :type threshold: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Outline(threshold).apply_to(self)

    def invert(self) -> "XAImage":
        """Inverts the color of the image.

        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Invert().apply_to(self)

    def sepia(self, intensity: float = 1.0) -> "XAImage":
        """Applies a sepia filter to the image; maps all colors of the image to shades of brown.

        :param intensity: The opacity of the sepia effect. A value of 0 will have no impact on the image. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Sepia(intensity).apply_to(self)

    def vignette(self, intensity: float = 1.0) -> "XAImage":
        """Applies vignette shading to the corners of the image.

        :param intensity: The intensity of the vignette effect, defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Vignette(intensity).apply_to(self)

    def depth_of_field(
        self,
        focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None] = None,
        intensity: float = 10.0,
        focal_region_saturation: float = 1.5,
    ) -> "XAImage":
        """Applies a depth of field filter to the image, simulating a tilt & shift effect.

        :param focal_region: Two points defining a line within the image to focus the effect around (pixels around the line will be in focus), or None to use the center third of the image, defaults to None
        :type focal_region: Union[tuple[tuple[int, int], tuple[int, int]], None]
        :param intensity: Controls the amount of distance around the focal region to keep in focus. Higher values decrease the distance before the out-of-focus effect starts. Defaults to 10.0
        :type intensity: float
        :param focal_region_saturation: Adjusts the saturation of the focial region. Higher values increase saturation. Defaults to 1.5 (1.5x default saturation)
        :type focal_region_saturation: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.DepthOfField(
            focal_region, intensity, focal_region_saturation
        ).apply_to(self)

    def crystallize(self, crystal_size: float = 20.0) -> "XAImage":
        """Applies a crystallization filter to the image. Creates polygon-shaped color blocks by aggregating pixel values.

        :param crystal_size: The radius of the crystals, defaults to 20.0
        :type crystal_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Crystallize(crystal_size).apply_to(self)

    def comic(self) -> "XAImage":
        """Applies a comic filter to the image. Outlines edges and applies a color halftone effect.

        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Comic().apply_to(self)

    def pointillize(self, point_size: float = 20.0) -> "XAImage":
        """Applies a pointillization filter to the image.

        :param crystal_size: The radius of the points, defaults to 20.0
        :type crystal_size: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Pointillize(point_size).apply_to(self)

    def bloom(self, intensity: float = 0.5) -> "XAImage":
        """Applies a bloom effect to the image. Softens edges and adds a glow.

        :param intensity: The strength of the softening and glow effects, defaults to 0.5
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Bloom(intensity).apply_to(self)

    def monochrome(self, color: XAColor, intensity: float = 1.0) -> "XAImage":
        """Remaps the colors of the image to shades of the specified color.

        :param color: The color of map the image's colors to
        :type color: XAColor
        :param intensity: The strength of recoloring effect. Higher values map colors to darker shades of the provided color. Defaults to 1.0
        :type intensity: float
        :return: The resulting image after applying the filter
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.Monochrome(color, intensity).apply_to(self)

    def bump(
        self,
        center: Union[tuple[int, int], None] = None,
        radius: float = 300.0,
        curvature: float = 0.5,
    ) -> "XAImage":
        """Creates a concave (inward) or convex (outward) bump at the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The radius of the bump in pixels, defaults to 300.0
        :type radius: float
        :param curvature: Controls the direction and intensity of the bump's curvature. Positive values create convex bumps while negative values create concave bumps. Defaults to 0.5
        :type curvature: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.distortions.Bump(center, radius, curvature).apply_to(self)

    def pinch(
        self, center: Union[tuple[int, int], None] = None, intensity: float = 0.5
    ) -> "XAImage":
        """Creates an inward pinch distortion at the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param intensity: Controls the scale of the pinch effect. Higher values stretch pixels away from the specified center to a greater degree. Defaults to 0.5
        :type intensity: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.distortions.Pinch(center, intensity).apply_to(self)

    def twirl(
        self,
        center: Union[tuple[int, int], None] = None,
        radius: float = 300.0,
        angle: float = 3.14,
    ) -> "XAImage":
        """Creates a twirl distortion by rotating pixels around the specified location within the image.

        :param center: The center point of the effect, or None to use the center of the image, defaults to None
        :type center: Union[tuple[int, int], None]
        :param radius: The pixel radius around the centerpoint that defines the area to apply the effect to, defaults to 300.0
        :type radius: float
        :param angle: The angle of the twirl in radians, defaults to 3.14
        :type angle: float
        :return: The resulting image after applying the distortion
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.distortions.Twirl(center, radius, angle).apply_to(self)

    def auto_enhance(
        self,
        correct_red_eye: bool = False,
        crop_to_features: bool = False,
        correct_rotation: bool = False,
    ) -> "XAImage":
        """Attempts to enhance the image by applying suggested filters.

        :param correct_red_eye: Whether to attempt red eye removal, defaults to False
        :type correct_red_eye: bool, optional
        :param crop_to_features: Whether to crop the image to focus on the main features with it, defaults to False
        :type crop_to_features: bool, optional
        :param correct_rotation: Whether attempt perspective correction by rotating the image, defaults to False
        :type correct_rotation: bool, optional
        :return: The resulting image after applying the enchantments
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.filters.AutoEnhance(
            correct_red_eye, crop_to_features, correct_rotation
        ).apply_to(self)

    def flip_horizontally(self) -> "XAImage":
        """Flips the image horizontally.

        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.transforms.Flip("horizontal").apply_to(self)

    def flip_vertically(self) -> "XAImage":
        """Flips the image vertically.

        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.transforms.Flip("vertical").apply_to(self)

    def rotate(self, degrees: float) -> "XAImage":
        """Rotates the image clockwise by the specified number of degrees.

        :param degrees: The number of degrees to rotate the image by
        :type degrees: float
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.transforms.Rotate(degrees).apply_to(self)

    def crop(
        self, size: tuple[int, int], corner: tuple[int, int] = (0, 0)
    ) -> "XAImage":
        """Crops the image to the specified dimensions.

        :param size: The width and height of the resulting image
        :type size: tuple[int, int]
        :param corner: The bottom-left corner location from which to crop the image, defaults to (0, 0)
        :type corner: tuple[int, int], optional
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.transforms.Crop(size, corner).apply_to(self)

    def scale(
        self, scale_factor_x: float, scale_factor_y: Union[float, None] = None
    ) -> "XAImage":
        """Scales the image by the specified horizontal and vertical factors.

        :param scale_factor_x: The factor by which to scale the image in the X dimension
        :type scale_factor_x: float
        :param scale_factor_y: The factor by which to scale the image in the Y dimension, or None to match the horizontal factor, defaults to None
        :type scale_factor_y: Union[float, None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.0
        """
        return macimg.transforms.Scale(scale_factor_x, scale_factor_y).apply_to(self)

    def resize(self, width: int, height: Union[int, None] = None) -> "XAImage":
        """Resizes the image to the specified width and height.

        :param width: The width of the resulting image, in pixels
        :type width: int
        :param height: The height of the resulting image, in pixels, or None to maintain width:height proportions, defaults to None
        :type height: Union[int, None]
        :return: The image object, modifications included
        :rtype: XAImage

        .. versionadded:: 0.1.1
        """
        return macimg.transforms.Resize(width, height).apply_to(self)

    def save(self, file_path: Union[XAPath, str, None] = None):
        """Saves the image to a file on the disk. Saves to the original file (if there was one) by default.

        :param file_path: The path at which to save the image file. Any existing file at that location will be overwritten, defaults to None
        :type file_path: Union[XAPath, str, None]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, XAPath):
            file_path = file_path.path
        super().save(file_path)

    def get_clipboard_representation(self) -> "AppKit.NSImage":
        """Gets a clipboard-codable representation of the iimage.

        When the clipboard content is set to an image, the image itself, including any modifications, is added to the clipboard. Pasting will then insert the image into the active document.

        :return: The raw NSImage object for this XAIMage
        :rtype: AppKit.NSImage

        .. versionadded:: 0.1.0
        """
        return self._nsimage

    def __eq__(self, other):
        return (
            isinstance(other, XAImage)
            and self._nsimage.TIFFRepresentation()
            == other._nsimage.TIFFRepresentation()
        )


class XASoundList(XAList, XAClipboardCodable):
    """A wrapper around lists of sounds that employs fast enumeration techniques.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASound, filter)

    def file(self) -> list[XAPath]:
        return [sound.file for sound in self]

    def num_sample_frames(self) -> list[int]:
        return [sound.num_sample_frames for sound in self]

    def sample_rate(self) -> list[float]:
        return [sound.sample_rate for sound in self]

    def duration(self) -> list[float]:
        return [sound.duration for sound in self]

    def play(self) -> "XASoundList":
        """Plays all sounds in the list simultaneously.

        :return: The list of sounds.
        :rtype: XASoundList

        .. versionadded:: 0.1.2
        """
        for sound in self:
            sound.play()
        return self

    def pause(self) -> "XASoundList":
        """Pauses playback of all sounds in the list.

        :return: The list of sounds.
        :rtype: XASoundList

        .. versionadded:: 0.1.2
        """
        for sound in self:
            sound.pause()
        return self

    def resume(self) -> "XASoundList":
        """Resumes playback of all sounds in the list.

        :return: The list of sounds.
        :rtype: XASoundList

        .. versionadded:: 0.1.2
        """
        for sound in self:
            sound.resume()
        return self

    def stop(self) -> "XASoundList":
        """Stops playback of all sounds in the list.

        :return: The list of sounds.
        :rtype: XASoundList

        .. versionadded:: 0.1.2
        """
        for sound in self:
            sound.stop()
        return self

    def trim(self, start_time: float, end_time: float) -> "XASoundList":
        """Trims each sound in the list to the specified start and end time, in seconds.

        :param start_time: The start time in seconds
        :type start_time: float
        :param end_time: The end time in seconds
        :type end_time: float
        :return: The list of updated sounds
        :rtype: XASoundList

        .. versionadded:: 0.1.2
        """
        return self._new_element(
            [sound.trim(start_time, end_time) for sound in self], XASoundList
        )

    def get_clipboard_representation(
        self,
    ) -> list[Union["AppKit.NSSound", "AppKit.NSURL", str]]:
        """Gets a clipboard-codable representation of each sound in the list.

        When the clipboard content is set to a list of sounds, each sound's raw sound data, its associated file URL, and its file path string are added to the clipboard.

        :return: The clipboard-codable form of the sound
        :rtype: Any

        .. versionadded:: 0.1.0
        """
        return [self.xa_elem, self.file(), [x.path() for x in self.file()]]


class XASound(XAObject, XAClipboardCodable):
    """A class for playing and interacting with audio files and data.

    .. versionadded:: 0.0.1
    """

    def __init__(self, sound_reference: Union[str, XAURL, XAPath]):
        self.file = None

        match sound_reference:
            case str() as ref if "://" in ref:
                self.file = XAURL(ref)

            case str() as ref if os.path.exists(ref):
                self.file = XAPath(sound_reference)

            case str() as ref:
                self.file = XAPath("/System/Library/Sounds/" + ref + ".aiff")

            case {"element": str() as ref}:
                self.file = XASound(ref).file

            case {"element": XASound() as ref}:
                self.file = ref.file

            case XAPath() as ref:
                self.file = ref

            case XAURL() as ref:
                self.file = ref

            case XASound() as sound:
                self.file = sound.file

        self.duration: float  #: The duration of the sound in seconds

        import AVFoundation

        self.__audio_file = AVFoundation.AVAudioFile.alloc().initForReading_error_(
            self.file.xa_elem if self.file is not None else None, None
        )[0]

        self.__audio_engine = AVFoundation.AVAudioEngine.alloc().init()
        self.__player_node = AVFoundation.AVAudioPlayerNode.alloc().init()
        self.__audio_engine.attachNode_(self.__player_node)

        self.__audio_engine.connect_to_format_(
            self.__player_node,
            self.__audio_engine.mainMixerNode(),
            self.__audio_file.processingFormat(),
        )

        self.__player_node.stop()
        self.__audio_engine.stop()

        self.xa_elem = self.__audio_file

    @property
    def num_sample_frames(self) -> int:
        """The number of sample frames in the audio file.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.length()

    @property
    def sample_rate(self) -> float:
        """The sample rate for the sound format, in hertz.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.processingFormat().sampleRate()

    @property
    def duration(self) -> float:
        """The duration of the sound in seconds.

        .. versionadded:: 0.1.0
        """
        return self.num_sample_frames / self.sample_rate

    def open(
        *sound_references: Union[str, XAPath, list[Union[str, XAPath]]]
    ) -> Union["XASound", XASoundList]:
        """Initializes one or more sounds from files.

        :param sound_references: The sound(s) to open
        :type sound_references: Union[str, XAPath, list[Union[str, XAPath]]]
        :return: The newly created sound object, or a list of sound objects
        :rtype: Union[XASound, XASoundList]

        .. versionadded:: 0.1.0
        """
        if len(sound_references) == 1:
            sound_references = sound_references[0]

        if isinstance(sound_references, list) or isinstance(sound_references, tuple):
            return XASoundList({"element": sound_references})
        else:
            return XASound(sound_references)

    def beep(self):
        """Plays the system Beep sound.

        .. versionadded:: 0.1.0
        """
        AppleScript(
            """
            beep
            delay 0.5
        """
        ).run()

    def play(self, new_thread = False) -> "XASound":
        """Plays the sound from the beginning.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :param new_thread: Whether to play the sound in a new thread, defaults to False
        :type new_thread: bool, optional
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> import time
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.play()
        >>> time.sleep(glass_sound.duration)

        .. seealso:: :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """

        def play_sound(self):
            self.__player_node.scheduleFile_atTime_completionHandler_(
                self.xa_elem, None, None
            )
            self.__audio_engine.startAndReturnError_(None)
            self.__player_node.play()
            start_date = AppKit.NSDate.date()
            while AppKit.NSDate.date().timeIntervalSinceDate_(start_date) < self.duration:
                AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                    datetime.now() + timedelta(seconds=0.1)
                )

        if new_thread:
            self._spawn_thread(play_sound, [self])
        else:
            play_sound(self)
        return self

    def pause(self) -> "XASound":
        """Pauses the sound.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.pause()

        .. seealso:: :func:`resume`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.__player_node.pause()
        return self

    def resume(self) -> "XASound":
        """Plays the sound starting from the time it was last paused at.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.resume()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """

        def play_sound(self):
            self.__player_node.scheduleFile_atTime_completionHandler_(
                self.xa_elem, None, None
            )
            self.__audio_engine.startAndReturnError_(None)
            self.__player_node.play()
            while self.__player_node.isPlaying():
                AppKit.NSRunLoop.currentRunLoop().runUntilDate_(
                    datetime.now() + timedelta(seconds=0.1)
                )

        self._spawn_thread(play_sound, [self])
        return self

    def stop(self) -> "XASound":
        """Stops playback of the sound and rewinds it to the beginning.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.stop()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        self.__audio_engine.stop()
        return self

    def set_volume(self, volume: float) -> "XASound":
        """Sets the volume of the sound.

        :param volume: The desired volume of the sound in the range [0.0, 1.0].
        :type volume: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.set_volume(1.0)

        .. seealso:: :func:`volume`

        .. versionadded:: 0.0.1
        """
        self.__audio_engine.mainMixerNode().setOutputVolume_(volume)
        return self

    def volume(self) -> float:
        """Returns the current volume of the sound.

        :return: The volume level of the sound.
        :rtype: int

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> print(glass_sound.volume())
        1.0

        .. seealso:: :func:`set_volume`

        .. versionadded:: 0.0.1
        """
        return self.__audio_engine.mainMixerNode().volume()

    def loop(self, times: int) -> "XASound":
        """Plays the sound the specified number of times.

        Audio playback runs in a separate thread. For the sound the play properly, you must keep the main thread alive over the duration of the desired playback.

        :param times: The number of times to loop the sound.
        :type times: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> import time
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.loop(10)
        >>> time.sleep(glass_sound.duration * 10)

        .. versionadded:: 0.0.1
        """

        def play_sound():
            num_plays = 0
            while num_plays < times:
                sound = XASound(self.file)
                sound.play()
                num_plays += 1
                time.sleep(self.duration)

        self._spawn_thread(play_sound)
        return self

    def trim(self, start_time: float, end_time: float) -> "XASound":
        """Trims the sound to the specified start and end time, in seconds.

        This will create a momentary sound data file in the current working directory for storing the intermediary trimmed sound data.

        :param start_time: The start time in seconds
        :type start_time: float
        :param end_time: The end time in seconds
        :type end_time: float
        :return: The updated sound object
        :rtype: XASound

        .. versionadded:: 0.1.0
        """
        # Clear the temp data path
        file_path = "sound_data_tmp.m4a"
        if os.path.exists(file_path):
            AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(
                file_path, None
            )

        # Configure the export session
        import AVFoundation

        asset = AVFoundation.AVAsset.assetWithURL_(self.file.xa_elem)
        export_session = (
            AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(
                asset, AVFoundation.AVAssetExportPresetAppleM4A
            )
        )

        import CoreMedia

        start_time = CoreMedia.CMTimeMake(start_time * 100, 100)
        end_time = CoreMedia.CMTimeMake(end_time * 100, 100)
        time_range = CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time)

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(XAPath(file_path).xa_elem)
        export_session.setOutputFileType_(AVFoundation.AVFileTypeAppleM4A)

        # Export to file path
        waiting = False

        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)

        while not waiting:
            time.sleep(0.01)

        # Load the sound file back into active memory
        self.__audio_file = AVFoundation.AVAudioFile.alloc().initForReading_error_(
            XAPath(file_path).xa_elem, None
        )[0]
        self.xa_elem = self.__audio_file
        AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(file_path, None)
        return self

    def save(self, file_path: Union[XAPath, str]):
        """Saves the sound to the specified file path.

        :param file_path: The path to save the sound to
        :type file_path: Union[XAPath, str]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        # Configure the export session
        import AVFoundation

        asset = AVFoundation.AVAsset.assetWithURL_(self.file.xa_elem)
        export_session = (
            AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(
                asset, AVFoundation.AVAssetExportPresetAppleM4A
            )
        )

        import CoreMedia

        start_time = CoreMedia.CMTimeMake(0, 100)
        end_time = CoreMedia.CMTimeMake(self.duration * 100, 100)
        time_range = CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time)

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(file_path.xa_elem)
        # export_session.setOutputFileType_(AVFoundation.AVFileTypeAppleM4A)

        # Export to file path
        waiting = False

        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)

        while not waiting:
            time.sleep(0.01)

    def get_clipboard_representation(
        self,
    ) -> list[Union["AppKit.NSSound", "AppKit.NSURL", str]]:
        """Gets a clipboard-codable representation of the sound.

        When the clipboard content is set to a sound, the raw sound data, the associated file URL, and the path string of the file are added to the clipboard.

        :return: The clipboard-codable form of the sound
        :rtype: Any

        .. versionadded:: 0.0.8
        """
        return [self.xa_elem, self.file.xa_elem, self.file.xa_elem.path()]


class XAVideo(XAObject):
    """A class for interacting with video files and data.

    .. versionadded:: 0.1.0
    """

    def __init__(self, video_reference: Union[str, XAURL, XAPath]):
        if isinstance(video_reference, str):
            # References is to some kind of path or URL
            if "://" in video_reference:
                video_reference = XAURL(video_reference)
            else:
                video_reference = XAPath(video_reference)

        import AVFoundation

        self.xa_elem = AVFoundation.AVURLAsset.alloc().initWithURL_options_(
            video_reference.xa_elem,
            {AVFoundation.AVURLAssetPreferPreciseDurationAndTimingKey: True},
        )

    def reverse(self, output_file: Union[XAPath, str]):
        """Reverses the video and exports the result to the specified output file path.

        :param output_file: The file to export the reversed video to
        :type output_file: Union[XAPath, str]

        .. versionadded:: 0.1.0
        """
        if isinstance(output_file, str):
            output_file = XAPath(output_file)
        output_url = output_file.xa_elem

        import AVFoundation

        reader = AVFoundation.AVAssetReader.alloc().initWithAsset_error_(
            self.xa_elem, None
        )[0]

        video_track = self.xa_elem.tracksWithMediaType_(AVFoundation.AVMediaTypeVideo)[
            -1
        ]

        reader_output = AVFoundation.AVAssetReaderTrackOutput.alloc().initWithTrack_outputSettings_(
            video_track,
            {
                Quartz.CoreVideo.kCVPixelBufferPixelFormatTypeKey: Quartz.CoreVideo.kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange
            },
        )

        reader.addOutput_(reader_output)
        reader.startReading()

        samples = []
        while sample := reader_output.copyNextSampleBuffer():
            samples.append(sample)

        writer = AVFoundation.AVAssetWriter.alloc().initWithURL_fileType_error_(
            output_url, AVFoundation.AVFileTypeMPEG4, None
        )[0]

        writer_settings = {
            AVFoundation.AVVideoCodecKey: AVFoundation.AVVideoCodecTypeH264,
            AVFoundation.AVVideoWidthKey: video_track.naturalSize().width,
            AVFoundation.AVVideoHeightKey: video_track.naturalSize().height,
            AVFoundation.AVVideoCompressionPropertiesKey: {
                AVFoundation.AVVideoAverageBitRateKey: video_track.estimatedDataRate()
            },
        }

        format_hint = video_track.formatDescriptions()[-1]
        writer_input = AVFoundation.AVAssetWriterInput.alloc().initWithMediaType_outputSettings_sourceFormatHint_(
            AVFoundation.AVMediaTypeVideo, writer_settings, format_hint
        )

        writer_input.setExpectsMediaDataInRealTime_(False)

        import CoreMedia

        pixel_buffer_adaptor = AVFoundation.AVAssetWriterInputPixelBufferAdaptor.alloc().initWithAssetWriterInput_sourcePixelBufferAttributes_(
            writer_input, None
        )
        writer.addInput_(writer_input)
        writer.startWriting()
        writer.startSessionAtSourceTime_(
            CoreMedia.CMSampleBufferGetPresentationTimeStamp(samples[0])
        )

        for index, sample in enumerate(samples):
            presentation_time = CoreMedia.CMSampleBufferGetPresentationTimeStamp(sample)

            image_buffer_ref = CoreMedia.CMSampleBufferGetImageBuffer(
                samples[len(samples) - index - 1]
            )
            if image_buffer_ref is not None:
                pixel_buffer_adaptor.appendPixelBuffer_withPresentationTime_(
                    image_buffer_ref, presentation_time
                )

            while not writer_input.isReadyForMoreMediaData():
                time.sleep(0.1)

        self._spawn_thread(writer.finishWriting)
        return AVFoundation.AVAsset.assetWithURL_(output_url)

    def show_in_quicktime(self):
        """Shows the video in QuickTime Player.

        This will create a momentary video data file in the current working directory to store intermediary video data.

        .. versionadded:: 0.1.0
        """
        global workspace
        if workspace is None:
            workspace = AppKit.NSWorkspace.sharedWorkspace()

        self.save("video-data-tmp.mp4")

        video_url = XAPath(os.getcwd() + "/video-data-tmp.mp4").xa_elem
        quicktime_url = XAPath("/System/Applications/QuickTime Player.app").xa_elem
        workspace.openURLs_withApplicationAtURL_configuration_completionHandler_(
            [video_url], quicktime_url, None, None
        )
        time.sleep(1)

        AppKit.NSFileManager.defaultManager().removeItemAtPath_error_(
            video_url.path(), None
        )

    def save(self, file_path: Union[XAPath, str]):
        """Saves the video at the specified file path.

        :param file_path: The path to save the video at
        :type file_path: Union[XAPath, str]

        .. versionadded:: 0.1.0
        """
        if isinstance(file_path, str):
            file_path = XAPath(file_path)

        # Configure the export session
        import AVFoundation

        export_session = (
            AVFoundation.AVAssetExportSession.exportSessionWithAsset_presetName_(
                self.xa_elem, AVFoundation.AVAssetExportPresetHighestQuality
            )
        )

        import CoreMedia

        start_time = CoreMedia.CMTimeMake(0, 100)
        end_time = CoreMedia.CMTimeMake(
            self.xa_elem.duration().value * self.xa_elem.duration().timescale, 100
        )
        time_range = CoreMedia.CMTimeRangeFromTimeToTime(start_time, end_time)

        export_session.setTimeRange_(time_range)
        export_session.setOutputURL_(file_path.xa_elem)

        # Export to file path
        waiting = False

        def handler():
            nonlocal waiting
            waiting = True

        export_session.exportAsynchronouslyWithCompletionHandler_(handler)

        while not waiting:
            time.sleep(0.01)
