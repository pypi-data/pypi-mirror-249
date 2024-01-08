""".. versionadded:: 0.0.1

Control the macOS Reminders application using JXA-like syntax.
"""

from datetime import datetime
from typing import Literal, Union, Any
from enum import Enum

import EventKit
import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable


class XARemindersApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with scripting elements of the Reminders application.

    .. seealso:: :class:`XARemindersAccount`, :class:`XARemindersList`, :class:`XARemindersReminder`

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """The types of objects that can be created using :func:`make`."""

        DOCUMENT = "document"
        LIST = "list"
        REMINDER = "reminder"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XARemindersWindow

        self.pasteboard_types = {
            "com.apple.reminders.reminderCopyPaste": self._get_clipboard_reminder,
        }

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Reminders is the active application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of Reminders.app."""
        return self.xa_scel.version()

    @property
    def default_account(self) -> "XARemindersAccount":
        """The default account in the Reminders application."""
        return self._new_element(self.xa_scel.defaultAccount(), XARemindersAccount)

    @property
    def default_list(self) -> "XARemindersList":
        """The default list in the Reminders application."""
        return self._new_element(self.xa_scel.defaultList(), XARemindersList)

    def _get_clipboard_reminder(self, reminder_name: str) -> "XARemindersReminder":
        return self.reminders({"name": reminder_name})[0]

    def documents(self, filter: Union[dict, None] = None) -> "XARemindersDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XARemindersDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.documents(), XARemindersDocumentList, filter
        )

    def accounts(self, filter: Union[dict, None] = None) -> "XARemindersAccountList":
        """Returns a list of accounts, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned accounts will have, or None
        :type filter: Union[dict, None]
        :return: The list of accounts
        :rtype: XARemindersAccountList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.accounts(), XARemindersAccountList, filter
        )

    def lists(self, filter: Union[dict, None] = None) -> "XARemindersListList":
        """Returns a list of reminder lists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lists will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminder lists
        :rtype: XARemindersListList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_scel.lists(), XARemindersListList, filter)

    def reminders(self, filter: Union[dict, None] = None) -> "XARemindersReminderList":
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.reminders(), XARemindersReminderList, filter
        )

    def new_list(
        self, name: str = "New List", color: str = "#FF0000", emblem: str = "symbol0"
    ) -> "XARemindersList":
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.

        If no list is provided, the reminder is created in the default list.

        :param title: The name of the list, defaults to "New List"
        :type name: str, optional
        :param color: The HEX color of the list's icon.
        :type color: str, optional
        :param emblem: The symbol to use as the list's icon.
        :type emblem: str, optional
        :return: A reference to the newly created list.
        :rtype: XAReminderList

        .. versionadded:: 0.0.1
        """
        new_list = self.make("list", {"name": name, "color": color, "emblem": emblem})
        self.lists().push(new_list)
        return self.lists()[-1]

    def new_reminder(
        self,
        name: str = "New Reminder",
        due_date: datetime = None,
        reminder_list: "XARemindersList" = None,
    ) -> "XARemindersReminder":
        """Creates a new reminder with the given name, body, and due date in the specified reminder list.
        If no list is provided, the reminder is created in the default list.

        :param title: The name of the reminder, defaults to "New Reminder"
        :type title: str, optional
        :param notes: The text notes attached to the reminder, defaults to ""
        :type notes: str, optional
        :param due_date: The date and time when the reminder will be due.
        :type due_date: datetime, optional
        :param reminder_list: The list that the new reminder will be added to.
        :type reminder_list: XAReminderList, optional
        :return: A reference to the newly created reminder.
        :rtype: XAReminder

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.Application("Reminder")
        >>> due_date = datetime.now() + timedelta(hours = 1)
        >>> reminder = app.new_reminder("Read PyXA listation", "Complete 1 tutorial", due_date)
        >>> print(reminder.id)
        B0DD7836-7C05-48D4-B806-D6A76317452E

        .. seealso:: :class:`XAReminder`, :func:`new_list`

        .. versionadded:: 0.0.1
        """
        new_reminder = self.make("reminder", {"name": name, "dueDate": due_date})
        if reminder_list is None:
            self.reminders().push(new_reminder)
            return self.reminders()[-1]
        reminder_list.push(new_reminder)
        return reminder_list.reminders()[-1]

    def make(
        self,
        specifier: Union[str, "XARemindersApplication.ObjectType"],
        properties: dict = None,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XARemindersApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to initialize the object with, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.6
        """
        if isinstance(specifier, XARemindersApplication.ObjectType):
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
            return self._new_element(obj, XARemindersDocument)
        elif specifier == "list":
            return self._new_element(obj, XARemindersList)
        elif specifier == "reminder":
            return self._new_element(obj, XARemindersReminder)


class XARemindersWindow(XABaseScriptable.XASBWindow):
    """A window of the Reminders application.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XARemindersDocument":
        """The document whose contents are displayed in the window."""
        return self._new_element(self.xa_elem.document(), XARemindersDocument)

    def close(self, save: bool = True) -> None:
        """Closes the window.

        :param save: Whether to save the current document before closing, defaults to True
        :type save: bool, optional
        :return: The window object
        :rtype: XARemindersDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.closeSaving_savingIn_(save, None)

    def save(self) -> "XARemindersWindow":
        """Saves the current document of the window.

        :return: The window object
        :rtype: XARemindersWindow

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.saveIn_as_(None, None)

    def print(self, properties: dict, show_dialog: bool = True) -> "XARemindersWindow":
        """Prints the window.

        :param properties: The settings to pre-populate the print dialog with
        :type properties: dict
        :param show_dialog: Whether to show the print dialog or skip right to printing, defaults to True
        :type show_dialog: bool, optional
        :return: The window object
        :rtype: XARemindersWindow

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.printWithProperties_printDialog_(properties, show_dialog)

    def lists(self, filter: Union[dict, None] = None) -> "XARemindersListList":
        """Returns a list of reminder lists, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned lists will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminder lists
        :rtype: XARemindersListList

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.lists(), XARemindersListList, filter)

    def reminders(self, filter: Union[dict, None] = None) -> "XARemindersReminderList":
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.reminders(), XARemindersReminderList, filter
        )


class XARemindersDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersDocument, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return [XABase.XAPath(x) for x in ls]

    def by_properties(self, properties: dict) -> Union["XARemindersDocument", None]:
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union["XARemindersDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XARemindersDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: XABase.XAPath) -> Union["XARemindersDocument", None]:
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XARemindersDocument(XABase.XAObject):
    """A document in the Reminders application.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document."""
        return self.xa_elem.properties()

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

    def close(
        self, save: bool = True, location: Union[str, AppKit.NSURL] = None
    ) -> None:
        """Closes a document."""
        file_path = XABase.XAPath(location).xa_elem
        return self.xa_elem.closeSaving_savingIn_(save, file_path)

    def save(self) -> None:
        """Saves a document."""
        return self.xa_elem.saveIn_as_(...)

    def print(self, properties: dict, show_dialog: bool = True) -> None:
        """Prints a document."""
        return self.xa_elem.printWithProperties_printDialog_(properties, show_dialog)

    def delete(self) -> None:
        """Deletes the document."""
        return self.xa_elem.delete()

    def duplicate(self) -> None:
        """Copies an object."""
        return self.xa_elem.duplicateTo_withProperties_(...)

    def move_to(self, window: XARemindersWindow) -> None:
        """Move an object to a new location."""
        return self.xa_elem.moveTo_(window.xa_elem)


class XARemindersAccountList(XABase.XAList):
    """A wrapper around lists of accounts that employs fast enumeration techniques.

    All properties of accounts can be called as methods on the wrapped list, returning a list containing each account's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersAccount, filter)

    def properties(self) -> list[dict]:
        ls = self.xa_elem.arrayByApplyingSelector_("properties") or []
        return [dict(x) for x in ls]

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_properties(self, properties: dict) -> Union["XARemindersAccount", None]:
        for account in self.xa_elem:
            if account.properties() == properties:
                return self._new_element(account, XARemindersAccount)

    def by_id(self, id: str) -> Union["XARemindersAccount", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XARemindersAccount", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XARemindersAccount(XABase.XAObject):
    """An account in the Reminders application."""

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the account."""
        return dict(self.xa_elem.properties())

    @property
    def id(self) -> str:
        """The unique identifier of the account."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the account."""
        return self.xa_elem.name()

    def show(self) -> "XARemindersAccount":
        """Shows the account in the front window.

        :return: The account object
        :rtype: XARemindersAccount

        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()


class XARemindersListList(XABase.XAList):
    """A wrapper around lists of reminder lists that employs fast enumeration techniques.

    All properties of reminder lists can be called as methods on the wrapped list, returning a list containing each list's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersList, filter)

    def properties(self) -> list[dict]:
        ls = self.xa_elem.arrayByApplyingSelector_("properties") or []
        return [dict(x) for x in ls]

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def container(self) -> XARemindersAccountList:
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XARemindersAccountList)

    def color(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("color") or [])

    def emblem(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("emblem") or [])

    def reminders(self) -> "XARemindersReminderList":
        ls = self.xa_elem.arrayByApplyingSelector_("reminders") or []
        return self._new_element(ls, XARemindersReminderList)

    def by_properties(self, properties: dict) -> Union["XARemindersList", None]:
        for ls in self.xa_elem:
            if ls.properties() == properties:
                return self._new_element(ls, XARemindersList)

    def by_id(self, id: str) -> Union["XARemindersList", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XARemindersList", None]:
        return self.by_property("name", name)

    def by_container(
        self, container: "XARemindersList"
    ) -> Union["XARemindersList", None]:
        for ls in self.xa_elem:
            if ls.container().get() == container.xa_elem.get():
                return self._new_element(ls, XARemindersList)

    def by_color(self, color: str) -> Union["XARemindersList", None]:
        return self.by_property("color", color)

    def by_emblem(self, emblem: str) -> Union["XARemindersList", None]:
        return self.by_property("emblem", emblem)

    def delete(self):
        """Deletes all reminder lists in the list.

        .. versionadded:: 0.0.6
        """
        [x.delete() for x in self.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XARemindersList(XABase.XAObject):
    """A class for..."""

    def __init__(self, properties):
        super().__init__(properties)

        # EventKit Properties
        if hasattr(self.xa_elem, "id"):
            lists = (
                XABase.XAPredicate()
                .from_args("calendarIdentifier", self.xa_elem.id())
                .evaluate(self.xa_estr.calendars())
            )
            if len(lists) > 0:
                elem = lists[0]

                self.summary = elem.summary()  #: An overview of the list's information
                self.subscription_url = (
                    elem.subscriptionURL()
                )  #: The URL of the list used to subscribe to it
                self.sharing_status: bool = (
                    elem.sharingStatus()
                )  #: Whether the list is shared
                self.sharees = (
                    elem.sharees()
                )  #: A list of individuals with whom the list is shared with

    @property
    def properties(self) -> dict:
        """All properties of the list."""
        return dict(self.xa_elem.properties())

    @property
    def id(self) -> str:
        """The unique identifier of the list."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the list."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def container(self) -> Union[XARemindersAccount, "XARemindersList"]:
        """The container of the list."""
        return self._new_element(self.xa_elem.container(), XARemindersAccount)

    @property
    def color(self) -> str:
        """The color of the list."""
        return self.xa_elem.color()

    @color.setter
    def color(self, color: str):
        self.set_property("color", color)

    @property
    def emblem(self) -> str:
        """The emblem icon name of the list."""
        return self.xa_elem.emblem()

    @emblem.setter
    def emblem(self, emblem: str):
        self.set_property("emblem", emblem)

    def delete(self) -> None:
        """Deletes the list.

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.delete()

    def show(self) -> "XARemindersList":
        """Shows the list in the front Reminders window.

        :return: The list object
        :rtype: XARemindersList

        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()
        return self

    def reminders(self, filter: Union[dict, None] = None) -> "XARemindersReminderList":
        """Returns a list of reminders, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned reminders will have, or None
        :type filter: Union[dict, None]
        :return: The list of reminders
        :rtype: XARemindersReminderList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.reminders(), XARemindersReminderList, filter
        )


class XARemindersReminderList(XABase.XAList):
    """A wrapper around lists of reminders that employs fast enumeration techniques.

    All properties of reminders can be called as methods on the wrapped list, returning a list containing each reminder's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersReminder, filter)

    def properties(self) -> list[dict]:
        ls = self.xa_elem.arrayByApplyingSelector_("properties") or []
        return [dict(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def container(self) -> XARemindersListList:
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XARemindersListList)

    def creation_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def body(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("body") or [])

    def completed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("completed") or [])

    def completion_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("completionDate") or [])

    def due_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("dueDate") or [])

    def allday_due_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("alldayDueDate") or [])

    def remind_me_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("remindMeDate") or [])

    def priority(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("priority") or [])

    def flagged(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("flagged") or [])

    def alarms(self) -> list["XARemindersAlarmList"]:
        return [x.alarms() for x in self]

    def by_properties(self, properties: dict) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.properties() == properties:
                return self._new_element(reminder, XARemindersReminder)

    def by_name(self, name: str) -> Union["XARemindersReminder", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XARemindersReminder", None]:
        return self.by_property("id", id)

    def by_container(
        self, container: "XARemindersList"
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.container().get() == container.xa_elem.get():
                return self._new_element(reminder, XARemindersReminder)

    def by_creation_date(
        self, creation_date: datetime
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.creationDate() == creation_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.modificationDate() == modification_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_body(self, body: str) -> Union["XARemindersReminder", None]:
        return self.by_property("body", body)

    def by_completed(self, completed: bool) -> Union["XARemindersReminder", None]:
        return self.by_property("completed", completed)

    def by_completion_date(
        self, completion_date: datetime
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.completionDate() == completion_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_due_date(self, due_date: datetime) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.dueDate() == due_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_allday_due_date(
        self, allday_due_date: datetime
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.alldayDueDate() == allday_due_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_remind_me_date(
        self, remind_me_date: datetime
    ) -> Union["XARemindersReminder", None]:
        for reminder in self.xa_elem:
            if reminder.remindMeDate() == remind_me_date:
                return self._new_element(reminder, XARemindersReminder)

    def by_priority(self, priority: int) -> Union["XARemindersReminder", None]:
        return self.by_property("priority", priority)

    def by_flagged(self, flagged: bool) -> Union["XARemindersReminder", None]:
        return self.by_property("flagged", flagged)

    def delete(self):
        """Deletes all reminders in the list.

        .. versionadded:: 0.0.6
        """
        [x.delete() for x in self.xa_elem]

    def move_to(self, list: XARemindersList):
        """Moves all reminders in the list to the specified reminder list.

        :param list: The list to move reminders into
        :type list: XARemindersList

        .. versionadded:: 0.0.6
        """
        [x.moveTo_(list.xa_elem) for x in self.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self)) + ">"


class XARemindersReminder(XABase.XAObject):
    """A reminder in Reminders.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.__properties = None

    @property
    def properties(self) -> dict:
        """All properties of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return dict(self.__properties.copy())

    @property
    def name(self) -> str:
        """The name of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["name"]

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def id(self) -> str:
        """The unique identifier of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["id"]

    @property
    def container(self) -> Union[XARemindersList, "XARemindersReminder"]:
        """The container of the reminder.

        .. versionadded:: 0.0.6
        """
        return self._new_element(self.xa_elem.container(), XARemindersList)

    @property
    def creation_date(self) -> datetime:
        """The creation date of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["creationDate"]

    @property
    def modification_date(self) -> datetime:
        """The modification date of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["modificationDate"]

    @property
    def body(self) -> str:
        """The notes attached to the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["body"] or ""

    @body.setter
    def body(self, body: str):
        self.set_property("body", body)

    @property
    def completed(self) -> bool:
        """Whether the reminder is completed.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["completed"]

    @completed.setter
    def completed(self, completed: bool):
        self.set_property("completed", completed)

    @property
    def completion_date(self) -> Union[datetime, None]:
        """The completion date of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["completionDate"]

    @completion_date.setter
    def completion_date(self, completion_date: datetime):
        self.set_property("completionDate", completion_date)

    @property
    def due_date(self) -> Union[datetime, None]:
        """The due date of the reminder; will set both date and time.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        print(self.__properties)
        return self.__properties["dueDate"]

    @due_date.setter
    def due_date(self, due_date: datetime):
        self.set_property("dueDate", due_date)

    @property
    def allday_due_date(self) -> Union[datetime, None]:
        """The all-day due date of the reminder; will only set a date.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["allDayDueDate"]

    @allday_due_date.setter
    def allday_due_date(self, allday_due_date: datetime):
        self.set_property("alldayDueDate", allday_due_date)

    @property
    def remind_me_date(self) -> Union[datetime, None]:
        """The remind date of the reminder.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["remindMeDate"]

    @remind_me_date.setter
    def remind_me_date(self, remind_me_date: datetime):
        self.set_property("remindMeDate", remind_me_date)

    @property
    def priority(self) -> int:
        """The priority of the reminder; 0: no priority, 1–4: high, 5: medium, 6–9: low.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["priority"]

    @priority.setter
    def priority(self, priority: int):
        self.set_property("priority", priority)

    @property
    def flagged(self) -> bool:
        """Whether the reminder is flagged.

        .. versionadded:: 0.0.6
        """
        if self.__properties is None:
            self.__properties = self.xa_elem.properties()
        return self.__properties["flagged"]

    @flagged.setter
    def flagged(self, flagged: bool):
        self.set_property("flagged", flagged)

    @property
    def all_day(self) -> bool:
        """Whether the reminder is all day or a specific time.

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        return reminder.allDay() == 1

    @property
    def notes(self) -> str:
        """User-inputted notes for this reminder.

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        return reminder.notes()

    @property
    def url(self) -> XABase.XAURL:
        """The URL attached to the reminder, if there is one.

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        return XABase.XAURL(reminder.URL())

    @property
    def recurrence_rule(self) -> "XARemindersRecurrenceRule":
        """The recurrence rule for the reminder.

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        if reminder.recurrenceRule() is not None:
            return self._new_element(
                reminder.recurrenceRule(), XARemindersRecurrenceRule
            )

    def __get_ek_reminder(self) -> EventKit.EKReminder:
        predicate = self.xa_estr.predicateForRemindersInCalendars_(None)
        reminders = self.xa_estr.remindersMatchingPredicate_(predicate)

        reminder_id = (
            self.xa_elem.properties()["id"]
            if self.__properties is None
            else self.__properties["id"]
        )

        if reminder_id is not None:
            predicate = AppKit.NSPredicate.predicateWithFormat_(
                "%@ CONTAINS calendarItemIdentifier", reminder_id
            )
            reminders = reminders.filteredArrayUsingPredicate_(predicate)

            if len(reminders) > 0:
                return reminders[0]

    def delete(self) -> None:
        """Deletes the reminder.

        .. versionadded:: 0.0.6
        """
        return self.xa_elem.delete()

    def move_to(self, list: XARemindersList) -> "XARemindersReminder":
        """Moves the reminder to the specified list.

        :param list: The list to move the reminder to
        :type list: XARemindersList
        :return: The moved reminder object
        :rtype: XARemindersReminder

        .. versionadded:: 0.0.6
        """
        self.xa_elem.moveTo_(list.xa_elem)
        return list.reminders()[-1]

    def show(self) -> "XARemindersReminder":
        """Shows the reminder in the front Reminders window.

        :return: The reminder object
        :rtype: XARemindersReminder

        .. versionadded:: 0.0.6
        """
        self.xa_elem.show()
        return self

    def alarms(self, filter: Union[dict, None] = None) -> "XARemindersAlarmList":
        """Returns a list of alarms, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned alarms will have, or None
        :type filter: Union[dict, None]
        :return: The list of alarms
        :rtype: XARemindersAlarmList

        .. versionadded:: 0.0.6
        """
        reminder = self.__get_ek_reminder()
        return self._new_element(
            reminder.alarms() or AppKit.NSArray.alloc().initWithArray_([]),
            XARemindersAlarmList,
            filter,
        )

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XARemindersRecurrenceRule(XABase.XAObject):
    """A class for interacting with Reminders.

    .. seealso:: :class:`XARemindersReminder`

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def frequency(self) -> str:
        """Specifier for the base unit of recurrence, i.e. daily, weekly, monthly, or yearly."""
        return self.xa_elem.frequency()

    @property
    def interval(self) -> int:
        """The number of frequency units between recurrences."""
        return self.xa_elem.interval()

    @property
    def end_date(self) -> datetime:
        """The end date and time of recurrence."""
        return self.xa_elem.endDate()

    def set_frequency(self, frequency: Literal["daily", "weekly", "monthly", "yearly"]):
        """Sets the frequency of recurrence.

        :param frequency: A specifier for the base unit of recurrence.
        :type frequency: Literal["daily", "weekly", "monthly", "yearly"]

        .. versionadded:: 0.0.2
        """
        freq_ids = {
            "daily": 0,
            "weekly": 1,
            "monthly": 2,
            "yearly": 3,
        }
        self.xa_elem.setFrequency_(freq_ids[frequency])
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def set_interval(self, interval: int):
        """Sets the interval of recurrence.

        :param interval: The interval; the number of frequency units between recurrences.
        :type interval: int

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setInterval_(interval)
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def set_end_date(self, end_date: datetime):
        """Sets the date and time when the recurrence ends.

        :param end_date: The absolute end day of recurrence.
        :type end_date: datetime

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setEndDate_(end_date)
        self.xa_estr.saveReminder_commit_error_(self.xa_prnt.xa_elem, True, None)

    def __repr__(self):
        return (
            "<"
            + str(type(self))
            + f"freq={self.xa_elem.frequencyString()}, interval={self.interval}, end_date={self.end_date}, id={self.id}>"
        )


class XARemindersAlarmList(XABase.XAList):
    """A wrapper around lists of reminder alarms that employs fast enumeration techniques.

    All properties of alarms can be called as methods on the wrapped list, returning a list containing each alarm's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XARemindersAlarm, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("sharedUID") or [])

    def snoozed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("isSnoozed") or [])

    def date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("absoluteDate") or [])

    def proximity_direction(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("proximityString") or [])

    def location(self) -> list[XABase.XALocation]:
        return [x.location for x in self]

    def by_id(self, id: str) -> Union["XARemindersAlarm", None]:
        return self.by_property("sharedUID", id)

    def by_snoozed(self, snoozed: bool) -> Union["XARemindersAlarm", None]:
        return self.by_property("isSnoozed", snoozed)

    def by_date(self, date: datetime) -> Union["XARemindersAlarm", None]:
        return self.by_property("absoluteDate", date)

    def by_proximity_direction(
        self, proximity_direction: str
    ) -> Union["XARemindersAlarm", None]:
        return self.by_property("proximityString", proximity_direction)

    def by_location(
        self, location: XABase.XALocation
    ) -> Union["XARemindersAlarm", None]:
        return self.by_property("structuredLocation", location.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.id()) + ">"


