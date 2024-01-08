""".. versionadded:: 0.0.6

Control the macOS FontBook application using JXA-like syntax.
"""

from typing import Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XAClipboardCodable


class XAFontBookApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Font Book.app.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAFontBookWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of the Font Book application."""
        return self.xa_scel.version()

    @property
    def validate_fonts_before_installing(self) -> bool:
        """Whether to validate fonts before installing them."""
        return self.xa_scel.validateFontsBeforeInstalling()

    @validate_fonts_before_installing.setter
    def validate_fonts_before_installing(self, validate_fonts_before_installing: bool):
        self.set_property(
            "validateFontsBeforeInstalling", validate_fonts_before_installing
        )

    @property
    def installation_target(self) -> "XAFontBookFontLibrary":
        """The library where new fonts are installed."""
        return self._new_element(
            self.xa_scel.installationTarget(), XAFontBookFontLibrary
        )

    @installation_target.setter
    def installation_target(self, installation_target: "XAFontBookFontLibrary"):
        self.set_property("installationTarget", installation_target.xa_elem)

    @property
    def fonts_library(self) -> "XAFontBookFontBookAllFontsLibraryObject":
        """The All Fonts library."""
        return self._new_element(
            self.xa_scel.fontsLibrary(), XAFontBookFontBookAllFontsLibraryObject
        )

    @property
    def selection(self) -> "XAFontBookTypefaceList":
        """The currently selected typefaces."""
        ls = self.xa_scel.selection()
        return self._new_element(ls, XAFontBookTypefaceList)

    @selection.setter
    def selection(
        self, selection: Union["XAFontBookTypefaceList", list["XAFontBookTypeface"]]
    ):
        if isinstance(selection, list):
            selection = [x.xa_elem for x in selection]
            self.set_property("selection", selection)
        else:
            self.set_property("selection", selection.xa_elem)

    @property
    def selected_font_families(self) -> "XAFontBookFontFamilyList":
        """The currently selected font families."""
        ls = self.xa_scel.selectedFontFamilies()
        return self._new_element(ls, XAFontBookFontFamilyList)

    @selected_font_families.setter
    def selected_font_families(
        self,
        selected_font_families: Union[
            "XAFontBookFontFamilyList", list["XAFontBookFontFamily"]
        ],
    ):
        if isinstance(selected_font_families, list):
            selected_font_families = [x.xa_elem for x in selected_font_families]
            self.set_property("selectedFontFamilies", selected_font_families)
        else:
            self.set_property("selectedFontFamilies", selected_font_families.xa_elem)

    @property
    def selected_collections(self) -> "XAFontBookFontCollectionList":
        """The currently selected collections."""
        ls = self.xa_scel.selectedCollections()
        return self._new_element(ls, XAFontBookFontCollectionList)

    @selected_collections.setter
    def selected_collections(
        self,
        selected_collections: Union[
            "XAFontBookFontCollectionList", list["XAFontBookFontCollection"]
        ],
    ):
        if isinstance(selected_collections, list):
            selected_collections = [x.xa_elem for x in selected_collections]
            self.set_property("selectedCollections", selected_collections)
        else:
            self.set_property("selectedCollections", selected_collections.xa_elem)

    def documents(self, filter: dict = None) -> "XAFontBookDocumentList":
        """Returns a list of documents matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.documents(), XAFontBookDocumentList, filter
        )

    def font_families(self, filter: dict = None) -> "XAFontBookFontFamilyList":
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.fontFamilies(), XAFontBookFontFamilyList, filter
        )

    def typefaces(self, filter: dict = None) -> "XAFontBookTypefaceList":
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.typefaces(), XAFontBookTypefaceList, filter
        )

    def font_collections(self, filter: dict = None) -> "XAFontBookFontCollectionList":
        """Returns a list of font collections matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.fontCollections(), XAFontBookFontCollectionList, filter
        )

    def font_domains(self, filter: dict = None) -> "XAFontBookFontDomainList":
        """Returns a list of font domains matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.fontDomains(), XAFontBookFontDomainList, filter
        )

    def font_libraries(self, filter: dict = None) -> "XAFontBookFontLibraryList":
        """Returns a list of font libraries matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.fontLibraries(), XAFontBookFontLibraryList, filter
        )

    def font_containers(self, filter: dict = None) -> "XAFontBookFontContainerList":
        """Returns a list of font containers matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_scel.fontContainers(), XAFontBookFontContainerList, filter
        )


class XAFontBookWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with documents in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

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
        """Whether the window is a modal window."""
        return self.xa_elem.modal()


