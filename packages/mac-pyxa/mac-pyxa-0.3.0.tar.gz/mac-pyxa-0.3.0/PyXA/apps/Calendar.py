from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Generator, Union

import EventKit
import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath


class XACalendarApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with scripting elements of the macOS Calendar application.

    .. seealso:: Classes :class:`XACalendarCalendar`, :class:`XACalendarEvent`

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """The object types that can be created using :func:`make`."""

        DOCUMENT = "document"  #: A document
        CALENDAR = "calendar"  #: A calendar
        EVENT = "event"  #: An event
        DISPLAY_ALARM = "display_alarm"  #: A display alarm
        MAIL_ALARM = "mail_alarm"  #: A mail alarm
        SOUND_ALARM = "sound_alarm"  #: A sound alarm
        OPEN_FILE_ALARM = "open_file_alarm"  #: An open file alarm

    class ParticipationStatus(Enum):
        """Event participation statuses."""

        UNKNOWN = XABase.OSType("E6na")  #: No answer yet
        ACCEPTED = XABase.OSType("E6ap")  #: Invitation has been accepted
        DECLINED = XABase.OSType("E6dp")  #: Invitation has been declined
        TENTATIVE = XABase.OSType("E6tp")  #: Invitation has been tentatively accepted

    class EventStatus(Enum):
        """Event confirmation statuses."""

        CANCELLED = XABase.OSType("E4ca")  #: A cancelled event
        CONFIRMED = XABase.OSType("E4cn")  #: A confirmed event
        NONE = XABase.OSType("E4no")  #: An event without a status
        TENTATIVE = XABase.OSType("E4te")  #: A tentative event

    class Priority(Enum):
        """Event priorities."""

        NONE = XABase.OSType("tdp0")  #: No priority assigned
        LOW = XABase.OSType("tdp9")  #: Low priority
        MEDIUM = XABase.OSType("tdp5")  #: Medium priority
        HIGH = XABase.OSType("tdp1")  #: High priority

    class ViewType(Enum):
        """Views in Calendar.app."""

        DAY = XABase.OSType("E5da")  #: The iCal day view
        WEEK = XABase.OSType("E5we")  #: The iCal week view
        MONTH = XABase.OSType("E5mo")  #: The iCal month view
        YEAR = XABase.OSType("E5ye")  #: The iCal year view

    def __init__(self, properties: dict):
        super().__init__(properties)
        self.xa_wcls = XACalendarWindow

    @property
    def properties(self) -> dict:
        """All properties of the application."""
        return dict(self.xa_scel.properties())

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Calendar is the frontmost application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version of the Calendar application."""
        return self.xa_scel.version()

    @property
    def default_calendar(self) -> "XACalendarCalendar":
        """The calendar that events are added to by default."""
        calendar_obj = self.xa_estr.defaultCalendarForNewEvents()
        return self.calendars().by_name(calendar_obj.title())

    def reload_calendars(self) -> "XACalendarApplication":
        """Reloads the contents of all calendars.

        :return: The application object
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.reloadCalendars()
        return self

    def switch_view_to(
        self, view: "XACalendarApplication.ViewType"
    ) -> "XACalendarApplication":
        """Switches to the target calendar view.

        :param view: The view to switch to.
        :type view: XACalendarApplication.ViewType
        :return: The application object
        :rtype: XACalendarApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> app.switch_view_to(app.ViewType.WEEK)
        >>> app.switch_view_to(app.ViewType.DAY)
        >>> app.switch_view_to(app.ViewType.MONTH)
        >>> app.switch_view_to(app.ViewType.YEAR)

        .. versionadded:: 0.0.1
        """
        if view == XACalendarApplication.ViewType.YEAR:
            self.xa_estr.showDateInCalendar_inView_(0, 3)
        else:
            self.xa_scel.switchViewTo_(view.value)
        return self

    def view_calendar_at(
        self, date: datetime, view: Union[None, "XACalendarApplication.ViewType"] = None
    ) -> "XACalendarApplication":
        """Displays the calendar at the provided date.

        :param date: The date to display.
        :type date: datetime
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        :Example:

        >>> import PyXA
        >>> from datetime import date
        >>> app = PyXA.Application("Calendar")
        >>> date1 = date(2022, 7, 20)
        >>> app.view_calendar_at(date1)

        .. versionadded:: 0.0.1
        """
        if view is None:
            self.xa_estr.showDateInCalendar_inView_(date, 1)
        elif view == XACalendarApplication.ViewType.YEAR:
            self.xa_estr.showDateInCalendar_inView_(date, 3)
        else:
            self.xa_estr.showDateInCalendar_inView_(date, 0)
            self.xa_scel.switchViewTo_(view.value)
        return self

    def subscribe_to(self, url: str) -> "XACalendarCalendar":
        """Subscribes to the calendar at the specified URL.

        :param url: The URL of the calendar (in iCal format) to subscribe to
        :type url: str
        :return: The newly created calendar object
        :rtype: XACalendarCalendar

        .. versionadded:: 0.0.1
        """
        self.xa_scel.GetURL_(url)
        return self.calendars()[-1]

    def documents(self, filter: Union[dict, None] = None) -> "XACalendarDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XARemindersDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.documents(), XACalendarDocumentList, filter
        )

    def calendars(self, filter: Union[dict, None] = None) -> "XACalendarCalendarList":
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned calendars will have, or None
        :type filter: Union[dict, None]
        :return: The list of calendars
        :rtype: XACalendarCalendarList

        :Example 1: Get all calendars

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> print(app.calendars())
        <<class 'PyXA.apps.Calendar.XACalendarCalendarList'>['Calendar', 'Calendar2', 'Calendar3', ...]>

        :Example 2: Get calendars using a filter

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> print(app.calendars({"name": "Calendar"})[0])
        <<class 'PyXA.apps.Calendar.XACalendarCalendar'>Calendar>

        :Example 3: Get calendars using list methods

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> print(app.calendars().by_name("Calendar"))
        <<class 'PyXA.apps.Calendar.XACalendarCalendar'>Calendar>

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.calendars(), XACalendarCalendarList, filter
        )

    def new_calendar(self, name: str = "New Calendar") -> "XACalendarCalendar":
        """Creates a new calendar with the given name.

        :param name: The name of the calendar, defaults to "New Calendar"
        :type name: str, optional
        :return: The newly created calendar object
        :rtype: XACalendarCalendar

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> app.new_calendar("PyXA Development")

        .. versionadded:: 0.0.1
        """
        new_calendar = self.make("calendar", {"name": name})
        self.calendars().push(new_calendar)
        return self.calendars()[self.calendars().index(new_calendar)]

    def new_event(
        self,
        summary: str,
        start_date: datetime,
        end_date: datetime,
        calendar: Union["XACalendarCalendar", None] = None,
    ) -> "XACalendarEvent":
        """Creates a new event with the given name and start/end dates in the specified calendar. If no calendar is specified, the default calendar is used.

        :param name: The name of the event
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example: Create event on the default calendar

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> app.new_event("Learn about PyXA", start_date, end_date)

        :Example: Create event on a specific calendar

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> calendar = app.calendars()[-1]
        >>> app.new_event("Learn about PyXA", start_date, end_date, calendar)

        .. versionadded:: 0.0.1
        """
        if calendar is None:
            calendar = self.default_calendar
        new_event = self.make(
            "event", {"summary": summary, "startDate": start_date, "endDate": end_date}
        )
        calendar.events().push(new_event)
        return calendar.events().by_uid(new_event.uid)

    def make(
        self,
        specifier: Union[str, "XACalendarApplication.ObjectType"],
        properties: dict = None,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XACalendarApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new calendar

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> new_calendar = app.make("calendar", {"name": "PyXA Development"})
        >>> app.calendars().push(new_calendar)

        :Example 2: Make a new event

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.make("event", {"summary": "Work on PyXA", "startDate": start_date, "endDate": end_date})
        >>> app.default_calendar.events().push(new_event)

        .. versionadded:: 0.0.6
        """
        if isinstance(specifier, XACalendarApplication.ObjectType):
            specifier = specifier.value

        if data is None:
            camelized_properties = {}

            if properties is None:
                properties = {}

            if specifier == "workflow":
                if "path" not in properties and "name" in properties:
                    fm = AppKit.NSFileManager.defaultManager()
                    properties.update(
                        {
                            "path": f"{fm.homeDirectoryForCurrentUser().path()}/Downloads/{properties.get('name')}.workflow"
                        }
                    )
                elif not properties.get("path").endswith(".workflow"):
                    properties.update({"path": properties.get("path") + ".workflow"})

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
            return self._new_element(obj, XACalendarDocument)
        elif specifier == "calendar":
            return self._new_element(obj, XACalendarCalendar)
        elif specifier == "event":
            return self._new_element(obj, XACalendarEvent)
        elif specifier == "display_alarm":
            return self._new_element(obj, XACalendarDisplayAlarm)
        elif specifier == "mail_alarm":
            return self._new_element(obj, XACalendarMailAlarm)
        elif specifier == "sound_alarm":
            return self._new_element(obj, XACalendarSoundAlarm)
        elif specifier == "open_file_alarm":
            return self._new_element(obj, XACalendarOpenFileAlarm)


class XACalendarWindow(XABaseScriptable.XASBWindow):
    """A window of Calendar.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the window."""
        return dict(self.xa_elem.properties())

    @property
    def document(self) -> "XACalendarDocument":
        """The current document displayed in the window."""
        return self._new_element(self.xa_elem.document(), XACalendarDocument)


class XACalendarDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarDocument, filter)

    def properties(self) -> list[dict]:
        ls = self.xa_elem.arrayByApplyingSelector_("properties") or []
        return [dict(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAPath(x) for x in ls]

    def by_properties(self, properties: dict) -> Union["XACalendarDocument", None]:
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union["XACalendarDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XACalendarDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAPath) -> Union["XACalendarDocument", None]:
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XACalendarDocument(XABase.XAObject):
    """A document in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document."""
        return dict(self.xa_elem.properties())

    @property
    def name(self) -> str:
        """The name of the document."""
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since it was last saved."""
        return self.xa_elem.modified()

    @property
    def file(self) -> XABase.XAPath:
        """The location of the document on disk, if it has one."""
        return XABase.XAPath(self.xa_elem.file())


class XACalendarCalendarList(XABase.XAList):
    """A wrapper around lists of calendars that employs fast enumeration techniques.

    All properties of calendars can be called as methods on the wrapped list, returning a list containing each calendar's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarCalendar, filter)

    def properties(self) -> list[dict]:
        properties_list = []
        for calendar in self.xa_elem:
            properties_list.append(
                {
                    "name": calendar.name(),
                    "color": XABase.XAColor(calendar.color()),
                    "writable": calendar.writable(),
                    "description": calendar.description(),
                }
            )
        return properties_list

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("color") or []
        return [XABase.XAColor(x) for x in ls]

    # ! BROKEN -- This seems to be a problem with Calendar.app
    # def calendar_identifier(self) -> list[str]:
    # return [calendar.get().calendarIdentifier() for calendar in self.xa_elem]

    def writable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("writable") or [])

    def description(self) -> list[str]:
        return [x.description() for x in self.xa_elem]

    def events(self) -> "XACalendarEventList":
        ls = self.xa_elem.arrayByApplyingSelector_("events") or []
        return self._new_element(ls, XACalendarEventList)

    def by_properties(self, properties: dict) -> Union["XACalendarCalendar", None]:
        for calendar in self.xa_elem:
            name = calendar.name()
            color = calendar.color()
            writable = calendar.writable()
            description = calendar.description()

            if (
                name == properties["name"]
                and color == properties["color"].xa_elem
                and writable == properties["writable"]
                and description[25:] == properties["description"][25:]
            ):
                return self._new_element(calendar, XACalendarCalendar)

    def by_name(self, name: str) -> Union["XACalendarCalendar", None]:
        return self.by_property("name", name)

    def by_color(self, color: XABase.XAColor) -> Union["XACalendarCalendar", None]:
        for calendar in self.xa_elem:
            if calendar.color() == color.xa_elem:
                return self._new_element(calendar, XACalendarCalendar)

    # ! BROKEN -- This seems to be a problem with Calendar.app
    # def by_calendar_identifier(self, calendar_identifier: str) -> Union['XACalendarCalendar', None]:
    #     return self.by_property("calendarIdentifier", calendar_identifier)

    def by_writable(self, writable: bool) -> Union["XACalendarCalendar", None]:
        return self.by_property("writable", writable)

    def by_description(self, description: str) -> Union["XACalendarCalendar", None]:
        for calendar in self.xa_elem:
            if calendar.description()[25:] == description[25:]:
                return self._new_element(calendar, XACalendarCalendar)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XACalendarCalendar(XABase.XAObject):
    """A calendar in Calendar.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties: dict):
        super().__init__(properties)
        self.__calendar_obj = None

    @property
    def calendar_obj(self) -> EventKit.EKCalendar:
        if self.__calendar_obj is None and hasattr(self.xa_elem, "name"):
            calendars = self.xa_estr.calendars()
            predicate = XABase.XAPredicate()
            predicate.add_eq_condition("title", self.name)
            self.__calendar_obj = predicate.evaluate(calendars)[0]
        return self.__calendar_obj

    @property
    def properties(self) -> dict:
        """All properties of the calendar."""
        return {
            "name": self.xa_elem.name(),
            "color": XABase.XAColor(self.xa_elem.color()),
            "writable": self.xa_elem.writable(),
            "description": self.xa_elem.description(),
        }

    @property
    def name(self) -> str:
        """The name of the calendar."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def color(self) -> XABase.XAColor:
        """The color of the calendar."""
        return XABase.XAColor(self.xa_elem.color())

    @color.setter
    def color(self, color: XABase.XAColor):
        self.set_property("color", color.xa_elem)

    # ! BROKEN -- This seems to be a problem with Calendar.app
    # @property
    # def calendar_identifier(self) -> str:
    #     """The unique identifier for the calendar.
    #     """
    #     return self.xa_elem.id()

    @property
    def writable(self) -> bool:
        """Whether the calendar is writable."""
        return self.xa_elem.writable()

    @property
    def description(self) -> str:
        """The description of the calendar."""
        return self.xa_elem.description()

    @description.setter
    def description(self, description: str):
        self.set_property("description", description)

    def delete(self) -> "XACalendarEvent":
        """Deletes the calendar.

        .. versionadded:: 0.0.2
        """
        # self.calendar_obj.delete()
        # print(self.xa_elem.lastError())
        self.xa_estr.removeCalendar_commit_error_(self.calendar_obj, True, None)

    def events_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> "XACalendarEventList":
        """Gets a list of events occurring between the specified start and end datetimes.

        :param start_date: The earliest date an event in the list should begin.
        :type start_date: datetime
        :param end_date: The latest date an event in the list should end.
        :type end_date: datetime
        :return: The list of events.
        :rtype: XACalendarEventList

        :Example:

        >>> from datetime import date
        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> calendar = app.default_calendar
        >>> start_date = date(2022, 6, 4)
        >>> end_date = date(2022, 6, 6)
        >>> print(calendar.events_in_range(start_date, end_date))
        [<PyXA.apps.Calendar.XACalendarEvent object at 0x105b83d90>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90bb0>, <PyXA.apps.Calendar.XACalendarEvent object at 0x105b90dc0>]

        .. note::

           Querying events from a wide date range can take significant time. If you are looking for a specific subset of events within a large date range, it *might* be faster to use :func:`events` with a well-constructed filter and then iterate through the resulting array of objects, parsing out events outside of the desired date range.

        .. versionadded:: 0.0.2
        """
        predicate = XABase.XAPredicate()
        predicate.add_geq_condition("startDate", start_date)
        predicate.add_leq_condition("endDate", end_date)
        events_in_range = predicate.evaluate(self.xa_elem.events())
        return self._new_element(events_in_range, XACalendarEventList)

    def events_today(self) -> "XACalendarEventList":
        """Gets a list of all events in the next 24 hours.

        :return: The list of events.
        :rtype: XACalendarEventList

        .. seealso:: :func:`week_events`

        .. versionadded:: 0.0.2
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days=1)
        return self.events_in_range(start_date, end_date)

    def new_event(
        self, name: str, start_date: datetime, end_date: datetime
    ) -> "XACalendarEvent":
        """Creates a new event and pushes it onto this calendar's events array.

        :param name: The name of the event.
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        return self.xa_prnt.xa_prnt.new_event(name, start_date, end_date, self)

    def events(self, filter: Union[dict, None] = None) -> "XACalendarEventList":
        """Returns a list of events, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned events will have, or None
        :type filter: Union[dict, None]
        :return: The list of events
        :rtype: XACalendarEventList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.events(), XACalendarEventList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XACalendarAlarm(XABase.XAObject):
    """An event alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the alarm."""
        return self.xa_elem.properties()

    @property
    def trigger_interval(self) -> int:
        """The interval in minutes between the event and the alarm."""
        return self.xa_elem.triggerInterval()

    @trigger_interval.setter
    def trigger_interval(self, trigger_interval: int):
        self.set_property("triggerInterval", trigger_interval)

    @property
    def trigger_date(self) -> datetime:
        """The date of the alarm."""
        return self.xa_elem.triggerDate()

    @trigger_date.setter
    def trigger_date(self, trigger_date: datetime):
        self.set_property("triggerDate", trigger_date)


class XACalendarDisplayAlarm(XACalendarAlarm):
    """A display alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)


