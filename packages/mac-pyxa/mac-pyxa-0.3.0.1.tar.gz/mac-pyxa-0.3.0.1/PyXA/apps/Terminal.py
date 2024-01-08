""".. versionadded:: 0.0.1

Control the macOS Terminal application using JXA-like syntax.
"""

import subprocess
from typing import Dict, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable


class XATerminalApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Messages.app

    .. seealso:: :class:`XATerminalWindow`, :class:`XATerminalTab`, :class:`XATerminalSettingsSet`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATerminalWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Terminal is the active application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version of Terminal.app."""
        return self.xa_scel.version()

    @property
    def default_settings(self) -> "XATerminalSettingsSet":
        """The settings set used for new windows."""
        return self._new_element(self.xa_scel.defaultSettings(), XATerminalSettingsSet)

    @default_settings.setter
    def default_settings(self, default_settings: "XATerminalSettingsSet"):
        self.set_property("defaultSettings", default_settings.xa_elem)

    @property
    def startup_settings(self) -> "XATerminalSettingsSet":
        """The settings set used for the window created on application startup."""
        return self._new_element(self.xa_scel.startupSettings(), XATerminalSettingsSet)

    @startup_settings.setter
    def startup_settings(self, startup_settings: "XATerminalSettingsSet"):
        self.set_property("startupSettings", startup_settings.xa_elem)

    @property
    def current_tab(self) -> "XATerminalTab":
        """The currently active Terminal tab."""
        return self.front_window.selected_tab

    @current_tab.setter
    def current_tab(self, current_tab: "XATerminalTab"):
        self.front_window.selected_tab = current_tab

    def do_script(
        self,
        script: str,
        window_tab: Union["XATerminalWindow", "XATerminalTab"] = None,
        return_result: bool = False,
    ) -> Union["XATerminalApplication", Dict[str, str]]:
        """Executes a Terminal script in the specified window or tab.

        If no window or tab is provided, the script will run in a new tab of the frontmost window. If return_result is True, the script will be run in a new tab no regardless of the value of window_tab.

        :param script: The script to execute.
        :type script: str
        :param window_tab: The window or tab to execute the script in, defaults to None
        :type window_tab: Union[XATerminalWindow, XATerminalTab], optional
        :param return_result: Whether to return the result of script execution, defaults to False
        :type return_result: bool, optional
        :return: A reference to the Terminal application object, or the result of script execution.
        :rtype: Union[XATerminalApplication, Dict[str, str]]

        .. versionchanged:: 0.0.9

           Now optionally returns the script execution result.

        .. versionadded:: 0.0.1
        """
        if window_tab is None:
            window_tab = self.front_window

        if return_result:
            value = subprocess.Popen(
                [script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            return {
                "stdout": value.stdout.read().decode(),
                "stderr": value.stderr.read().decode(),
            }
        else:
            self.xa_scel.doScript_in_(script, window_tab.xa_elem)
            return self

    def settings_sets(
        self, filter: dict = None
    ) -> Union["XATerminalSettingsSetList", None]:
        """Returns a list of settings sets, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned settings sets will have, or None
        :type filter: Union[dict, None]
        :return: The list of settings sets
        :rtype: XATerminalSettingsSetList

        .. versionadded:: 0.0.7
        """
        return self._new_element(
            self.xa_scel.settingsSets(), XATerminalSettingsSetList, filter
        )


class XATerminalWindow(
    XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject
):
    """A class for managing and interacting with windows in Terminal.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def frontmost(self) -> bool:
        """Whether the window is currently the frontmost Terminal window."""
        return self.xa_elem.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def selected_tab(self) -> "XATerminalTab":
        """The Terminal tab currently displayed in the window."""
        return self._new_element(self.xa_elem.selectedTab(), XATerminalTab)

    @selected_tab.setter
    def selected_tab(self, selected_tab: "XATerminalTab"):
        self.set_property("selectedTab", selected_tab.xa_elem)

    @property
    def position(self) -> tuple[int, int]:
        return tuple(self.xa_elem.position())

    @position.setter
    def position(self, position: tuple[int, int]):
        """The position of the top-left corner of the window."""
        self.set_property("position", position)

    def tabs(self, filter: dict = None) -> Union["XATerminalTabList", None]:
        """Returns a list of tabs, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned tabs will have, or None
        :type filter: Union[dict, None]
        :return: The list of tabs
        :rtype: XATerminalTabList

        .. versionadded:: 0.0.7
        """
        return self._new_element(self.xa_elem.tabs(), XATerminalTabList, filter)


