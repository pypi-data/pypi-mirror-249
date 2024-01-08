""".. versionadded:: 0.0.3

Control Chromium using JXA-like syntax.
"""

from typing import Any, Union
from enum import Enum

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable

class XAChromiumApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Chromium.app.

    .. seealso:: :class:`XAChromiumWindow`, :class:`XAChromiumBookmarkFolder`, :class:`XAChromiumBookmarkItem`, :class:`XAChromiumTab`

    .. versionadded:: 0.0.3
    """
    class ObjectType(Enum):
        """The object types that can be created using :func:`make`.
        """
        TAB = "tab"
        WINDOW = "window"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAChromiumWindow

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Chromium is the active application.
        """
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version of Chromium.app.
        """
        return self.xa_scel.version()

    @property
    def bookmarks_bar(self) -> 'XAChromiumBookmarkFolder':
        """The bookmarks bar bookmark folder.
        """
        return self._new_element(self.xa_scel.bookmarksBar(), XAChromiumBookmarkFolder)

    @property
    def other_bookmarks(self) -> 'XAChromiumBookmarkFolder':
        """The other bookmarks bookmark folder.
        """
        return self._new_element(self.xa_scel.otherBookmarks(), XAChromiumBookmarkFolder)

    def open(self, url: Union[str, XABase.XAURL] = "https://google.com") -> 'XAChromiumApplication':
        """Opens a URL in a new tab.

        :param url: _description_, defaults to "http://google.com"
        :type url: str, optional
        :return: A reference to the Chromium application object.
        :rtype: XAChromiumApplication

        :Example 1: Open a local or external URL

           >>> import PyXA
           >>> app = PyXA.Application("Chromium")
           >>> app.open("https://www.google.com")
           >>> app.open("google.com")
           >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.3
        """
        if isinstance(url, str):
            if url.startswith("/"):
                # URL is a path to file
                self.xa_wksp.openFile_application_(url, self.xa_scel)
                return self
            # Otherwise, URL is web address
            elif not url.startswith("http"):
                url = "http://" + url
            url = XABase.XAURL(url)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAChromiumBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_scel.bookmarkFolders(), XAChromiumBookmarkFolderList, filter)

    def new_window(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumWindow':
        """Opens a new window at the specified URL.


        :param url: The URL to open in a new window, or None to open the window at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created window object
        :rtype: XAChromiumWindow

        .. seealso:: :func:`new_tab`, :func:`make`

        .. versionadded:: 0.0.5
        """
        new_window = self.make("window")
        self.windows().push(new_window)

        if isinstance(url, str):
            if url.startswith("/"):
                # URL is a path to file
                self.xa_wksp.openFile_application_(url, self.xa_scel)
                return self
            # Otherwise, URL is web address
            elif not url.startswith("http"):
                url = "http://" + url
            url = XABase.XAURL(url)
        new_window.active_tab.set_property("URL", url.xa_elem)
        return new_window

    def new_tab(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumTab':
        """Opens a new tab at the specified URL.

        :param url: The URL to open in a new tab, or None to open the tab at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created tab object
        :rtype: XAChromiumTab

        .. seealso:: :func:`new_window`, :func:`make`

        .. versionadded:: 0.0.5
        """
        new_tab = None
        if url is None:
            new_tab = self.make("tab")
        else:
            new_tab = self.make("tab", {"URL": url})
        self.front_window.tabs().push(new_tab)
        return new_tab

    def make(self, specifier: Union[str, 'XAChromiumApplication.ObjectType'], properties: dict = None, data: Any = None):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAChromiumApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. seealso:: :func:`new_window`, :func:`new_tab`

        .. versionadded:: 0.0.4
        """
        if isinstance(specifier, XAChromiumApplication.ObjectType):
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

        if specifier == "tab":
            return self._new_element(obj, XAChromiumTab)
        elif specifier == "window":
            return self._new_element(obj, XAChromiumWindow)




class XAChromiumWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Chromium windows.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumTab`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def given_name(self) -> str:
        """The given name of the window.
        """
        return self.xa_elem.givenName()

    @given_name.setter
    def given_name(self, given_name: str):
        self.set_property("givenName", given_name)

    @property
    def minimizable(self) -> bool:
        """Whether the window can be minimized.
        """
        return self.xa_elem.minimizable()

    @property
    def minimized(self) -> bool:
        """Whether the window is currently minimized.
        """
        return self.xa_elem.minimized()

    @minimized.setter
    def minimized(self, minimized: bool):
        self.set_property("minimized", minimized)

    @property
    def mode(self) -> str:
        """The mode of the window, either 'normal' or 'incognito'.
        """
        return self.xa_elem.mode()

    @mode.setter
    def mode(self, mode: str):
        self.set_property("mode", mode)

    @property
    def active_tab_index(self) -> int:
        """The index of the active tab.
        """
        return self.xa_elem.activeTabIndex() 

    @active_tab_index.setter
    def active_tab_index(self, active_tab_index: int):
        self.set_property("activeTabIndex", active_tab_index)

    @property
    def active_tab(self) -> 'XAChromiumTab':
        """The currently selected tab.
        """
        return self._new_element(self.xa_elem.activeTab(), XAChromiumTab)

    @active_tab.setter
    def active_tab(self, active_tab: 'XAChromiumTab'):
        self.set_property("activeTab", active_tab.xa_elem)

    def new_tab(self, url: Union[str, XABase.XAURL, None] = None) -> 'XAChromiumTab':
        """Opens a new tab at the specified URL.

        :param url: The URL to open in a new tab, or None to open the tab at the homepage, defaults to None
        :type url: Union[str, XABase.XAURL, None], optional
        :return: The newly created tab object
        :rtype: XAChromiumTab

        .. versionadded:: 0.0.5
        """
        new_tab = None
        if url is None:
            new_tab = self.xa_prnt.xa_prnt.make("tab")
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", {"URL": url})
        self.tabs().push(new_tab)
        return new_tab

    def tabs(self, filter: Union[dict, None] = None) -> 'XAChromiumTabList':
        """Returns a list of tabs, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter tabs by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of tabs
        :rtype: XAChromiumTabList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.tabs(), XAChromiumTabList, filter)




class XAChromiumTabList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of tabs.

    .. seealso:: :class:`XAChromiumTab`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumTab, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def loading(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("loading") or [])

    def by_id(self, id: int) -> Union['XAChromiumTab', None]:
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumTab', None]:
        return self.by_property("title", title)

    def by_url(self, url: XABase.XAURL) -> Union['XAChromiumTab', None]:
        return self.by_property("url", str(url.xa_elem))

    def by_loading(self, loading: bool) -> Union['XAChromiumTab', None]:
        return self.by_property("loading", loading)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each tab in the list.

        When the clipboard content is set to a list of Chromium tabs, each tab's URL is added to the clipboard.

        :return: A list of tab URLs
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        titles = self.title()
        urls = self.url()
        for index, title in enumerate(titles):
            items.append(title)
            items.append(urls[index].xa_elem)
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAChromiumTab(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with Chromium tabs.

    .. seealso:: :class:`XAChromiumWindow`, :class:`XAChromiumTabList`, :class:`XAChromiumWindow`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique identifier for the tab.
        """
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        """The title of the tab.
        """
        return self.xa_elem.title()

    @property
    def url(self) -> XABase.XAURL:
        """The URL visible to the user.
        """
        return XABase.XAURL(self.xa_elem.URL())

    @url.setter
    def url(self, url: XABase.XAURL):
        self.set_property("URL", url.url)

    @property
    def loading(self) -> bool:
        """Is the tab currently loading?
        """
        return self.xa_elem.loading()

    def undo(self) -> 'XAChromiumTab':
        """Undoes the last action done on the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.undo()
        return self

    def redo(self) -> 'XAChromiumTab':
        """Redoes the last action done on the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.redo()
        return self

    def cut_selection(self) -> 'XAChromiumTab':
        """Attempts to cut the selected content and copy it to the clipboard. If the content cannot be deleted, then it is only copied to the clipboard.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.cutSelection()
        return self

    def copy_selection(self) -> 'XAChromiumTab':
        """Copies the selected element to the clipboard.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.copySelection()
        return self

    def paste_selection(self) -> 'XAChromiumTab':
        """Attempts to paste the clipboard into the selected element.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.pasteSelection()
        return self

    def select_all(self) -> 'XAChromiumTab':
        """Selects all text content within the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.selectAll()
        return self

    def go_back(self) -> 'XAChromiumTab':
        """Goes to the previous URL in the tab's history.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.goBack()
        return self

    def go_forward(self) -> 'XAChromiumTab':
        """Goes to the next URL in the tab's history, or does nothing if the current document is the most recent URL.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.goForward()
        return self

    def reload(self) -> 'XAChromiumTab':
        """Reloads the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.reload()
        return self

    def stop(self) -> 'XAChromiumTab':
        """Forces the tab to stop loading.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.stop()
        return self

    def print(self) -> 'XAChromiumTab':
        """Opens the print dialog for the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.print()
        return self

    def view_source(self) -> 'XAChromiumTab':
        """Opens the source HTML of the tab's document in a separate tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.viewSource()
        return self

    def save(self, file_path: Union[str, AppKit.NSURL], save_assets: bool = True) -> 'XAChromiumTab':
        if isinstance(file_path, str):
            file_path = AppKit.NSURL.alloc().initFileURLWithPath_(file_path)
        if save_assets:
            self.xa_elem.saveIn_as_(file_path, "complete html")
        else:
            self.xa_elem.saveIn_as_(file_path, "only html")
        return self

    def close(self) -> 'XAChromiumTab':
        """Closes the tab.
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.close()
        return self

    def execute(self, script: str) -> Any:
        """Executes JavaScript in the tab.
        
        .. versionadded:: 0.0.4
        """
        return self.xa_elem.executeJavascript_(script)

    def move_to(self, window: 'XAChromiumWindow') -> 'XAChromiumWindow':
        """Moves the tab to the specified window. After, the tab will exist in only one location.

        :param window: The window to move the tab to.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariGeneric

        :Example 1: Move the current tab to the second window

        >>> import PyXA
        >>> app = PyXA.Application("Chromium")
        >>> tab = app.front_window.active_tab
        >>> window2 = app.windows()[1]
        >>> tab.move_to(window2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.1
        """
        current = self.xa_elem.get()
        properties = {"URL": self.url}
        if isinstance(self.xa_prnt, XABase.XAList):
            new_tab = self.xa_prnt.xa_prnt.xa_prnt.make("tab", properties)
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", properties)
        window.tabs().push(new_tab)
        current.close()
        return self

    def duplicate_to(self, window: 'XAChromiumWindow') -> 'XAChromiumWindow':
        """Duplicates the tab in the specified window. The tab will then exist in two locations.

        :param window: The window to duplicate the tab in.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariTab

        :Example 1: Duplicate the current tab in the second window

        >>> import PyXA
        >>> app = PyXA.Application("Chromium")
        >>> tab = app.front_window.active_tab
        >>> window2 = app.windows()[1]
        >>> tab.duplicate_to(window2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.1
        """
        properties = {"URL": self.url}

        new_tab = None
        print(self.xa_prnt)
        if isinstance(self.xa_prnt, XABase.XAList):
            new_tab = self.xa_prnt.xa_prnt.xa_prnt.make("tab", properties)
        else:
            new_tab = self.xa_prnt.xa_prnt.make("tab", properties)
        window.tabs().push(new_tab)
        return self

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of the tab.

        When the clipboard content is set to a Chromium tab, the tab's title and URL are added to the clipboard.

        :return: The tab's title and URL
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [self.title, self.url.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"




class XAChromiumBookmarkFolderList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of bookmark folders.

    .. seealso:: :class:`XAChromiumBookmarkFolder`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkFolder, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def by_id(self, id: int) -> Union['XAChromiumBookmarkFolder', None]:
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumBookmarkFolder', None]:
        return self.by_property("title", title)

    def by_index(self, index: int) -> Union['XAChromiumBookmarkFolder', None]:
        return self.by_property("index", index)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each bookmark folder in the list.

        When the clipboard content is set to a list of bookmark folders, each folder's title is added to the clipboard.

        :return: The list of each bookmark folder's title
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.title()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAChromiumBookmarkFolder(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with bookmark folders in Chromium.app.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumBookmarkFolderList`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique identifier for the bookmark folder.
        """
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        """The name of the bookmark folder.
        """
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property("title", title)

    @property
    def index(self) -> int:
        """The index of the bookmark folder with respect to its parent folder.
        """
        return self.xa_elem.index()

    def bookmark_folders(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkFolderList':
        """Returns a list of bookmark folders, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter folders by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark folders
        :rtype: XAChromiumBookmarkFolderList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkFolders(), XAChromiumBookmarkFolderList, filter)

    def bookmark_items(self, filter: Union[dict, None] = None) -> 'XAChromiumBookmarkItemList':
        """Returns a list of bookmark items, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter items by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of bookmark items
        :rtype: XAChromiumBookmarkItemList

        .. versionadded:: 0.0.3
        """
        return self._new_element(self.xa_elem.bookmarkItems(), XAChromiumBookmarkItemList, filter)

    def delete(self):
        """Permanently deletes the bookmark folder.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the bookmark folder.

        When the clipboard content is set to a bookmark folder, the folders's title is added to the clipboard.

        :return: The bookmark folders's title
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.title

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"




class XAChromiumBookmarkItemList(XABase.XAList, XAClipboardCodable):
    """A wrapper around a list of bookmark items.

    .. seealso:: :class:`XAChromiumBookmarkItem`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAChromiumBookmarkItem, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def by_id(self, id: int) -> Union['XAChromiumBookmarkItem', None]:
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union['XAChromiumBookmarkItem', None]:
        return self.by_property("title", title)

    def by_url(self, url: XABase.XAURL) -> Union['XAChromiumBookmarkItem', None]:
        return self.by_property("URL", str(url.xa_elem))

    def by_index(self, index: int) -> Union['XAChromiumBookmarkItem', None]:
        return self.by_property("index", index)

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of each bookmark item in the list.

        When the clipboard content is set to a list of bookmark items, each item's title and URL are added to the clipboard.

        :return: The list of each bookmark items's title and URL
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        items = []
        titles = self.title()
        urls = self.url()
        for index, title in enumerate(titles):
            items.append(title)
            items.append(urls[index].xa_elem)
        return items

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title()) + ">"

