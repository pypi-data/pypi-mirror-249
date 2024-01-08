""".. versionadded:: 0.0.1

Control Safari using JXA-like syntax.
"""

from typing import Any, Union
import threading
from enum import Enum

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XAClipboardCodable, XACloseable


class XASafariApplication(
    XABaseScriptable.XASBApplication,
    XABaseScriptable.XASBPrintable,
    XABase.XAObject,
    XACanOpenPath,
):
    """A class for interacting with Safari.app.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`, :class:`XABaseScriptable.XASBApplication`, :class:`XABaseScriptable.XASBSaveable`, :class:`XABaseScriptable.XASBPrintable`

    .. versionadded:: 0.0.1
    """

    class ObjectType(Enum):
        """Object types that can be created using :func:`make`."""

        DOCUMENT = "document"
        TAB = "tab"

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XASafariWindow

    @property
    def frontmost(self) -> bool:
        """Whether Safari is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of Safari.app."""
        return self.xa_scel.version()

    @property
    def current_document(self) -> "XASafariDocument":
        """The currently displayed document in the active tab."""
        return self._new_element(self.xa_scel.documents()[0], XASafariDocument)

    @property
    def current_tab(self) -> "XASafariTab":
        """The currently active tab."""
        return self.front_window.current_tab

    @current_tab.setter
    def current_tab(self, current_tab: "XASafariTab"):
        self.front_window.current_tab = current_tab

    def open(
        self, url: Union[str, XABase.XAURL, XABase.XAPath] = "https://google.com"
    ) -> "XASafariTab":
        """Opens a URL in new tab.

        :param url: The URL or path to open, defaults to "http://google.com"
        :type url: Union[str, XABase.XAURL, XABase.XAPath], optional
        :return: A reference to the newly created tab object
        :rtype: XASafariTab

        :Example 1: Open local and external URLs

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> app.open("https://www.google.com")
        >>> app.open("google.com")
        >>> app.open("/Users/exampleuser/Documents/WebPage.html")

        .. versionadded:: 0.0.1
        """
        if isinstance(url, str):
            url = XABase.XAURL(url)

        self.activate()
        new_tab = self.make("tab", {"URL": url.url})
        tab = self.front_window.tabs().push(new_tab)
        self.front_window.current_tab = tab
        return tab

    def show_bookmarks(self) -> "XASafariApplication":
        """Activates Safari and opens Safari's bookmarks page.

        :return: A reference to the newly opened Bookmarks tab
        :rtype: XASafariTab

        .. versionadded:: 0.0.1
        """
        self.activate()
        self.xa_scel.showBookmarks()
        return self.front_window.current_tab

    def add_to_reading_list(
        self, item: Union[str, XABase.XAURL, "XASafariTab", "XASafariDocument"]
    ) -> "XASafariApplication":
        """Adds a URL to the reading list.

        :param item: A URL string or a Safari tab or document containing the URL to add to the reading list.
        :type item: Union[str, XASafariTab, XASafariDocument]
        :return: A reference to the Safari application object.
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> window = app.front_window
        >>> doc = app.current_document
        >>> tab = window.current_tab
        >>> app.add_to_reading_list(doc)
        >>> app.add_to_reading_list(tab)

        .. versionadded:: 0.0.1
        """
        if isinstance(item, str) or isinstance(item, XABase.XAURL):
            item = XABase.XAURL(item).xa_elem
        elif isinstance(item, XASafariTab) or isinstance(item, XASafariDocument):
            item = item.xa_elem.URL()

        self.xa_scel.addReadingListItem_andPreviewText_withTitle_(item, None, None)
        return self

    def search(self, term: str) -> "XASafariApplication":
        """Activates Safari and searches the specified string in a new tab of the frontmost Safari window. Uses the default search engine.

        :param term: The string to search
        :type term: str
        :return: A reference to the newly opened Search tab
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> app.search("What is PyXA?")

        .. seealso:: :func:`search_in_tab`

        .. versionadded:: 0.0.1
        """
        self.activate()
        self.xa_scel.searchTheWebIn_for_(self.xa_scel.windows()[0], term)
        return self.front_window.current_tab

    def search_in_tab(self, tab: "XASafariTab", term: str) -> "XASafariApplication":
        """Searches the given search string in the specified tab. Uses the default search engine.

        :param tab: The tab to conduct the web search in.
        :type tab: XASafariTab
        :param term: The string to search.
        :type term: str
        :return: A reference to the tab object
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> tab = app.front_window.current_tab
        >>> app.search_in_tab(tab, "What is PyXA?")

        .. seealso:: :func:`search`

        .. versionadded:: 0.0.1
        """
        self.xa_scel.searchTheWebIn_for_(tab.xa_elem, term)
        return tab

    def do_javascript(self, script: str, tab: "XASafariTab" = None) -> Any:
        """Runs JavaScript in the specified tab. If no tab is specified, the script is run in the current tab of the frontmost Safari window.

        :param script: The script to run.
        :type script: str
        :param tab: The tab to execute the JavaScript script in, defaults to None
        :type tab: XASafariTab
        :return: The value returned from the script after it completes execution.
        :rtype: Any

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> tab = app.front_window.current_tab
        >>> script = "(function example() { return 1 + 1 })()"
        >>> print(app.do_javascript(script, tab))
        2.0

        .. versionadded:: 0.0.1
        """
        if tab is None:
            tab = self.front_window.current_tab
        return self.xa_scel.doJavaScript_in_(script, tab.xa_elem)

    def email(self, item: Union["XASafariDocument", "XASafariTab"]):
        """Opens a new email draft with the content of a tab or document.

        :param item: The object to email
        :type item: Union[XASafariDocument, XASafariTab]

        .. versionadded:: 0.0.4
        """
        self.xa_scel.emailContentsOf_(item.xa_elem)

    def save(self):
        self.xa_elem.saveIn_as_(None, None)

    def documents(self, filter: dict = None) -> "XASafariDocumentList":
        """Returns a list of documents matching the given filter.

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XASafariDocumentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.documents(), XASafariDocumentList, filter)

    def new_tab(self, url: Union[str, XABase.XAURL, XABase.XAPath]) -> "XASafariTab":
        """Activates Safari to a new tab at the specified URL or path.

        :param url: The URL or path to open in a new tab
        :type url: Union[str, XABase.XAURL, XABase.XAPath]
        :return: A reference to the newly opened tab
        :rtype: XASafariTab

        .. versionadded:: 0.1.0
        """
        url = XABase.XAURL(url).url
        new_tab = self.make("tab", {"URL": url})
        tab = self.front_window.tabs().push(new_tab)
        self.front_window.current_tab = tab
        self.activate()
        return tab

    def make(
        self,
        specifier: Union[str, "XASafariApplication.ObjectType"],
        properties: dict,
        data: Any = None,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XASafariApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object, defaults to None
        :type data: Any, optional
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        :Example 1: Make a new tab in Safari's front window

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> new_tab = app.make("tab", {"URL": "http://google.com"})
        >>> app.front_window.tabs().push(new_tab)

        :Example 2: Open a page in a new window by making a new document

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> new_doc = app.make("document", {"URL": "http://google.com"})
        >>> app.documents().push(new_doc)

        .. versionadded:: 0.0.4
        """
        if isinstance(specifier, XASafariApplication.ObjectType):
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
            return self._new_element(obj, XASafariDocument)
        elif specifier == "tab":
            return self._new_element(obj, XASafariTab)


