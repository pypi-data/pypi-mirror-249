""".. versionadded:: 0.1.0

Control the macOS System Events application using JXA-like syntax.
"""
from datetime import datetime
from enum import Enum
from pprint import pprint
from time import sleep
from typing import Any, Union

import Quartz

from PyXA import XABase
from PyXA.XABase import OSType
from PyXA import XABaseScriptable
from PyXA.XAEvents import KEYCODES
from PyXA.XAProtocols import XACanPrintPath, XACloseable, XAPrintable, XASelectable


class XASystemEventsApplication(
    XABase.XAEventsApplication, XABaseScriptable.XASBApplication, XACanPrintPath
):
    """A class for managing and interacting with System Events.app.

    .. versionadded:: 0.1.0
    """

    class ObjectType(Enum):
        """Types of objects that can be created."""

        LOGIN_ITEM = "login_item"
        FILE = "file"
        FOLDER = "folder"

    class DynamicStyle(Enum):
        """Options for the dynamic style of the desktop background."""

        AUTO = OSType(
            "atmt"
        )  #: automatic (if supported, follows light/dark appearance)
        DYNAMIC = OSType(
            "dynm"
        )  #: dynamic (if supported, updates desktop picture based on time and/or location)
        LIGHT = OSType("lite")  #: light style
        DARK = OSType("dark")  #: dark style
        UNKNOWN = OSType("unk\?")  #: unknown style

    class DoubleClickBehavior(Enum):
        """Options for double click behaviors."""

        MINIMIZE = OSType("ddmi")  #: Minimize
        OFF = OSType("ddof")  #: Off
        ZOOM = OSType("ddzo")  #: Zoom

    class MinimizeEffect(Enum):
        """Options for the effect to use when minimizing applications."""

        GENIE = OSType("geni")  #: Genie effect
        SCALE = OSType("scal")  #: Scale effect

    class ScreenLocation(Enum):
        """Locations on the screen."""

        BOTTOM = OSType("bott")  #: Bottom of screen
        LEFT = OSType("left")  #: Left side of screen
        RIGHT = OSType("righ")  #: Right side of screen

    class ScrollPageBehavior(Enum):
        """Scroll page behaviors."""

        JUMP_TO_HERE = OSType("tohr")  #: Jump to here
        JUMP_TO_NEXT_PAGE = OSType("nxpg")  #: Jump to next page

    class FontSmoothingStyle(Enum):
        """Font smoothing styles."""

        AUTOMATIC = OSType("autm")
        LIGHT = OSType("lite")
        MEDIUM = OSType("medi")
        STANDARD = OSType("stnd")
        STRONG = OSType("strg")

    class Appearance(Enum):
        """Appearance colors."""

        BLUE = OSType("blue")
        GRAPHITE = OSType("grft")

    class HighlightColor(Enum):
        """Highlight colors."""

        BLUE = OSType("blue")
        GOLD = OSType("gold")
        GRAPHITE = OSType("grft")
        GREEN = OSType("gren")
        ORANGE = OSType("orng")
        PURPLE = OSType("prpl")
        RED = OSType("red ")
        SILVER = OSType("slvr")

    class MediaInsertionAction(Enum):
        """Actions to perform when media is inserted."""

        ASK_WHAT_TO_DO = OSType("dhas")
        IGNORE = OSType("dhig")
        OPEN_APPLICATION = OSType("dhap")
        RUN_A_SCRIPT = OSType("dhrs")

    class Key(Enum):
        """Keys and key actions."""

        COMMAND = 0
        CONTROL = 1
        OPTION = 2
        SHIFT = 3
        CAPS_LOCK = 4
        FUNCTION = 5

    class AccessRight(Enum):
        """Access right levels."""

        NONE = OSType("none")
        READ = OSType("read")  #: Read only
        READ_WRITE = OSType("rdwr")  #: Read and write
        WRITE = OSType("writ")  #: Write only

    class PictureRotation(Enum):
        """Desktop image picture rotation settings."""

        NEVER = 0
        USING_INTERVAL = 1
        USING_LOGIN = 2
        AFTER_SLEEP = 3

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Is this the active application?"""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of the application."""
        return self.xa_scel.version()

    @property
    def quit_delay(self) -> int:
        """The time in seconds the application will idle before quitting; if set to zero, idle time will not cause the application to quit."""
        return self.xa_scel.quitDelay()

    @quit_delay.setter
    def quit_delay(self, quit_delay: int):
        self.set_property("quitDelay", quit_delay)

    @property
    def script_menu_enabled(self) -> bool:
        """Is the Script menu installed in the menu bar?"""
        return self.xa_scel.scriptMenuEnabled()

    @property
    def current_user(self) -> "XASystemEventsUser":
        """The currently logged in user."""
        return self._new_element(self.xa_scel.currentUser(), XASystemEventsUser)

    @property
    def appearance_preferences(self) -> "XASystemEventsAppearancePreferencesObject":
        """A collection of appearance preferences."""
        return self._new_element(
            self.xa_scel.appearancePreferences(),
            XASystemEventsAppearancePreferencesObject,
        )

    @appearance_preferences.setter
    def appearance_preferences(
        self, appearance_preferences: "XASystemEventsAppearancePreferencesObject"
    ):
        self.set_property("appearancePreferences", appearance_preferences.xa_elem)

    @property
    def cd_and_dvd_preferences(self) -> "XASystemEventsCDAndDVDPreferencesObject":
        """The preferences for the current user when a CD or DVD is inserted."""
        return self._new_element(
            self.xa_scel.CDAndDVDPreferences(), XASystemEventsCDAndDVDPreferencesObject
        )

    @cd_and_dvd_preferences.setter
    def cd_and_dvd_preferences(
        self, cd_and_dvd_preferences: "XASystemEventsCDAndDVDPreferencesObject"
    ):
        self.set_property("cd_and_dvd_preferences", cd_and_dvd_preferences.xa_elem)

    @property
    def current_desktop(self) -> "XASystemEventsDesktop":
        """The primary desktop."""
        return self._new_element(self.xa_scel.currentDesktop(), XASystemEventsDesktop)

    @property
    def dock_preferences(self) -> "XASystemEventsDockPreferencesObject":
        """The preferences for the current user's dock."""
        return self._new_element(
            self.xa_scel.dockPreferences(), XASystemEventsDockPreferencesObject
        )

    @dock_preferences.setter
    def dock_preferences(self, dock_preferences: "XASystemEventsDockPreferencesObject"):
        self.set_property("dock_preferences", dock_preferences.xa_elem)

    @property
    def network_preferences(self) -> "XASystemEventsNetworkPreferencesObject":
        """The preferences for the current user's network."""
        return self._new_element(
            self.xa_scel.networkPreferences(), XASystemEventsNetworkPreferencesObject
        )

    @network_preferences.setter
    def network_preferences(
        self, network_preferences: "XASystemEventsNetworkPreferencesObject"
    ):
        self.set_property("network_preferences", network_preferences.xa_elem)

    @property
    def current_screen_saver(self) -> "XASystemEventsScreenSaver":
        """The currently selected screen saver."""
        return self._new_element(
            self.xa_scel.currentScreenSaver(), XASystemEventsScreenSaver
        )

    @current_screen_saver.setter
    def current_screen_saver(self, current_screen_saver: "XASystemEventsScreenSaver"):
        self.set_property("currentScreenSaver", current_screen_saver.xa_elem)

    @property
    def screen_saver_preferences(self) -> "XASystemEventsScreenSaverPreferencesObject":
        """The preferences common to all screen savers."""
        return self._new_element(
            self.xa_scel.screenSaverPreferences(),
            XASystemEventsScreenSaverPreferencesObject,
        )

    @screen_saver_preferences.setter
    def screen_saver_preferences(
        self, screen_saver_preferences: "XASystemEventsScreenSaverPreferencesObject"
    ):
        self.set_property("screenSaverPreferences", screen_saver_preferences.xa_elem)

    @property
    def security_preferences(self) -> "XASystemEventsSecurityPreferencesObject":
        """A collection of security preferences."""
        return self._new_element(
            self.xa_scel.securityPreferences(), XASystemEventsSecurityPreferencesObject
        )

    @security_preferences.setter
    def security_preferences(
        self, security_preferences: "XASystemEventsSecurityPreferencesObject"
    ):
        self.set_property("securityPreferences", security_preferences.xa_elem)

    @property
    def application_support_folder(self) -> "XABase.XAFolder":
        """The Application Support folder."""
        return self._new_element(
            self.xa_scel.applicationSupportFolder(), XABase.XAFolder
        )

    @property
    def applications_folder(self) -> "XABase.XAFolder":
        """The user's Applications folder."""
        return self._new_element(self.xa_scel.applicationsFolder(), XABase.XAFolder)

    @property
    def classic_domain(self) -> "XABase.XAClassicDomainObject":
        """The collection of folders belonging to the Classic System."""
        return self._new_element(
            self.xa_scel.ClassicDomain(), XABase.XAClassicDomainObject
        )

    @property
    def desktop_folder(self) -> "XABase.XAFolder":
        """The user's Desktop folder."""
        return self._new_element(self.xa_scel.desktopFolder(), XABase.XAFolder)

    @property
    def desktop_pictures_folder(self) -> "XABase.XAFolder":
        """The Desktop Pictures folder."""
        return self._new_element(self.xa_scel.desktopPicturesFolder(), XABase.XAFolder)

    @property
    def documents_folder(self) -> "XABase.XAFolder":
        """The user's Documents folder."""
        return self._new_element(self.xa_scel.documentsFolder(), XABase.XAFolder)

    @property
    def downloads_folder(self) -> "XABase.XAFolder":
        """The user's Downloads folder."""
        return self._new_element(self.xa_scel.downloadsFolder(), XABase.XAFolder)

    @property
    def favorites_folder(self) -> "XABase.XAFolder":
        """The user's Favorites folder."""
        return self._new_element(self.xa_scel.favoritesFolder(), XABase.XAFolder)

    @property
    def folder_action_scripts_folder(self) -> "XABase.XAFolder":
        """The user's Folder Action Scripts folder."""
        return self._new_element(
            self.xa_scel.FolderActionScriptsFolder(), XABase.XAFolder
        )

    @property
    def fonts_folder(self) -> "XABase.XAFolder":
        """The Fonts folder."""
        return self._new_element(self.xa_scel.fontsFolder(), XABase.XAFolder)

    @property
    def home_folder(self) -> "XABase.XAFolder":
        """The Home folder of the currently logged in user."""
        return self._new_element(self.xa_scel.homeFolder(), XABase.XAFolder)

    @property
    def library_folder(self) -> "XABase.XAFolder":
        """The Library folder."""
        return self._new_element(self.xa_scel.libraryFolder(), XABase.XAFolder)

    @property
    def local_domain(self) -> "XABase.XALocalDomainObject":
        """The collection of folders residing on the Local machine."""
        return self._new_element(self.xa_scel.localDomain(), XABase.XALocalDomainObject)

    @property
    def movies_folder(self) -> "XABase.XAFolder":
        """The user's Movies folder."""
        return self._new_element(
            self.xa_scel.moviesFolder(), XABase.XALocalDomainObject
        )

    @property
    def music_folder(self) -> "XABase.XAFolder":
        """The user's Music folder."""
        return self._new_element(self.xa_scel.musicFolder(), XABase.XAFolder)

    @property
    def network_domain(self) -> "XABase.XANetworkDomainObject":
        """The collection of folders residing on the Network."""
        return self._new_element(
            self.xa_scel.networkDomain(), XABase.XANetworkDomainObject
        )

    @property
    def pictures_folder(self) -> "XABase.XAFolder":
        """The user's Pictures folder."""
        return self._new_element(self.xa_scel.picturesFolder(), XABase.XAFolder)

    @property
    def preferences_folder(self) -> "XABase.XAFolder":
        """The user's Preferences folder."""
        return self._new_element(self.xa_scel.preferencesFolder(), XABase.XAFolder)

    @property
    def public_folder(self) -> "XABase.XAFolder":
        """The user's Public folder."""
        return self._new_element(self.xa_scel.publicFolder(), XABase.XAFolder)

    @property
    def scripting_additions_folder(self) -> "XABase.XAFolder":
        """The Scripting Additions folder."""
        return self._new_element(
            self.xa_scel.scriptingAdditionsFolder(), XABase.XAFolder
        )

    @property
    def scripts_folder(self) -> "XABase.XAFolder":
        """The user's Scripts folder."""
        return self._new_element(self.xa_scel.scriptsFolder(), XABase.XAFolder)

    @property
    def shared_documents_folder(self) -> "XABase.XAFolder":
        """The Shared Documents folder."""
        return self._new_element(self.xa_scel.sharedDocumentsFolder(), XABase.XAFolder)

    @property
    def sites_folder(self) -> "XABase.XAFolder":
        """The user's Sites folder."""
        return self._new_element(self.xa_scel.sitesFolder(), XABase.XAFolder)

    @property
    def speakable_items_folder(self) -> "XABase.XAFolder":
        """The Speakable Items folder."""
        return self._new_element(self.xa_scel.speakableItemsFolder(), XABase.XAFolder)

    @property
    def startup_disk(self) -> "XABase.XADisk":
        """The disk from which Mac OS X was loaded."""
        return self._new_element(self.xa_scel.startupDisk(), XABase.XADisk)

    @property
    def system_domain(self) -> "XABase.XASystemDomainObject":
        """The collection of folders belonging to the System."""
        return self._new_element(
            self.xa_scel.systemDomain(), XABase.XASystemDomainObject
        )

    @property
    def temporary_items_folder(self) -> "XABase.XAFolder":
        """The Temporary Items folder."""
        return self._new_element(self.xa_scel.temporaryItemsFolder(), XABase.XAFolder)

    @property
    def trash(self) -> "XABase.XAFolder":
        """The user's Trash folder."""
        return self._new_element(self.xa_scel.trash(), XABase.XAFolder)

    @property
    def user_domain(self) -> "XABase.XAUserDomainObject":
        """The collection of folders belonging to the User."""
        return self._new_element(self.xa_scel.userDomain(), XABase.XAUserDomainObject)

    @property
    def utilities_folder(self) -> "XABase.XAFolder":
        """The Utilities folder."""
        return self._new_element(self.xa_scel.utilitiesFolder(), XABase.XAFolder)

    @property
    def workflows_folder(self) -> "XABase.XAFolder":
        """The Automator Workflows folder."""
        return self._new_element(self.xa_scel.workflowsFolder(), XABase.XAFolder)

    @property
    def folder_actions_enabled(self) -> bool:
        """Are Folder Actions currently being processed?"""
        return self.xa_scel.folderActionsEnabled()

    @folder_actions_enabled.setter
    def folder_actions_enabled(self, folder_actions_enabled: bool):
        self.set_property("folderActionsEnabled", folder_actions_enabled)

    @property
    def ui_elements_enabled(self) -> bool:
        """Are UI element events currently being processed?"""
        return self.xa_scel.UIElementsEnabled()

    @property
    def scripting_definition(self) -> "XASystemEventsScriptingDefinitionObject":
        """The scripting definition of the System Events application."""
        return self._new_element(
            self.xa_scel.scriptingDefinition(), XASystemEventsScriptingDefinitionObject
        )

    def log_out(self):
        """Logs out the current user.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.logOut()

    def restart(self, state_saving_preference: bool = False):
        """Restarts the computer.

        :param state_saving_preference: Whether the user defined state saving preference is followed, defaults to False (always saved)
        :type state_saving_preference: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_scel.restartStateSavingPreference_(state_saving_preference)

    def shut_down(self, state_saving_preference: bool = False):
        """Shuts down the computer.

        :param state_saving_preference: Whether the user defined state saving preference is followed, defaults to False (always saved)
        :type state_saving_preference: bool, optional

        .. versionadded:: 0.1.0
        """
        self.xa_scel.shutDownStateSavingPreference_(state_saving_preference)

    def sleep(self):
        """Puts the computer to sleep.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.sleep()

    def begin_transaction(self) -> int:
        """Discards the results of a bounded update session with one or more files.

        :return: _description_
        :rtype: int
        """
        return self.xa_scel.beginTransaction()

    def end_transaction(self):
        """Ends the current transaction gracefully.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.endTransaction()

    def abort_transaction(self):
        """Aborts the current transaction.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.abortTransaction()

    def click(self):
        """Clicks on the application.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.click()

    def key_code(
        self,
        key_code: Union[int, list[int]],
        modifier: Union[
            "XASystemEventsApplication.Key", list["XASystemEventsApplication.Key"], None
        ] = None,
    ):
        """Cause the target (active) process to behave as if key codes were entered.

        :param key_code: The key code(s) to be sent
        :type key_code: Union[int, list[int]]
        :param modifier: _description_, defaults to None
        :type modifier: Union[XASystemEventsApplication.Key, list[XASystemEventsApplication.Key], None], optional

        .. versionadded:: 0.1.0
        """
        if not isinstance(key_code, list):
            key_code = [key_code]

        if not isinstance(modifier, list):
            modifier = [modifier]

        for key in key_code:
            key_down_event = Quartz.CGEventCreateKeyboardEvent(None, key, True)
            key_up_event = Quartz.CGEventCreateKeyboardEvent(None, key, False)

            for mod in modifier:
                if mod == XASystemEventsApplication.Key.COMMAND:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskCommand
                    )
                elif mod == XASystemEventsApplication.Key.CONTROL:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskControl
                    )
                elif mod == XASystemEventsApplication.Key.OPTION:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskAlternate
                    )
                elif mod == XASystemEventsApplication.Key.SHIFT:
                    Quartz.CGEventSetFlags(key_down_event, Quartz.kCGEventFlagMaskShift)
                elif mod == XASystemEventsApplication.Key.CAPS_LOCK:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskAlphaShift
                    )
                elif mod == XASystemEventsApplication.Key.FUNCTION:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskSecondaryFn
                    )

            Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_down_event)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_up_event)

    def key_stroke(
        self,
        keystroke: Union[int, list[int]],
        modifier: Union[
            "XASystemEventsApplication.Key", list["XASystemEventsApplication.Key"], None
        ] = None,
    ):
        """Cause the target (active) process to behave as if keystrokes were entered.

        :param keystroke: The keystrokes to be sent
        :type keystroke: Union[int, list[int]]
        :param modifier: _description_, defaults to None
        :type modifier: Union[XASystemEventsApplication.Key, list[XASystemEventsApplication.Key], None], optional

        .. versionadded:: 0.1.0
        """
        for key in keystroke:
            key = str(key).lower()
            if key in KEYCODES:
                key = KEYCODES[key]
            else:
                print("Unknown key(s).")

            if not isinstance(modifier, list):
                modifier = [modifier]

            key_down_event = Quartz.CGEventCreateKeyboardEvent(None, key, True)
            key_up_event = Quartz.CGEventCreateKeyboardEvent(None, key, False)

            for mod in modifier:
                if mod == XASystemEventsApplication.Key.COMMAND:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskCommand
                    )
                elif mod == XASystemEventsApplication.Key.CONTROL:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskControl
                    )
                elif mod == XASystemEventsApplication.Key.OPTION:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskAlternate
                    )
                elif mod == XASystemEventsApplication.Key.SHIFT:
                    Quartz.CGEventSetFlags(key_down_event, Quartz.kCGEventFlagMaskShift)
                elif mod == XASystemEventsApplication.Key.CAPS_LOCK:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskAlphaShift
                    )
                elif mod == XASystemEventsApplication.Key.FUNCTION:
                    Quartz.CGEventSetFlags(
                        key_down_event, Quartz.kCGEventFlagMaskSecondaryFn
                    )

            Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_down_event)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_up_event)

    def documents(
        self, filter: dict = None
    ) -> Union["XASystemEventsDocumentList", None]:
        """Returns a list of documents, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XASystemEventsDocumentList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.documents(), XASystemEventsDocumentList, filter
        )

    def users(self, filter: dict = None) -> Union["XASystemEventsUserList", None]:
        """Returns a list of users, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned users will have, or None
        :type filter: Union[dict, None]
        :return: The list of users
        :rtype: XASystemEventsUserList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.users(), XASystemEventsUserList, filter)

    def desktops(self, filter: dict = None) -> Union["XASystemEventsDesktopList", None]:
        """Returns a list of desktops, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned desktops will have, or None
        :type filter: Union[dict, None]
        :return: The list of desktops
        :rtype: XASystemEventsDesktopList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.desktops(), XASystemEventsDesktopList, filter
        )

    def login_items(
        self, filter: dict = None
    ) -> Union["XASystemEventsLoginItemList", None]:
        """Returns a list of login items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned login items will have, or None
        :type filter: Union[dict, None]
        :return: The list of login items
        :rtype: XASystemEventsLoginItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.loginItems(), XASystemEventsLoginItemList, filter
        )

    def screen_savers(
        self, filter: dict = None
    ) -> Union["XASystemEventsScreenSaverList", None]:
        """Returns a list of screen savers, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned screen savers will have, or None
        :type filter: Union[dict, None]
        :return: The list of screen savers
        :rtype: XASystemEventsScreenSaverList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.screenSavers(), XASystemEventsScreenSaverList, filter
        )

    def aliases(self, filter: dict = None) -> Union["XABase.XAAliasList", None]:
        """Returns a list of aliases, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned aliases will have, or None
        :type filter: Union[dict, None]
        :return: The list of aliases
        :rtype: XABase.XAAliasList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.aliases(), XABase.XAAliasList, filter)

    def disks(self, filter: dict = None) -> Union["XABase.XADiskList", None]:
        """Returns a list of disks, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned disks will have, or None
        :type filter: Union[dict, None]
        :return: The list of disks
        :rtype: XABase.XADiskList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.disks(), XABase.XADiskList, filter)

    def disk_items(self, filter: dict = None) -> Union["XABase.XADiskItemList", None]:
        """Returns a list of disk items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned disk items will have, or None
        :type filter: Union[dict, None]
        :return: The list of disk items
        :rtype: XABase.XADiskItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.diskItems(), XABase.XADiskItemList, filter
        )

    def domains(self, filter: dict = None) -> Union["XABase.XADomainList", None]:
        """Returns a list of domains, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned domains will have, or None
        :type filter: Union[dict, None]
        :return: The list of domains
        :rtype: XABase.XADomainList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.domains(), XABase.XADomainList, filter)

    def files(self, filter: dict = None) -> Union["XABase.XAFileList", None]:
        """Returns a list of files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned files will have, or None
        :type filter: Union[dict, None]
        :return: The list of files
        :rtype: XABase.XAFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.files(), XABase.XAFileList, filter)

    def file_packages(
        self, filter: dict = None
    ) -> Union["XABase.XAFilePackageList", None]:
        """Returns a list of file packages, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned file packages will have, or None
        :type filter: Union[dict, None]
        :return: The list of file packages
        :rtype: XABase.XAFilePackageList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.filePackages(), XABase.XAFilePackageList, filter
        )

    def folders(self, filter: dict = None) -> Union["XABase.XAFolderList", None]:
        """Returns a list of folders, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folders will have, or None
        :type filter: Union[dict, None]
        :return: The list of folders
        :rtype: XABase.XAFolderList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_scel.folders(), XABase.XAFolderList, filter)

    def folder_actions(
        self, filter: dict = None
    ) -> Union["XABase.XAFolderActionList", None]:
        """Returns a list of folder actions, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned folder actions will have, or None
        :type filter: Union[dict, None]
        :return: The list of folder actions
        :rtype: XABase.XAFolderActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.folderActions(), XABase.XAFolderActionList, filter
        )

    def application_processes(
        self, filter: dict = None
    ) -> Union["XASystemEventsApplicationProcessList", None]:
        """Returns a list of application processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsApplicationProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.applicationProcesses(),
            XASystemEventsApplicationProcessList,
            filter,
        )

    def desk_accessory_processes(
        self, filter: dict = None
    ) -> Union["XASystemEventsDeskAccessoryProcessList", None]:
        """Returns a list of desk accessory processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsDeskAccessoryProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.deskAccessoryProcesses(),
            XASystemEventsDeskAccessoryProcessList,
            filter,
        )

    def processes(
        self, filter: dict = None
    ) -> Union["XASystemEventsProcessList", None]:
        """Returns a list of processes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned processes will have, or None
        :type filter: Union[dict, None]
        :return: The list of processes
        :rtype: XASystemEventsProcessList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.processes(), XASystemEventsProcessList, filter
        )

    def ui_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned UI elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.UIElements(), XASystemEventsUIElementList, filter
        )

    def property_list_files(
        self, filter: dict = None
    ) -> Union["XASystemEventsPropertyListFileList", None]:
        """Returns a list of property list files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list files will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list files
        :rtype: XASystemEventsPropertyListFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.propertyListFiles(), XASystemEventsPropertyListFileList, filter
        )

    def property_list_items(
        self, filter: dict = None
    ) -> Union["XASystemEventsPropertyListItemList", None]:
        """Returns a list of property list items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list items will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list items
        :rtype: XASystemEventsPropertyListItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.propertyListItems(), XASystemEventsPropertyListItemList, filter
        )

    def xml_datas(
        self, filter: dict = None
    ) -> Union["XASystemEventsXMLDataList", None]:
        """Returns a list of XML datas, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML datas will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML datas
        :rtype: XASystemEventsXMLDataList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.xmlDatas(), XASystemEventsXMLDataList, filter
        )

    def xml_files(
        self, filter: dict = None
    ) -> Union["XASystemEventsXMLFileList", None]:
        """Returns a list of XML files, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML files will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML files
        :rtype: XASystemEventsXMLFileList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_scel.xmlFiles(), XASystemEventsXMLFileList, filter
        )

    def make(
        self,
        specifier: Union[str, "XASystemEventsApplication.ObjectType"],
        properties: dict,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XASystemEventsApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.1.0
        """
        if isinstance(specifier, XASystemEventsApplication.ObjectType):
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

        if specifier == "login_item":
            return self._new_element(obj, XASystemEventsLoginItem)
        elif specifier == "file":
            return self._new_element(obj, XABase.XAFile)
        elif specifier == "folder":
            return self._new_element(obj, XABase.XAFolder)


class XASystemEventsDocumentList(XABase.XAList):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> "XABase.XAFileList":
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return self._new_element(ls, XABase.XAFileList)

    def by_name(self, name: str) -> Union["XASystemEventsDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XASystemEventsDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: "XABase.XAFile") -> Union["XASystemEventsDocument", None]:
        return self.by_property("file", file.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsDocument(XABase.XAObject, XACloseable, XAPrintable):
    """A document of System Events.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """Its name."""
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Has it been modified since the last save?"""
        return self.xa_elem.modified()

    @property
    def file(self) -> "XABase.XAFile":
        """Its location on disk, if it has one."""
        return self._new_element(self.xa_elem.file(), XABase.XAFile)

    def save(self, path: Union[str, XABase.XAPath, None] = None):
        """Saves the document at the specified file path.

        :param path: The path to save the document at, defaults to None
        :type path: Union[str, XABase.XAPath, None], optional

        .. versionadded:: 0.1.0
        """
        if isinstance(path, str):
            path = XABase.XAPath(path)
        if path is not None:
            self.xa_elem.saveIn_as_(
                path.xa_elem, XASystemEventsApplication, XABase.OSType("ctxt")
            )


class XASystemEventsWindowList(XABaseScriptable.XASBWindowList):
    """A wrapper around a list of windows.

    .. versionadded:: 0.1.2
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        super().__init__(properties, filter, obj_class)
        if obj_class is None or issubclass(self.xa_prnt.xa_wcls, obj_class):
            self.xa_ocls = self.xa_prnt.xa_wcls

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def collapse(self) -> "XASystemEventsWindowList":
        """Collapses all windows in the list.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().collapse()

        .. versionadded:: 0.0.5
        """
        for window in self:
            window.collapse()
            sleep(0.025)
        return self

    def uncollapse(self) -> "XASystemEventsWindowList":
        """Uncollapses all windows in the list.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().uncollapse()

        .. versionadded:: 0.0.6
        """
        for window in self:
            window.uncollapse()
        return self

    def close(self):
        """Closes all windows in the list.add()

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Keychain Access")
        >>> app.windows().close()

        .. versionadded:: 0.0.6
        """
        for window in self:
            window.close()


class XASystemEventsWindow(XABaseScriptable.XASBWindow, XASelectable):
    """A window belonging to a process.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> XASystemEventsDocument:
        """The document whose contents are displayed in the window."""
        return self._new_element(self.xa_elem.document(), XASystemEventsDocument)

    @property
    def accessibility_description(self) -> Union[str, None]:
        """A more complete description of the window and its capabilities."""
        return self.xa_elem.accessibilityDescription()

    @property
    def object_description(self) -> Union[str, None]:
        """The accessibility description, if available; otherwise, the role description."""
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> Union[bool, None]:
        """Is the window enabled? (Does it accept clicks?)"""
        return self.xa_elem.enabled()

    @property
    def entire_contents(self) -> list[XABase.XAObject]:
        """A list of every UI element contained in this window and its child UI elements, to the limits of the tree."""
        return self._new_element(
            self.xa_elem.entireContents(), XASystemEventsUIElementList
        )

    @property
    def focused(self) -> Union[bool, None]:
        """Is the focus on this window?"""
        return self.xa_elem.focused()

    @focused.setter
    def focused(self, focused: bool):
        self.set_property("focused", focused)

    @property
    def help(self) -> Union[str, None]:
        """An elaborate description of the window and its capabilities."""
        return self.xa_elem.help()

    @property
    def maximum_value(self) -> Union[int, float, None]:
        """The maximum value that the UI element can take on."""
        return self.xa_elem.maximumValue()

    @property
    def minimum_value(self) -> Union[int, float, None]:
        """The minimum value that the UI element can take on."""
        return self.xa_elem.minimumValue()

    @property
    def name(self) -> str:
        """The name of the window, which identifies it within its container."""
        return self.xa_elem.name()

    @property
    def orientation(self) -> Union[str, None]:
        """The orientation of the window."""
        return self.xa_elem.orientation()

    @property
    def position(self) -> Union[list[Union[int, float]], None]:
        """The position of the window."""
        return self.xa_elem.position()

    @position.setter
    def position(self, position: list[Union[int, float]]):
        self.set_property("position", position)

    @property
    def role(self) -> str:
        """An encoded description of the window and its capabilities."""
        return self.xa_elem.role()

    @property
    def role_description(self) -> str:
        """A more complete description of the window's role."""
        return self.xa_elem.roleDescription()

    @property
    def selected(self) -> Union[bool, None]:
        """Is the window selected?"""
        return self.xa_elem.selected()

    @selected.setter
    def selected(self, selected: bool):
        self.set_property("selected", selected)

    @property
    def size(self) -> Union[list[Union[int, float]], None]:
        """The size of the window."""
        return self.xa_elem.size()

    @size.setter
    def size(self, size: list[Union[int, float]]):
        self.set_property("size", size)

    @property
    def subrole(self) -> Union[str, None]:
        """An encoded description of the window and its capabilities."""
        return self.xa_elem.subrole()

    @property
    def title(self) -> Union[str, None]:
        """The title of the window as it appears on the screen."""
        return self.xa_elem.title()

    @property
    def value(self) -> Any:
        """The current value of the window."""
        return self.xa_elem.value()

    def close(self) -> "XASystemEventsWindow":
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XASystemEventsWindow

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.close()

        .. versionadded:: 0.0.1
        """
        try:
            close_button = self.buttons().by_subrole("AXCloseButton")
            close_button.click()
        except:
            pass
        return self

    def collapse(self) -> "XASystemEventsWindow":
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XASystemEventsWindow

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.collapse()

        .. versionadded:: 0.0.1
        """
        try:
            button = self.buttons().by_subrole("AXMinimizeButton")
            button.click()
            while self.visible:
                sleep(0.01)
        except:
            pass
        return self

    def uncollapse(self) -> "XASystemEventsWindow":
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XASystemEventsWindow

        :Example:

        >>> import PyXA
        >>> PyXA.Application("App Store").front_window.uncollapse()

        .. versionadded:: 0.0.1
        """
        dock_process = self.xa_sevt.application_processes().by_name("Dock")
        app_icon = dock_process.lists()[0].ui_elements().by_name(self.name)
        if app_icon is not None:
            app_icon.actions()[0].perform()
            while not self.visible:
                sleep(0.01)
        return self

    def actions(self, filter: dict = None) -> Union["XASystemEventsActionList", None]:
        """Returns a list of action elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of actions
        :rtype: XASystemEventsActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.actions(), XASystemEventsActionList)

    def attributes(
        self, filter: dict = None
    ) -> Union["XASystemEventsAttributeList", None]:
        """Returns a list of attribute elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of attributes
        :rtype: XASystemEventsAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.attributes(), XASystemEventsAttributeList)

    def browsers(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of browser elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.browsers(), XASystemEventsUIElementList)

    def busy_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of busy indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of busy indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.busyIndicators(), XASystemEventsUIElementList
        )

    def buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.buttons(), XASystemEventsUIElementList)

    def checkboxes(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of checkbox elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of checkboxes
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.checkboxes(), XASystemEventsUIElementList)

    def color_wells(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of color well elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of color wells
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.colorWells(), XASystemEventsUIElementList)

    def combo_boxes(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of combo box elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of combo boxes
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.comboBoxes(), XASystemEventsUIElementList)

    def drawers(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of drawer elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of drawers
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.drawers(), XASystemEventsUIElementList)

    def groups(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.groups(), XASystemEventsUIElementList)

    def grow_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of grow area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of grow areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.growAreas(), XASystemEventsUIElementList)

    def images(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of image elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.images(), XASystemEventsUIElementList)

    def incrementors(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of incrementor elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of incrementors
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.incrementors(), XASystemEventsUIElementList
        )

    def lists(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of list elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of lists
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.lists(), XASystemEventsUIElementList)

    def menu_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.menuButtons(), XASystemEventsUIElementList
        )

    def outlines(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of outline elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.outlines(), XASystemEventsUIElementList)

    def pop_overs(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of pop-over elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-overs
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popOvers(), XASystemEventsUIElementList)

    def pop_up_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of pop-up button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-up buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.popUpButtons(), XASystemEventsUIElementList
        )

    def progress_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of progress indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of progress indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.progressIndicators(), XASystemEventsUIElementList
        )

    def radio_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of radio button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.radioButtons(), XASystemEventsUIElementList
        )

    def radio_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of radio group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.radioGroups(), XASystemEventsUIElementList
        )

    def relevance_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of relevance indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of relevance indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.relevanceIndicators(), XASystemEventsUIElementList
        )

    def scroll_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of scroll area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scrollAreas(), XASystemEventsUIElementList
        )

    def scroll_bars(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of scroll bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll bars
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollBars(), XASystemEventsUIElementList)

    def sheets(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of sheet elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sheets(), XASystemEventsUIElementList)

    def sliders(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of slider elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sliders
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sliders(), XASystemEventsUIElementList)

    def splitters(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of splitter elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitters
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitters(), XASystemEventsUIElementList)

    def splitter_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of splitter group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitter groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.splitterGroups(), XASystemEventsUIElementList
        )

    def static_texts(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of static text elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of static texts
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.staticTexts(), XASystemEventsUIElementList
        )

    def tab_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of tab group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tab groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tabGroups(), XASystemEventsUIElementList)

    def tables(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of table elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tables(), XASystemEventsUIElementList)

    def text_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of text area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textAreas(), XASystemEventsUIElementList)

    def text_fields(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of text fields elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text fields
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textFields(), XASystemEventsUIElementList)

    def toolbars(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of toolbar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsUIElementList)

    def ui_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.UIElements(), XASystemEventsUIElementList)

    def click(self, point: Union[tuple[int, int], None] = None):
        """Cause the window.

        :param point: The coordinate location at which to click, defaults to None
        :type point: Union[tuple[int, int], None], optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.clickAt_(point)

    def increment(self):
        """Increments the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.increment()

    def decrement(self):
        """Decrements the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.decrement()

    def confirm(self):
        """Confirms the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.confirm()

    def pick(self):
        """Picks the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.pick()

    def cancel(self):
        """Cancels the window, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cancel()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XASystemEventsUserList(XABase.XAList):
    """A wrapper around lists of users that employs fast enumeration techniques.

    All properties of users can be called as methods on the wrapped list, returning a list containing each user's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsUser, filter)

    def full_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fullName") or [])

    def home_directory(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("homeDirectory") or []
        return [XABase.XAPath(x) for x in ls]

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def picture_path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("picturePath") or []
        return [XABase.XAPath(x) for x in ls]

    def by_full_name(self, full_name: str) -> Union["XASystemEventsUser", None]:
        return self.by_property("fullName", full_name)

    def by_home_directory(
        self, home_directory: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsUser", None]:
        if isinstance(home_directory, str):
            home_directory = XABase.XAPath(home_directory)
        return self.by_property("homeDirectory", home_directory.xa_elem)

    def by_name(self, name: str) -> Union["XASystemEventsUser", None]:
        return self.by_property("name", name)

    def by_picture_path(
        self, picture_path: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsUser", None]:
        if isinstance(picture_path, str):
            picture_path = XABase.XAPath(picture_path)
        return self.by_property("picturePath", picture_path.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.full_name()) + ">"


class XASystemEventsUser(XABase.XAObject):
    """A user of the system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def full_name(self) -> str:
        """The user's full name."""
        return self.xa_elem.fullName()

    @property
    def home_directory(self) -> XABase.XAPath:
        """The path to user's home directory."""
        return XABase.XAPath(self.xa_elem.homeDirectory())

    @property
    def name(self) -> str:
        """The user's short name."""
        return self.xa_elem.name()

    @property
    def picture_path(self) -> XABase.XAPath:
        """Path to user's picture. Can be set for current user only!"""
        return XABase.XAPath(self.xa_elem.picturePath())

    @picture_path.setter
    def picture_path(self, picture_path: Union[XABase.XAPath, str]):
        if isinstance(picture_path, str):
            self.set_property("picturePath", picture_path)
        else:
            self.set_property("picturePath", picture_path.xa_elem)


class XASystemEventsAppearancePreferencesObject(XABase.XAObject):
    """A collection of appearance preferences.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def appearance(self) -> XASystemEventsApplication.Appearance:
        """The overall look of buttons, menus and windows."""
        return XASystemEventsApplication.Appearance(self.xa_elem.appearance())

    @appearance.setter
    def appearance(self, appearance: XASystemEventsApplication.Appearance):
        self.set_property("appearance", appearance.value)

    @property
    def font_smoothing(self) -> bool:
        """Is font smoothing on?"""
        return self.xa_elem.fontSmoothing()

    @font_smoothing.setter
    def font_smoothing(self, font_smoothing: bool):
        self.set_property("fontSmoothing", font_smoothing)

    @property
    def font_smoothing_style(self) -> XASystemEventsApplication.FontSmoothingStyle:
        """The method used for smoothing fonts."""
        return XASystemEventsApplication.FontSmoothingStyle(
            self.xa_elem.fontSmoothingStyle()
        )

    @font_smoothing_style.setter
    def font_smoothing_style(
        self, font_smoothing_style: XASystemEventsApplication.FontSmoothingStyle
    ):
        self.set_property("fontSmoothingStyle", font_smoothing_style.value)

    @property
    def highlight_color(self) -> XASystemEventsApplication.HighlightColor:
        """The color used for hightlighting selected text and lists."""
        return XASystemEventsApplication.HighlightColor(self.xa_elem.highlightColor())

    @highlight_color.setter
    def highlight_color(
        self, highlight_color: XASystemEventsApplication.HighlightColor
    ):
        self.set_property("highlightColor", highlight_color.value)

    @property
    def recent_applications_limit(self) -> int:
        """The number of recent applications to track."""
        return self.xa_elem.recentApplicationsLimit()

    @recent_applications_limit.setter
    def recent_applications_limit(self, recent_applications_limit: int):
        self.set_property("recentApplicationsLimit", recent_applications_limit)

    @property
    def recent_documents_limit(self) -> int:
        """The number of recent documents to track."""
        return self.xa_elem.recentDocumentsLimit()

    @recent_documents_limit.setter
    def recent_documents_limit(self, recent_documents_limit: int):
        self.set_property("recentDocumentsLimit", recent_documents_limit)

    @property
    def recent_servers_limit(self) -> int:
        """The number of recent servers to track."""
        return self.xa_elem.recentServersLimit()

    @recent_servers_limit.setter
    def recent_servers_limit(self, recent_servers_limit: int):
        self.set_property("recentServersLimit", recent_servers_limit)

    @property
    def scroll_bar_action(self) -> XASystemEventsApplication.ScrollPageBehavior:
        """The action performed by clicking the scroll bar."""
        return XASystemEventsApplication.ScrollPageBehavior(
            self.xa_elem.scrollBarAction()
        )

    @scroll_bar_action.setter
    def scroll_bar_action(
        self, scroll_bar_action: XASystemEventsApplication.ScrollPageBehavior
    ):
        self.set_property("scrollBarAction", scroll_bar_action.value)

    @property
    def smooth_scrolling(self) -> bool:
        """Is smooth scrolling used?"""
        return self.xa_elem.smoothScrolling()

    @smooth_scrolling.setter
    def smooth_scrolling(self, smooth_scrolling: bool):
        self.set_property("smoothScrolling", smooth_scrolling)

    @property
    def dark_mode(self) -> bool:
        """Whether to use dark menu bar and dock."""
        return self.xa_elem.darkMode()

    @dark_mode.setter
    def dark_mode(self, dark_mode: bool):
        self.set_property("darkMode", dark_mode)


class XASystemEventsCDAndDVDPreferencesObject(XABase.XAObject):
    """The user's CD and DVD insertion preferences.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def blank_cd(self) -> "XASystemEventsInsertionPreference":
        """The blank CD insertion preference."""
        return self._new_element(
            self.xa_elem.blankCD(), XASystemEventsInsertionPreference
        )

    @property
    def blank_dvd(self) -> "XASystemEventsInsertionPreference":
        """The blank DVD insertion preference."""
        return self._new_element(
            self.xa_elem.blankDVD(), XASystemEventsInsertionPreference
        )

    @property
    def blank_bd(self) -> "XASystemEventsInsertionPreference":
        """The blank BD insertion preference."""
        return self._new_element(
            self.xa_elem.blankBD(), XASystemEventsInsertionPreference
        )

    @property
    def music_cd(self) -> "XASystemEventsInsertionPreference":
        """The music CD insertion preference."""
        return self._new_element(
            self.xa_elem.musicCD(), XASystemEventsInsertionPreference
        )

    @property
    def picture_cd(self) -> "XASystemEventsInsertionPreference":
        """The picture CD insertion preference."""
        return self._new_element(
            self.xa_elem.pictureCD(), XASystemEventsInsertionPreference
        )

    @property
    def video_dvd(self) -> "XASystemEventsInsertionPreference":
        """The video DVD insertion preference."""
        return self._new_element(
            self.xa_elem.videoDVD(), XASystemEventsInsertionPreference
        )

    @property
    def video_bd(self) -> "XASystemEventsInsertionPreference":
        """The video BD insertion preference."""
        return self._new_element(
            self.xa_elem.videoBD(), XASystemEventsInsertionPreference
        )


class XASystemEventsInsertionPreference(XABase.XAObject):
    """A specific insertion preference.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def custom_application(self) -> Union[str, None]:
        """Application to launch or activate on the insertion of media."""
        return self.xa_elem.customApplication()

    @custom_application.setter
    def custom_application(self, custom_application: Union[str, None]):
        self.set_property("customApplication", custom_application)

    @property
    def custom_script(self) -> Union[str, None]:
        """AppleScript to launch or activate on the insertion of media."""
        return self.xa_elem.customScript()

    @custom_script.setter
    def custom_script(self, custom_script: Union[str, None]):
        self.set_property("customScript", custom_script)

    @property
    def insertion_action(self) -> XASystemEventsApplication.MediaInsertionAction:
        """The action to perform on media insertion."""
        return XASystemEventsApplication.MediaInsertionAction(
            self.xa_elem.insertionAction()
        )

    @insertion_action.setter
    def insertion_action(
        self, insertion_action: XASystemEventsApplication.MediaInsertionAction
    ):
        self.set_property("insertionAction", insertion_action.value)


class XASystemEventsDesktopList(XABase.XAList):
    """A wrapper around lists of desktops that employs fast enumeration techniques.

    All properties of desktops can be called as methods on the wrapped list, returning a list containing each desktop's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsUser, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def change_interval(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("changeInterval") or [])

    def display_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName") or [])

    def picture(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("picture") or []
        return [XABase.XAPath(x) for x in ls]

    def picture_rotation(self) -> list[XASystemEventsApplication.PictureRotation]:
        ls = self.xa_elem.arrayByApplyingSelector_("pictureRotation") or []
        return [XASystemEventsApplication.PictureRotation(x) for x in ls]

    def pictures_folder(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("picturesFolder") or []
        return [XABase.XAPath(x) for x in ls]

    def random_folder(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("randomOrder") or [])

    def translucent_menu_bar(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("translucentMenuBar") or [])

    def dynamic_style(self) -> list[XASystemEventsApplication.DynamicStyle]:
        ls = self.xa_elem.arrayByApplyingSelector_("dynamicStyle") or []
        return [XASystemEventsApplication.DynamicStyle(x) for x in ls]

    def by_name(self, name: str) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("name", name)

    def by_id(self, id: int) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("id", id)

    def by_change_interval(
        self, change_interval: float
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("changeInterval", change_interval)

    def by_display_name(
        self, display_name: str
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("displayName", display_name)

    def by_picture(
        self, picture: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsDesktop", None]:
        if isinstance(picture, str):
            picture = XABase.XAPath(picture)
        return self.by_property("picture", picture.xa_elem)

    def by_picture_rotation(
        self, picture_rotation: XASystemEventsApplication.PictureRotation
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("pictureRotation", picture_rotation.value)

    def by_pictures_folder(
        self, pictures_folder: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsDesktop", None]:
        if isinstance(pictures_folder, str):
            pictures_folder = XABase.XAPath(pictures_folder)
        return self.by_property("picturesFolder", pictures_folder.xa_elem)

    def by_random_order(
        self, random_order: bool
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("randomOrder", random_order)

    def by_translucent_menu_bar(
        self, translucent_menu_bar: bool
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("translucentMenuBar", translucent_menu_bar)

    def by_dynamic_style(
        self, dynamic_style: XASystemEventsApplication.DynamicStyle
    ) -> Union["XASystemEventsDesktop", None]:
        return self.by_property("dynamicStyle", dynamic_style.value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsDesktop(XABase.XAObject):
    """Desktop picture settings for desktops belonging to the user.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the desktop."""
        return self.xa_elem.name()

    @property
    def id(self) -> int:
        """The unique identifier of the desktop."""
        return self.xa_elem.id()

    @property
    def change_interval(self) -> float:
        """The number of seconds to wait between changing the desktop picture."""
        return self.xa_elem.changeInterval()

    @change_interval.setter
    def change_interval(self, change_interval: float):
        self.set_property("changeInterval", change_interval)

    @property
    def display_name(self) -> str:
        """The name of display on which this desktop appears."""
        return self.xa_elem.displayName()

    @property
    def picture(self) -> XABase.XAPath:
        """The path to file used as desktop picture."""
        return XABase.XAPath(self.xa_elem.picture().get())

    @picture.setter
    def picture(self, picture: Union[XABase.XAPath, str]):
        if isinstance(picture, str):
            picture = XABase.XAPath(picture)
        self.set_property("picture", picture.xa_elem)

    @property
    def picture_rotation(self) -> XASystemEventsApplication.PictureRotation:
        """Never, using interval, using login, after sleep."""
        return XASystemEventsApplication.PictureRotation(self.xa_elem.pictureRotation())

    @picture_rotation.setter
    def picture_rotation(
        self, picture_rotation: XASystemEventsApplication.PictureRotation
    ):
        self.set_property("pictureRotation", picture_rotation.value)

    @property
    def pictures_folder(self) -> XABase.XAPath:
        """The path to folder containing pictures for changing desktop background."""
        return XABase.XAPath(self.xa_elem.picturesFolder())

    @pictures_folder.setter
    def pictures_folder(self, pictures_folder: Union[XABase.XAPath, str]):
        if isinstance(pictures_folder, str):
            pictures_folder = XABase.XAPath(pictures_folder)
        self.set_property("picturesFolder", pictures_folder.xa_elem)

    @property
    def random_order(self) -> bool:
        """Turn on for random ordering of changing desktop pictures."""
        return self.xa_elem.randomOrder()

    @random_order.setter
    def random_order(self, random_order: bool):
        self.set_property("randomOrder", random_order)

    @property
    def translucent_menu_bar(self) -> bool:
        """Indicates whether the menu bar is translucent."""
        return self.xa_elem.translucentMenuBar()

    @translucent_menu_bar.setter
    def transluscent_menu_bar(self, transluscent_menu_bar: bool):
        self.set_property("transluscent_menu_bar", transluscent_menu_bar)

    @property
    def dynamic_style(self) -> XASystemEventsApplication.DynamicStyle:
        """The desktop picture dynamic style."""
        return XASystemEventsApplication.DynamicStyle(self.xa_elem.dynamicStyle())

    @dynamic_style.setter
    def dynamic_style(self, dynamic_style: XASystemEventsApplication.DynamicStyle):
        self.set_property("dynamicStyle", dynamic_style.value)


class XASystemEventsDockPreferencesObject(XABase.XAObject):
    """The current user's dock preferences.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def animate(self) -> bool:
        """Is the animation of opening applications on or off?"""
        return self.xa_elem.animate()

    @animate.setter
    def animate(self, animate: bool):
        self.set_property("animate", animate)

    @property
    def autohide(self) -> bool:
        """Is autohiding the dock on or off?"""
        return self.xa_elem.autohide()

    @autohide.setter
    def autohide(self, autohide: bool):
        self.set_property("autohide", autohide)

    @property
    def dock_size(self) -> float:
        """Size/height of the items (between 0.0 (minimum) and 1.0 (maximum))."""
        return self.xa_elem.dockSize()

    @dock_size.setter
    def dock_size(self, dock_size: float):
        self.set_property("dockSize", dock_size)

    @property
    def autohide_menu_bar(self) -> bool:
        """Is autohiding the menu bar on or off?"""
        return self.xa_elem.autohideMenuBar()

    @autohide_menu_bar.setter
    def autohide_menu_bar(self, autohide_menu_bar: bool):
        self.set_property("autohideMenuBar", autohide_menu_bar)

    @property
    def double_click_behavior(self) -> XASystemEventsApplication.DoubleClickBehavior:
        """Behavior when double clicking window a title bar."""
        return XASystemEventsApplication.DoubleClickBehavior(
            self.xa_elem.doubleClickBehavior()
        )

    @double_click_behavior.setter
    def double_click_behavior(
        self, double_click_behavior: XASystemEventsApplication.DoubleClickBehavior
    ):
        self.set_property("double_click_behavior", double_click_behavior.value)

    @property
    def magnification(self) -> bool:
        """Is magnification on or off?"""
        return self.xa_elem.magnification()

    @magnification.setter
    def magnification(self, magnification: bool):
        self.set_property("magnification", magnification)

    @property
    def magnification_size(self) -> float:
        """Maximum magnification size when magnification is on (between 0.0 (minimum) and 1.0 (maximum))."""
        return self.xa_elem.magnificationSize()

    @magnification_size.setter
    def magnification_size(self, magnification_size: float):
        self.set_property("magnificationSize", magnification_size)

    @property
    def minimize_effect(self) -> XASystemEventsApplication.MinimizeEffect:
        """Minimization effect."""
        return XASystemEventsApplication.MinimizeEffect(self.xa_elem.minimizeEffect())

    @minimize_effect.setter
    def minimize_effect(
        self, minimize_effect: XASystemEventsApplication.MinimizeEffect
    ):
        self.set_property("minimizeEffect", minimize_effect.value)

    @property
    def minimize_into_application(self) -> bool:
        """Minimize window into its application?"""
        return self.xa_elem.minimizeIntoApplication()

    @minimize_into_application.setter
    def minimize_into_application(self, minimize_into_application: bool):
        self.set_property("minimizeIntoApplication", minimize_into_application)

    @property
    def screen_edge(self) -> XASystemEventsApplication.ScreenLocation:
        """Location on screen."""
        return XASystemEventsApplication.ScreenLocation(self.xa_elem.screenEdge())

    @screen_edge.setter
    def screen_edge(self, screen_edge: XASystemEventsApplication.ScreenLocation):
        self.set_property("screenEdge", screen_edge.value)

    @property
    def show_indicators(self) -> bool:
        """Show indicators for open applications?"""
        return self.xa_elem.showIndicators()

    @show_indicators.setter
    def show_indicators(self, show_indicators: bool):
        self.set_property("showIndicators", show_indicators)

    @property
    def show_recents(self) -> bool:
        """Show recent applications?"""
        return self.xa_elem.showRecents()

    @show_recents.setter
    def show_recents(self, show_recents: bool):
        self.set_property("showRecents", show_recents)


class XASystemEventsLoginItemList(XABase.XAList):
    """A wrapper around lists of login items that employs fast enumeration techniques.

    All properties of property login items can be called as methods on the wrapped list, returning a list containing each login item's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsLoginItem, filter)

    def hidden(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("contents") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def by_hidden(self, hidden: bool) -> Union["XASystemEventsLoginItem", None]:
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union["XASystemEventsLoginItem", None]:
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union["XASystemEventsLoginItem", None]:
        return self.by_property("name", name)

    def by_path(
        self, path: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsLoginItem", None]:
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsLoginItem(XABase.XAObject):
    """An item to be launched or opened at login.add()

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def hidden(self) -> bool:
        """Is the Login Item hidden when launched?"""
        return self.xa_elem.hidden()

    @hidden.setter
    def hidden(self, hidden: bool):
        self.set_property("hidden", hidden)

    @property
    def kind(self) -> str:
        """The file type of the Login Item."""
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        """The name of the Login Item."""
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        """The file system path to the Login Item."""
        return self.xa_elem.path()

    def delete(self):
        """Deletes the login item.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.delete()


class XASystemEventsConfigurationList(XABase.XAList):
    """A wrapper around lists of configurations that employs fast enumeration techniques.

    All properties of configurations can be called as methods on the wrapped list, returning a list containing each configuration's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsConfiguration, filter)

    def account_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("accountName") or [])

    def connected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("connected") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_account_name(
        self, account_name: str
    ) -> Union["XASystemEventsConfiguration", None]:
        return self.by_property("accountName", account_name)

    def by_connected(
        self, connected: bool
    ) -> Union["XASystemEventsConfiguration", None]:
        return self.by_property("connected", connected)

    def by_id(self, id: str) -> Union["XASystemEventsConfiguration", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XASystemEventsConfiguration", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsConfiguration(XABase.XAObject):
    """A collection of settings for configuring a connection.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def account_name(self) -> str:
        """The name used to authenticate."""
        return self.xa_elem.accountName()

    @account_name.setter
    def account_name(self, account_name: str):
        self.set_property("accountName", account_name)

    @property
    def connected(self) -> bool:
        """Is the configuration connected?"""
        return self.xa_elem.connected()

    @property
    def id(self) -> str:
        """The unique identifier for the configuration."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the configuration."""
        return self.xa_elem.name()

    def connect(self) -> "XASystemEventsConfiguration":
        """Connects the configuration.

        :return: The configuration object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.connect(), XASystemEventsConfiguration)

    def disconnect(self) -> "XASystemEventsConfiguration":
        """Disconnects the configuration.

        :return: The configuration object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.disconnect(), XASystemEventsConfiguration)


class XASystemEventsInterfaceList(XABase.XAList):
    """A wrapper around lists of network interfaces that employs fast enumeration techniques.

    All properties of interfaces can be called as methods on the wrapped list, returning a list containing each interfaces's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsInterface, filter)

    def automatic(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("automatic") or [])

    def duplex(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("duplex") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def mac_address(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("macAddress") or [])

    def mtu(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("mtu") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def speed(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("speed") or [])

    def by_automatic(self, automatic: bool) -> Union["XASystemEventsInterface", None]:
        return self.by_property("automatic", automatic)

    def by_duplex(self, duplex: str) -> Union["XASystemEventsInterface", None]:
        return self.by_property("duplex", duplex)

    def by_id(self, id: str) -> Union["XASystemEventsInterface", None]:
        return self.by_property("id", id)

    def by_kind(self, kind: str) -> Union["XASystemEventsInterface", None]:
        return self.by_property("kind", kind)

    def by_mac_address(
        self, mac_address: str
    ) -> Union["XASystemEventsInterface", None]:
        return self.by_property("macAddress", mac_address)

    def by_mtu(self, mtu: int) -> Union["XASystemEventsInterface", None]:
        return self.by_property("mtu", mtu)

    def by_name(self, name: str) -> Union["XASystemEventsInterface", None]:
        return self.by_property("name", name)

    def by_speed(self, speed: int) -> Union["XASystemEventsInterface", None]:
        return self.by_property("speed", speed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsInterface(XABase.XAObject):
    """A collection of settings for a network interface.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def automatic(self) -> bool:
        """Configure the interface speed, duplex, and mtu automatically?"""
        return self.xa_elem.automatic()

    @automatic.setter
    def automatic(self, automatic: bool):
        self.set_property("automatic", automatic)

    @property
    def duplex(self) -> str:
        """The duplex setting half | full | full with flow control."""
        return self.xa_elem.duplex()

    @duplex.setter
    def duplex(self, duplex: str):
        self.set_property("duplex", duplex)

    @property
    def id(self) -> str:
        """The unique identifier for the interface."""
        return self.xa_elem.id()

    @property
    def kind(self) -> str:
        """The type of interface."""
        return self.xa_elem.kind()

    @property
    def mac_address(self) -> str:
        """The MAC address for the interface."""
        return self.xa_elem.MACAddress()

    @property
    def mtu(self) -> int:
        """The packet size."""
        return self.xa_elem.mtu()

    @mtu.setter
    def mtu(self, mtu: int):
        self.set_property("mtu", mtu)

    @property
    def name(self) -> str:
        """The name of the interface."""
        return self.xa_elem.name()

    @property
    def speed(self) -> int:
        """Ethernet speed 10 | 100 | 1000."""
        return self.xa_elem.speed()

    @speed.setter
    def speed(self, speed: int):
        self.set_property("speed", speed)


class XASystemEventsLocationList(XABase.XAList):
    """A wrapper around lists of service locations that employs fast enumeration techniques.

    All properties of locations can be called as methods on the wrapped list, returning a list containing each location's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsLocation, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_id(self, id: str) -> Union["XASystemEventsLocation", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XASystemEventsLocation", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsLocation(XABase.XAObject):
    """A set of services.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier for the location."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the location."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)


class XASystemEventsNetworkPreferencesObject(XABase.XAObject):
    """The preferences for the current user's network.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def current_location(self) -> XASystemEventsLocation:
        """The current location."""
        return self._new_element(self.xa_elem.currentLocation(), XASystemEventsLocation)

    @current_location.setter
    def current_location(self, current_location: XASystemEventsLocation):
        self.set_property("currentLocation", current_location.xa_elem)

    def interfaces(
        self, filter: dict = None
    ) -> Union["XASystemEventsInterfaceList", None]:
        """Returns a list of interfaces, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned interfaces will have, or None
        :type filter: Union[dict, None]
        :return: The list of interfaces
        :rtype: XASystemEventsInterfaceList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.interfaces(), XASystemEventsInterfaceList, filter
        )

    def locations(
        self, filter: dict = None
    ) -> Union["XASystemEventsLocationList", None]:
        """Returns a list of locations, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned locations will have, or None
        :type filter: Union[dict, None]
        :return: The list of locations
        :rtype: XASystemEventsLocationList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.locations(), XASystemEventsLocationList, filter
        )

    def services(self, filter: dict = None) -> Union["XASystemEventsServiceList", None]:
        """Returns a list of services, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned services will have, or None
        :type filter: Union[dict, None]
        :return: The list of services
        :rtype: XASystemEventsServiceList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.services(), XASystemEventsServiceList, filter
        )


class XASystemEventsServiceList(XABase.XAList):
    """A wrapper around lists of services that employs fast enumeration techniques.

    All properties of services can be called as methods on the wrapped list, returning a list containing each service's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsService, filter)

    def active(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("active") or [])

    def current_configuration(self) -> XASystemEventsConfigurationList:
        ls = self.xa_elem.arrayByApplyingSelector_("currentConfiguration") or []
        return self._new_element(ls, XASystemEventsConfigurationList)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def interface(self) -> XASystemEventsInterfaceList:
        ls = self.xa_elem.arrayByApplyingSelector_("interface") or []
        return self._new_element(ls, XASystemEventsInterfaceList)

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_active(self, active: bool) -> Union["XASystemEventsService", None]:
        return self.by_property("active", active)

    def by_current_configuration(
        self, current_configuration: XASystemEventsConfiguration
    ) -> Union["XASystemEventsService", None]:
        return self.by_property("currentConfiguration", current_configuration.xa_elem)

    def by_id(self, id: str) -> Union["XASystemEventsService", None]:
        return self.by_property("id", id)

    def by_interface(
        self, interface: XASystemEventsInterface
    ) -> Union["XASystemEventsService", None]:
        return self.by_property("interface", interface.xa_elem)

    def by_kind(self, kind: str) -> Union["XASystemEventsService", None]:
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union["XASystemEventsService", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsService(XABase.XAObject):
    """A collection of settings for a network service.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def active(self) -> bool:
        """Is the service active?"""
        return self.xa_elem.active()

    @property
    def current_configuration(self) -> XASystemEventsConfiguration:
        """The currently selected configuration."""
        return self._new_element(
            self.xa_elem.currentConfiguration(), XASystemEventsConfiguration
        )

    @current_configuration.setter
    def current_configuration(self, current_configuration: XASystemEventsConfiguration):
        self.set_property("currentConfiguration", current_configuration.xa_elem)

    @property
    def id(self) -> str:
        """The unique identifier for the service."""
        return self.xa_elem.id()

    @property
    def interface(self) -> XASystemEventsInterface:
        """The interface the service is built on."""
        return self._new_element(self.xa_elem.interface(), XASystemEventsInterface)

    @interface.setter
    def interface(self, interface: XASystemEventsInterface):
        self.set_property("interface", interface.xa_elem)

    @property
    def kind(self) -> int:
        """The type of service."""
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        """The name of the service."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    def connect(self) -> XASystemEventsConfiguration:
        """Connects the service.

        :return: The service object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.connect()

    def disconnect(self) -> XASystemEventsConfiguration:
        """Disconnects the service.

        :return: The service object
        :rtype: XASystemEventsConfiguration

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.disconnect()


class XASystemEventsScreenSaverList(XABase.XAList):
    """A wrapper around lists of screen savers that employs fast enumeration techniques.

    All properties of screen savers can be called as methods on the wrapped list, returning a list containing each screen saver's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScreenSaver, filter)

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def picture_display_style(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("pictureDisplayStyle") or [])

    def by_displayed_name(
        self, displayed_name: str
    ) -> Union["XASystemEventsScreenSaver", None]:
        return self.by_property("displayedName", displayed_name)

    def by_name(self, name: str) -> Union["XASystemEventsScreenSaver", None]:
        return self.by_property("name", name)

    def by_path(
        self, path: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsScreenSaver", None]:
        if isinstance(path, str):
            path = XABase.XAPath(path)
        return self.by_property("path", path.xa_elem)

    def by_picture_display_style(
        self, picture_display_style: str
    ) -> Union["XASystemEventsScreenSaver", None]:
        return self.by_property("pictureDisplayStyle", picture_display_style)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScreenSaver(XABase.XAObject):
    """An installed screen saver.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def displayedName(self) -> str:
        """Name of the screen saver module as displayed to the user."""
        return self.xa_elem.displayedName()

    @property
    def name(self) -> str:
        """Name of the screen saver module to be displayed."""
        return self.xa_elem.name()

    @property
    def path(self) -> "XABase.XAAlias":
        """Path to the screen saver module."""
        return self._new_element(self.xa_elem.path(), XABase.XAAlias)

    @property
    def picture_display_style(self) -> str:
        """Effect to use when displaying picture-based screen savers (slideshow, collage, or mosaic)."""
        return self.xa_elem.pictureDisplayStyle()

    @picture_display_style.setter
    def picture_display_style(self, picture_display_style: str):
        self.set_property("pictureDisplayStyle", picture_display_style)

    def start(self):
        """Starts the screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.start()

    def stop(self):
        """Stops the screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stop()


class XASystemEventsScreenSaverPreferencesObject(XABase.XAObject):
    """Screen saver settings.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def delay_interval(self) -> int:
        """Number of seconds of idle time before the screen saver starts; zero for never."""
        return self.xa_elem.delayInterval()

    @delay_interval.setter
    def delay_interval(self, delay_interval: int):
        self.set_property("delayInterval", delay_interval)

    @property
    def main_screen_only(self) -> bool:
        """Should the screen saver be shown only on the main screen?"""
        return self.xa_elem.mainScreenOnly()

    @main_screen_only.setter
    def main_screen_only(self, main_screen_only: bool):
        self.set_property("mainScreenOnly", main_screen_only)

    @property
    def running(self) -> bool:
        """Is the screen saver running?"""
        return self.xa_elem.running()

    @property
    def show_clock(self) -> bool:
        """Should a clock appear over the screen saver?"""
        return self.xa_elem.showClock()

    @show_clock.setter
    def show_clock(self, show_clock: bool):
        self.set_property("showClock", show_clock)

    def start(self):
        """Starts the current screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.start()

    def stop(self):
        """Stops the current screen saver.

        .. versionadded:: 0.1.0
        """
        return self.xa_elem.stop()


class XASystemEventsSecurityPreferencesObject(XABase.XAObject):
    """A collection of security preferences.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def automatic_login(self) -> bool:
        """Is automatic login allowed?"""
        return self.xa_elem.automaticLogin()

    @automatic_login.setter
    def automatic_login(self, automatic_login: bool):
        self.set_property("automaticLogin", automatic_login)

    @property
    def log_out_when_inactive(self) -> bool:
        """Will the computer log out when inactive?"""
        return self.xa_elem.logOutWhenInactive()

    @log_out_when_inactive.setter
    def log_out_when_inactive(self, log_out_when_inactive: bool):
        self.set_property("logOutWhenInactive", log_out_when_inactive)

    @property
    def log_out_when_inactive_interval(self) -> int:
        """The interval of inactivity after which the computer will log out."""
        return self.xa_elem.logOutWhenInactiveInterval()

    @log_out_when_inactive_interval.setter
    def log_out_when_inactive_interval(self, log_out_when_inactive_interval: int):
        self.set_property("logOutWhenInactiveInterval", log_out_when_inactive_interval)

    @property
    def require_password_to_unlock(self) -> bool:
        """Is a password required to unlock secure preferences?"""
        return self.xa_elem.requirePasswordToUnlock()

    @require_password_to_unlock.setter
    def require_password_to_unlock(self, require_password_to_unlock: bool):
        self.set_property("requirePasswordToUnlock", require_password_to_unlock)

    @property
    def require_password_to_wake(self) -> bool:
        """Is a password required to wake the computer from sleep or screen saver?"""
        return self.xa_elem.requirePasswordToWake()

    @require_password_to_wake.setter
    def require_password_to_wake(self, require_password_to_wake: bool):
        self.set_property("requirePasswordToWake", require_password_to_wake)

    @property
    def secure_virtual_memory(self) -> bool:
        """Is secure virtual memory being used?"""
        return self.xa_elem.secureVirtualMemory()

    @secure_virtual_memory.setter
    def secure_virtual_memory(self, secure_virtual_memory: bool):
        self.set_property("secureVirtualMemory", secure_virtual_memory)


class XASystemEventsFolderActionList(XABase.XAList):
    """A wrapper around lists of folder actions that employs fast enumeration techniques.

    All properties of folder actions can be called as methods on the wrapped list, returning a list containing each actions's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XABase.XAFolderAction, filter)

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def volume(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("volume") or [])

    def by_enabled(self, enabled: bool) -> Union["XABase.XAFolderAction", None]:
        return self.by_property("enabled", enabled)

    def by_name(self, name: str) -> Union["XABase.XAFolderAction", None]:
        return self.by_property("name", name)

    def by_path(
        self, path: Union[XABase.XAPath, str]
    ) -> Union["XABase.XAFolderAction", None]:
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_volume(self, volume: str) -> Union["XABase.XAFolderAction", None]:
        return self.by_property("volume", volume)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsFolderAction(XABase.XAObject):
    """An action attached to a folder in the file system.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def enabled(self) -> bool:
        """Is the folder action enabled?"""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def name(self) -> str:
        """The name of the folder action, which is also the name of the folder."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> str:
        """The path to the folder to which the folder action applies."""
        return self.xa_elem.path()

    @property
    def volume(self) -> str:
        """The volume on which the folder to which the folder action applies resides."""
        return self.xa_elem.volume()

    def enable(self):
        """Enables the folder action.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.enable()

    def scripts(self, filter: dict = None) -> Union["XASystemEventsScriptList", None]:
        """Returns a list of scripts, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripts will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripts
        :rtype: XASystemEventsScriptList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scripts(), XASystemEventsScriptList)


class XASystemEventsScriptList(XABase.XAList):
    """A wrapper around lists of scripts that employs fast enumeration techniques.

    All properties of scripts can be called as methods on the wrapped list, returning a list containing each script's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScript, filter)

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("path") or []
        return [XABase.XAPath(x) for x in ls]

    def posix_path(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("posixPath") or [])

    def by_enabled(self, enabled: bool) -> Union["XASystemEventsScript", None]:
        return self.by_property("enabled", enabled)

    def by_name(self, name: str) -> Union["XASystemEventsScript", None]:
        return self.by_property("name", name)

    def by_path(
        self, path: Union[XABase.XAPath, str]
    ) -> Union["XASystemEventsScript", None]:
        if isinstance(path, XABase.XAPath):
            path = path.path
        return self.by_property("path", path)

    def by_posix_path(self, posix_path: str) -> Union["XASystemEventsScript", None]:
        return self.by_property("posixPath", posix_path)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScript(XABase.XAObject):
    """A script invoked by a folder action.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def enabled(self) -> bool:
        """Is the script enabled?"""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def name(self) -> str:
        """The name of the script."""
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        """The file system path of the disk."""
        return self.xa_elem.path()

    @property
    def posix_path(self) -> str:
        """The POSIX file system path of the disk."""
        return self.xa_elem.POSIXPath()


class XASystemEventsActionList(XABase.XAList):
    """A wrapper around lists of actions that employs fast enumeration techniques.

    All properties of actions can be called as methods on the wrapped list, returning a list containing each action's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsAction, filter)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsAction", None]:
        return self.by_property("objectDescription", object_description)

    def by_name(self, name: str) -> Union["XASystemEventsAction", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsAction(XABase.XAObject):
    """An action that can be performed on the UI element.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_description(self) -> str:
        """What the action does."""
        return self.xa_elem.objectDescription()

    @property
    def name(self) -> str:
        """The name of the action."""
        return self.xa_elem.name()

    def perform(self):
        """Performs the action.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.perform()


class XASystemEventsAttributeList(XABase.XAList):
    """A wrapper around lists of attributes that employs fast enumeration techniques.

    All properties of attributes can be called as methods on the wrapped list, returning a list containing each attribute's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsAttribute, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def settable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("settable") or [])

    def value(self) -> Any:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_name(self, name: str) -> Union["XASystemEventsAttribute", None]:
        return self.by_property("name", name)

    def by_settable(self, settable: bool) -> Union["XASystemEventsAttribute", None]:
        return self.by_property("settable", settable)

    def by_value(self, value: Any) -> Union["XASystemEventsAttribute", None]:
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsAttribute(XABase.XAObject):
    """A named data value associated with the UI element.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the attribute."""
        return self.xa_elem.name()

    @property
    def settable(self) -> bool:
        """Can the attribute be set?"""
        return self.xa_elem.settable()

    @property
    def value(self) -> Any:
        """The current value of the attribute."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)


class XASystemEventsUIElementList(XABase.XAList):
    """A wrapper around lists of UI elements that employs fast enumeration techniques.

    All properties of UI elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XASystemEventsUIElement
        super().__init__(properties, obj_class, filter)

    def accessibility_description(self) -> list[str]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("accessibilityDescription") or []
        )

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def entire_contents(self) -> "XASystemEventsUIElementList":
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents") or []
        return self._new_element(ls, XASystemEventsUIElementList)

    def focused(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("focused") or [])

    def help(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("help") or [])

    def maximum_value(self) -> list[Union[int, float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximumValue") or [])

    def minimum_value(self) -> list[Union[int, float]]:
        return list(self.xa_elem.arrayByApplyingSelector_("minimumValue") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def orientation(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("orientation") or [])

    def position(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position") or [])

    def role(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("role") or [])

    def role_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("roleDescription") or [])

    def selected(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("selected") or [])

    def size(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def subrole(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("subrole") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_accessibility_description(
        self, accessibility_description: str
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("accessibilityDescription", accessibility_description)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("objectDescription", object_description)

    def by_enabled(self, enabled: bool) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("enabled", enabled)

    def by_entire_contents(
        self, entire_contents: "XASystemEventsUIElementList"
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("entireContents", entire_contents.xa_elem)

    def by_focused(self, focused: bool) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("focused", focused)

    def by_help(self, help: str) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("help", help)

    def by_maximum_value(
        self, maximum_value: Union[int, float]
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("maximumValue", maximum_value)

    def by_minimum_value(
        self, minimum_value: Union[int, float]
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("minimumValue", minimum_value)

    def by_name(self, name: str) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("name", name)

    def by_orientation(
        self, orientation: str
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("orientation", orientation)

    def by_position(
        self, position: tuple[int, int]
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("position", position)

    def by_role(self, role: str) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("role", role)

    def by_role_description(
        self, role_description: str
    ) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("roleDescription", role_description)

    def by_selected(self, selected: bool) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("selected", selected)

    def by_size(self, size: tuple[int, int]) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("size", size)

    def by_subrole(self, subrole: str) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("subrole", subrole)

    def by_title(self, title: str) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("title", title)

    def by_value(self, value: Any) -> Union["XASystemEventsUIElement", None]:
        return self.by_property("value", value)

    def actions(self, filter: dict = None) -> "XASystemEventsActionList":
        ls = [
            x for y in self.xa_elem.arrayByApplyingSelector_("actions") or [] for x in y
        ]
        return self._new_element(ls, XASystemEventsActionList)

    def windows(self, filter: dict = None) -> "XASystemEventsWindowList":
        ls = list(self.xa_elem.arrayByApplyingSelector_("windows") or [])
        self.xa_wcls = XASystemEventsWindow
        return self._new_element(ls, XASystemEventsWindowList)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.object_description()) + ">"


class XASystemEventsUIElement(XABase.XAObject, XASelectable):
    """A piece of the user interface of a process.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def accessibility_description(self) -> Union[str, None]:
        """A more complete description of the UI element and its capabilities."""
        return self.xa_elem.accessibilityDescription()

    @property
    def object_description(self) -> Union[str, None]:
        """The accessibility description, if available; otherwise, the role description."""
        return self.xa_elem.objectDescription()

    @property
    def enabled(self) -> Union[bool, None]:
        """Is the UI element enabled? (Does it accept clicks?)"""
        return self.xa_elem.enabled()

    @property
    def entire_contents(self) -> XABase.XAList:
        """A list of every UI element contained in this UI element and its child UI elements, to the limits of the tree."""
        return self._new_element(self.xa_elem.entireContents(), XABase.XAList)

    @property
    def focused(self) -> Union[bool, None]:
        """Is the focus on this UI element?"""
        return self.xa_elem.focused()

    @focused.setter
    def focused(self, focused: bool):
        self.set_property("focused", focused)

    @property
    def help(self) -> Union[str, None]:
        """An elaborate description of the UI element and its capabilities."""
        return self.xa_elem.help()

    @property
    def maximum_value(self) -> Union[int, float, None]:
        """The maximum value that the UI element can take on."""
        return self.xa_elem.maximumValue()

    @property
    def minimum_value(self) -> Union[int, float, None]:
        """The minimum value that the UI element can take on."""
        return self.xa_elem.minimumValue()

    @property
    def name(self) -> str:
        """The name of the UI Element, which identifies it within its container."""
        return self.xa_elem.name()

    @property
    def orientation(self) -> Union[str, None]:
        """The orientation of the UI element."""
        return self.xa_elem.orientation()

    @property
    def position(self) -> Union[list[Union[int, float]], None]:
        """The position of the UI element."""
        return self.xa_elem.position()

    @position.setter
    def position(self, position: tuple[int, int]):
        self.set_property("position", position)

    @property
    def role(self) -> str:
        """An encoded description of the UI element and its capabilities."""
        return self.xa_elem.role()

    @property
    def role_description(self) -> str:
        """A more complete description of the UI element's role."""
        return self.xa_elem.roleDescription()

    @property
    def selected(self) -> Union[bool, None]:
        """Is the UI element selected?"""
        selected = self.xa_elem.selected()
        try:
            selected = selected.get()
        finally:
            return selected

    @selected.setter
    def selected(self, selected: bool):
        self.set_property("selected", selected)

    @property
    def size(self) -> Union[list[Union[int, float]], None]:
        """The size of the UI element."""
        return self.xa_elem.size()

    @size.setter
    def size(self, size: list[Union[int, float]]):
        self.set_property("size", size)

    @property
    def subrole(self) -> Union[str, None]:
        """An encoded description of the UI element and its capabilities."""
        return self.xa_elem.subrole()

    @property
    def title(self) -> str:
        """The title of the UI element as it appears on the screen."""
        return self.xa_elem.title()

    @property
    def value(self) -> Any:
        """The current value of the UI element."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def click(self, point: Union[tuple[int, int], None] = None):
        """Cause the target process to behave as if the UI element were clicked.

        :param point: The coordinate location at which to click, defaults to None
        :type point: Union[tuple[int, int], None], optional

        .. versionadded:: 0.1.0
        """
        self.xa_elem.clickAt_(point)

    def increment(self):
        """Increments the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.increment()

    def decrement(self):
        """Decrements the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.decrement()

    def confirm(self):
        """Confirms the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.confirm()

    def pick(self):
        """Picks the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.pick()

    def cancel(self):
        """Cancels the UI element, if applicable.

        .. versionadded:: 0.1.0
        """
        self.xa_elem.cancel()

    def actions(self, filter: dict = None) -> Union["XASystemEventsActionList", None]:
        """Returns a list of action elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of actions
        :rtype: XASystemEventsActionList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.actions(), XASystemEventsActionList)

    def attributes(
        self, filter: dict = None
    ) -> Union["XASystemEventsAttributeList", None]:
        """Returns a list of attribute elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of attributes
        :rtype: XASystemEventsAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.attributes(), XASystemEventsAttributeList)

    def browsers(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of browser elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of browsers
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.browsers(), XASystemEventsUIElementList)

    def busy_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of busy indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of busy indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.busyIndicators(), XASystemEventsUIElementList
        )

    def buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.buttons(), XASystemEventsUIElementList)

    def checkboxes(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of checkbox elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of checkboxes
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.checkboxes(), XASystemEventsUIElementList)

    def color_wells(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of color well elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of color wells
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.colorWells(), XASystemEventsUIElementList)

    def columns(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of table column elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of columns
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.columns(), XASystemEventsUIElementList)

    def combo_boxes(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of combo box elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of combo boxes
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.comboBoxes(), XASystemEventsUIElementList)

    def drawers(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of drawer elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of drawers
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.drawers(), XASystemEventsUIElementList)

    def groups(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.groups(), XASystemEventsUIElementList)

    def grow_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of grow area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of grow areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.growAreas(), XASystemEventsUIElementList)

    def images(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of image elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of images
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.images(), XASystemEventsUIElementList)

    def incrementors(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of incrementor elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of incrementors
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.incrementors(), XASystemEventsUIElementList
        )

    def lists(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of list elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of lists
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.lists(), XASystemEventsUIElementList)

    def menus(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menus
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menus(), XASystemEventsUIElementList)

    def menu_bars(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu bars
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuBars(), XASystemEventsUIElementList)

    def menu_bar_items(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu bar item elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu bar items
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.menuBarItems(), XASystemEventsUIElementList
        )

    def menu_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.menuButtons(), XASystemEventsUIElementList
        )

    def menu_items(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of menu item elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of menu items
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.menuItems(), XASystemEventsUIElementList)

    def outlines(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of outline elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.outlines(), XASystemEventsUIElementList)

    def pop_overs(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of pop-over elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-overs
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.popOvers(), XASystemEventsUIElementList)

    def pop_up_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of pop-up button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of pop-up buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.popUpButtons(), XASystemEventsUIElementList
        )

    def progress_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of progress indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of progress indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.progressIndicators(), XASystemEventsUIElementList
        )

    def radio_buttons(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of radio button elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio buttons
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.radioButtons(), XASystemEventsUIElementList
        )

    def radio_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of radio group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of radio groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.radioGroups(), XASystemEventsUIElementList
        )

    def relevance_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of relevance indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of relevance indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.relevanceIndicators(), XASystemEventsUIElementList
        )

    def rows(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of table row elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of rows
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.rows(), XASystemEventsUIElementList)

    def scroll_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of scroll area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scrollAreas(), XASystemEventsUIElementList
        )

    def scroll_bars(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of scroll bar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scroll bars
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.scrollBars(), XASystemEventsUIElementList)

    def sheets(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of sheet elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sheets
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sheets(), XASystemEventsUIElementList)

    def sliders(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of slider elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of sliders
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.sliders(), XASystemEventsUIElementList)

    def splitters(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of splitter elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitters
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.splitters(), XASystemEventsUIElementList)

    def splitter_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of splitter group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of splitter groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.splitterGroups(), XASystemEventsUIElementList
        )

    def static_texts(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of static text elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of static texts
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.staticTexts(), XASystemEventsUIElementList
        )

    def tab_groups(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of tab group elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tab groups
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tabGroups(), XASystemEventsUIElementList)

    def tables(self, filter: dict = None) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of table elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of tables
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.tables(), XASystemEventsUIElementList)

    def text_areas(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of text area elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text areas
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textAreas(), XASystemEventsUIElementList)

    def text_fields(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of text fields elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of text fields
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.textFields(), XASystemEventsUIElementList)

    def toolbars(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of toolbar elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of outlines
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.toolbars(), XASystemEventsUIElementList)

    def ui_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of UI elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of UI elements
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(self.xa_elem.UIElements(), XASystemEventsUIElementList)

    def value_indicators(
        self, filter: dict = None
    ) -> Union["XASystemEventsUIElementList", None]:
        """Returns a list of value indicator elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of value indicators
        :rtype: XASystemEventsUIElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.valueIndicators(), XASystemEventsUIElementList
        )

    def windows(self, filter: dict = None) -> Union["XASystemEventsWindowList", None]:
        """Returns a list of window elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of windows
        :rtype: XASystemEventsWindowList

        .. versionadded:: 0.1.0
        """
        self.xa_wcls = XASystemEventsWindow
        return self._new_element(self.xa_elem.windows(), XASystemEventsWindowList)


class XASystemEventsProcessList(XASystemEventsUIElementList):
    """A wrapper around lists of processes that employs fast enumeration techniques.

    All properties of processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XASystemEventsProcess
        super().__init__(properties, filter, obj_class)

    def accepts_high_level_events(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("acceptsHighLevelEvents") or []
        )

    def accepts_remote_events(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("acceptsRemoteEvents") or [])

    def architecture(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("architecture") or [])

    def background_only(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("backgroundOnly") or [])

    def bundle_identifier(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bundleIdentifier") or [])

    def classic(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("class") or [])

    def creator_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def file(self) -> XABase.XAFileList:
        ls = self.xa_elem.arrayByApplyingSelector_("file") or []
        return self._new_element(ls, XABase.XAFileList)

    def file_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def has_scripting_terminology(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("hasScriptingTerminology") or []
        )

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def partition_space_used(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("partitionSpaceUsed") or [])

    def short_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("shortName") or [])

    def total_partition_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("totalPartitionSize") or [])

    def unix_id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("unixId") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def by_accepts_high_level_events(
        self, accepts_high_level_events: bool
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("acceptsHighLevelEvents", accepts_high_level_events)

    def by_accepts_remote_events(
        self, accepts_remote_events: bool
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("acceptsRemoteEvents", accepts_remote_events)

    def by_architecture(
        self, architecture: str
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("architecture", architecture)

    def by_background_only(
        self, background_only: bool
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("backgroundOnly", background_only)

    def by_bundle_identifier(
        self, bundle_identifier: str
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("bundleIdentifier", bundle_identifier)

    def by_classic(self, classic: bool) -> Union["XASystemEventsProcess", None]:
        return self.by_property("classic", classic)

    def by_creator_type(
        self, creator_type: str
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("creatorType", creator_type)

    def by_displayed_name(
        self, displayed_name: str
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("displayedName", displayed_name)

    def by_file(self, file: XABase.XAFile) -> Union["XASystemEventsProcess", None]:
        return self.by_property("file", file.xa_elem)

    def by_file_type(self, file_type: str) -> Union["XASystemEventsProcess", None]:
        return self.by_property("fileType", file_type)

    def by_frontmost(self, frontmost: bool) -> Union["XASystemEventsProcess", None]:
        return self.by_property("frontmost", frontmost)

    def by_has_scripting_terminology(
        self, has_scripting_terminology: str
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("hasScriptingTerminology", has_scripting_terminology)

    def by_id(self, id: str) -> Union["XASystemEventsProcess", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XASystemEventsProcess", None]:
        return self.by_property("name", name)

    def by_partition_space_used(
        self, partition_space_used: int
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("partitionSpaceUsed", partition_space_used)

    def by_short_name(self, short_name: str) -> Union["XASystemEventsProcess", None]:
        return self.by_property("shortName", short_name)

    def by_total_partition_size(
        self, total_partition_size: int
    ) -> Union["XASystemEventsProcess", None]:
        return self.by_property("totalPartitionSize", total_partition_size)

    def by_unix_id(self, unix_id: str) -> Union["XASystemEventsProcess", None]:
        return self.by_property("unixId", unix_id)

    def by_visible(self, visible: bool) -> Union["XASystemEventsProcess", None]:
        return self.by_property("visible", visible)

    def __repr__(self):
        return "<" + str(type(self)) + "length: " + str(len(self)) + ">"


class XASystemEventsProcess(XASystemEventsUIElement):
    """A process running on this computer.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def front_window(self) -> "XABaseScriptable.XASBWindow":
        """The front window of the application process."""
        return self._new_element(self.xa_elem.windows()[0], XASystemEventsWindow)

    @property
    def accepts_high_level_events(self) -> bool:
        """Is the process high-level event aware (accepts open application, open document, print document, and quit)?"""
        return self.xa_elem.acceptsHighLevelEvents()

    @property
    def accepts_remote_events(self) -> bool:
        """Does the process accept remote events?"""
        return self.xa_elem.acceptsRemoteEvents()

    @property
    def architecture(self) -> str:
        """The architecture in which the process is running."""
        return self.xa_elem.architecture()

    @property
    def background_only(self) -> bool:
        """Does the process run exclusively in the background?"""
        return self.xa_elem.backgroundOnly()

    @property
    def bundle_identifier(self) -> str:
        """The bundle identifier of the process' application file."""
        return self.xa_elem.bundleIdentifier()

    @property
    def classic(self) -> bool:
        """Is the process running in the Classic environment?"""
        return self.xa_elem.Classic()

    @property
    def creator_type(self) -> str:
        """The OSType of the creator of the process (the signature)."""
        return self.xa_elem.creatorType()

    @property
    def displayed_name(self) -> str:
        """The name of the file from which the process was launched, as displayed in the User Interface."""
        return self.xa_elem.displayedName()

    @property
    def file(self) -> XABase.XAFile:
        """The file from which the process was launched."""
        return self._new_element(self.xa_elem.file(), XABase.XAFile)

    @property
    def file_type(self) -> str:
        """The OSType of the file type of the process."""
        return self.xa_elem.fileType()

    @property
    def frontmost(self) -> bool:
        """Is the process the frontmost process?"""
        return self.xa_elem.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def has_scripting_terminology(self) -> bool:
        """Does the process have a scripting terminology, i.e., can it be scripted?"""
        return self.xa_elem.hasScriptingTerminology()

    @property
    def id(self) -> int:
        """The unique identifier of the process."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the process."""
        return self.xa_elem.name()

    @property
    def partition_space_used(self) -> int:
        """The number of bytes currently used in the process' partition."""
        return self.xa_elem.partitionSpaceUsed()

    @property
    def short_name(self) -> Union[str, None]:
        """The short name of the file from which the process was launched."""
        return self.xa_elem.shortName()

    @property
    def total_partition_size(self) -> int:
        """The size of the partition with which the process was launched."""
        return self.xa_elem.totalPartitionSize()

    @property
    def unix_id(self) -> int:
        """The Unix process identifier of a process running in the native environment, or -1 for a process running in the Classic environment."""
        return self.xa_elem.unixId()

    @property
    def visible(self) -> bool:
        """Is the process' layer visible?"""
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)


class XASystemEventsApplicationProcessList(XASystemEventsProcessList):
    """A wrapper around lists of application processes that employs fast enumeration techniques.

    All properties of application processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsApplicationProcess)

    def application_file(self) -> XABase.XAFileList:
        ls = self.xa_elem.arrayByApplyingSelector_("applicationFile") or []
        return self._new_element(ls, XABase.XAFileList)

    def by_application_file(
        self, application_file: XABase.XAFile
    ) -> Union["XASystemEventsApplicationProcess", None]:
        return self.by_property("applicationFile", application_file.xa_elem)


class XASystemEventsApplicationProcess(XASystemEventsProcess):
    """A process launched from an application file.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def application_file(self) -> XABase.XAFile:
        """A reference to the application file from which this process was launched."""
        return self._new_element(self.xa_elem.applicationFile(), XABase.XAFile)


class XASystemEventsDeskAccessoryProcessList(XASystemEventsProcessList):
    """A wrapper around lists of desk accessory processes that employs fast enumeration techniques.

    All properties of desk accessory processes can be called as methods on the wrapped list, returning a list containing each process' value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsDeskAccessoryProcess)

    def desk_accessory_file(self) -> XABase.XAFileList:
        ls = self.xa_elem.arrayByApplyingSelector_("deskAccessoryFile") or []
        return self._new_element(ls, XABase.XAFileList)

    def by_desk_accessory_file(
        self, desk_accessory_file: XABase.XAFile
    ) -> Union["XASystemEventsDeskAccessoryProcess", None]:
        return self.by_property("deskAccessoryFile", desk_accessory_file.xa_elem)


class XASystemEventsDeskAccessoryProcess(XASystemEventsProcess):
    """A process launched from an desk accessory file.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def desk_accessory_file(self) -> XABase.XAAlias:
        """A reference to the desk accessory file from which this process was launched."""
        return self._new_element(self.xa_elem.deskAccessoryFile(), XABase.XAAlias)


class XASystemEventsPropertyListFileList(XABase.XAList):
    """A wrapper around lists of property list files that employs fast enumeration techniques.

    All properties of property list files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsPropertyListFile, filter)

    def contents(self) -> "XASystemEventsPropertyListItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XASystemEventsPropertyListItemList)

    def by_content(
        self, contents: "XASystemEventsPropertyListItemList"
    ) -> Union["XASystemEventsPropertyListFile", None]:
        return self.by_property("contents", contents.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.contents()) + ">"


class XASystemEventsPropertyListFile(XABase.XAObject):
    """A file containing data in Property List format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def contents(self) -> "XASystemEventsPropertyListItem":
        """The contents of the property list file; elements and properties of the property list item may be accessed as if they were elements and properties of the property list file."""
        return self._new_element(
            self.xa_elem.contents(), XASystemEventsPropertyListItem
        )

    @contents.setter
    def contents(self, contents: "XASystemEventsPropertyListItem"):
        self.set_property("contents", contents.xa_elem)


class XASystemEventsPropertyListItemList(XABase.XAList):
    """A wrapper around lists of property list items that employs fast enumeration techniques.

    All properties of property list items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsPropertyListItem, filter)

    def kind(self) -> list[str]:
        # TODO
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("text") or [])

    def value(self) -> list[Union[int, bool, datetime, dict, str, bytes]]:
        # TODO: SPECIALIZE TYPE
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_kind(self, kind: str) -> Union["XASystemEventsPropertyListItem", None]:
        # TODO
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union["XASystemEventsPropertyListItem", None]:
        return self.by_property("name", name)

    def by_text(self, text: str) -> Union["XASystemEventsPropertyListItem", None]:
        return self.by_property("text", text)

    def by_value(self, value: Any) -> Union["XASystemEventsPropertyListItem", None]:
        # TODO
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsPropertyListItem(XABase.XAObject):
    """A unit of data in Property List format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def kind(self) -> str:
        """The kind of data stored in the property list item: boolean/data/date/list/number/record/string."""
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        """The name of the property list item (if any)."""
        return self.xa_elem.name()

    @property
    def text(self) -> str:
        """The text representation of the property list data."""
        return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        self.set_property("text", text)

    # TODO: Specialize to exact type
    @property
    def value(self) -> Any:
        """The value of the property list item."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def property_list_items(
        self, filter: dict = None
    ) -> Union["XASystemEventsPropertyListItemList", None]:
        """Returns a list of property list items, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned property list items will have, or None
        :type filter: Union[dict, None]
        :return: The list of property list items
        :rtype: XASystemEventsPropertyListItemList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.propertyListItems(), XASystemEventsPropertyListItemList
        )


class XASystemEventsXMLAttributeList(XABase.XAList):
    """A wrapper around lists of XML attributes that employs fast enumeration techniques.

    All properties of XML attributes can be called as methods on the wrapped list, returning a list containing each attribute's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLAttribute, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_name(self, name: str) -> Union["XASystemEventsXMLAttribute", None]:
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union["XASystemEventsXMLAttribute", None]:
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsXMLAttribute(XABase.XAObject):
    """A named value associated with a unit of data in XML format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the XML attribute."""
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        """The value of the XML attribute."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)


class XASystemEventsXMLDataList(XABase.XAList):
    """A wrapper around lists of XML data that employs fast enumeration techniques.

    All properties of XML datas can be called as methods on the wrapped list, returning a list containing each XML data's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLData, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def text(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("text") or [])

    def by_id(self, id: str) -> Union["XASystemEventsXMLData", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XASystemEventsXMLData", None]:
        return self.by_property("name", name)

    def by_text(self, text: str) -> Union["XASystemEventsXMLData", None]:
        return self.by_property("text", text)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsXMLData(XABase.XAObject):
    """Data in XML format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier of the XML data."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the XML data."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def text(self) -> str:
        """The text representation of the XML data."""
        return self.xa_elem.text()

    @text.setter
    def text(self, text: str):
        self.set_property("text", text)

    def xml_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsXMLElementList", None]:
        """Returns a list of XML elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML elements
        :rtype: XASystemEventsXMLElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.xmlElements(), XASystemEventsXMLElementList
        )


class XASystemEventsXMLElementList(XABase.XAList):
    """A wrapper around lists of XML elements that employs fast enumeration techniques.

    All properties of XML elements can be called as methods on the wrapped list, returning a list containing each elements's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsXMLElement, filter)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_id(self, id: str) -> Union["XASystemEventsXMLElement", None]:
        return self.by_property("id", id)

    def by_name(self, name: str) -> Union["XASystemEventsXMLElement", None]:
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union["XASystemEventsXMLElement", None]:
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsXMLElement(XABase.XAObject):
    """A unit of data in XML format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier of the XML element."""
        return self.xa_elem.id()

    @property
    def name(self) -> str:
        """The name of the XML element."""
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        """The value of the XML element."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def xml_attributes(
        self, filter: dict = None
    ) -> Union["XASystemEventsXMLAttributeList", None]:
        """Returns a list of XML attributes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML attributes will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML attributes
        :rtype: XASystemEventsXMLAttributeList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.xmlAttributes(), XASystemEventsXMLAttributeList
        )

    def xml_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsXMLElementList", None]:
        """Returns a list of XML elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned XML elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of XML elements
        :rtype: XASystemEventsXMLElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.xmlElements(), XASystemEventsXMLElementList
        )


class XASystemEventsXMLFileList(XABase.XAFileList):
    """A wrapper around lists of XML files that employs fast enumeration techniques.

    All properties of XML files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsXMLFile)

    def contents(self) -> XASystemEventsXMLDataList:
        ls = self.xa_elem.arrayByApplyingSelector_("contents") or []
        return self._new_element(ls, XASystemEventsXMLDataList)

    def by_contents(
        self, contents: XASystemEventsXMLData
    ) -> Union["XASystemEventsXMLFile", None]:
        return self.by_property("contents", contents.xa_elem)


class XASystemEventsXMLFile(XABase.XAObject):
    """A file containing data in XML format.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def contents(self) -> XASystemEventsXMLData:
        """The contents of the XML file; elements and properties of the XML data may be accessed as if they were elements and properties of the XML file."""
        return self._new_element(self.xa_elem.contents(), XASystemEventsXMLData)

    @contents.setter
    def contents(self, contents: XASystemEventsXMLData):
        self.set_property("contents", contents.xa_elem)


class XASystemEventsPrintSettings(XABase.XAObject):
    """Settings for printing.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def copies(self) -> int:
        """The number of copies of a document to be printed."""
        return self.xa_elem.copies()

    @copies.setter
    def copies(self, copies: int):
        self.set_property("copies", copies)

    @property
    def collating(self) -> bool:
        """Should printed copies be collated?"""
        return self.xa_elem.collating()

    @collating.setter
    def collating(self, collating: bool):
        self.set_property("collating", collating)

    @property
    def starting_page(self) -> int:
        """The first page of the document to be printed."""
        return self.xa_elem.startingPage()

    @starting_page.setter
    def starting_page(self, starting_page: int):
        self.set_property("startingPage", starting_page)

    @property
    def ending_page(self) -> int:
        """The last page of the document to be printed."""
        return self.xa_elem.endingPage()

    @ending_page.setter
    def ending_page(self, ending_page: int):
        self.set_property("endingPage", ending_page)

    @property
    def pages_across(self) -> int:
        """The number of logical pages laid across a physical page."""
        return self.xa_elem.pagesAcross()

    @pages_across.setter
    def pages_across(self, pages_across: int):
        self.set_property("pagesAcross", pages_across)

    @property
    def pages_down(self) -> int:
        """The number of logical pages laid out down a physical page."""
        return self.xa_elem.pagesDown()

    @pages_down.setter
    def pages_down(self, pages_down: int):
        self.set_property("pagesDown", pages_down)

    @property
    def requested_print_time(self) -> datetime:
        """The time at which the desktop printer should print the document."""
        return self.xa_elem.requestedPrintTime()

    @requested_print_time.setter
    def requested_print_time(self, requested_print_time: datetime):
        self.set_property("requestedPrintTime", requested_print_time)

    @property
    def error_handling(self) -> XASystemEventsApplication.PrintErrorHandling:
        """How should errors be handled?"""
        return XASystemEventsApplication.PrintErrorHandling(
            self.xa_elem.errorHandling()
        )

    @error_handling.setter
    def error_handling(
        self, error_handling: XASystemEventsApplication.PrintErrorHandling
    ):
        self.set_property("error_handling", error_handling.value)

    @property
    def fax_number(self) -> str:
        """The target fax number."""
        return self.xa_elem.faxNumber()

    @fax_number.setter
    def fax_number(self, fax_number: str):
        self.set_property("faxNumber", fax_number)

    @property
    def target_printer(self) -> str:
        """The target printer."""
        return self.xa_elem.targetPrinter()

    @target_printer.setter
    def target_printer(self, target_printer: str):
        self.set_property("targetPrinter", target_printer)


class XASystemEventsScriptingClassList(XABase.XAList):
    """A wrapper around lists of scripting classes that employs fast enumeration techniques.

    All properties of scripting classes can be called as methods on the wrapped list, returning a list containing each class' value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingClass, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def plural_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("pluralName") or [])

    def suite_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("suiteName") or [])

    def superclass(self) -> "XASystemEventsScriptingClassList":
        ls = self.xa_elem.arrayByApplyingSelector_("superclass") or []
        return self._new_element(ls, XASystemEventsScriptingClassList)

    def by_name(self, name: str) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("hidden", hidden)

    def by_plural_name(
        self, plural_name: str
    ) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("pluralName", plural_name)

    def by_suite_name(
        self, suite_name: str
    ) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("suiteName", suite_name)

    def by_superclass(
        self, superclass: "XASystemEventsScriptingClass"
    ) -> Union["XASystemEventsScriptingClass", None]:
        return self.by_property("superclass", superclass.xa_elem)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingClass(XABase.XAObject):
    """A class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the class."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the class."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The description of the class."""
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        """Is the class hidden?"""
        return self.xa_elem.hidden()

    @property
    def plural_name(self) -> str:
        """The plural name of the class."""
        return self.xa_elem.pluralName()

    @property
    def suite_name(self) -> str:
        """The name of the suite to which this class belongs."""
        return self.xa_elem.suiteName()

    @property
    def superclass(self) -> "XASystemEventsScriptingClass":
        """The class from which this class inherits."""
        return self._new_element(
            self.xa_elem.superclass(), XASystemEventsScriptingClass
        )

    def scripting_elements(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingElementList", None]:
        """Returns a list of scripting elements, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting elements will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting elements
        :rtype: XASystemEventsScriptingElementList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingElements(), XASystemEventsScriptingElementList
        )

    def scripting_properties(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingPropertyList", None]:
        """Returns a list of scripting properties, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting properties will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting properties
        :rtype: XASystemEventsScriptingPropertyList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingProperties(), XASystemEventsScriptingPropertyList
        )


class XASystemEventsScriptingCommandList(XABase.XAList):
    """A wrapper around lists of scripting commands that employs fast enumeration techniques.

    All properties of scripting commands can be called as methods on the wrapped list, returning a list containing each command's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingCommand, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def direct_parameter(self) -> "XASystemEventsScriptingParameterList":
        ls = self.xa_elem.arrayByApplyingSelector_("directParameter") or []
        return self._new_element(ls, XASystemEventsScriptingParameterList)

    def hidden(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def scripting_result(self) -> "XASystemEventsScriptingResultObjectList":
        ls = self.xa_elem.arrayByApplyingSelector_("scriptingResult") or []
        return self._new_element(ls, XASystemEventsScriptingResultObjectList)

    def suite_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("suiteName") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("objectDescription", object_description)

    def by_direct_parameter(
        self, direct_parameter: "XASystemEventsScriptingParameter"
    ) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("directParameter", direct_parameter.xa_elem)

    def by_hidden(self, hidden: bool) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("hidden", hidden)

    def by_scripting_result(
        self, scripting_result: "XASystemEventsScriptingResultObject"
    ) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("scriptingResult", scripting_result.xa_elem)

    def by_suite_name(
        self, suite_name: str
    ) -> Union["XASystemEventsScriptingCommand", None]:
        return self.by_property("suiteName", suite_name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingCommand(XABase.XAObject):
    """A command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the command."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the command."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The description of the command."""
        return self.xa_elem.objectDescription()

    @property
    def direct_parameter(self) -> "XASystemEventsScriptingParameter":
        """The direct parameter of the command."""
        return self._new_element(
            self.xa_elem.directParameter(), XASystemEventsScriptingParameter
        )

    @property
    def hidden(self) -> bool:
        """Is the command hidden?"""
        return self.xa_elem.hidden()

    @property
    def scripting_result(self) -> "XASystemEventsScriptingResultObject":
        """The object or data returned by this command."""
        return self._new_element(
            self.xa_elem.scriptingResult(), XASystemEventsScriptingResultObject
        )

    @property
    def suite_name(self) -> str:
        """The name of the suite to which this command belongs."""
        return self.xa_elem.suiteName()

    def scripting_parameters(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingParameterList", None]:
        """Returns a list of scripting parameters, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting parameters will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting parameters
        :rtype: XASystemEventsScriptingParameterList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingParameters(), XASystemEventsScriptingParameterList
        )


class XASystemEventsScriptingDefinitionObject(XABase.XAObject):
    """The scripting definition of the System Events application.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    def scripting_suites(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingSuiteList", None]:
        """Returns a list of scripting suites, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting suites will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting suites
        :rtype: XASystemEventsScriptingSuiteList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingSuites(), XASystemEventsScriptingSuiteList, filter
        )


class XASystemEventsScriptingElementList(XABase.XAList):
    """A wrapper around lists of scripting elements that employs fast enumeration techniques.

    All properties of scripting elements can be called as methods on the wrapped list, returning a list containing each element's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XASystemEventsScriptingElement)


class XASystemEventsScriptingElement(XASystemEventsScriptingClass):
    """An element within a class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)


class XASystemEventsScriptingEnumerationList(XABase.XAList):
    """A wrapper around lists of scripting enumerations that employs fast enumeration techniques.

    All properties of scripting enumerations can be called as methods on the wrapped list, returning a list containing each enumerations's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingEnumeration, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def hidden(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingEnumeration", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingEnumeration", None]:
        return self.by_property("id", id)

    def by_hidden(
        self, hidden: bool
    ) -> Union["XASystemEventsScriptingEnumeration", None]:
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingEnumeration(XABase.XAObject):
    """An enumeration within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the enumeration."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the enumeration."""
        return self.xa_elem.id()

    @property
    def hidden(self) -> bool:
        """Is the enumeration hidden?"""
        return self.xa_elem.hidden()

    def scripting_enumerators(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingEnumeratorList", None]:
        """Returns a list of scripting enumerators, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting enumerators will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting enumerators
        :rtype: XASystemEventsScriptingEnumeratorList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingEnumerators(), XASystemEventsScriptingEnumeratorList
        )


class XASystemEventsScriptingEnumeratorList(XABase.XAList):
    """A wrapper around lists of scripting enumerators that employs fast enumeration techniques.

    All properties of scripting enumerators can be called as methods on the wrapped list, returning a list containing each enumerator's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingEnumerator, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingEnumerator", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingEnumerator", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingEnumerator", None]:
        return self.by_property("objectDescription", object_description)

    def by_hidden(
        self, hidden: bool
    ) -> Union["XASystemEventsScriptingEnumerator", None]:
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingEnumerator(XABase.XAObject):
    """An enumerator within an enumeration within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the enumerator."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the enumerator."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The description of the enumerator."""
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        """Is the enumerator hidden?"""
        return self.xa_elem.hidden()


class XASystemEventsScriptingParameterList(XABase.XAList):
    """A wrapper around lists of scripting parameters that employs fast enumeration techniques.

    All properties of scripting parameters can be called as methods on the wrapped list, returning a list containing each parameter's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingParameter, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def optional(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("optional") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("objectDescription", object_description)

    def by_hidden(
        self, hidden: bool
    ) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("kind", kind)

    def by_optional(
        self, optional: bool
    ) -> Union["XASystemEventsScriptingParameter", None]:
        return self.by_property("optional", optional)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingParameter(XABase.XAObject):
    """A parameter within a command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the parameter."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the parameter."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The description of the parameter."""
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        """Is the parameter hidden?"""
        return self.xa_elem.hidden()

    @property
    def kind(self) -> str:
        """The kind of object or data specified by this parameter."""
        return self.xa_elem.kind()

    @property
    def optional(self) -> bool:
        """Is the parameter optional?"""
        return self.xa_elem.optional()


class XASystemEventsScriptingPropertyList(XABase.XAList):
    """A wrapper around lists of scripting properties that employs fast enumeration techniques.

    All properties of scripting properties can be called as methods on the wrapped list, returning a list containing each scripting property's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingProperty, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def access(self) -> list[XASystemEventsApplication.AccessRight]:
        ls = self.xa_elem.arrayByApplyingSelector_("access") or []
        return [XASystemEventsApplication.AccessRight(x) for x in ls]

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enumerated(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enumerated") or [])

    def hidden(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def listed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("listed") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("id", id)

    def by_access(
        self, access: XASystemEventsApplication.AccessRight
    ) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("access", access.value)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("objectDescription", object_description)

    def by_enumerated(
        self, enumerated: bool
    ) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("enumerated", enumerated)

    def by_hidden(self, hidden: bool) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("hidden", hidden)

    def by_kind(self, kind: str) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("kind", kind)

    def by_listed(self, listed: bool) -> Union["XASystemEventsScriptingProperty", None]:
        return self.by_property("listed", listed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingProperty(XABase.XAObject):
    """A property within a class within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the property."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the property."""
        return self.xa_elem.id()

    @property
    def access(self) -> XASystemEventsApplication.AccessRight:
        """The type of access to this property."""
        return XASystemEventsApplication.AccessRight(self.xa_elem.access())

    @property
    def object_description(self) -> str:
        """The description of the property."""
        return self.xa_elem.objectDescription()

    @property
    def enumerated(self) -> bool:
        """Is the property's value an enumerator?"""
        return self.xa_elem.enumerated()

    @property
    def hidden(self) -> bool:
        """Is the property hidden?"""
        return self.xa_elem.hidden()

    @property
    def kind(self) -> str:
        """The kind of object or data returned by this property."""
        return self.xa_elem.kind()

    @property
    def listed(self) -> bool:
        """Is the property's value a list?"""
        return self.xa_elem.listed()


class XASystemEventsScriptingResultObjectList(XABase.XAList):
    """A wrapper around lists of scripting result objects that employs fast enumeration techniques.

    All properties of scripting result objects can be called as methods on the wrapped list, returning a list containing each result's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingResultObject, filter)

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def enumerated(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enumerated") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def listed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("listed") or [])

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingResultObject", None]:
        return self.by_property("objectDescription", object_description)

    def by_enumerated(
        self, enumerated: bool
    ) -> Union["XASystemEventsScriptingResultObject", None]:
        return self.by_property("enumerated", enumerated)

    def by_kind(self, kind: str) -> Union["XASystemEventsScriptingResultObject", None]:
        return self.by_property("kind", kind)

    def by_listed(
        self, listed: bool
    ) -> Union["XASystemEventsScriptingResultObject", None]:
        return self.by_property("listed", listed)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.kind()) + ">"


class XASystemEventsScriptingResultObject(XABase.XAObject):
    """The result of a command within a suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def object_description(self) -> str:
        """The description of the property."""
        return self.xa_elem.objectDescription()

    @property
    def enumerated(self) -> bool:
        """Is the scripting result's value an enumerator?"""
        return self.xa_elem.enumerated()

    @property
    def kind(self) -> str:
        """The kind of object or data returned by this property."""
        return self.xa_elem.kind()

    @property
    def listed(self) -> bool:
        """Is the scripting result's value a list?"""
        return self.xa_elem.listed()


class XASystemEventsScriptingSuiteList(XABase.XAList):
    """A wrapper around lists of scripting suites that employs fast enumeration techniques.

    All properties of scripting suites can be called as methods on the wrapped list, returning a list containing each suite's value for the property.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASystemEventsScriptingSuite, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def object_description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("objectDescription") or [])

    def hidden(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("hidden") or [])

    def by_name(self, name: str) -> Union["XASystemEventsScriptingSuite", None]:
        return self.by_property("name", name)

    def by_id(self, id: str) -> Union["XASystemEventsScriptingSuite", None]:
        return self.by_property("id", id)

    def by_object_description(
        self, object_description: str
    ) -> Union["XASystemEventsScriptingSuite", None]:
        return self.by_property("objectDescription", object_description)

    def by_hidden(self, hidden: bool) -> Union["XASystemEventsScriptingSuite", None]:
        return self.by_property("hidden", hidden)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASystemEventsScriptingSuite(XABase.XAObject):
    """A suite within a scripting definition.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the suite."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier of the suite."""
        return self.xa_elem.id()

    @property
    def object_description(self) -> str:
        """The description of the suite."""
        return self.xa_elem.objectDescription()

    @property
    def hidden(self) -> bool:
        """Is the suite hidden?"""
        return self.xa_elem.hidden()

    def scripting_commands(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingCommandList", None]:
        """Returns a list of scripting commands, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting commands will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting commands
        :rtype: XASystemEventsScriptingCommandList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingCommands(), XASystemEventsScriptingCommandList
        )

    def scripting_classes(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingClassList", None]:
        """Returns a list of scripting classes, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting classes will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting classes
        :rtype: XASystemEventsScriptingClassList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingClasses(), XASystemEventsScriptingClassList
        )

    def scripting_enumerations(
        self, filter: dict = None
    ) -> Union["XASystemEventsScriptingEnumerationList", None]:
        """Returns a list of scripting enumerations, as PyXA-wrapped objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned scripting enumerations will have, or None
        :type filter: Union[dict, None]
        :return: The list of scripting enumerations
        :rtype: XASystemEventsScriptingEnumerationList

        .. versionadded:: 0.1.0
        """
        return self._new_element(
            self.xa_elem.scriptingEnumerations(), XASystemEventsScriptingEnumerationList
        )
