""".. versionadded:: 0.0.1

Control Finder using JXA-like syntax.
"""

from datetime import datetime
from enum import Enum
from typing import Union
from Foundation import NSFileManager

import AppKit
from ScriptingBridge import SBObject

from PyXA import XABase
from PyXA.XABase import OSType, XAImage, XAList
from PyXA import XABaseScriptable
from PyXA.XAProtocols import (
    XACanOpenPath,
    XAClipboardCodable,
    XADeletable,
    XASelectable,
)
from PyXA.XATypes import XAPoint, XARectangle


class XAFinderApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Finder.app.

    .. versionchanged:: 0.0.3

       Added methods and properties to reach parity with Finder.h.

    .. versionadded:: 0.0.1
    """

    class PrivacySetting(Enum):
        """Options for privacy settings on Finder items."""

        READ_ONLY = OSType("read")
        READ_WRITE = OSType("rdwr")
        WRITE_ONLY = OSType("writ")
        NONE = OSType("none")

    class ItemFormat(Enum):
        """Options for file and disk formats of Finder items."""

        MACOS = OSType("dfhf")
        MACOS_EXTENDED = OSType("dfh+")
        UFS = OSType("dfuf")
        NFS = OSType("dfnf")
        AUDIO = OSType("dfau")
        PRO_DOS = OSType("dfpr")
        MSDOS = OSType("dfms")
        NTFS = OSType("dfnt")
        ISO9660 = OSType("df96")
        HIGH_SIERRA = OSType("dfhs")
        QUICKTAKE = OSType("dfqt")
        APPLE_PHOTO = OSType("dfph")
        APPLE_SHARE = OSType("dfas")
        UDF = OSType("dfud")
        WEBDAV = OSType("dfwd")
        FTP = OSType("dfft")
        PACKET_WRITTEN_UDF = OSType("dfpu")
        XSAN = OSType("dfac")
        APFS = OSType("dfap")
        EXFAT = OSType("dfxf")
        SMB = OSType("dfsm")
        UNKNOWN = OSType("df\?\?")

    class Panel(Enum):
        """Options for information panels in Finder."""

        GENERAL_INFORMATION = OSType("gpnl")
        SHARING = OSType("spnl")
        MEMORY = OSType("mpnl")
        PREVIEW = OSType("vpnl")
        APPLICATION = OSType("apnl")
        LANGUAGES = OSType("pklg")
        PLUGINS = OSType("pkpg")
        NAME_EXTENSION = OSType("npnl")
        COMMENTS = OSType("cpnl")
        CONTENT_INDEX = OSType("cinl")
        BURNING = OSType("bpnl")
        MORE_INFO = OSType("minl")
        SIMPLE_HEADER = OSType("shnl")
        GENERAL_PREFERENCES = OSType("pgnp")
        LABEL_PREFERENCES = OSType("plbp")
        SIDEBAR_PREFERENCES = OSType("psid")
        ADVANCED_PREFERENCES = OSType("padv")

    class ViewSetting(Enum):
        """View options for lists of items in Finder windows."""

        ICON_VIEW = OSType("icnv")
        LIST_VIEW = OSType("lsvw")
        COLUMN_VIEW = OSType("clvw")
        GROUP_VIEW = OSType("flvw")
        FLOW_VIEW = OSType("flvw")

    class Arrangement(Enum):
        """Arrangement options for lists of items in Finder windows."""

        NOT_ARRANGED = OSType("narr")
        SNAP_TO_GRID = OSType("grda")
        BY_NAME = OSType("nama")
        BY_MODIFICATION_DATE = OSType("mdta")
        BY_CREATION_DATE = OSType("cdta")
        BY_SIZE = OSType("siza")
        BY_KIND = OSType("kina")
        BY_LABEL = OSType("laba")

    class LabelPosition(Enum):
        """Options for the label position of items in Finder windows."""

        RIGHT = OSType("lrgt")
        BOTTOM = OSType("lbot")

    class SortDirection(Enum):
        """Options for sort direction of lists of Finder items."""

        NORMAL = OSType("snrm")
        REVERSED = OSType("srvs")

    class ColumnName(Enum):
        """Columns in Finder windows."""

        NAME = OSType("esln")
        MODIFICATE_DATE = OSType("elsm")
        CREATION_DATE = OSType("elsc")
        SIZE = OSType("elss")
        KIND = OSType("elsk")
        LABEL = OSType("elsl")
        VERSION = OSType("elsv")
        COMMENT = OSType("elsC")

    class IconSize(Enum):
        """Options for the size of icons in Finder windows."""

        SMALL = OSType("smic")
        LARGE = OSType("lgic")

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFinderWindow
        self.xa_fmgr = NSFileManager.defaultManager()

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def visible(self) -> bool:
        """Whether Finder is currently visible."""
        return self.xa_scel.visible()

    @property
    def frontmost(self) -> bool:
        """Whether Finder is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def product_version(self) -> str:
        """The system software version."""
        return self.xa_scel.productVersion()

    @property
    def version(self) -> str:
        """The version of Finder"""
        return self.xa_scel.version()

    @property
    def selection(self) -> "XAFinderItemList":
        """The currently selected items in Finder."""
        return self._new_element(self.xa_scel.selection().get(), XAFinderItemList)

    @selection.setter
    def selection(self, selection: Union[list["XAFinderItem"], "XAFinderItemList"]):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property("selection", None)
        else:
            self.set_property("selection", selection.xa_elem)

    @property
    def insertion_location(self) -> "XAFinderFolder":
        """The container in which a new folder would be created in by default in the frontmost window."""
        folder_obj = self.xa_scel.windows()[0].target()
        return self._new_element(folder_obj, XAFinderFolder)

    @property
    def startup_disk(self) -> "XAFinderDisk":
        """The startup disk for this system."""
        disk_obk = self.xa_scel.startupDisk()
        return self._new_element(disk_obk, XAFinderDisk)

    @property
    def desktop(self) -> "XAFinderDesktop":
        """The user's desktop."""
        desktop_obj = self.xa_scel.desktop()
        return self._new_element(desktop_obj, XAFinderDesktop)

    @property
    def trash(self) -> "XAFinderTrash":
        """The system Trash."""
        trash_obj = self.xa_scel.trash()
        return self._new_element(trash_obj, XAFinderTrash)

    @property
    def home(self) -> "XAFinderFolder":
        """The home directory."""
        return self.home_directory()

    @property
    def computer_container(self) -> "XAFinderComputer":
        """The computer directory."""
        computer_obj = self.xa_scel.computerContainer()
        return self._new_element(computer_obj, XAFinderComputer)

    @property
    def desktop_picture(self) -> "XAFinderFile":
        """The desktop picture of the main monitor."""
        return self._new_element(self.xa_scel.desktopPicture(), XAFinderFile)

    @property
    def finder_preferences(self) -> "XAFinderPreferences":
        """Preferences for Finder as a whole."""
        prefs_obj = self.xa_scel.FinderPreferences()
        return self._new_element(prefs_obj, XAFinderPreferences)

    def _resolve_symlinks(self, path: str) -> str:
        """Resolves all symlinks in the specified path.

        :param path: The path to resolve.
        :type path: str
        :return: The fully resolved path as a string.
        :rtype: str

        .. versionadded:: 0.0.1
        """
        NS_str = AppKit.NSString.alloc().initWithString_(path)
        return NS_str.stringByResolvingSymlinksInPath()

    def select_item(self, path: str) -> "XAFinderApplication":
        """Selects the file or folder at the specified path.

        This opens a new tab of Finder unless the current tab is the parent folder of the provided path and no item is currently selected.

        :param path: The path of the file or folder to select.
        :type path: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Finder")
        >>> app.select_item("/Users/exampleuser/Documents/Example.txt")

        .. seealso:: :func:`select_items`

        .. versionadded:: 0.0.1
        """
        path = self._resolve_symlinks(path)
        self.xa_wksp.selectFile_inFileViewerRootedAtPath_(path, None)
        return self

    def select_items(self, paths: list[str]) -> "XAFinderApplication":
        """Selects the files or folders at the specified paths.

        This opens a new tab of Finder for each different parent folder in the list of paths to select. This method utilizes fast specialized methods from Objective-C to improve the performance of selecting large amounts of files. As such, when dealing with multiple file paths, this method should always be used instead of calling :func:`select_item` repeatedly.

        :param path: The paths to select.
        :type filepath: Union[str, AppKit.NSURL]
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Finder")
        >>> items = ["/Users/exampleuser/Documents/Example 1.txt", "/Users/exampleuser/Documents/Example 2.txt"]
        >>> app.select_items(items)

        .. seealso:: :func:`select_item`

        .. versionadded:: 0.0.1
        """
        self.temp_urls = []

        def resolve(path: Union[str, AppKit.NSURL], index: int, stop: bool):
            url = AppKit.NSURL.alloc().initWithString_(self._resolve_symlinks(path))
            self.temp_urls.append(url)

        AppKit.NSArray.alloc().initWithArray_(paths).enumerateObjectsUsingBlock_(
            resolve
        )
        self.xa_wksp.activateFileViewerSelectingURLs_(self.temp_urls)
        return self

    def recycle_item(self, path: Union[str, AppKit.NSURL]) -> "XAFinderApplication":
        """Moves the file or folder at the specified path to the trash.

         :param path: The path of the file or folder to recycle.
         :type path: Union[str, AppKit.NSURL]
         :return: A reference to the Finder application object.
         :rtype: XAFinderApplication

        :Example:

         >>> import PyXA
         >>> app = PyXA.Application("Finder")
         >>> app.recycle_item("/Users/exampleuser/Documents/Example.txt")

         .. seealso:: :func:`recycle_items`

         .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            if path.startswith("file://"):
                path = AppKit.NSURL.alloc().initWithString_(path)
            else:
                path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_fmgr.trashItemAtURL_resultingItemURL_error_(path, None, None)
        return self

    def empty_trash(self) -> "XAFinderApplication":
        """Empties the trash.

         :return: A reference to the Finder application object.
         :rtype: XAFinderApplication

        :Example:

         >>> import PyXA
         >>> app = PyXA.Application("Finder")
         >>> app.empty_trash()

         .. versionadded:: 0.0.1
        """
        self.xa_scel.emptySecurity_(True)
        return self

    def delete_item(self, path: Union[str, AppKit.NSURL]) -> "XAFinderApplication":
        """Permanently deletes the file or folder at the specified path.

         :param path: The path of the file or folder to delete.
         :type path: Union[str, AppKit.NSURL]
         :return: A reference to the Finder application object.
         :rtype: XAFinderApplication

        :Example:

         >>> import PyXA
         >>> app = PyXA.Application("Finder")
         >>> app.delete_item("/Users/exampleuser/Documents/Example.txt")

         .. seealso:: :func:`delete_items`

         .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            if path.startswith("file://"):
                path = AppKit.NSURL.alloc().initWithString_(path)
            else:
                path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_fmgr.removeItemAtURL_error_(path, None)
        return self

    def duplicate_item(self, path: str) -> "XAFinderApplication":
        """Duplicates the specified file or folder in its containing folder.

         The duplicated item will have the name of the original with " 2" added to the end.

         :param path: The path of the file or folder to duplicate.
         :type path: str
         :return: A reference to the Finder application object.
         :rtype: XAFinderApplication

        :Example:

         >>> import PyXA
         >>> app = PyXA.Application("Finder")
         >>> app.duplicate_item("/Users/exampleuser/Documents/Example.txt")

         .. seealso:: :func:`duplicate_items`

         .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            if path.startswith("file://"):
                path = AppKit.NSURL.alloc().initWithString_(path)
            else:
                path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        new_path = path

        copy_num = 1
        while new_path.checkResourceIsReachableAndReturnError_(None)[0]:
            if path.hasDirectoryPath():
                new_path = path.path() + f" {copy_num}"
            else:
                new_path = path.path().replace(
                    "." + path.pathExtension(), f" {copy_num}." + path.pathExtension()
                )
            new_path = AppKit.NSURL.alloc().initFileURLWithPath_(new_path)
            copy_num += 1
        self.xa_fmgr.copyItemAtURL_toURL_error_(path, new_path, None)
        return self

    def search(self, query: str) -> "XAFinderApplication":
        """Opens a Finder search window and searches for the specified term.

        :param query: The term to search.
        :type query: str
        :return: A reference to the Finder application object.
        :rtype: XAFinderApplication

        .. versionadded:: 0.0.1
        """
        self.xa_wksp.showSearchResultsForQueryString_(query)
        return self

    def get_labels(self) -> list[str]:
        """Gets the list of file labels.

        :return: The list of file labels.
        :rtype: str

        .. versionadded:: 0.0.1
        """
        return self.xa_wksp.fileLabels()

    # Directories
    def directory(self, path: Union[str, AppKit.NSURL]):
        """.. deprecated:: 0.1.1

        Use the :func:`folders` method with a filter instead.
        """
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def home_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's home directory.

        :return: A PyXA reference to the user's home directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = self.xa_fmgr.homeDirectoryForCurrentUser()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def temp_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the temporary directory for the current user.

        :return: A PyXA reference to the user's temporary directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = self.xa_fmgr.temporaryDirectory()
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def documents_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's documents directory.

        :return: A PyXA reference to the user's documents directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Documents"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def downloads_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's downloads directory.

        :return: A PyXA reference to the user's downloads directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Downloads"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def pictures_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's pictures directory.

        :return: A PyXA reference to the user's pictures directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Pictures"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def movies_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's movies directory.

        :return: A PyXA reference to the user's movies directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Movies"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def music_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's music directory.

        :return: A PyXA reference to the user's music directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Music"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def public_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the public directory.

        :return: A PyXA reference to the public directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Public"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def applications_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the system applications directory.

        :return: A PyXA reference to the system applications directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_("/Applications")
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def trash_directory(self) -> "XAFinderFolder":
        """Obtains a reference to the current user's trash directory.

        :return: A PyXA reference to the user's trash directory.
        :rtype: XAFinderFolder

        .. versionadded:: 0.0.1
        """
        path = AppKit.NSURL.alloc().initFileURLWithPath_(
            self.xa_fmgr.homeDirectoryForCurrentUser().path() + "/Trash"
        )
        folder_obj = self.xa_scel.folders().objectAtLocation_(path)
        return self._new_element(folder_obj, XAFinderFolder)

    def items(self, filter: dict = None) -> "XAFinderItemList":
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.items(), XAFinderItemList, filter)

    def containers(self, filter: dict = None) -> "XAFinderContainerList":
        """Returns a list of containers matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.containers(), XAFinderContainerList, filter
        )

    def disks(self, filter: dict = None) -> "XAFinderDiskList":
        """Returns a list of disks matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.disks(), XAFinderDiskList, filter)

    def folders(self, filter: dict = None) -> "XAFinderFolderList":
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.folders(), XAFinderFolderList, filter)

    def files(self, filter: dict = None) -> "XAFinderFileList":
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.files(), XAFinderFileList, filter)

    def alias_files(self, filter: dict = None) -> "XAFinderAliasFileList":
        """Returns a list of alias files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.aliasFiles(), XAFinderAliasFileList, filter
        )

    def application_files(self, filter: dict = None) -> "XAFinderApplicationFileList":
        """Returns a list of application files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.applicationFiles(), XAFinderApplicationFileList, filter
        )

    def document_files(self, filter: dict = None) -> "XAFinderDocumentFileList":
        """Returns a list of document files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.documentFiles(), XAFinderDocumentFileList, filter
        )

    def internet_location_files(
        self, filter: dict = None
    ) -> "XAFinderInternetLocationFileList":
        """Returns a list of internet location files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.internetLocationFiles(),
            XAFinderInternetLocationFileList,
            filter,
        )

    def clippings(self, filter: dict = None) -> "XAFinderClippingList":
        """Returns a list of clippings matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.clippings(), XAFinderClippingList, filter)

    def packages(self, filter: dict = None) -> "XAFinderPackageList":
        """Returns a list of packages matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.packages(), XAFinderPackageList, filter)

    def finder_windows(self, filter: dict = None) -> "XAFinderFinderWindowList":
        """Returns a list of Finder windows matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.FinderWindows(), XAFinderFinderWindowList, filter
        )

    def clipping_windows(self, filter: dict = None) -> "XAFinderClippingWindowList":
        """Returns a list of clipping windows matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_scel.clippingWindows(), XAFinderClippingWindowList, filter
        )


class XAFinderItemList(XABase.XAList):
    """A wrapper around lists of Finder items that employs fast enumeration techniques.

    All properties of Finder items can be called as methods on the wrapped list, returning a list containing each item's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, object_class=None
    ):
        if object_class is None:
            object_class = XAFinderItem
        super().__init__(properties, object_class, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def name_extension(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("nameExtension") or [])

    def extension_hidden(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("extensionHidden") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def position(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("position") or [])

    def desktop_position(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("desktopPosition") or [])

    def bounds(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        return list(self.xa_elem.arrayByApplyingSelector_("bounds") or [])

    def label_index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("labelIndex") or [])

    def locked(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("locked") or [])

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def description(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("description") or [])

    def comment(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment") or [])

    def size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("size") or [])

    def physical_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("physicalSize") or [])

    def creation_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("creationDate") or [])

    def modification_date(self) -> list[datetime]:
        return list(self.xa_elem.arrayByApplyingSelector_("modificationDate") or [])

    def url(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAPath(x[7:]) for x in ls]

    def owner(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("owner") or [])

    def group(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("group") or [])

    def owner_privileges(self) -> list[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("ownerPrivileges") or [])

    def group_privileges(self) -> list[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("groupPrivileges") or [])

    def everyone_privileges(self) -> list[XAFinderApplication.PrivacySetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("everyonePrivileges") or [])

    def container(self) -> "XAFinderContainerList":
        ls = self.xa_elem.arrayByApplyingSelector_("container") or []
        return self._new_element(ls, XAFinderContainerList)

    def disk(self) -> "XAFinderDiskList":
        ls = self.xa_elem.arrayByApplyingSelector_("disk") or []
        return self._new_element(ls, XAFinderDiskList)

    def icon(self) -> XABase.XAImageList:
        ls = self.xa_elem.arrayByApplyingSelector_("icon") or []
        return self._new_element(ls, XABase.XAImageList)

    def information_window(self) -> "XAFinderInformationWindowList":
        ls = self.xa_elem.arrayByApplyingSelector_("informationWindow") or []
        return self._new_element(ls, XAFinderInformationWindowList)

    def by_name(self, name: str) -> Union["XAFinderItem", None]:
        return self.by_property("name", name)

    def by_displayed_name(self, displayed_name: str) -> Union["XAFinderItem", None]:
        return self.by_property("displayedName", displayed_name)

    def by_name_extension(self, name_extension: str) -> Union["XAFinderItem", None]:
        return self.by_property("nameExtension", name_extension)

    def by_extension_hidden(
        self, extension_hidden: bool
    ) -> Union["XAFinderItem", None]:
        return self.by_property("extensionHidden", extension_hidden)

    def by_index(self, index: int) -> Union["XAFinderItem", None]:
        return self.by_property("index", index)

    def by_position(self, position: tuple[int, int]) -> Union["XAFinderItem", None]:
        return self.by_property("position", position)

    def by_desktop_position(
        self, desktop_position: tuple[int, int]
    ) -> Union["XAFinderItem", None]:
        return self.by_property("desktopPosition", desktop_position)

    def by_bounds(
        self, bounds: tuple[tuple[int, int], tuple[int, int]]
    ) -> Union["XAFinderItem", None]:
        return self.by_property("bounds", bounds)

    def by_label_index(self, label_index: index) -> Union["XAFinderItem", None]:
        return self.by_property("labelIndex", label_index)

    def by_locked(self, locked: bool) -> Union["XAFinderItem", None]:
        return self.by_property("locked", locked)

    def by_kind(self, kind: str) -> Union["XAFinderItem", None]:
        return self.by_property("kind", kind)

    def by_description(self, description: str) -> Union["XAFinderItem", None]:
        return self.by_property("description", description)

    def by_comment(self, comment: str) -> Union["XAFinderItem", None]:
        return self.by_property("comment", comment)

    def by_size(self, size: int) -> Union["XAFinderItem", None]:
        return self.by_property("size", size)

    def by_physical_size(self, physical_size: int) -> Union["XAFinderItem", None]:
        return self.by_property("physicalSize", physical_size)

    def by_creation_date(self, creation_date: datetime) -> Union["XAFinderItem", None]:
        return self.by_property("creationDate", creation_date)

    def by_modification_date(
        self, modification_date: datetime
    ) -> Union["XAFinderItem", None]:
        return self.by_property("modificationDate", modification_date)

    def by_url(self, url: Union[str, XABase.XAPath]) -> Union["XAFinderItem", None]:
        if isinstance(url, str):
            url = XABase.XAPath(url)
        return self.by_property("URL", str(url.xa_elem))

    def by_owner(self, owner: str) -> Union["XAFinderItem", None]:
        return self.by_property("owner", owner)

    def by_group(self, group: str) -> Union["XAFinderItem", None]:
        return self.by_property("group", group)

    def by_owner_privileges(
        self, owner_privileges: XAFinderApplication.PrivacySetting
    ) -> Union["XAFinderItem", None]:
        return self.by_property("ownerPrivileges", owner_privileges)

    def by_group_privileges(
        self, group_privileges: XAFinderApplication.PrivacySetting
    ) -> Union["XAFinderItem", None]:
        return self.by_property("groupPrivileges", group_privileges)

    def by_everyone_privileges(
        self, everyone_privileges: XAFinderApplication.PrivacySetting
    ) -> Union["XAFinderItem", None]:
        return self.by_property("everyonePrivileges", everyone_privileges)

    def by_container(
        self, container: "XAFinderContainer"
    ) -> Union["XAFinderItem", None]:
        return self.by_property("container", container.xa_elem)

    def by_disk(self, disk: "XAFinderDisk") -> Union["XAFinderItem", None]:
        return self.by_property("disk", disk.xa_elem)

    def by_icon(self, icon: XAImage) -> Union["XAFinderItem", None]:
        return self.by_property("icon", icon.value)

    def by_information_window(
        self, information_window: "XAFinderInformationWindow"
    ) -> Union["XAFinderItem", None]:
        return self.by_property("informationWindow", information_window.xa_elem)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each item in the list.

        When the clipboard content is set to a list of Finder items, each item's name and URL are added to the clipboard.

        :return: The name and URL of each item in the list
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        names = self.name()
        urls = self.url()
        for index, name in enumerate(names):
            items.append(name)
            items.append(urls[index].xa_elem)
        return items

    def __repr__(self):
        return f"<{str(type(self))}{str(self.name())}>"