class XASafariWindow(
    XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable, XABase.XAObject
):
    """A window of Safari.app.

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def document(self) -> "XASafariDocument":
        """The document currently displayed in the window."""
        return self._new_element(self.xa_elem.document(), XASafariDocument)

    @property
    def current_tab(self) -> "XASafariTab":
        """The currently selected tab."""
        return self._new_element(self.xa_elem.currentTab(), XASafariTab)

    @current_tab.setter
    def current_tab(self, current_tab: "XASafariTab"):
        self.set_property("currentTab", current_tab.xa_elem)

    def tabs(self, filter: dict = None) -> "XASafariTabList":
        """Returns a list of tabs matching the given filter.

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XASafariTabList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_elem.tabs(), XASafariTabList, filter)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XASafariGeneric(XACloseable, XABase.XAObject):
    """A generic class containing methods relevant to Safari tabs and documents.

    .. seealso:: :class:`XASafariDocument`, :class:`XASafariTab`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    def search(self, term: str) -> "XASafariGeneric":
        """Searches for the specified term in the current tab or document.

        :param term: The term to search
        :type term: str
        :return: A reference to the object that called this method
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.xa_elem.searchTheWebIn_for_(self.xa_elem, term)
        return self

    def add_to_reading_list(self) -> "XASafariGeneric":
        """Adds the URL of a tab or document to the reading list.

        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.1
        """
        self.xa_elem.addReadingListItem_andPreviewText_withTitle_(
            self.xa_elem.URL(), None, None
        )
        return self

    def do_javascript(self, script: str) -> Any:
        """Runs JavaScript in a tab or document.

        :return: The value returned from the script after it completes execution
        :rtype: Any

        .. versionadded:: 0.0.1
        """
        return self.xa_elem.doJavaScript_in_(script, self.xa_elem)

    def email(self) -> "XASafariGeneric":
        """Opens a new email draft with the content of a tab or document.

        :param item: The object to email
        :type item: Union[XASafariDocument, XASafariTab]
        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.4
        """
        self.xa_elem.emailContentsOf_(self.xa_elem)
        return self

    def reload(self) -> "XASafariGeneric":
        """Reloads the tab or document.

        :return: A reference to the object that called this method.
        :rtype: XASafariGeneric

        .. versionadded:: 0.0.4
        """
        self.set_property("URL", self.url)
        return self