class XARemindersAlarm(XABase.XAObject):
    """An alarm attached to a reminder.

    .. seealso:: :class:`XARemindersReminder`

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """A unique identifier for this alarm."""
        return self.xa_elem.sharedUID()

    @property
    def snoozed(self) -> bool:
        """Whether the alarm is snoozed."""
        return self.xa_elem.isSnoozed()

    @property
    def date(self) -> datetime:
        """The date and time of a date-based alarm."""
        return self.xa_elem.absoluteDate()

    @property
    def proximity_direction(self) -> str:
        """Whether a location-based alarm is for arriving or departing."""
        return self.xa_elem.proximityString()

    @property
    def location(self) -> XABase.XALocation:
        location = self.xa_elem.structuredLocation()
        if location is not None:
            return XABase.XALocation(
                title=location.title(),
                latitude=location.geoLocation().coordinate()[0],
                longitude=location.geoLocation().coordinate()[1],
                radius=location.radiusNumber() or 0,
                raw_value=location,
            )

    def set_date(self, date: datetime):
        """Sets the date and time of the alarm.

        :param date: The absolute date that the alarm will go off.
        :type date: datetime

        .. versionadded:: 0.0.2
        """
        self.xa_elem.setAbsoluteDate_(date)
        self.xa_estr.saveReminder_commit_error_(
            self.xa_prnt.xa_prnt.xa_elem, True, None
        )

    def set_location(self, location: XABase.XALocation):
        """Sets the location and radius of the alarm.

        :param location: The location (with specified radius) that the alarm will go off.
        :type location: XABase.XALocation

        .. versionadded:: 0.0.2
        """
        location.raw_value = self.location.raw_value
        location.prepare_for_export()
        self.xa_estr.saveReminder_commit_error_(
            self.xa_prnt.xa_prnt.xa_elem, True, None
        )

    def __repr__(self):
        return "<" + str(type(self)) + "id=" + self.id + ">"