class XAFinderItem(XABase.XAObject, XASelectable, XADeletable, XAClipboardCodable):
    """A generic class with methods common to the various item classes of Finder.

    .. seealso:: :class:`XAFinderContainer`, :class:`XAFinderFile`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """Every property of an item."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the item."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def displayed_name(self) -> str:
        """The user-visible name of the item."""
        return self.xa_elem.displayedName()

    @property
    def name_extension(self) -> str:
        """The file extension of the item."""
        return self.xa_elem.nameExtension()

    @name_extension.setter
    def name_extension(self, name_extension: str):
        self.set_property("nameExtension", name_extension)

    @property
    def extension_hidden(self) -> bool:
        """Whether the file extension is hidden."""
        return self.xa_elem.extensionHidden()

    @extension_hidden.setter
    def extension_hidden(self, extension_hidden: bool):
        self.set_property("extensionHidden", extension_hidden)

    @property
    def index(self) -> int:
        """The index within the containing folder/disk."""
        return self.xa_elem.index()

    @property
    def position(self) -> XAPoint:
        """The position of the item within the parent window."""
        return XAPoint(*self.xa_elem.position())

    @position.setter
    def position(self, position: Union[tuple[int, int], XAPoint]):
        position = AppKit.NSValue.valueWithPoint_(position)
        self.set_property("position", position)

    @property
    def desktop_position(self) -> XAPoint:
        """The position of an item on the desktop."""
        return XAPoint(*self.xa_elem.desktopPosition())

    @desktop_position.setter
    def desktop_position(self, desktop_position: Union[tuple[int, int], XAPoint]):
        desktop_position = AppKit.NSValue.valueWithPoint_(desktop_position)
        self.set_property("desktopPosition", desktop_position)

    @property
    def bounds(self) -> XARectangle:
        """The bounding rectangle of an item."""
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
    def label_index(self) -> int:
        """The label assigned to the item."""
        return self.xa_elem.labelIndex()

    @label_index.setter
    def label_index(self, label_index: int):
        self.set_property("labelIndex", label_index)

    @property
    def locked(self) -> bool:
        """Whether the file is locked."""
        return self.xa_elem.locked()

    @locked.setter
    def locked(self, locked: bool):
        self.set_property("locked", locked)

    @property
    def kind(self) -> str:
        """The kind of the item, e.g. "Folder" or "File"."""
        return self.xa_elem.kind()

    @property
    def description(self) -> str:
        """The description of the item."""
        return self.xa_elem.description()

    @property
    def comment(self) -> str:
        """The user-specified comment on the item."""
        return self.xa_elem.comment()

    @comment.setter
    def comment(self, comment: str):
        self.set_property("comment", comment)

    @property
    def size(self) -> int:
        """The logical size of the item."""
        return self.xa_elem.size()

    @property
    def physical_size(self) -> int:
        """The actual disk space used by the item."""
        return self.xa_elem.physicalSize()

    @property
    def creation_date(self) -> datetime:
        """The date the item was created."""
        return self.xa_elem.creationDate()

    @property
    def modification_date(self) -> datetime:
        """The date the item was last modified."""
        return self.xa_elem.modificationDate()

    @modification_date.setter
    def modification_date(self, modification_date: datetime):
        self.set_property("modificationDate", modification_date)

    @property
    def url(self) -> XABase.XAPath:
        """The URL of the item."""
        return XABase.XAPath(self.xa_elem.URL()[7:])

    @property
    def owner(self) -> str:
        """The name of the user that owns the item."""
        return self.xa_elem.owner()

    @owner.setter
    def owner(self, owner: str):
        self.set_property("owner", owner)

    @property
    def group(self) -> str:
        """The name of the group that has access to the item."""
        return self.xa_elem.group()

    @group.setter
    def group(self, group: str):
        self.set_property("group", group)

    @property
    def owner_privileges(self) -> XAFinderApplication.PrivacySetting:
        """The privilege level of the owner, e.g. "read only"."""
        return self.xa_elem.ownerPrivileges()

    @owner_privileges.setter
    def owner_privileges(self, owner_privileges: XAFinderApplication.PrivacySetting):
        self.set_property("ownerPrivileges", owner_privileges.value)

    @property
    def group_privileges(self) -> XAFinderApplication.PrivacySetting:
        """The privilege level of the group, e.g. "write only"."""
        return self.xa_elem.groupPrivileges()

    @group_privileges.setter
    def group_privileges(self, group_privileges: XAFinderApplication.PrivacySetting):
        self.set_property("groupPrivileges", group_privileges.value)

    @property
    def everyone_privileges(self) -> XAFinderApplication.PrivacySetting:
        """The privilege level of everyone else, e.g. "none"."""
        return self.xa_elem.everyonePrivileges()

    @everyone_privileges.setter
    def everyone_privileges(
        self, everyone_privileges: XAFinderApplication.PrivacySetting
    ):
        self.set_property("everyoneErivileges", everyone_privileges.value)

    @property
    def container(self) -> "XAFinderContainer":
        """The container of the item."""
        container_obj = self.xa_elem.container()
        kind = container_obj.kind()
        if kind == "Folder":
            return self._new_element(container_obj, XAFinderFolder)
        elif kind == "Volume":
            return self._new_element(container_obj, XAFinderDisk)
        elif kind == "":
            # TODO: Computer container
            print("item container todo")
            pass

    @property
    def disk(self) -> "XAFinderDisk":
        """The disk on which the item is stored."""
        disk_obj = self.xa_elem.disk()
        return self._new_element(disk_obj, XAFinderDisk)

    @property
    def icon(self) -> XAImage:
        """The icon bitmap of the item's icon."""
        icon_obj = self.xa_elem.icon()
        return self._new_element(icon_obj, XAImage)

    @icon.setter
    def icon(self, icon: XAImage):
        self.set_property("icon", icon.xa_elem)

    @property
    def information_window(self) -> "XAFinderInformationWindow":
        """The information window for this item."""
        window_obj = self.xa_elem.informationWindow()
        return self._new_element(window_obj, XAFinderInformationWindow)

    def reveal(self) -> "XAFinderItem":
        """Reveals the item in the frontmost Finder window.

        :return: A reference to the item object
        :rtype: XAFinderItem

        .. versionadded:: 0.0.4
        """
        self.xa_elem.reveal()
        return self

    def copy(self) -> "XAFinderItem":
        """Copies the item to the clipboard.

        :return: A reference to the Finder item that called this method.
        :rtype: XAFinderItem

        .. versionadded:: 0.0.1
        """
        url = AppKit.NSURL.alloc().initWithString_(self.URL).absoluteURL()
        self.set_clipboard(url)
        return self

    def move_to(
        self, new_path: Union[str, AppKit.NSURL], overwrite: bool = False
    ) -> "XAFinderItem":
        """Moves the item to the specified path.

        :param new_path: The path to move the item to.
        :type new_path: Union[str, AppKit.NSURL]
        :param overwrite: Whether to overwrite existing files of the same name at the target path, defaults to False
        :type overwrite: bool, optional
        :return: A reference to the Finder item that called this method.
        :rtype: XAFinderItem

        .. versionadded:: 0.0.1
        """
        if isinstance(new_path, str):
            new_path = AppKit.NSURL.alloc().initFileURLWithPath_(new_path)
        old_path = AppKit.NSURL.alloc().initWithString_(self.URL)
        self.xa_fmgr.moveItemAtURL_toURL_error_(old_path, new_path, None)
        return self

    def exists(self) -> bool:
        """Checks whether the item exists on the disk or not.

        :return: True if the item exists, false otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.exists()

    def open(self):
        """Opens the item in its default application.

        .. versionadded:: 0.0.2
        """
        self.url.open()

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of the item.

        When the clipboard content is set to a Finder item, the item's name and URL are added to the clipboard.

        :return: The name and URL of the item
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [self.name, self.url.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAFinderContainerList(XAFinderItemList):
    """A wrapper around lists of containers that employs fast enumeration techniques.

    All properties of containers can be called as methods on the wrapped list, returning a list with each container's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, object_class=None
    ):
        if object_class is None:
            object_class = XAFinderContainer
        super().__init__(properties, filter, object_class)

    def entire_contents(self) -> "XAFinderItemList":
        ls = self.xa_elem.arrayByApplyingSelector_("entireContents") or []
        return self._new_element(ls, XAFinderItemList)

    def container_window(self) -> "XAFinderFinderWindowList":
        ls = self.xa_elem.arrayByApplyingSelector_("containerWindow") or []

        parent = self.xa_prnt
        while not hasattr(parent, "xa_wcls"):
            parent = parent.xa_prnt
        self.xa_wcls = parent.xa_wcls

        return self._new_element(ls, XAFinderFinderWindowList)

    def items(self) -> XAFinderItemList:
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("items") or [], XAFinderItemList
        )

    def containers(self) -> "XAFinderContainerList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("containers") or [],
            XAFinderContainerList,
        )

    def folders(self) -> "XAFinderFolderList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("folders") or [], XAFinderFolderList
        )

    def files(self) -> "XAFinderFileList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("files") or [], XAFinderFileList
        )

    def alias_files(self) -> "XAFinderAliasFileList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("aliasFiles") or [],
            XAFinderAliasFileList,
        )

    def application_files(self) -> "XAFinderApplicationFileList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("applicationFiles") or [],
            XAFinderApplicationFileList,
        )

    def document_files(self) -> "XAFinderDocumentFileList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("documentFiles") or [],
            XAFinderDocumentFileList,
        )

    def internet_location_files(self) -> "XAFinderInternetLocationFileList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("internetLocationFiles") or [],
            XAFinderInternetLocationFileList,
        )

    def clippings(self) -> "XAFinderClippingList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("clippings") or [],
            XAFinderClippingList,
        )

    def packages(self) -> "XAFinderPackageList":
        return self._new_element(
            self.xa_elem.arrayByApplyingSelector_("packages") or [], XAFinderPackageList
        )

    def by_entire_contents(
        self, entire_contents: XAFinderItemList
    ) -> Union["XAFinderContainer", None]:
        return self.by_property("entireContents", entire_contents.xa_elem)

    def by_container_window(
        self, container_window: "XAFinderFinderWindow"
    ) -> Union["XAFinderContainer", None]:
        return self.by_property("containerWindow", container_window.xa_elem)