class XACalendarMailAlarm(XACalendarAlarm):
    """A mail alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)


class XACalendarSoundAlarm(XACalendarAlarm):
    """A sound alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def sound_name(self) -> str:
        """The system sound name to be used for the alarm"""
        return self.xa_elem.soundName()

    @sound_name.setter
    def sound_name(self, sound_name: str):
        self.set_property("soundName", sound_name)

    @property
    def sound_file(self) -> str:
        """The path to the sound file to be used for the alarm"""
        return self.xa_elem.soundFile()

    @sound_file.setter
    def sound_file(self, sound_file: str):
        self.set_property("soundFile", sound_file)


class XACalendarOpenFileAlarm(XACalendarAlarm):
    """An open file alarm in Calendar.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def file_path(self) -> str:
        """The path to be opened by the alarm."""
        return self.xa_elem.filePath()

    @file_path.setter
    def file_path(self, file_path: str):
        self.set_property("filePath", file_path)


class XACalendarAttendeeList(XABase.XAList):
    """A wrapper around lists of attendees that employs fast enumeration techniques.

    All properties of attendees can be called as methods on the wrapped list, returning a list containing each attendee's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarEvent, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def display_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName") or [])

    def email(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("email") or [])

    def participation_status(self) -> list[XACalendarApplication.ParticipationStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("participationStatus") or []
        return [
            XACalendarApplication.ParticipationStatus(XABase.OSType(x.stringValue()))
            for x in ls
        ]

    def by_properties(self, properties: dict) -> Union["XACalendarAttendee", None]:
        return self.by_property("properties", properties)

    def by_display_name(self, display_name: str) -> Union["XACalendarAttendee", None]:
        return self.by_property("displayName", display_name)

    def by_email(self, email: str) -> Union["XACalendarAttendee", None]:
        return self.by_property("email", email)

    def by_participation_status(
        self, participation_status: XACalendarApplication.ParticipationStatus
    ) -> Union["XACalendarAttendee", None]:
        return self.by_property("participationStatus", participation_status.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.display_name()) + ">"


class XACalendarAttendee(XABase.XAObject):
    """An event attendee in Calendar.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the attendee."""
        return self.xa_elem.properties()

    @property
    def display_name(self) -> str:
        """The first and last name of the attendee."""
        return self.xa_elem.displayName()

    @property
    def email(self) -> str:
        """The email address of the attendee."""
        return self.xa_elem.email()

    @property
    def participation_status(self) -> XACalendarApplication.ParticipationStatus:
        """The invitation status for the attendee."""
        return XACalendarApplication.ParticipationStatus(
            self.xa_elem.participationStatus()
        )


class XACalendarEventList(XABase.XAList):
    """A wrapper around lists of events that employs fast enumeration techniques.

    All properties of events can be called as methods on the wrapped list, returning a list containing each event's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarEvent, filter)

    def properties(self) -> Generator[dict[str, Any], None, None]:
        """Gets the properties of every event in the list.

        :return: A generator that generates a dictionary of element properties.
        :rtype: Generator[dict[str, Any], None, None]
        """
        properties_list = (
            {
                "description": event.description()[25:],
                "start_date": event.startDate(),
                "end_date": event.endDate(),
                "allday_event": event.alldayEvent(),
                "recurrence": event.recurrence(),
                "sequence": event.sequence(),
                "stamp_date": event.stampDate(),
                "excluded_dates": list(event.excludedDates()),
                "status": XACalendarApplication.EventStatus(event.status()),
                "summary": event.summary(),
                "location": event.location(),
                "uid": event.uid(),
                "url": XABase.XAURL(event.url()),
            }
            for event in self.xa_elem
        )
        return properties_list

    def description(self) -> list[str]:
        return [event.description() for event in self.xa_elem]

    def start_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("startDate") or [])

    def end_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("endDate") or [])

    def allday_event(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("alldayEvent") or [])

    def recurrence(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("recurrence") or [])

    def sequence(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("sequence") or [])

    def stamp_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("stampDate") or [])

    def excluded_dates(self) -> list[list[datetime]]:
        return [list(event.excludedDates() or []) for event in self.xa_elem]

    def status(self) -> list[XACalendarApplication.EventStatus]:
        ls = self.xa_elem.arrayByApplyingSelector_("status") or []
        return [
            XACalendarApplication.EventStatus(XABase.OSType(x.stringValue()))
            for x in ls
        ]

    def summary(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("summary") or [])

    def location(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("location") or [])

    def uid(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("uid") or [])

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("url") or []
        return [XABase.XAURL(url) for url in ls if url is not None]

    def by_properties(self, properties: dict) -> Union["XACalendarEvent", None]:
        if "uid" in properties:
            return self.by_uid(properties["uid"])

        for event in self.xa_elem:
            event_properties = {
                "start_date": event.startDate() if "start_date" in properties else None,
                "end_date": event.endDate() if "end_date" in properties else None,
                "allday_event": event.alldayEvent()
                if "allday_event" in properties
                else None,
                "recurrence": event.recurrence()
                if "recurrence" in properties
                else None,
                "sequence": event.sequence() if "sequence" in properties else None,
                "stamp_date": event.stampDate() if "stamp_date" in properties else None,
                "excluded_dates": list(event.excludedDates())
                if "excluded_dates" in properties
                else None,
                "status": XACalendarApplication.EventStatus(event.status())
                if "status" in properties
                else None,
                "summary": event.summary() if "summary" in properties else None,
                "location": event.location() if "location" in properties else None,
                "url": XABase.XAURL(event.url()) if "url" in properties else None,
            }
            if all([event_properties[x] == properties[x] for x in properties]):
                return self._new_element(event, XACalendarEvent)

    def by_description(self, description: str) -> Union["XACalendarEvent", None]:
        for event in self.xa_elem:
            if event.description()[25:] == description[25:]:
                return self._new_element(event, XACalendarEvent)

    def by_start_date(self, start_date: datetime) -> Union["XACalendarEvent", None]:
        return self.by_property("startDate", start_date)

    def by_end_date(self, end_date: datetime) -> Union["XACalendarEvent", None]:
        return self.by_property("endDate", end_date)

    def by_allday_event(self, allday_event: bool) -> Union["XACalendarEvent", None]:
        return self.by_property("alldayEvent", allday_event)

    def by_recurrence(self, recurrence: str) -> Union["XACalendarEvent", None]:
        return self.by_property("recurrence", recurrence)

    def by_sequence(self, sequence: int) -> Union["XACalendarEvent", None]:
        return self.by_property("sequence", sequence)

    def by_stamp_date(self, stamp_date: datetime) -> Union["XACalendarEvent", None]:
        return self.by_property("stampDate", stamp_date)

    def by_excluded_dates(
        self, excluded_dates: list[datetime]
    ) -> Union["XACalendarEvent", None]:
        return self.by_property("excludedDates", excluded_dates)

    def by_status(
        self, status: XACalendarApplication.EventStatus
    ) -> Union["XACalendarEvent", None]:
        for event in self.xa_elem:
            if event.status() == status.value:
                return self._new_element(event, XACalendarEvent)

    def by_summary(self, summary: str) -> Union["XACalendarEvent", None]:
        return self.by_property("summary", summary)

    def by_location(self, location: str) -> Union["XACalendarEvent", None]:
        return self.by_property("location", location)

    def by_uid(self, uid: str) -> Union["XACalendarEvent", None]:
        return self.by_property("uid", uid)

    def by_url(self, url: Union[str, XABase.XAURL]) -> Union["XACalendarEvent", None]:
        if isinstance(url, XABase.XAURL):
            url = url.url
        return self.by_property("url", url)

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self)) + ">"


class XACalendarEvent(XABase.XAObject):
    """An event in Calendar.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties: dict):
        super().__init__(properties)
        self.__xa_event_obj = None

    @property
    def xa_event_obj(self) -> type:
        if self.__xa_event_obj is None and hasattr(self.xa_elem, "uid"):
            events = AppKit.NSMutableArray.arrayWithArray_([])
            for year in range(2006, datetime.now().year + 4, 4):
                start_date = date(year, 1, 1)
                end_date = start_date + timedelta(days=365 * 4)
                predicate = (
                    self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(
                        start_date, end_date, None
                    )
                )
                events.addObjectsFromArray_(
                    self.xa_estr.eventsMatchingPredicate_(predicate)
                )
            self.__xa_event_obj = XABase.XAPredicate.evaluate_with_dict(
                events, {"calendarItemIdentifier": self.uid}
            )[0]
        return self.__xa_event_obj

    @property
    def properties(self) -> dict:
        """All properties of the event."""
        return {
            "description": self.xa_elem.description(),
            "start_date": self.xa_elem.startDate(),
            "end_date": self.xa_elem.endDate(),
            "allday_event": self.xa_elem.alldayEvent(),
            "recurrence": self.xa_elem.recurrence(),
            "sequence": self.xa_elem.sequence(),
            "stamp_date": self.xa_elem.stampDate(),
            "excluded_dates": list(self.xa_elem.excludedDates()),
            "status": XACalendarApplication.EventStatus(self.xa_elem.status()),
            "summary": self.xa_elem.summary(),
            "location": self.xa_elem.location(),
            "uid": self.xa_elem.uid(),
            "url": XABase.XAURL(self.xa_elem.url()),
        }

    @property
    def description(self) -> str:
        """The event's notes."""
        return self.xa_elem.description()

    @description.setter
    def description(self, description: str):
        self.set_property("description", description)

    @property
    def start_date(self) -> datetime:
        """The start date and time of the event."""
        return self.xa_elem.startDate()

    @start_date.setter
    def start_date(self, start_date: datetime):
        self.set_property("startDate", start_date)

    @property
    def end_date(self) -> datetime:
        """The end date and time of the event."""
        return self.xa_elem.endDate()

    @end_date.setter
    def end_date(self, end_date: datetime):
        self.set_property("endDate", end_date)

    @property
    def allday_event(self) -> bool:
        """Whether the event is an all-day event."""
        return self.xa_elem.alldayEvent()

    @allday_event.setter
    def allday_event(self, allday_event: bool):
        self.set_property("alldayEvent", allday_event)

    @property
    def recurrence(self) -> str:
        """A string describing the event recurrence."""
        return self.xa_elem.recurrence() or ""

    @recurrence.setter
    def recurrence(self, recurrence: str):
        self.set_property("recurrence", recurrence)

    @property
    def sequence(self) -> int:
        """The event version."""
        return self.xa_elem.sequence()

    @property
    def stamp_date(self) -> datetime:
        """The date the event was last modified."""
        return self.xa_elem.stampDate()

    @stamp_date.setter
    def stamp_date(self, stamp_date: datetime):
        self.set_property("stampDate", stamp_date)

    @property
    def excluded_dates(self) -> list[datetime]:
        """The exception dates for the event."""
        return list(self.xa_elem.excludedDates())

    @excluded_dates.setter
    def excluded_dates(self, excluded_dates: list[datetime]):
        self.set_property("excludedDates", excluded_dates)

    @property
    def status(self) -> XACalendarApplication.EventStatus:
        """The status of the event."""
        return XACalendarApplication.EventStatus(self.xa_elem.status())

    @status.setter
    def status(self, status: XACalendarApplication.EventStatus):
        self.set_property("status", status.value)

    @property
    def summary(self) -> str:
        """The summary (title) of the event."""
        return self.xa_elem.summary()

    @summary.setter
    def summary(self, summary: str):
        self.set_property("summary", summary)

    @property
    def location(self) -> str:
        """The location of the event."""
        return self.xa_elem.location()

    @location.setter
    def location(self, location: str):
        self.set_property("location", location)

    @property
    def uid(self) -> str:
        """A unique identifier for the event."""
        return self.xa_elem.uid()

    @property
    def url(self) -> str:
        """The URL associated with the event."""
        return self.xa_elem.url()

    @url.setter
    def url(self, url: str):
        self.set_property("URL", url)

    def show(self) -> "XACalendarEvent":
        """Shows the event in the front calendar window.

        :return: The event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_elem.show()
        return self

    def delete(self):
        """Deletes the event.

        .. versionadded:: 0.0.1
        """
        self.xa_estr.removeEvent_span_error_(
            self.xa_event_obj, EventKit.EKSpanThisEvent, None
        )

    def duplicate(self) -> "XACalendarEvent":
        """Duplicates the event, placing the copy on the same calendar.

        :return:The newly created event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        new_event = self.xa_event_obj.duplicate()
        self.xa_estr.saveEvent_span_commit_error_(
            new_event, EventKit.EKSpanThisEvent, True, None
        )

        parent = self.xa_prnt
        while not hasattr(parent, "events"):
            parent = parent.xa_prnt

        return parent.events().by_uid(new_event.calendarItemIdentifier())

    def duplicate_to(self, calendar: XACalendarCalendar) -> "XACalendarEvent":
        """Duplicates the event, placing the copy on the same calendar.

        :return: The event object that this method was called from
        :rtype: XACalendarEvent

        :Example: Copy today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[2]
        >>> event = calendar.events_today()[0]
        >>> event.duplicate_to(calendar2)

        .. seealso:: :func:`duplicate`, :func:`move_to`

        .. versionadded:: 0.0.1
        """
        calendars = self.xa_estr.calendars()
        calendar_obj = XABase.XAPredicate.evaluate_with_dict(
            calendars, {"title": calendar.name}
        )[0]
        new_event = self.xa_event_obj.copyToCalendar_withOptions_(calendar_obj, 1)
        self.xa_estr.saveEvent_span_commit_error_(
            new_event, EventKit.EKSpanThisEvent, True, None
        )
        return calendar.events().by_uid(new_event.calendarItemIdentifier())

    def move_to(self, calendar: XACalendarCalendar) -> "XACalendarEvent":
        """Moves this event to the specified calendar.

        :param calendar: The calendar to move the event to.
        :type calendar: XACalendar
        :return: A reference to the moved event object.
        :rtype: XACalendarEvent

        :Example: Move today's event to another calendar

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[2]
        >>> event = calendar.events_today()[0]
        >>> event.move_to(calendar2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.2
        """
        new_event = self.duplicate_to(calendar)
        self.delete()
        return new_event

    def add_attachment(self, path: str) -> "XACalendarEvent":
        """Adds the file at the specified path as an attachment to the event.

        :param path: The path of the file to attach to the event.
        :type path: str
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> calendar = app.default_calendar
        >>> calendar2 = app.calendars()[1]
        >>> event = calendar.events_today()[0]
        >>> event.add_attachment("/Users/exampleuser/Image.png")

        .. versionadded:: 0.0.2
        """
        file_url = XABase.XAPath(path).xa_elem
        attachment = EventKit.EKAttachment.alloc().initWithFilepath_(file_url)
        self.xa_elem.addAttachment_(attachment)
        self.xa_estr.saveEvent_span_error_(
            self.xa_event_obj, EventKit.EKSpanThisEvent, None
        )
        return self

    def attendees(self, filter: Union[dict, None] = None) -> "XACalendarAttendeeList":
        """Returns a list of attendees, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned attendees will have, or None
        :type filter: Union[dict, None]
        :return: The list of attendees
        :rtype: XACalendarAttendeeList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.attendees(), XACalendarAttendeeList, filter
        )

    def attachments(self, filter: dict = None) -> "XACalendarAttachmentList":
        """ "Returns a list of attachments, as PyXA objects, matching the given filter.

        :return: The list of attachments.
        :rtype: XACalendarAttachmentList

        .. versionadded:: 0.0.2
        """
        return self._new_element(
            self.xa_event_obj.attachments(), XACalendarAttachmentList, filter
        )

    def __repr__(self):
        return "<" + str(type(self)) + str(self.start_date) + ">"


class XACalendarAttachmentList(XABase.XAList):
    """A wrapper around lists of event attachments that employs fast enumeration techniques.

    All properties of attachments can be called as methods on the wrapped list, returning a list containing each attachment's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XACalendarAttachment, filter)

    def type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("contentType") or [])

    def file_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileName") or [])

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("urlOnDisk") or []
        return [XABase.XAPath(x) for x in ls]

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def uuid(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("UUID") or [])

    def by_type(self, type: str) -> Union["XACalendarAttachment", None]:
        return self.by_property("contentType", type)

    def by_file_name(self, file_name: str) -> Union["XACalendarAttachment", None]:
        return self.by_property("fileName", file_name)

    def by_file(
        self, file: Union[XABase.XAPath, str]
    ) -> Union["XACalendarAttachment", None]:
        if isinstance(file, str):
            file = XABase.XAPath(file)
        return self.by_property("urlOnDisk", file.xa_elem)

    def by_url(
        self, url: Union[XABase.XAURL, str]
    ) -> Union["XACalendarAttachment", None]:
        if isinstance(url, str):
            url = XABase.XAURL(url)
        return self.by_property("URL", url.xa_elem)

    def by_uuid(self, uuid: str) -> Union["XACalendarAttachment", None]:
        return self.by_property("UUID", uuid)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.file_name()) + ">"


class XACalendarAttachment(XABase.XAObject):
    """A class for interacting with calendar event attachments.

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties: dict):
        super().__init__(properties)

    @property
    def type(self) -> str:
        """The content type of the attachment, e.g. `image/png`."""
        return self.xa_elem.contentType()

    @property
    def file_name(self) -> str:
        """The filename of the original document."""
        return self.xa_elem.fileName()

    @property
    def file(self) -> XABase.XAPath:
        """The location of the attachment on the local disk."""
        return XABase.XAPath(self.xa_elem.urlOnDisk())

    @property
    def url(self) -> XABase.XAURL:
        """The iCloud URL of the attachment."""
        return XABase.XAURL(self.xa_elem.URL())

    @property
    def uuid(self) -> str:
        """A unique identifier for the attachment."""
        return self.xa_elem.UUID()

    def open(self) -> "XACalendarAttachment":
        """Opens the attachment in its default application.

        :return: A reference to the attachment object.
        :rtype: XACalendarAttachment

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Calendar")
        >>> calendar = app.default_calendar
        >>> event = calendar.events_today()[0]
        >>> event.attachments()[0].open()

        .. versionadded:: 0.0.2
        """
        self.xa_wksp.openURL_(self.file)
        return self