class XATerminalTabList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Terminal tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XATerminalTab, filter)

    def number_of_rows(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfRows") or [])

    def number_of_columns(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfColumns") or [])

    def contents(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("contents") or [])

    def history(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("history") or [])

    def busy(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("busy") or [])

    def processes(self) -> list[list[str]]:
        return [
            list(x) for x in self.xa_elem.arrayByApplyingSelector_("processes") or []
        ]

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def title_displays_custom_title(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysCustomTitle") or []
        )

    def custom_title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("customTitle") or [])

    def tty(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("tty") or [])

    def current_settings(self) -> "XATerminalSettingsSetList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentSettings") or []
        return self._new_element(ls, XATerminalSettingsSetList)

    def by_number_of_rows(self, number_of_rows: int) -> Union["XATerminalTab", None]:
        return self.by_property("numberOfRows", number_of_rows)

    def by_number_of_columns(
        self, number_of_columns: int
    ) -> Union["XATerminalTab", None]:
        return self.by_property("numberOfColumns", number_of_columns)

    def by_contents(self, contents: str) -> Union["XATerminalTab", None]:
        return self.by_property("contents", contents)

    def by_history(self, history: str) -> Union["XATerminalTab", None]:
        return self.by_property("history", history)

    def by_busy(self, busy: bool) -> Union["XATerminalTab", None]:
        return self.by_property("busy", busy)

    def by_processes(self, processes: list[str]) -> Union["XATerminalTab", None]:
        return self.by_property("processes", processes)

    def by_selected(self, selected: bool) -> Union["XATerminalTab", None]:
        return self.by_property("selected", selected)

    def by_title_displays_custom_title(
        self, title_displays_custom_title: bool
    ) -> Union["XATerminalTab", None]:
        return self.by_property("titleDisplaysCustomTitle", title_displays_custom_title)

    def by_custom_title(self, custom_title: str) -> Union["XATerminalTab", None]:
        return self.by_property("customTitle", custom_title)

    def by_tty(self, tty: str) -> Union["XATerminalTab", None]:
        return self.by_property("tty", tty)

    def by_current_settings(
        self, current_settings: "XATerminalSettingsSet"
    ) -> Union["XATerminalTab", None]:
        return self.by_property("currentSettings", current_settings.xa_elem)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each tab in the list.

        When the clipboard content is set to a list of Terminal tabs, each tab's custom title and history are added to the clipboard.

        :return: The list of each tab's custom title and history
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        items = []
        titles = self.custom_title()
        histories = self.history()
        for index, title in enumerate(titles):
            items.append(title)
            items.append(histories[index])
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.custom_title()) + ">"