class XAFinderContainer(XAFinderItem):
    """A class for managing and interacting with containers in Finder.

    .. seealso:: :class:`XAFinderDisk`, :class:`XAFinderFolder`

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def entire_contents(self):
        """The entire contents of the container, including the contents of its children."""
        obj = self.xa_elem.entireContents().get()
        return self._new_element(obj, XAFinderItemList)

    @property
    def container_window(self):
        """The container window for this folder."""
        window_obj = self.xa_elem.containerWindow()
        return self._new_element(window_obj, XAFinderFinderWindow)

    def items(self, filter: dict = None) -> "XAFinderItemList":
        """Returns a list of items matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.items(), XAFinderItemList, filter)

    def containers(self, filter: dict = None) -> "XAFinderContainerList":
        """Returns a list of containers matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_elem.containers(), XAFinderContainerList, filter
        )

    def folders(self, filter: dict = None) -> "XAFinderFolderList":
        """Returns a list of folders matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.folders(), XAFinderFolderList, filter)

    def files(self, filter: dict = None) -> "XAFinderFileList":
        """Returns a list of files matching the filter.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.files(), XAFinderFileList, filter)

    def alias_files(self, filter: dict = None) -> "XAFinderAliasFileList":
        """Returns a list of alias files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_elem.aliasFiles(), XAFinderAliasFileList, filter
        )

    def application_files(self, filter: dict = None) -> "XAFinderApplicationFileList":
        """Returns a list of application files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_elem.applicationFiles(), XAFinderApplicationFileList, filter
        )

    def document_files(self, filter: dict = None) -> "XAFinderDocumentFileList":
        """Returns a list of document files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_elem.documentFiles(), XAFinderDocumentFileList, filter
        )

    def internet_location_files(
        self, filter: dict = None
    ) -> "XAFinderInternetLocationFileList":
        """Returns a list of internet location files matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(
            self.xa_elem.internetLocationFiles(),
            XAFinderInternetLocationFileList,
            filter,
        )

    def clippings(self, filter: dict = None) -> "XAFinderClippingList":
        """Returns a list of clippings matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.clippings(), XAFinderClippingList, filter)

    def packages(self, filter: dict = None) -> "XAFinderPackageList":
        """Returns a list of packages matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.packages(), XAFinderPackageList, filter)


class XAFinderDiskList(XAFinderContainerList):
    """A wrapper around lists of disks that employs fast enumeration techniques.

    All properties of disks can be called as methods on the wrapped list, returning a list containing each disk's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderDisk)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def capacity(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("capacity") or [])

    def free_space(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("freeSpace") or [])

    def ejectable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ejectable") or [])

    def local_volume(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("localVolume") or [])

    def startup(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("startup") or [])

    def format(self) -> list[XAFinderApplication.ItemFormat]:
        return list(self.xa_elem.arrayByApplyingSelector_("format") or [])

    def journaling_enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("journalingEnabled") or [])

    def ignore_privileges(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ignorePrivileges") or [])

    def by_id(self, id: int) -> Union["XAFinderDisk", None]:
        return self.by_property("id", id)

    def by_capacity(self, capacity: int) -> Union["XAFinderDisk", None]:
        return self.by_property("capacity", capacity)

    def by_free_space(self, free_space: int) -> Union["XAFinderDisk", None]:
        return self.by_property("freeSpace", free_space)

    def by_ejectable(self, ejectable: bool) -> Union["XAFinderDisk", None]:
        return self.by_property("ejectable", ejectable)

    def by_local_volume(self, local_volume: bool) -> Union["XAFinderDisk", None]:
        return self.by_property("localVolume", local_volume)

    def by_startup(self, startup: bool) -> Union["XAFinderDisk", None]:
        return self.by_property("startup", startup)

    def by_format(
        self, format: XAFinderApplication.ItemFormat
    ) -> Union["XAFinderDisk", None]:
        return self.by_property("format", format)

    def by_journaling_enabled(
        self, journaling_enabled: bool
    ) -> Union["XAFinderDisk", None]:
        return self.by_property("journalingEnabled", journaling_enabled)

    def by_ignore_privileges(
        self, ignore_privileges: bool
    ) -> Union["XAFinderDisk", None]:
        return self.by_property("ignorePrivileges", ignore_privileges)


class XAFinderDisk(XAFinderContainer):
    """A class for managing and interacting with disks in Finder.

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """A unique identifier for the disk that is persistent for as long as the disc is connected and Finder is running."""
        return self.xa_elem.id()

    @property
    def capacity(self) -> int:
        """The total number of bytes on the disk."""
        return self.xa_elem.capacity()

    @property
    def free_space(self) -> int:
        """The number of free bytes left on the disk."""
        return self.xa_elem.freeSpace()

    @property
    def ejectable(self) -> bool:
        """Whether the disk can be ejected."""
        return self.xa_elem.ejectable()

    @property
    def local_volume(self) -> bool:
        """Whether the disk is a local volume vs. a file server."""
        return self.xa_elem.localVolume()

    @property
    def startup(self) -> bool:
        """Whether the disk is the boot disk."""
        return self.xa_elem.startup()

    @property
    def format(self) -> XAFinderApplication.ItemFormat:
        """The format of the disk, e.g. "APFS format"."""
        return self.xa_elem.format()

    @property
    def journaling_enabled(self) -> bool:
        """Whether the disk does file system journaling."""
        return self.xa_elem.journalingEnabled()

    @property
    def ignore_privileges(self) -> bool:
        """Whether to ignore permissions on the disk."""
        return self.xa_elem.ignorePrivileges()

    @ignore_privileges.setter
    def ignore_privileges(self, ignore_privileges: bool):
        self.set_property("ignorePrivileges", ignore_privileges)


class XAFinderFolderList(XAFinderContainerList):
    """A wrapper around lists of folders that employs fast enumeration techniques.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderFolder)