class XASafariDocumentList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Safari documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASafariDocument, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def file(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("file") or [])

    def source(self) -> list[str]:
        return [x.source() for x in self.xa_elem]

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def text(self) -> list[XABase.XAText]:
        ls = [x.text() for x in self.xa_elem]
        return [XABase.XAText(x) for x in ls]

    def by_name(self, name: str) -> Union["XASafariDocument", None]:
        return self.by_property("name", name)

    def by_modified(self, modified: bool) -> Union["XASafariDocument", None]:
        return self.by_property("modified", modified)

    def by_file(self, file: str) -> Union["XASafariDocument", None]:
        return self.by_property("file", file)

    def by_source(self, source: str) -> Union["XASafariDocument", None]:
        for doc in self.xa_elem:
            if doc.source() == source:
                return self._new_element(doc, XASafariDocument)

    def by_url(self, url: XABase.XAURL) -> Union["XASafariDocument", None]:
        return self.by_property("URL", str(url.xa_elem))

    def by_text(
        self, text: Union[str, XABase.XAText]
    ) -> Union["XASafariDocument", None]:
        for doc in self.xa_elem:
            if doc.text() == str(text):
                return self._new_element(doc, XASafariDocument)

    def reload(self) -> "XASafariDocumentList":
        """Reloads all documents in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList

        .. versionadded:: 0.0.4
        """
        for document in self.xa_elem:
            document.setValue_forKey_(document.URL(), "URL")
        return self

    def add_to_reading_list(self) -> "XASafariDocumentList":
        """Adds the URL of all documents in the list to the reading list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList

        .. versionadded:: 0.0.5
        """
        for document in self:
            document.add_to_reading_list()
        return self

    def email(self) -> "XASafariDocumentList":
        """Opens a new email draft with embedded links to the URL of each document in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList

        .. versionadded:: 0.0.5
        """
        for document in self:
            document.email()
        return self

    def do_javascript(self, script: str) -> "XASafariDocumentList":
        """Runs a given JavaScript script in each document in the list.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList

        .. versionadded:: 0.0.5
        """
        for document in self:
            document.do_javascript(script)
        return self

    def search(self, term: str) -> "XASafariDocumentList":
        """Searches for the given term in each document in the list, using the default search engine.

        :return: A reference to the document list object.
        :rtype: XASafariDocumentList

        .. versionadded:: 0.0.5
        """
        for document in self:
            document.search(term)
        return self

    def close(self):
        """Closes each tab in the list.

        .. versionadded:: 0.0.5
        """
        length = len(self)
        for _index in range(length):
            self[0].close()

    def get_clipboard_representation(self) -> list[AppKit.NSURL]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a list of Safari documents, each document's URL is added to the clipboard.

        :return: A list of document URLs
        :rtype: list[AppKit.NSURL]

        .. versionadded:: 0.0.8
        """
        urls = self.url()
        return [x.xa_elem for x in urls]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASafariDocument(
    XASafariGeneric, XAClipboardCodable, XABaseScriptable.XASBPrintable
):
    """A class for interacting with Safari documents.

    .. seealso:: :class:`XASafariGeneric`, :class:`XABaseScriptable.XASBPrintable`, :class:`XABaseScriptable.XASBSaveable`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The title of the document."""
        return self.xa_elem.name()

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save."""
        return self.xa_elem.modified()

    @property
    def file(self) -> str:
        """The location of the document on the disk, if there is one."""
        file = self.xa_elem.file()
        if file is not None:
            return XABase.XAPath(file)

    @property
    def source(self) -> str:
        """The HTML source of the web page currently loaded in the document."""
        return self.xa_elem.source()

    @property
    def url(self) -> XABase.XAURL:
        """The current URL of the document."""
        return XABase.XAURL(self.xa_elem.URL())

    @url.setter
    def url(self, url: Union[str, XABase.XAURL]):
        if isinstance(url, str):
            url = XABase.XAURL(url)
        self.set_property("URL", url.xa_elem)

    @property
    def text(self) -> XABase.XAText:
        """The text of the web page currently loaded in the document."""
        return self._new_element(self.xa_elem.text(), XABase.XAText)

    def print(self, properties: dict = None, show_dialog: bool = True):
        """Prints or opens the print dialog for the document.

        :param properties: The print properties to pre-set for the print, defaults to None
        :type properties: dict, optional
        :param show_dialog: Whether to display the print dialog, defaults to True
        :type show_dialog: bool, optional

        .. versionadded:: 0.0.5
        """
        if properties is None:
            properties = {}

        print_thread = threading.Thread(
            target=self.xa_elem.printWithProperties_printDialog_,
            args=(properties, show_dialog),
            name="Print Document",
        )
        print_thread.start()

    def get_clipboard_representation(self) -> AppKit.NSURL:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a Safari document, the document's URL is added to the clipboard.

        :return: The document's URL
        :rtype: AppKit.NSURL

        .. versionadded:: 0.0.8
        """
        return self.url.xa_elem

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XASafariTabList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of tabs that employs fast enumeration techniques.

    All properties of tabs can be called as methods on the wrapped list, returning a list containing each tab's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XASafariTab, filter)

    def source(self) -> list[str]:
        """Gets the source HTML of each tab in the list.

        This will activate Safari, individually focus each tab, refocus the original tab, then return a list of all tabs' source HTML.

        :return: A list of source HTML
        :rtype: list[str]

        .. versionadded:: 0.0.4
        """
        current_tab = self.xa_prnt.current_tab.index - 1
        sources = [""] * len(self.xa_elem)
        self.xa_aref.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        for index, tab in enumerate(self):
            self.xa_prnt.current_tab = tab
            sources[index] = tab.source
        self.xa_prnt.current_tab = self.xa_prnt.tabs()[current_tab]
        return sources

    def url(self) -> list[XABase.XAURL]:
        ls = self.xa_elem.arrayByApplyingSelector_("URL") or []
        return [XABase.XAURL(x) for x in ls]

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def text(self) -> list[XABase.XAText]:
        """Gets the visible text of each tab in the list.

        This will activate Safari, individually focus each tab, refocus the original tab, then return a list of all tabs' visible text.

        :return: A list of visible text
        :rtype: list[XABase.XAText]

        .. versionadded:: 0.0.4
        """
        current_tab = self.xa_prnt.current_tab.index - 1
        texts = [""] * len(self.xa_elem)
        self.xa_aref.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        for index, tab in enumerate(self):
            self.xa_prnt.current_tab = tab
            texts[index] = tab.text
        self.xa_prnt.current_tab = self.xa_prnt.tabs()[current_tab]
        return texts

    def visible(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("visible") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_source(self, source: str) -> Union["XASafariTab", None]:
        for tab in self.xa_elem:
            if tab.source() == source:
                return self._new_element(tab, XASafariTab)

    def by_url(self, url: XABase.XAURL) -> Union["XASafariTab", None]:
        return self.by_property("URL", str(url.xa_elem))

    def by_index(self, index: int) -> Union["XASafariTab", None]:
        return self.by_property("index", index)

    def by_text(self, text: Union[str, XABase.XAText]) -> Union["XASafariTab", None]:
        for tab in self.xa_elem:
            if tab.text() == str(text):
                return self._new_element(tab, XASafariTab)

    def by_visible(self, visible: bool) -> Union["XASafariTab", None]:
        return self.by_property("visible", visible)

    def by_name(self, name: str) -> Union["XASafariTab", None]:
        return self.by_property("name", name)

    def reload(self) -> "XASafariTabList":
        """Reloads all tabs in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList

        .. versionadded:: 0.0.4
        """
        for tab in self.xa_elem:
            tab.setValue_forKey_(tab.URL(), "URL")
        return self

    def add_to_reading_list(self) -> "XASafariTabList":
        """Adds the URL of all tabs in the list to the reading list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList

        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.add_to_reading_list()
        return self

    def email(self) -> "XASafariTabList":
        """Opens a new email draft with embedded links to the URL of each tab in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList

        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.email()
        return self

    def do_javascript(self, script: str) -> "XASafariTabList":
        """Runs a given JavaScript script in each tab in the list.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList

        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.do_javascript(script)
        return self

    def search(self, term: str) -> "XASafariTabList":
        """Searches for the given term in each tab in the list, using the default search engine.

        :return: A reference to the tab list object.
        :rtype: XASafariTabList

        .. versionadded:: 0.0.5
        """
        for tab in self:
            tab.search(term)
        return self

    def move_to(self, window: XASafariWindow) -> "XASafariTabList":
        """Moves all tabs in the list to the specified window.

        :param window: The window to move tabs to
        :type window: XASafariWindow
        :return: The tab list object
        :rtype: XASafariTabList

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.5
        """
        for tab in self.xa_elem:
            tab.moveTo_(window.xa_elem)
            tab.close()
        return self

    def duplicate_to(self, window: XASafariWindow) -> "XASafariTabList":
        """Duplicate all tabs in the list in the specified window.

        :param window: The window to duplicate tabs in
        :type window: XASafariWindow
        :return: The tab list object
        :rtype: XASafariTabList

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.5
        """
        for tab in self.xa_elem:
            tab.moveTo_(window.xa_elem)
        return self

    def close(self):
        """Closes each tab in the list.

        .. versionadded:: 0.0.5
        """
        length = len(self)
        for _index in range(length):
            self[0].close()

    def get_clipboard_representation(self) -> list[AppKit.NSURL]:
        """Gets a clipboard-codable representation of each tab in the list.

        When the clipboard content is set to a list of Safari tabs, each tabs's URL is added to the clipboard. Pasting the copied list into an app such as Numbers will place each URL in a separate cell of a column.

        :return: A list of tab URLs
        :rtype: list[AppKit.NSURL]

        .. versionadded:: 0.0.8
        """
        urls = self.url()
        return [x.xa_elem for x in urls]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XASafariTab(XASafariGeneric, XAClipboardCodable):
    """A class for interacting with Safari tabs.

    .. seealso:: :class:`XASafariGeneric`

    .. versionadded:: 0.0.1
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def source(self) -> str:
        """The HTML source of the web page currently loaded in the tab."""
        return self.xa_elem.source()

    @property
    def url(self) -> XABase.XAURL:
        """The current URL of the tab."""
        return XABase.XAURL(self.xa_elem.URL())

    @url.setter
    def url(self, url: Union[str, XABase.XAURL]):
        if isinstance(url, str):
            url = XABase.XAURL(url)
        self.set_property("URL", url.xa_elem)

    @property
    def index(self) -> int:
        """The index of the tab, ordered left to right."""
        return self.xa_elem.index()

    @property
    def text(self) -> XABase.XAText:
        """The text of the web page currently loaded in the tab."""
        return self._new_element(self.xa_elem.text(), XABase.XAText)

    @property
    def visible(self) -> bool:
        """Whether the tab is currently visible."""
        return self.xa_elem.visible()

    @property
    def name(self) -> str:
        """The title of the tab."""
        return self.xa_elem.name()

    def move_to(self, window: "XASafariWindow") -> "XASafariTab":
        """Moves the tab to the specified window. After, the tab will exist in only one location.

        :param window: The window to move the tab to.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> tab = app.front_window.current_tab
        >>> window2 = app.window(1)
        >>> tab.move_to(window2)

        .. seealso:: :func:`duplicate_to`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.moveTo_(window.xa_elem)
        self.close()
        return self

    def duplicate_to(self, window: "XASafariWindow") -> "XASafariTab":
        """Duplicates the tab in the specified window. The tab will then exist in two locations.

        :param window: The window to duplicate the tab in.
        :type window: XASafariWindow
        :return: A reference to the tab object.
        :rtype: XASafariTab

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Safari")
        >>> tab = app.front_window.current_tab
        >>> window2 = app.window(1)
        >>> tab.duplicate_to(window2)

        .. seealso:: :func:`move_to`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.moveTo_(window.xa_elem)
        return self

    def get_clipboard_representation(self) -> AppKit.NSURL:
        """Gets a clipboard-codable representation of the tab.

        When the clipboard content is set to a Safari tab, the tab's URL is added to the clipboard.

        :return: The tabs's URL
        :rtype: AppKit.NSURL

        .. versionadded:: 0.0.8
        """
        return self.url.xa_elem

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"