class XATerminalTab(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with tabs in Terminal.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def number_of_rows(self) -> int:
        """The number of rows displayed in the tab."""
        return self.xa_elem.numberOfRows()

    @number_of_rows.setter
    def number_of_rows(self, number_of_rows: int):
        self.set_property("numberOfRows", number_of_rows)

    @property
    def number_of_columns(self) -> int:
        """The number of columns displayed in the tab."""
        return self.xa_elem.numberOfColumns()

    @number_of_columns.setter
    def number_of_columns(self, number_of_columns: int):
        self.set_property("numberOfColumns", number_of_columns)

    @property
    def contents(self) -> str:
        """The currently visible contents of the tab."""
        return self.xa_elem.contents()

    @property
    def history(self) -> str:
        """The contents of the entire scrolling buffer of the tab."""
        return self.xa_elem.history()

    @property
    def busy(self) -> bool:
        """Whether the tab is currently busy running a process."""
        return self.xa_elem.busy()

    @property
    def processes(self) -> list[str]:
        """The processes currently running in the tab."""
        return list(self.xa_elem.processes())

    @property
    def selected(self) -> bool:
        """Whether the tab is currently selected."""
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property("selected", selected)

    @property
    def title_displays_custom_title(self) -> bool:
        """Whether the tab's title contains a custom title."""
        return self.xa_elem.titleDisplaysCustomTitle()

    @title_displays_custom_title.setter
    def title_displays_custom_title(self, title_displays_custom_title: bool):
        self.set_property("titleDisplaysCustomTitle", title_displays_custom_title)

    @property
    def custom_title(self) -> str:
        """The tab's custom title."""
        return self.xa_elem.customTitle()

    @custom_title.setter
    def custom_title(self, custom_title: str):
        self.set_property("customTitle", custom_title)

    @property
    def tty(self) -> str:
        """The tab's TTY device."""
        return self.xa_elem.tty()

    @property
    def current_settings(self) -> "XATerminalSettingsSet":
        """The set of settings which control the tab's behavior and appearance."""
        return self._new_element(self.xa_elem.currentSettings(), XATerminalSettingsSet)

    @current_settings.setter
    def current_settings(self, current_settings: "XATerminalSettingsSet"):
        self.set_property("currentSettings", current_settings.xa_elem)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of the tab.

        When the clipboard content is set to a Terminal tab, the tab's custom title and its history are added to the clipboard.

        :return: The tab's custom title and history
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return [self.custom_title, self.history]

    def __repr__(self):
        return "<" + str(type(self)) + self.custom_title + ">"


class XATerminalSettingsSetList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Terminal settings sets that employs fast enumeration techniques.

    All properties of settings sets can be called as methods on the wrapped list, returning a list containing each settings set's value for the property.

    .. versionadded:: 0.0.7
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XATerminalSettingsSet, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def number_of_rows(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfRows") or [])

    def number_of_columns(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("numberOfColumns") or [])

    def cursor_color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("cursorColor") or []
        return [XABase.XAColor(x) for x in ls]

    def background_color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("backgroundColor") or []
        return [XABase.XAColor(x) for x in ls]

    def normal_text_color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("normalTextColor") or []
        return [XABase.XAColor(x) for x in ls]

    def bold_text_color(self) -> list[XABase.XAColor]:
        ls = self.xa_elem.arrayByApplyingSelector_("boldTextColor") or []
        return [XABase.XAColor(x) for x in ls]

    def font_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontName") or [])

    def font_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontSize") or [])

    def font_antialiasing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontAntialiasing") or [])

    def clean_commands(self) -> list[list[str]]:
        return [
            list(x)
            for x in self.xa_elem.arrayByApplyingSelector_("cleanCommands") or []
        ]

    def title_displays_device_name(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysDeviceName") or []
        )

    def title_displays_shell_path(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysShellPath") or []
        )

    def title_displays_window_size(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysWindowSize") or []
        )

    def title_displays_settings_name(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysSettingsName") or []
        )

    def title_displays_custom_title(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("titleDisplaysCustomTitle") or []
        )

    def custom_title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("customTitle") or [])

    def by_id(self, id: int) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("name", name)

    def by_number_of_rows(
        self, number_of_rows: int
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("numberOfRows", number_of_rows)

    def by_number_of_columns(
        self, number_of_columns: int
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("numberOfColumns", number_of_columns)

    def by_cursor_color(
        self, cursor_color: XABase.XAColor
    ) -> Union["XATerminalSettingsSet", None]:
        for settings_set in self.xa_elem:
            if settings_set.cursorColor() == cursor_color.xa_elem:
                return self._new_element(settings_set, XATerminalSettingsSet)

    def by_background_color(
        self, background_color: XABase.XAColor
    ) -> Union["XATerminalSettingsSet", None]:
        for settings_set in self.xa_elem:
            if settings_set.backgroundColor() == background_color.xa_elem:
                return self._new_element(settings_set, XATerminalSettingsSet)

    def by_normal_text_color(
        self, normal_text_color: XABase.XAColor
    ) -> Union["XATerminalSettingsSet", None]:
        for settings_set in self.xa_elem:
            if settings_set.normalTextColor() == normal_text_color.xa_elem:
                return self._new_element(settings_set, XATerminalSettingsSet)

    def by_bold_text_color(
        self, bold_text_color: XABase.XAColor
    ) -> Union["XATerminalSettingsSet", None]:
        for settings_set in self.xa_elem:
            if settings_set.boldTextColor() == bold_text_color.xa_elem:
                return self._new_element(settings_set, XATerminalSettingsSet)

    def by_font_name(self, font_name: str) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("fontName", font_name)

    def by_font_size(self, font_size: int) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("fontSize", font_size)

    def by_font_antialiasing(
        self, font_antialiasing: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("fontAntialiasing", font_antialiasing)

    def by_clean_commands(
        self, clean_commands: list[str]
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("cleanCommands", clean_commands)

    def by_title_displays_device_name(
        self, title_displays_device_name: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("titleDisplaysDeviceName", title_displays_device_name)

    def by_title_displays_shell_path(
        self, title_displays_shell_path: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("titleDisplaysShellPath", title_displays_shell_path)

    def by_title_displays_window_size(
        self, title_displays_window_size: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("titleDisplaysWindowSize", title_displays_window_size)

    def by_title_displays_settings_name(
        self, title_displays_settings_name: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property(
            "titleDisplaysSettingsName", title_displays_settings_name
        )

    def by_title_displays_custom_title(
        self, title_displays_custom_title: bool
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("titleDisplaysCustomTitle", title_displays_custom_title)

    def by_custom_title(
        self, custom_title: str
    ) -> Union["XATerminalSettingsSet", None]:
        return self.by_property("customTitle", custom_title)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each settings set in the list.

        When the clipboard content is set to a list of settings sets, each setting set's name is added to the clipboard.

        :return: The list of setting set names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XATerminalSettingsSet(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with settings sets in Terminal.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique identifier of the settings set."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the settings set."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def number_of_rows(self) -> int:
        """The number of rows displayed in the tab."""
        return self.xa_elem.numberOfRows()

    @number_of_rows.setter
    def number_of_rows(self, number_of_rows: int):
        self.set_property("numberOfRows", number_of_rows)

    @property
    def number_of_columns(self) -> int:
        """The number of columns displayed in the tab."""
        return self.xa_elem.numberOfColumns()

    @number_of_columns.setter
    def number_of_columns(self, number_of_columns: int):
        self.set_property("numberOfColumns", number_of_columns)

    @property
    def cursor_color(self) -> XABase.XAColor:
        """The cursor color for the tab."""
        return XABase.XAColor(self.xa_elem.cursorColor())

    @cursor_color.setter
    def cursor_color(self, cursor_color: XABase.XAColor):
        self.set_property("cursorColor", cursor_color.xa_elem)

    @property
    def background_color(self) -> XABase.XAColor:
        """The background color for the tab."""
        return XABase.XAColor(self.xa_elem.backgroundColor())

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property("backgroundColor", background_color.xa_elem)

    @property
    def normal_text_color(self) -> XABase.XAColor:
        """The normal text color for the tab."""
        return XABase.XAColor(self.xa_elem.normalTextColor())

    @normal_text_color.setter
    def normal_text_color(self, normal_text_color: XABase.XAColor):
        self.set_property("normalTextColor", normal_text_color.xa_elem)

    @property
    def bold_text_color(self) -> XABase.XAColor:
        """The bold text color for the tab."""
        return XABase.XAColor(self.xa_elem.boldTextColor())

    @bold_text_color.setter
    def bold_text_color(self, bold_text_color: XABase.XAColor):
        self.set_property("boldTextColor", bold_text_color.xa_elem)

    @property
    def font_name(self) -> str:
        """The name of the font used to display the tab's contents."""
        return self.xa_elem.fontName()

    @font_name.setter
    def font_name(self, font_name: str):
        self.set_property("fontName", font_name)

    @property
    def font_size(self) -> int:
        """The size of the font used to display the tab's contents."""
        return self.xa_elem.fontSize()

    @font_size.setter
    def font_size(self, font_size: int):
        self.set_property("fontSize", font_size)

    @property
    def font_antialiasing(self) -> bool:
        """Whether the font used to display the tab's contents is antialiased."""
        return self.xa_elem.fontAntialiasing()

    @font_antialiasing.setter
    def font_antialiasing(self, font_antialiasing: bool):
        self.set_property("fontAntialiasing", font_antialiasing)

    @property
    def clean_commands(self) -> list[str]:
        """The processes which will be ignored when checking whether a tab can be closed without showing a prompt."""
        return list(self.xa_elem.cleanCommands())

    @clean_commands.setter
    def clean_commands(self, clean_commands: list[str]):
        self.set_property("cleanCommands", clean_commands)

    @property
    def title_displays_device_name(self) -> bool:
        """Whether the title contains the device name."""
        return self.xa_elem.titleDisplaysDeviceName()

    @title_displays_device_name.setter
    def title_displays_device_name(self, title_displays_device_name: bool):
        self.set_property("titleDisplaysDeviceName", title_displays_device_name)

    @property
    def title_displays_shell_path(self) -> bool:
        """Whether the title contains the shell path."""
        return self.xa_elem.titleDisplaysShellPath()

    @title_displays_shell_path.setter
    def title_displays_shell_path(self, title_displays_shell_path: bool):
        self.set_property("titleDisplaysShellPath", title_displays_shell_path)

    @property
    def title_displays_window_size(self) -> bool:
        """Whether the title contains the tab's size, in rows and columns."""
        return self.xa_elem.titleDisplaysWindowSize()

    @title_displays_window_size.setter
    def title_displays_window_size(self, title_displays_window_size: bool):
        self.set_property("titleDisplaysWindowSize", title_displays_window_size)

    @property
    def title_displays_settings_name(self) -> bool:
        """Whether the title contains the settings set name."""
        return self.xa_elem.titleDisplaysSettingsName()

    @title_displays_settings_name.setter
    def title_displays_settings_name(self, title_displays_settings_name: bool):
        self.set_property("titleDisplaysSettingsName", title_displays_settings_name)

    @property
    def title_displays_custom_title(self) -> bool:
        """Whether the title contains a custom title."""
        return self.xa_elem.titleDisplaysCustomTitle()

    @title_displays_custom_title.setter
    def title_displays_custom_title(self, title_displays_custom_title: bool):
        self.set_property("titleDisplaysCustomTitle", title_displays_custom_title)

    @property
    def custom_title(self) -> str:
        """The tab's custom title."""
        return self.xa_elem.customTitle()

    @custom_title.setter
    def custom_title(self, custom_title: str):
        self.set_property("customTitle", custom_title)

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the settings set.

        When the clipboard content is set to a settings set, the setting set's name is added to the clipboard.

        :return: The setting set's name
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"