class XAFinderFolder(XAFinderContainer):
    """A class for managing and interacting with folders in Finder.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderTrash(XAFinderContainer):
    """A class for managing and interacting with Finder's Trash.

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def warns_before_emptying(self) -> bool:
        """Whether to display a dialog before emptying the Trash."""
        return self.xa_elem.warnsBeforeEmptying()

    @warns_before_emptying.setter
    def warns_before_emptying(self, warns_before_emptying: bool):
        self.set_property("warnsBeforeEmptying", warns_before_emptying)


class XAFinderComputer(XAFinderItem):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderFileList(XAFinderItemList):
    """A wrapper around lists of files that employs fast enumeration techniques.

    All properties of files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAFinderFile
        super().__init__(properties, filter, obj_class)

    def file_type(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("fileType") or [])

    def creator_type(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("creatorType") or [])

    def stationery(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("stationery") or [])

    def product_version(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("productVersion") or [])

    def version(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("version") or [])

    def by_file_type(self, file_type: int) -> Union["XAFinderFile", None]:
        return self.by_property("fileType", file_type)

    def by_creator_type(self, creator_type: int) -> Union["XAFinderFile", None]:
        return self.by_property("creatorType", creator_type)

    def by_stationery(self, stationery: bool) -> Union["XAFinderFile", None]:
        return self.by_property("stationery", stationery)

    def by_product_version(self, product_version: str) -> Union["XAFinderFile", None]:
        return self.by_property("productVersion", product_version)

    def by_version(self, version: str) -> Union["XAFinderFile", None]:
        return self.by_property("version", version)


class XAFinderFile(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with files in Finder.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def file_type(self) -> int:
        """The OSType of the file and the data within it."""
        return self.xa_elem.fileType()

    @file_type.setter
    def file_type(self, file_type: int):
        self.set_property("fileType", file_type)

    @property
    def creator_type(self) -> int:
        """The OSType of the application that created the file."""
        return self.xa_elem.creatorType()

    @creator_type.setter
    def creator_type(self, creator_type: int):
        self.set_property("creatorType", creator_type)

    @property
    def stationery(self) -> bool:
        """Whether the file is a stationery pad."""
        return self.xa_elem.stationery()

    @stationery.setter
    def stationery(self, stationery: bool):
        self.set_property("stationery", stationery)

    @property
    def product_version(self) -> str:
        """The version of the application the file was created with."""
        return self.xa_elem.productVersion()

    @property
    def version(self) -> str:
        """The version of the file."""
        return self.xa_elem.version()


class XAFinderAliasFileList(XAFinderFileList):
    """A wrapper around lists of alias files that employs fast enumeration techniques.

    All properties of alias files can be called as methods on the wrapped list, returning a list containing each alias files's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderAliasFile)

    def original_item(self) -> list[XAFinderItem]:
        return list(self.xa_elem.arrayByApplyingSelector_("originalItem") or [])

    def by_original_item(
        self, original_item: XAFinderItem
    ) -> Union["XAFinderAliasFile", None]:
        return self.by_property("originalItem", original_item)