class XAChromiumBookmarkItem(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with bookmarks in Chromium.app.

    .. seealso:: :class:`XAChromiumApplication`, :class:`XAChromiumBookmarkItemList`

    .. versionadded:: 0.0.3
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> int:
        """The unique identifier for the bookmark item.
        """
        return self.xa_elem.id()

    @property
    def title(self) -> str:
        """The title of the bookmark item.
        """
        return self.xa_elem.title()

    @title.setter
    def title(self, title: str):
        self.set_property("title", title)

    @property
    def url(self) -> XABase.XAURL:
        """The URL of the bookmark.
        """
        return XABase.XAURL(self.xa_elem.URL())

    @url.setter
    def url(self, url: XABase.XAURL):
        self.set_property("URL", url.url)

    @property
    def index(self) -> int:
        """The index of the item with respect to its parent folder.
        """
        return self.xa_elem.index()

    def delete(self):
        """Permanently deletes the bookmark.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def get_clipboard_representation(self) -> list[Union[str, AppKit.NSURL]]:
        """Gets a clipboard-codable representation of the bookmark item.

        When the clipboard content is set to a bookmark item, the item's title and URL are added to the clipboard.

        :return: The bookmark items's title and URL
        :rtype: list[Union[str, AppKit.NSURL]]

        .. versionadded:: 0.0.8
        """
        return [self.title, self.url.xa_elem]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.title) + ">"