class XAFontBookDocumentList(XABase.XAList):
    """A wrapper around lists of Font Book documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookDocument, filter)

    def path(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path") or [])

    def modified(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("modified") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_path(self, path: str) -> "XAFontBookDocument":
        return self.by_property("path", path)

    def by_modified(self, modified: bool) -> "XAFontBookDocument":
        return self.by_property("modified", modified)

    def by_name(self, name: str) -> "XAFontBookDocument":
        return self.by_property("name", name)


class XAFontBookDocument(XABase.XAObject):
    """A class for managing and interacting with documents in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def path(self) -> XABase.XAPath:
        """The file path of the document."""
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: XABase.XAPath):
        self.set_property("path", path.path)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save."""
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        """The name of the document."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)


class XAFontBookFontFamilyList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font families that employs fast enumeration techniques.

    All properties of font families can be called as methods on the wrapped list, returning a list containing each font family's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontFamily, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def display_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName") or [])

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def duplicated(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("duplicated") or [])

    def files(self) -> list[list[XABase.XAPath]]:
        ls = self.xa_elem.arrayByApplyingSelector_("files") or []
        return [XABase.XAURL(x) for x in [y for y in ls]]

    def by_properties(self, properties: dict) -> "XAFontBookFontFamily":
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> "XAFontBookFontFamily":
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> "XAFontBookFontFamily":
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> "XAFontBookFontFamily":
        return self.by_property("displayedName", displayed_name)

    def by_enabled(self, enabled: bool) -> "XAFontBookFontFamily":
        return self.by_property("enabled", enabled)

    def by_duplicates(self, duplicated: bool) -> "XAFontBookFontFamily":
        return self.by_property("duplicated", duplicated)

    def by_files(self, files: list[XABase.XAPath]) -> "XAFontBookFontFamily":
        return files == self.files()

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each font family in the list.

        When the clipboard content is set to a list of font families, the name of each font family is added to the clipboard.

        :return: The list of font family names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAFontBookFontFamily(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font families in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the font family."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the font family."""
        return self.xa_elem.name()

    @property
    def display_name(self) -> str:
        """The display name of the font family."""
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        """The display name of the font family."""
        return self.xa_elem.displayedName()

    @property
    def enabled(self) -> bool:
        """Whether the font family is enabled."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def duplicated(self) -> bool:
        """Whether teh font family contains duplicated faces."""
        return self.xa_elem.duplicated()

    @property
    def files(self) -> list[XABase.XAPath]:
        """The font files of the font family."""
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    def delete(self):
        """Permanently deletes the typeface.

        .. versionadded:: 0.0.6
        """
        self.xa_elem.delete()

    def typefaces(self, filter: dict = None) -> "XAFontBookTypefaceList":
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.typefaces(), XAFontBookTypefaceList, filter
        )

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the font family.

        When the clipboard content is set to a font family, the name of the font family is added to the clipboard.

        :return: The name of the font family
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAFontBookTypefaceList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookTypeface, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def display_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName") or [])

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def font_family(self) -> XAFontBookFontFamilyList:
        ls = self.xa_elem.arrayByApplyingSelector_("fontFamily") or []
        return self._new_element(ls, XAFontBookFontFamilyList)

    def family_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("familyName") or [])

    def style_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("styleName") or [])

    def post_script_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("postScriptName") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def duplicated(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("duplicated") or [])

    def font_type(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("fontType") or [])

    def copyright(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("copyright") or [])

    def font_container(self) -> "XAFontBookFontContainerList":
        ls = self.xa_elem.arrayByApplyingSelector_("fontContainer") or []
        return self._new_element(ls, XAFontBookFontContainerList)

    def files(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("files") or []
        return [XABase.XAPath(x) for y in ls for x in y]

    def by_properties(self, properties: dict) -> "XAFontBookTypeface":
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> "XAFontBookTypeface":
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> "XAFontBookTypeface":
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> "XAFontBookTypeface":
        return self.by_property("displayedName", displayed_name)

    def by_font_family(self, font_family: XAFontBookFontFamily) -> "XAFontBookTypeface":
        return self.by_property("fontFamily", font_family.xa_elem)

    def by_family_name(self, family_name: str) -> "XAFontBookTypeface":
        return self.by_property("familyName", family_name)

    def by_style_name(self, style_name: str) -> "XAFontBookTypeface":
        return self.by_property("styleName", style_name)

    def by_post_script_name(self, post_script_name: str) -> "XAFontBookTypeface":
        return self.by_property("postScriptName", post_script_name)

    def by_id(self, id: str) -> "XAFontBookTypeface":
        return self.by_property("id", id)

    def by_enabled(self, enabled: bool) -> "XAFontBookTypeface":
        return self.by_property("enabled", enabled)

    def by_duplicated(self, duplicated: bool) -> "XAFontBookTypeface":
        return self.by_property("duplicated", duplicated)

    def by_font_type(self, font_type: str) -> "XAFontBookTypeface":
        return self.by_property("fontType", font_type)

    def by_copyright(self, copyright: str) -> "XAFontBookTypeface":
        return self.by_property("copyright", copyright)

    def by_font_container(
        self, font_container: "XAFontBookFontContainer"
    ) -> "XAFontBookTypeface":
        return self.by_property("fontContainer", font_container.xa_elem)

    def by_files(self, files: list[XABase.XAPath]) -> "XAFontBookTypeface":
        for typeface in self:
            if typeface.files == files:
                return typeface

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each typeface in the list.

        When the clipboard content is set to a list of typefaces, the name of each typeface is added to the clipboard.

        :return: The list of typeface names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAFontBookTypeface(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with typefaces in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the typeface."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the typeface."""
        return self.xa_elem.name()

    @property
    def display_name(self) -> str:
        """The display name of the typeface."""
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        """The display name of the typeface."""
        return self.xa_elem.displayedName()

    @property
    def font_family(self) -> XAFontBookFontFamily:
        """The font family that contains the typeface."""
        return self._new_element(self.xa_elem.fontFamily(), XAFontBookFontFamily)

    @property
    def family_name(self) -> str:
        """The name of the typeface's font family."""
        return self.xa_elem.familyName()

    @property
    def style_name(self) -> str:
        """The name of the typeface's style."""
        return self.xa_elem.styleName()

    @property
    def post_script_name(self) -> str:
        """The PostScript font name."""
        return self.xa_elem.PostScriptName()

    @property
    def id(self) -> str:
        """The unique identifier for the typeface."""
        return self.xa_elem.ID()

    @property
    def enabled(self) -> bool:
        """Whether the typeface is enabled."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def duplicated(self) -> bool:
        """Whether the typeface is duplicated."""
        return self.xa_elem.duplicated()

    @property
    def font_type(self) -> str:
        """The type of the typeface."""
        return self.xa_elem.fontType()

    @property
    def copyright(self) -> str:
        """The copyright string for the typeface."""
        return self.xa_elem.copyright()

    @property
    def font_container(self) -> "XAFontBookFontContainer":
        """The container of the typeface."""
        return self._new_element(self.xa_elem.fontContainer(), XAFontBookFontContainer)

    @property
    def files(self) -> list[XABase.XAPath]:
        """The font files for the typeface."""
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the typeface.

        When the clipboard content is set to a typeface, the name of the typeface is added to the clipboard.

        :return: The name of the typeface
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAFontBookFontContainerList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAFontBookFontContainer, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def path(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path") or [])

    def files(self) -> list[XABase.XAPath]:
        ls = self.xa_elem.arrayByApplyingSelector_("files") or []
        return [XABase.XAPath(x) for y in ls for x in y]

    def domain(self) -> "XAFontBookFontDomainList":
        ls = self.xa_elem.arrayByApplyingSelector_("domain") or []
        return self._new_element(ls, XAFontBookFontDomainList)

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def by_properties(self, properties: dict) -> "XAFontBookFontContainer":
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> "XAFontBookFontContainer":
        return self.by_property("name", name)

    def by_path(self, path: str) -> "XAFontBookFontContainer":
        return self.by_property("path", path)

    def by_files(self, files: list[XABase.XAPath]) -> "XAFontBookFontContainer":
        return files == self.files()

    def by_domain(self, domain: "XAFontBookFontDomain") -> "XAFontBookFontContainer":
        return self.by_property("domain", domain.xa_elem)

    def by_id(self, id: str) -> "XAFontBookFontContainer":
        return self.by_property("id", id)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each container in the list.

        When the clipboard content is set to a list of containers, the name of each container is added to the clipboard.

        :return: The list of container names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAFontBookFontContainer(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font containers in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the container."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the container."""
        return self.xa_elem.name()

    @property
    def path(self) -> str:
        """The path to the main container."""
        return self.xa_elem.path()

    @property
    def files(self) -> list[XABase.XAPath]:
        """The files for the container."""
        ls = self.xa_elem.files()
        return [XABase.XAPath(x) for x in ls]

    @property
    def domain(self) -> "XAFontBookFontDomain":
        """The font domain for the container."""
        return self._new_element(self.xa_elem.domain(), XAFontBookFontDomain)

    @property
    def id(self) -> str:
        """The unique identifier of the container."""
        return self.xa_elem.ID()

    def font_families(self, filter: dict = None) -> "XAFontBookFontFamilyList":
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.fontFamilies(), XAFontBookFontFamilyList, filter
        )

    def typefaces(self, filter: dict = None) -> "XAFontBookTypefaceList":
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.typefaces(), XAFontBookTypefaceList, filter
        )

    def font_domains(self, filter: dict = None) -> "XAFontBookFontDomainList":
        """Returns a list of font domains matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.fontDomains(), XAFontBookFontDomainList, filter
        )

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the container.

        When the clipboard content is set to a container, the name of the container is added to the clipboard.

        :return: The name of the container
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAFontBookFontCollectionList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of Font Book font containers that employs fast enumeration techniques.

    All properties of font containers can be called as methods on the wrapped list, returning a list containing each container's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(
        self, properties: dict, filter: Union[dict, None] = None, obj_class=None
    ):
        if obj_class is None:
            obj_class = XAFontBookFontCollection
        super().__init__(properties, obj_class, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def display_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayName") or [])

    def displayed_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("displayedName") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def by_properties(self, properties: dict) -> "XAFontBookFontCollection":
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> "XAFontBookFontCollection":
        return self.by_property("name", name)

    def by_display_name(self, display_name: str) -> "XAFontBookFontCollection":
        return self.by_property("displayName", display_name)

    def by_displayed_name(self, displayed_name: str) -> "XAFontBookFontCollection":
        return self.by_property("displayedName", displayed_name)

    def by_enabled(self, enabled: bool) -> "XAFontBookFontCollection":
        return self.by_property("enabled", enabled)

    def get_clipboard_representation(self) -> list[str]:
        """Gets a clipboard-codable representation of each collection in the list.

        When the clipboard content is set to a list of collections, the name of each collection is added to the clipboard.

        :return: The list of collection names
        :rtype: list[str]

        .. versionadded:: 0.0.8
        """
        return self.name()

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAFontBookFontCollection(XABase.XAObject, XAClipboardCodable):
    """A class for managing and interacting with font collections in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the collection."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the collection."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def display_name(self) -> str:
        """The display name of the collection."""
        return self.xa_elem.displayName()

    @property
    def displayed_name(self) -> str:
        """The display name of the collection."""
        return self.xa_elem.displayedName()

    @property
    def enabled(self) -> bool:
        """Whether the collection is enabled."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    def font_families(self, filter: dict = None) -> "XAFontBookFontFamilyList":
        """Returns a list of font families matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.fontFamilies(), XAFontBookFontFamilyList, filter
        )

    def typefaces(self, filter: dict = None) -> "XAFontBookTypefaceList":
        """Returns a list of typefaces matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.typefaces(), XAFontBookTypefaceList, filter
        )

    def get_clipboard_representation(self) -> str:
        """Gets a clipboard-codable representation of the collection.

        When the clipboard content is set to a collection, the name of the collection is added to the clipboard.

        :return: The name of the collection
        :rtype: str

        .. versionadded:: 0.0.8
        """
        return self.name

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name) + ">"


class XAFontBookFontLibraryList(XAFontBookFontCollectionList):
    """A wrapper around lists of Font Book font libraries that employs fast enumeration techniques.

    All properties of font libraries can be called as methods on the wrapped list, returning a list containing each library's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFontBookFontLibrary)


class XAFontBookFontLibrary(XAFontBookFontCollection):
    """A class for managing and interacting with font libraries in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def id(self) -> str:
        """The unique identifier of the domain."""
        return self.xa_elem.ID()

    def font_containers(self, filter: dict = None) -> "XAFontBookFontContainerList":
        """Returns a list of font containers matching the filter.

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.fontContainers(), XAFontBookFontContainerList, filter
        )


class XAFontBookFontDomainList(XAFontBookFontLibraryList):
    """A wrapper around lists of Font Book font domains that employs fast enumeration techniques.

    All properties of font domains can be called as methods on the wrapped list, returning a list containing each domain's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, filter, XAFontBookFontDomain)


class XAFontBookFontDomain(XAFontBookFontLibrary):
    """A class for managing and interacting with font domains in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)


class XAFontBookFontBookAllFontsLibraryObject(XAFontBookFontDomain):
    """A class for managing and interacting with the all fonts library object in Font Book.app.

    .. seealso:: :class:`XAFontBookApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)