class XAFinderAliasFile(XAFinderFile):
    """A class for managing and interacting with alias files in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def original_item(self) -> XAFinderItem:
        """The original item pointed to by the alias."""
        item_obj = self.xa_elem.originalItem()
        return self._new_element(item_obj, XAFinderItem)

    @original_item.setter
    def original_item(self, original_item: XAFinderItem):
        self.set_property("originalItem", original_item.xa_elem)


class XAFinderApplicationFileList(XAFinderFileList):
    """A wrapper around lists of application files that employs fast enumeration techniques.

    All properties of application files can be called as methods on the wrapped list, returning a list containing each application file's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderApplicationFile)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def has_scripting_terminology(self) -> list[bool]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("hasScriptingTerminology") or []
        )

    def by_id(self, id: str) -> Union["XAFinderApplicationFile", None]:
        return self.by_property("id", id)

    def by_has_scripting_terminology(
        self, has_scripting_terminology: bool
    ) -> Union["XAFinderApplicationFile", None]:
        return self.by_property("hasScriptingTerminology", has_scripting_terminology)


class XAFinderApplicationFile(XAFinderFile):
    """A class for managing and interacting with application files in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The bundle identifier or creator type of the application."""
        return self.xa_elem.id()

    @property
    def has_scripting_terminology(self) -> bool:
        """Whether the process can be scripted."""
        return self.xa_elem.hasScriptingTerminology()


class XAFinderDocumentFileList(XAFinderFileList):
    """A wrapper around lists of document files that employs fast enumeration techniques.

    All properties of document files can be called as methods on the wrapped list, returning a list containing each document file's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderDocumentFile)


class XAFinderDocumentFile(XAFinderFile):
    """A class for managing and interacting with document files in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderInternetLocationFileList(XAFinderFileList):
    """A wrapper around lists of internet location files that employs fast enumeration techniques.

    All properties of internet location files can be called as methods on the wrapped list, returning a list containing each file's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderInternetLocationFile)

    def location(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("location") or [])

    def by_location(self, location: str) -> Union["XAFinderInternetLocationFile", None]:
        return self.by_property("location", location)


class XAFinderInternetLocationFile(XAFinderFile):
    """A class for managing and interacting with internet location files in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def location(self) -> str:
        """The internet location."""
        return self.xa_elem.location()


class XAFinderClippingList(XAFinderFileList):
    """A wrapper around lists of clippings that employs fast enumeration techniques.

    All properties of clippings can be called as methods on the wrapped list, returning a list containing each clipping's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderClipping)


class XAFinderClipping(XAFinderFile):
    """A class for managing and interacting with clippings in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPackageList(XAFinderItemList):
    """A wrapper around lists of packages that employs fast enumeration techniques.

    All properties of packages can be called as methods on the wrapped list, returning a list containing each package's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderPackage)


class XAFinderPackage(XAFinderItem):
    """A class for managing and interacting with packages in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderWindowList(XABaseScriptable.XASBWindowList):
    """A wrapper around lists of Finder windows that employs fast enumeration techniques.

    All properties of Finder windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAFinderWindowList
        super().__init__(properties, filter, obj_class)

    def position(self) -> list[XAPoint]:
        ls = self.xa_elem.arrayByApplyingSelector_("position") or []
        return [XAPoint(value) for value in ls]

    def titled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("titled") or [])

    def floating(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("floating") or [])

    def modal(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modal") or [])

    def collapsed(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("collapsed") or [])

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def by_position(self, position: tuple[int, int]) -> Union["XAFinderWindow", None]:
        return self.by_property("position", position)

    def by_titled(self, titled: bool) -> Union["XAFinderWindow", None]:
        return self.by_property("titled", titled)

    def by_floating(self, floating: bool) -> Union["XAFinderWindow", None]:
        return self.by_property("floating", floating)

    def by_modal(self, modal: bool) -> Union["XAFinderWindow", None]:
        return self.by_property("modal", modal)

    def by_collapsed(self, collapsed: bool) -> Union["XAFinderWindow", None]:
        return self.by_property("collapsed", collapsed)

    def by_properties(self, properties: dict) -> Union["XAFinderWindow", None]:
        return self.by_property("properties", properties)


class XAFinderWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with windows of Finder.app.

    :Example 1: Setting the bounds of a Finder window

    >>> import PyXA
    >>> app = PyXA.Application("Finder")
    >>> window = app.windows()[0]
    >>> lock = False
    >>> (old_w, old_h) = (0,0)
    >>> while True:
    >>>     if window.position.y < 50 and lock is False:
    >>>         # Increase height of window when user drags it to the top
    >>>         (old_w, old_h) = window.bounds.size
    >>>         (x, y) = window.position
    >>>         window.set_property("bounds", ((x, y), (old_w, 2000)))
    >>>         lock = True
    >>>     if lock is True and window.position.y > 55:
    >>>         # Return to original size if user moves window down
    >>>         (x, y) = window.position
    >>>         window.set_property("bounds", ((x, y), (old_w, old_h)))
    >>>         lock = False

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def position(self) -> XAPoint:
        """The upper left position of the window."""
        return XAPoint(*self.xa_elem.position())

    @position.setter
    def position(self, position: Union[tuple[int, int], XAPoint]):
        value = AppKit.NSValue.valueWithPoint_(position)
        self.set_property("position", value)

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar."""
        return self.xa_elem.titled()

    @property
    def floating(self) -> bool:
        """Whether the window floats."""
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is modal."""
        return self.xa_elem.modal()

    @property
    def collapsed(self) -> bool:
        """Whether the window is collapsed."""
        return self.xa_elem.collapsed()

    @collapsed.setter
    def collapsed(self, collapsed: bool):
        self.set_property("collapsed", collapsed)

    @property
    def properties(self) -> dict:
        """Every property of a Finder window."""
        return self.xa_elem.properties()


class XAFinderFinderWindowList(XAFinderWindowList):
    """A wrapper around lists of Finder internal windows (such as preference and information windows) that employs fast enumeration techniques.

    All properties of the windows can be called as methods on the wrapped list, returning a list containing each windows's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderFinderWindow)

        parent = self.xa_prnt
        while not hasattr(parent, "xa_wcls"):
            parent = parent.xa_prnt
        self.xa_wcls = parent.xa_wcls

    def current_view(self) -> list[XAFinderApplication.ViewSetting]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentView") or [])

    def toolbar_visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("toolbarVisible") or [])

    def statusbar_visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("statusbarVisible") or [])

    def pathbar_visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("pathbarVisible") or [])

    def sidebar_width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("sidebarWidth") or [])

    def target(self) -> XAFinderContainerList:
        ls = self.xa_elem.arrayByApplyingSelector_("target") or []
        return self._new_element(ls, XAFinderContainerList)

    def icon_view_options(self) -> list["XAFinderIconViewOptions"]:
        return list(self.xa_elem.arrayByApplyingSelector_("iconViewOptions") or [])

    def list_view_options(self) -> list["XAFinderListViewOptions"]:
        return list(self.xa_elem.arrayByApplyingSelector_("listViewOptions") or [])

    def column_view_options(self) -> list["XAFinderColumnViewOptions"]:
        return list(self.xa_elem.arrayByApplyingSelector_("columnViewOptions") or [])

    def by_current_view(
        self, current_view: XAFinderApplication.ViewSetting
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("currentView", current_view)

    def by_toolbar_visible(
        self, toolbar_visible: bool
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("toolbarVisible", toolbar_visible)

    def by_statusbar_visible(
        self, statusbar_visible: bool
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("statusbarVisible", statusbar_visible)

    def by_pathbar_visible(
        self, pathbar_visible: bool
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("pathbarVisible", pathbar_visible)

    def by_sidebar_width(
        self, sidebar_width: int
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("sidebarWidth", sidebar_width)

    def by_target(
        self, target: XAFinderContainer
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("target", target)

    def by_icon_view_options(
        self, icon_view_options: "XAFinderIconViewOptions"
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("iconViewOptions", icon_view_options)

    def by_list_view_options(
        self, list_view_options: "XAFinderListViewOptions"
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("listViewOptions", list_view_options)

    def by_column_view_options(
        self, column_view_options: "XAFinderColumnViewOptions"
    ) -> Union["XAFinderFinderWindow", None]:
        return self.by_property("columnViewOptions", column_view_options)


class XAFinderFinderWindow(XAFinderWindow):
    """A class for managing and interacting with internal windows within Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def current_view(self) -> XAFinderApplication.ViewSetting:
        """The current view for the container window."""
        return self.xa_elem.currentView()

    @current_view.setter
    def current_view(self, current_view: XAFinderApplication.ViewSetting):
        self.set_property("currentView", current_view.value)

    @property
    def toolbar_visible(self) -> bool:
        """Whether the window's toolbar is visible."""
        return self.xa_elem.toolbarVisible()

    @toolbar_visible.setter
    def toolbar_visible(self, toolbar_visible: bool):
        self.set_property("toolbarVisible", toolbar_visible)

    @property
    def statusbar_visible(self) -> bool:
        """Whether the window's status bar is visible."""
        return self.xa_elem.statusbarVisible()

    @statusbar_visible.setter
    def statusbar_visible(self, statusbar_visible: bool):
        self.set_property("statusbarVisible", statusbar_visible)

    @property
    def pathbar_visible(self) -> bool:
        """Whether the window's path bar is visible."""
        return self.xa_elem.pathbarVisible()

    @pathbar_visible.setter
    def pathbar_visible(self, pathbar_visible: bool):
        self.set_property("pathbarVisible", pathbar_visible)

    @property
    def sidebar_width(self) -> int:
        """The width of the sidebar in pixels."""
        return self.xa_elem.sidebarWidth()

    @sidebar_width.setter
    def sidebar_width(self, sidebar_width: int):
        self.set_property("sidebarWidth", sidebar_width)

    @property
    def target(self) -> XAFinderContainer:
        """The container at which this file viewer is targeted."""
        obj = self.xa_elem.target()
        return self._new_element(obj, XAFinderContainer)

    @target.setter
    def target(self, target: XAFinderContainer):
        self.set_property("target", target.xa_elem)

    @property
    def icon_view_options(self) -> "XAFinderIconViewOptions":
        """The icon view options for the container window."""
        options_obj = self.xa_elem.iconViewOptions()
        return self._new_element(options_obj, XAFinderIconViewOptions)

    @property
    def list_view_options(self) -> "XAFinderListViewOptions":
        """The list view options for the container window."""
        options_obj = self.xa_elem.listViewOptions()
        return self._new_element(options_obj, XAFinderListViewOptions)

    @property
    def column_view_options(self) -> "XAFinderColumnViewOptions":
        """The column view options for the container window."""
        options_obj = self.xa_elem.columnViewOptions()
        return self._new_element(options_obj, XAFinderColumnViewOptions)


class XAFinderDesktop(XAFinderContainer):
    """A class for managing and interacting with the Desktop.

    .. versionadded:: 0.0.2
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def window(self) -> "XAFinderDesktopWindow":
        """The desktop window."""
        return self._new_element(self.xa_elem.window(), XAFinderDesktopWindow)


class XAFinderDesktopWindow(XAFinderWindow):
    """A class representing the containing window around Finder's desktop element.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderClippingWindowList(XAFinderWindowList):
    """A wrapper around lists of clipping windows that employs fast enumeration techniques.

    All properties of clipping windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderClippingWindow)


class XAFinderClippingWindow(XAFinderWindow, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with clipping windows in Finder.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFinderPreferences(XAFinderItem, XABaseScriptable.XASBPrintable):
    """A class for managing general preferences of Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def folders_spring_open(self) -> bool:
        """Whether folders spring open after a delay."""
        return self.xa_elem.foldersSpringOpen()

    @property
    def delay_before_springing(self) -> bool:
        """The delay, in seconds, before springing open folders."""
        return self.xa_elem.delayBeforeSpringing()

    @property
    def desktop_shows_hard_disks(self) -> bool:
        """Whether hard drives appear on the desktop."""
        return self.xa_elem.desktopShowsHardDisks()

    @property
    def desktop_shows_external_hard_disks(self) -> bool:
        """Whether external hard disks appear on the desktop."""
        return self.xa_elem.desktopShowsExternalHardDisks()

    @property
    def desktop_shows_removable_media(self) -> bool:
        """Whether CDs, DVDs, and iPods appear on the desktop."""
        return self.xa_elem.desktopShowsRemovableMedia()

    @property
    def desktop_shows_connected_servers(self) -> bool:
        """Whether connected servers appear on the desktop."""
        return self.xa_elem.desktopShowsConnectedServers()

    @property
    def folders_open_in_new_windows(self) -> bool:
        """Whether folders open into new windows."""
        return self.xa_elem.foldersOpenInNewWindows()

    @property
    def folders_open_in_new_tabs(self) -> bool:
        """Whether folders open into new tabs."""
        return self.xa_elem.foldersOpenInNewTabs()

    @property
    def new_windows_open_in_column_view(self) -> bool:
        """Whether new Finder windows open in column view."""
        return self.xa_elem.newWindowsOpenInColumnView()

    @property
    def all_name_extensions_showing(self) -> bool:
        """Whether all name extensions are shown regardless of the "extension hidden" setting."""
        return self.xa_elem.allNameExtensionsShowing()

    @property
    def window(self) -> bool:
        """The Finder preferences window."""
        window_obj = self.xa_elem.window()
        return self._new_element(window_obj, XAFinderPreferencesWindow)

    @property
    def icon_view_options(self) -> "XAFinderIconViewOptions":
        """The default icon view options."""
        options_obj = self.xa_elem.iconViewOptions()
        return self._new_element(options_obj, XAFinderIconViewOptions)

    @property
    def list_view_options(self) -> "XAFinderListViewOptions":
        """The default list view options."""
        options_obj = self.xa_elem.listViewOptions()
        return self._new_element(options_obj, XAFinderListViewOptions)

    @property
    def column_view_options(self) -> "XAFinderColumnViewOptions":
        """The default column view options."""
        options_obj = self.xa_elem.columnViewOptions()
        return self._new_element(options_obj, XAFinderColumnViewOptions)

    @property
    def new_window_target(self) -> XAFinderAliasFile:
        """The target location for a newly opened Finder window."""
        target_obj = self.xa_elem.newWindowTarget()
        return self._new_element(target_obj, XAFinderAliasFile)


class XAFinderPreferencesWindow(XAFinderWindow):
    """A class for managing and interacting with preference windows in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def current_panel(self) -> XAFinderApplication.Panel:
        """The current panel in the Finder preferences window."""
        return self.xa_elem.currentPanel()

    @current_panel.setter
    def current_panel(self, current_panel: XAFinderApplication.Panel):
        self.set_property("currentPanel", current_panel.value)


class XAFinderInformationWindowList(XAFinderWindowList):
    """A wrapper around lists of info windows that employs fast enumeration techniques.

    All properties of info windows can be called as methods on the wrapped list, returning a list containing each window's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFinderInformationWindow)

    def item(self) -> XAFinderItemList:
        ls = self.xa_elem.arrayByApplyingSelector_("item") or []
        return self._new_element(ls, XAFinderItemList)

    def current_panel(self) -> list[XAFinderApplication.Panel]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentPanel") or [])

    def by_item(self, item: XAFinderItem) -> Union["XAFinderInformationWindow", None]:
        return self.by_property("item", item)

    def by_current_panel(
        self, current_panel: XAFinderApplication.Panel
    ) -> Union["XAFinderInformationWindow", None]:
        return self.by_property("currentPanel", current_panel)


class XAFinderInformationWindow(XAFinderWindow):
    """A class for interacting with information windows in Finder.app.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def item(self) -> XAFinderItem:
        """The item from which this window was opened."""
        item_obj = self.xa_elem.item()
        return self._new_element(item_obj, XAFinderItem)

    @property
    def current_panel(self) -> XAFinderApplication.Panel:
        """The current panel in the information window."""
        return self.xa_elem.currentPanel()

    @current_panel.setter
    def current_panel(self, current_panel: XAFinderApplication.Panel):
        self.set_property("currentPanel", current_panel.value)


class XAFinderIconViewOptions(XABase.XAObject):
    """A class representing the icon view options of a Finder window.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def arrangement(self) -> XAFinderApplication.Arrangement:
        """The arrangement setting of icons in icon view."""
        return self.xa_elem.arrangement()

    @arrangement.setter
    def arrangement(self, arrangement: XAFinderApplication.Arrangement):
        self.set_property("arrangement", arrangement.value)

    @property
    def icon_size(self) -> int:
        """The size of icons in icon view."""
        return self.xa_elem.iconSize()

    @icon_size.setter
    def icon_size(self, icon_size: int):
        self.set_property("iconSize", icon_size)

    @property
    def shows_item_info(self) -> bool:
        """Whether additional item information is shown in the window."""
        return self.xa_elem.showsItemInfo()

    @shows_item_info.setter
    def shows_item_info(self, shows_item_info: bool):
        self.set_property("showsItemInfo", shows_item_info)

    @property
    def shows_icon_preview(self) -> bool:
        """Whether a preview of the icon is shown in the window."""
        return self.xa_elem.showsIconPreview()

    @shows_icon_preview.setter
    def shows_icon_preview(self, shows_icon_preview: bool):
        self.set_property("showsIconPreview", shows_icon_preview)

    @property
    def text_size(self) -> int:
        """The size of text in icon view."""
        return self.xa_elem.textSize()

    @text_size.setter
    def text_size(self, text_size: int):
        self.set_property("textSize", text_size)

    @property
    def label_position(self) -> XAFinderApplication.LabelPosition:
        """The position of a label around an icon in icon view."""
        return self.xa_elem.labelPosition()

    @label_position.setter
    def label_position(self, label_position: XAFinderApplication.LabelPosition):
        self.set_property("labelPosition", label_position.value)

    @property
    def background_picture(self) -> XAFinderFile:
        """The background picture of the icon view."""
        bg_obj = self.xa_elem.backgroundPicture()
        return self._new_element(bg_obj, XAFinderFile)

    @background_picture.setter
    def background_picture(self, background_picture: XAFinderFile):
        self.set_property("backgroundPicture", background_picture.xa_elem)

    @property
    def background_color(self) -> XABase.XAColor:
        """The background color of the icon view."""
        bg_obj = self.xa_elem.backgroundColor()
        return self._new_element(bg_obj, XABase.XAColor)

    @background_color.setter
    def background_color(self, background_color: XABase.XAColor):
        self.set_property("backgroundColor", background_color.xa_elem)


class XAFinderColumnViewOptions(XABase.XAObject):
    """A class representing the column view options of a Finder window.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def text_size(self) -> int:
        """The size of text in the column view."""
        return self.xa_elem.textSize()

    @text_size.setter
    def text_size(self, text_size: int):
        self.set_property("textSize", text_size)

    @property
    def shows_icon(self) -> bool:
        """Whether icons are shown in the column view."""
        return self.xa_elem.showsIcon()

    @shows_icon.setter
    def shows_icon(self, shows_icon: bool):
        self.set_property("showsIcon", shows_icon)

    @property
    def shows_icon_preview(self) -> bool:
        """Whether icon previews are shown in the column view."""
        return self.xa_elem.showsIconPreview()

    @shows_icon_preview.setter
    def shows_icon_preview(self, shows_icon_preview: bool):
        self.set_property("showsIconPreview", shows_icon_preview)

    @property
    def shows_preview_column(self) -> bool:
        """Whether the preview column is shown in the column view."""
        return self.xa_elem.showsPreviewColumn()

    @shows_preview_column.setter
    def shows_preview_column(self, shows_preview_column: bool):
        self.set_property("showsPreviewColumn", shows_preview_column)

    @property
    def discloses_preview_pane(self) -> bool:
        """Whether the preview pane is disclosed in the column view."""
        return self.xa_elem.disclosesPreviewPane()

    @discloses_preview_pane.setter
    def discloses_preview_pane(self, discloses_preview_pane: bool):
        self.set_property("disclosesPreviewPane", discloses_preview_pane)


class XAFinderListViewOptions(XABase.XAObject):
    """A class representing the list view options in a Finder window.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def calculates_folder_sizes(self) -> bool:
        """Whether folder sizes are calculated and displayed in the window."""
        return self.xa_elem.calculatesFolderSizes()

    @calculates_folder_sizes.setter
    def calculates_folder_sizes(self, calculates_folder_sizes: bool):
        self.set_property("calculatesFolderSizes", calculates_folder_sizes)

    @property
    def shows_icon_preview(self) -> bool:
        """Whether a preview of the item is shown in the window."""
        return self.xa_elem.showsIconPreview()

    @shows_icon_preview.setter
    def shows_icon_preview(self, shows_icon_preview: bool):
        self.set_property("showsIconPreview", shows_icon_preview)

    @property
    def icon_size(self) -> XAFinderApplication.IconSize:
        """The size of icons in the window."""
        return self.xa_elem.iconSize()

    @icon_size.setter
    def icon_size(self, icon_size: XAFinderApplication.IconSize):
        self.set_property("iconSize", icon_size.value)

    @property
    def text_size(self) -> int:
        """The size of text in the window."""
        return self.xa_elem.textSize()

    @text_size.setter
    def text_size(self, text_size: int):
        self.set_property("textSize", text_size)

    @property
    def uses_relative_dates(self) -> bool:
        """Whether relative dates are shown in the window."""
        return self.xa_elem.usesRelativeDates()

    @uses_relative_dates.setter
    def uses_relative_dates(self, uses_relative_dates: bool):
        self.set_property("usesRelativeDates", uses_relative_dates)

    @property
    def sort_column(self) -> "XAFinderColumn":
        """The column that the list view is sorted on."""
        column_obj = self.xa_elem.sortColumn()
        return self._new_element(column_obj, XAFinderColumn)

    @sort_column.setter
    def sort_column(self, sort_column: "XAFinderColumn"):
        self.set_property("sortColumn", sort_column.xa_elem)

    def columns(self, filter: dict = None) -> "XAFinderColumnList":
        """Returns a list of columns matching the filter.

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.columns(), XAFinderColumnList, filter)


class XAFinderColumnList(XABase.XAList):
    """A wrapper around lists of Finder columns that employs fast enumeration techniques.

    All properties of Finder columns can be called as methods on the wrapped list, returning a list containing each columns's value for the property.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFinderColumn, filter)

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def sort_direction(self) -> list[XAFinderApplication.SortDirection]:
        return list(self.xa_elem.arrayByApplyingSelector_("sortDirection") or [])

    def width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("width") or [])

    def minimum_width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("minimum_width") or [])

    def maximum_width(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("maximum_width") or [])

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def by_index(self, index: int) -> Union["XAFinderColumn", None]:
        return self.by_property("index", index)

    def by_name(self, name: str) -> Union["XAFinderColumn", None]:
        return self.by_property("name", name)

    def by_sort_direction(
        self, sort_direction: XAFinderApplication.SortDirection
    ) -> Union["XAFinderColumn", None]:
        return self.by_property("sortDirection", sort_direction.value)

    def by_width(self, width: int) -> Union["XAFinderColumn", None]:
        return self.by_property("width", width)

    def by_minimum_width(self, minimum_width: int) -> Union["XAFinderColumn", None]:
        return self.by_property("minimumWidth", minimum_width)

    def by_maximum_width(self, maximum_width: int) -> Union["XAFinderColumn", None]:
        return self.by_property("maximumWidth", maximum_width)

    def by_visible(self, visible: bool) -> Union["XAFinderColumn", None]:
        return self.by_property("visible", visible)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAFinderColumn(XABase.XAObject):
    """A class for managing and interacting with columns in Finder windows.

    .. versionadded:: 0.0.3
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def index(self) -> int:
        """The index of the column in the front-to-back ordering within the containing window."""
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def name(self) -> XAFinderApplication.ColumnName:
        """The column name."""
        return self.xa_elem.name()

    @property
    def sort_direction(self) -> XAFinderApplication.SortDirection:
        """The direction which the window is sorted."""
        return self.xa_elem.sortDirection()

    @sort_direction.setter
    def sort_direction(self, sort_direction: XAFinderApplication.SortDirection):
        self.set_property("sortDirection", sort_direction.value)

    @property
    def width(self) -> int:
        """The current width of the column in pixels."""
        return self.xa_elem.width()

    @width.setter
    def width(self, width: int):
        self.set_property("width", width)

    @property
    def minimum_width(self) -> int:
        """The minimum width allowed for the column in pixels."""
        return self.xa_elem.minimumWidth()

    @property
    def maximum_width(self) -> int:
        """The maximum width allowed for the column in pixels."""
        return self.xa_elem.maximumWidth()

    @property
    def visible(self) -> bool:
        """Whether the column is visible."""
        return self.xa_elem.visible()

    @visible.setter
    def visible(self, visible: bool):
        self.set_property("visible", visible)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"
