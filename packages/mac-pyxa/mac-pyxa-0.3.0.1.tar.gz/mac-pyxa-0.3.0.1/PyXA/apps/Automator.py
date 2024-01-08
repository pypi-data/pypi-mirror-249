""".. versionadded:: 0.0.4

Control Automator using JXA-like syntax.
"""

from enum import Enum
from typing import Any, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath


class XAAutomatorApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with Automator.app.

    .. seealso:: :class:`XAAutomatorWindow`, :class:`XAAutomatorDocument`

    .. versionadded:: 0.0.4
    """

    class ObjectType(Enum):
        """The object types available for creation in Automator.

        .. versionadded:: 0.3.0
        """

        ACTION = "action"
        DOCUMENT = "document"
        REQUIRED_RESOURCE = "required_resource"
        SETTING = "setting"
        VARIABLE = "variable"

    class WarningLevel(Enum):
        """Options for warning level in regard to likelihood of data loss."""

        IRREVERSIBLE = XABase.OSType("irrv")
        NONE = XABase.OSType("none")
        REVERSIBLE = XABase.OSType("rvbl")

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAAutomatorWindow

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Automator is the active application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version of Automator.app."""
        return self.xa_scel.version()

    def open(self, path: Union[str, AppKit.NSURL]) -> "XAAutomatorWorkflow":
        """Opens the file at the given filepath.

        :param target: The path to a file or the URL to a website to open.
        :type target: Union[str, AppKit.NSURL]
        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        if not isinstance(path, AppKit.NSURL):
            path = XABase.XAPath(path)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
            [path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None
        )
        return self.workflows()[0]

    def add(
        self,
        action: "XAAutomatorAction",
        workflow: "XAAutomatorWorkflow",
        index: int = -1,
    ) -> "XAAutomatorApplication":
        """Adds the specified action to a workflow at the specified index.

        :param action: The action to add
        :type action: XAAutomatorAction
        :param workflow: The workflow to add the action to
        :type workflow: XAAutomatorWorkflow
        :param index: The index at which to add the action, defaults to -1
        :type index: int, optional
        :return: A reference to the application object
        :rtype: XAAutomatorApplication

        .. versionadded:: 0.0.4
        """
        self.xa_scel.add_to_atIndex_(action.xa_elem, workflow.xa_elem, index)
        return self

    def documents(self, filter: Union[dict, None] = None) -> "XAAutomatorDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter documents by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of documents
        :rtype: XAAutomatorDocumentList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.documents(), XAAutomatorDocumentList, filter
        )

    def automator_actions(
        self, filter: Union[dict, None] = None
    ) -> "XAAutomatorActionList":
        """Returns a list of Automator actions, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter actions by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of actions
        :rtype: XAAutomatorActionList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.AutomatorActions(), XAAutomatorActionList, filter
        )

    def variables(self, filter: Union[dict, None] = None) -> "XAAutomatorVariableList":
        """Returns a list of Automator variables, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter variables by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of variables
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.variables(), XAAutomatorVariableList, filter
        )

    def workflows(self, filter: Union[dict, None] = None) -> "XAAutomatorWorkflowList":
        """Returns a list of Automator workflows, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter workflows by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of workflows
        :rtype: XAAutomatorWorkflowList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_scel.workflows(), XAAutomatorWorkflowList, filter
        )

    def make(
        self,
        specifier: Union[str, "XAAutomatorApplication.ObjectType"],
        properties: dict,
        data: Any,
    ):
        """Creates a new element of the given specifier class without adding it to any list.

        Use :func:`XABase.XAList.push` to push the element onto a list.

        :param specifier: The classname of the object to create
        :type specifier: Union[str, XAAutomatorApplication.ObjectType]
        :param properties: The properties to give the object
        :type properties: dict
        :param data: The data to give the object
        :type data: Any
        :return: A PyXA wrapped form of the object
        :rtype: XABase.XAObject

        .. versionadded:: 0.0.4
        """
        if isinstance(specifier, XAAutomatorApplication.ObjectType):
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

        if specifier == "workflow":
            return self._new_element(obj, XAAutomatorWorkflow)
        elif specifier == "variable":
            return self._new_element(obj, XAAutomatorVariable)
        elif specifier == "document":
            return self._new_element(obj, XAAutomatorDocument)
        elif specifier == "action":
            return self._new_element(obj, XAAutomatorAction)
        elif specifier == "required_resource":
            return self._new_element(obj, XAAutomatorRequiredResource)
        elif specifier == "setting":
            return self._new_element(obj, XAAutomatorSetting)


class XAAutomatorWindow(XABaseScriptable.XASBWindow):
    """A class for managing and interacting with Automator windows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def floating(self) -> bool:
        """Whether the window floats."""
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is a modal window."""
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar."""
        return self.xa_elem.titled()

    @property
    def document(self) -> "XAAutomatorDocument":
        """The document currently displayed in the window."""
        return self._new_element(self.xa_elem.document(), XAAutomatorDocument)


class XAAutomatorDocumentList(XABase.XAList):
    """A wrapper around a list of Automator documents which utilizes fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each document's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorDocument, filter)

    def id(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("id") or [])

    def title(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("title") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def by_id(self, id: int) -> Union["XAAutomatorDocument", None]:
        return self.by_property("id", id)

    def by_title(self, title: str) -> Union["XAAutomatorDocument", None]:
        return self.by_property("title", title)

    def by_index(self, index: int) -> Union["XAAutomatorDocument", None]:
        return self.by_property("index", index)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorDocument(XABase.XAObject):
    """A class for managing and interacting with Automator windows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since its last save."""
        return self.xa_elem.modified()

    @property
    def name(self) -> str:
        """The title of the document."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> XABase.XAPath:
        """The path to the document on the disk."""
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: Union[str, XABase.XAPath]):
        if isinstance(path, str):
            path = XABase.XAPath(path)
        self.set_property("path", path.path)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorActionList(XABase.XAList):
    """A wrapper around a list of Automator required resources which utilizes fast enumeration techniques.

    All properties of required resources can be called as methods on the wrapped list, returning a list containing each resource's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorAction, filter)

    def bundle_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("bundleId") or [])

    def category(self) -> list[list[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("category") or [])

    def comment(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("comment") or [])

    def enabled(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("enabled") or [])

    def execution_error_message(self) -> list[str]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("executionErrorMessage") or []
        )

    def execution_error_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorNumber") or [])

    def execution_result(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionResult") or [])

    def icon_name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("iconName") or [])

    def ignores_input(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("ignoresInput") or [])

    def index(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("index") or [])

    def input_types(self) -> list[list[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("inputTypes") or [])

    def keywords(self) -> list[list[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("keywords") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def output_types(self) -> list[list[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("outputTypes") or [])

    def parent_workflow(self) -> "XAAutomatorWorkflowList":
        ls = self.xa_elem.arrayByApplyingSelector_("parentWorkflow") or []
        return self._new_element(ls, XAAutomatorWorkflowList)

    def path(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("path") or [])

    def show_action_when_run(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("showActionWhenRun") or [])

    def target_application(self) -> list[list[str]]:
        return list(self.xa_elem.arrayByApplyingSelector_("targetApplication") or [])

    def version(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("version") or [])

    def warning_action(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("warningAction") or [])

    def warning_level(self) -> list[XAAutomatorApplication.WarningLevel]:
        ls = self.xa_elem.arrayByApplyingSelector_("warningLevel") or []
        return [XAAutomatorApplication.WarningLevel(x) for x in ls]

    def warning_message(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("warningMessage") or [])

    def by_bundle_id(self, bundle_id: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("bundleId", bundle_id)

    def by_category(self, category: list[str]) -> Union["XAAutomatorAction", None]:
        return self.by_property("category", category)

    def by_comment(self, comment: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("comment", comment)

    def by_enabled(self, enabled: bool) -> Union["XAAutomatorAction", None]:
        return self.by_property("enabled", enabled)

    def by_execution_error_message(
        self, execution_error_message: str
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("executionErrorMessage", execution_error_message)

    def by_execution_error_number(
        self, execution_error_number: int
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("executionErrorNumber", execution_error_number)

    def by_execution_result(
        self, execution_result: Any
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("executionResult", execution_result)

    def by_icon_name(self, icon_name: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("iconName", icon_name)

    def by_id(self, id: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("id", id)

    def by_ignores_input(self, ignores_input: bool) -> Union["XAAutomatorAction", None]:
        return self.by_property("ignoresInput", ignores_input)

    def by_input_types(
        self, input_types: list[str]
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("inputTypes", input_types)

    def by_keywords(self, keywords: list[str]) -> Union["XAAutomatorAction", None]:
        return self.by_property("keywords", keywords)

    def by_name(self, name: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("name", name)

    def by_output_types(
        self, output_types: list[str]
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("outputTypes", output_types)

    def by_parent_workflow(
        self, parent_workflow: "XAAutomatorWorkflow"
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("parentWorkflow", parent_workflow.xa_elem)

    def by_path(self, path: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("path", path)

    def by_show_action_when_run(
        self, show_action_when_run: bool
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("show_action_when_run", show_action_when_run)

    def by_target_application(
        self, target_application: list[str]
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("targetApplication", target_application)

    def by_version(self, version: str) -> Union["XAAutomatorAction", None]:
        return self.by_property("version", version)

    def by_warning_action(
        self, warning_action: str
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("warningAction", warning_action)

    def by_warning_level(
        self, warning_level: XAAutomatorApplication.WarningLevel
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("warningLevel", warning_level.value)

    def by_warning_message(
        self, warning_message: str
    ) -> Union["XAAutomatorAction", None]:
        return self.by_property("warningMessage", warning_message)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorAction(XABase.XAObject):
    """A class for managing and interacting with actions in Automator.app.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def bundle_id(self) -> str:
        """The bundle identifier for the action."""
        return self.xa_elem.bundleId()

    @property
    def category(self) -> list[str]:
        """The categories that contain the action"""
        return self.xa_elem.category()

    @property
    def comment(self) -> str:
        """The comment for the name of the action."""
        return self.xa_elem.comment()

    @comment.setter
    def comment(self, comment: str):
        self.set_property("comment", comment)

    @property
    def enabled(self) -> bool:
        """Whether the action is enabled."""
        return self.xa_elem.enabled()

    @enabled.setter
    def enabled(self, enabled: bool):
        self.set_property("enabled", enabled)

    @property
    def execution_error_message(self) -> str:
        """The text error message generated by execution of the action."""
        return self.xa_elem.executionErrorMessage()

    @property
    def execution_error_number(self) -> int:
        """The numeric error code generated by execution of the action."""
        return self.xa_elem.executionErrorNumber()

    @property
    def execution_result(self) -> Any:
        """The result of the action, passed as input to the next action."""
        return self.xa_elem.executionResult()

    @property
    def icon_name(self) -> str:
        """The name for the icon associated with the action."""
        return self.xa_elem.iconName()

    @property
    def id(self) -> str:
        """The unique identifier for the action."""
        return self.xa_elem.id()

    @property
    def ignores_input(self) -> bool:
        """Whether the action ignores input when run."""
        return self.xa_elem.ignoresInput()

    @ignores_input.setter
    def ignores_input(self, ignores_input: bool):
        self.set_property("ignoresInput", ignores_input)

    @property
    def index(self) -> int:
        """The index of the action from the first action in the workflow."""
        return self.xa_elem.index()

    @index.setter
    def index(self, index: int):
        self.set_property("index", index)

    @property
    def input_types(self) -> list[str]:
        """The input types accepted by the action."""
        return self.xa_elem.inputTypes()

    @property
    def keywords(self) -> list[str]:
        """The keywords that describe the action."""
        return self.xa_elem.keywords()

    @property
    def name(self) -> str:
        """The localized name of the action."""
        return self.xa_elem.name()

    @property
    def output_types(self) -> list[str]:
        """The output types produced by the action."""
        return self.xa_elem.outputTypes()

    @property
    def parent_workflow(self) -> "XAAutomatorWorkflow":
        """The workflow that contains the action."""
        return self._new_element(self.xa_elem.parentWorkflow(), XAAutomatorWorkflow)

    @property
    def path(self) -> XABase.XAPath:
        """The path of the file that contains the action."""
        return XABase.XAPath(self.xa_elem.path())

    @property
    def show_action_when_run(self) -> bool:
        """Whether the action should show its user interface when run."""
        return self.xa_elem.showActionWehnRun()

    @show_action_when_run.setter
    def show_action_when_run(self, show_action_when_run: bool):
        self.set_property("showActionWhenRun", show_action_when_run)

    @property
    def target_application(self) -> list[str]:
        """The application(s) with which the action communicates."""
        return self.xa_elem.targetApplication()

    @property
    def version(self) -> str:
        """The version of the action."""
        return self.xa_elem.version()

    @property
    def warning_action(self) -> str:
        """The action suggested by the warning, if any."""
        return self.xa_elem.warningAction()

    @property
    def warning_level(self) -> XAAutomatorApplication.WarningLevel:
        """The level of the warning, increasing in likelihood of data loss."""
        return XAAutomatorApplication.WarningLevel(self.xa_elem.warningLevel())

    @property
    def warning_message(self) -> str:
        """The message that accompanies the warning, if any."""
        return self.xa_elem.warningMessage()

    def required_resources(
        self, filter: Union[dict, None] = None
    ) -> "XAAutomatorRequiredResourceList":
        """Returns a list of required resource, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter resources by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of required resources
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.requiredResources(), XAAutomatorRequiredResourceList, filter
        )

    def settings(self, filter: Union[dict, None] = None) -> "XAAutomatorSettingList":
        """Returns a list of settings, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter settings by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of settings
        :rtype: XAAutomatorWorkflowList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.settings(), XAAutomatorSettingList, filter
        )

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorRequiredResourceList(XABase.XAList):
    """A wrapper around a list of Automator required resources which utilizes fast enumeration techniques.

    All properties of required resources can be called as methods on the wrapped list, returning a list containing each resource's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorRequiredResource, filter)

    def kind(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("kind") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def resource(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("resource") or [])

    def version(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("version") or [])

    def by_kind(self, kind: str) -> Union["XAAutomatorRequiredResource", None]:
        return self.by_property("kind", kind)

    def by_name(self, name: str) -> Union["XAAutomatorRequiredResource", None]:
        return self.by_property("name", name)

    def by_resource(self, resource: str) -> Union["XAAutomatorRequiredResource", None]:
        return self.by_property("resource", resource)

    def by_version(self, version: int) -> Union["XAAutomatorRequiredResource", None]:
        return self.by_property("version", version)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorRequiredResource(XABase.XAObject):
    """A class for managing and interacting with required resources in Automator.app.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def kind(self) -> str:
        """The kind of required resource."""
        return self.xa_elem.kind()

    @property
    def name(self) -> str:
        """The name of the required resource."""
        return self.xa_elem.name()

    @property
    def resource(self) -> str:
        """The specification of the required resource."""
        return self.xa_elem.resource()

    @property
    def version(self) -> int:
        """The minimum acceptable version of the required resource."""
        return self.xa_elem.version()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorSettingList(XABase.XAList):
    """A wrapper around a list of Automator settings which utilizes fast enumeration techniques.

    All properties of settings can be called as methods on the wrapped list, returning a list containing each setting's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorSetting, filter)

    def default_value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("defaultValue") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_default_value(self, default_value: Any) -> Union["XAAutomatorSetting", None]:
        if isinstance(default_value, XABase.XAObject):
            default_value = default_value.xa_elem
        return self.by_property("defaultValue", default_value)

    def by_name(self, name: str) -> Union["XAAutomatorSetting", None]:
        return self.by_property("name", name)

    def by_value(self, value: Any) -> Union["XAAutomatorSetting", None]:
        if isinstance(value, XABase.XAObject):
            value = value.xa_elem
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorSetting(XABase.XAObject):
    """A class for managing and interacting with Automator settings (i.e. named values).

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def default_value(self) -> Any:
        """The default value of the setting."""
        return self.xa_elem.defaultValue()

    @property
    def name(self) -> str:
        """The name of the setting."""
        return self.xa_elem.name()

    @property
    def value(self) -> Any:
        """The value of the setting."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorVariableList(XABase.XAList):
    """A wrapper around a list of Automator variables which utilizes fast enumeration techniques.

    All properties of variables can be called as methods on the wrapped list, returning a list containing each variable's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorVariable, filter)

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def settable(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("settable") or [])

    def value(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("value") or [])

    def by_name(self, name: str) -> Union["XAAutomatorVariable", None]:
        return self.by_property("name", name)

    def by_settable(self, settable: bool) -> Union["XAAutomatorVariable", None]:
        return self.by_property("settable", settable)

    def by_value(self, value: Any) -> Union["XAAutomatorVariable", None]:
        if isinstance(value, XABase.XAObject):
            value = value.xa_elem
        return self.by_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorVariable(XABase.XAObject):
    """A class for managing and interacting with Automator variables.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the variable."""
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def settable(self) -> bool:
        """Whether the name and value of the variable can be changed."""
        return self.xa_elem.settable()

    @property
    def value(self) -> Any:
        """The value of the variable."""
        return self.xa_elem.value()

    @value.setter
    def value(self, value: Any):
        self.set_property("value", value)

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"


class XAAutomatorWorkflowList(XABase.XAList):
    """A wrapper around a list of Automator workflows which utilizes fast enumeration techniques.

    All properties of workflows can be called as methods on the wrapped list, returning a list containing each workflow's value for the property.

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAAutomatorWorkflow, filter)

    def current_action(self) -> XAAutomatorActionList:
        ls = self.xa_elem.arrayByApplyingSelector_("currentAction") or []
        return self._new_element(ls, XAAutomatorActionList)

    def execution_error_message(self) -> list[str]:
        return list(
            self.xa_elem.arrayByApplyingSelector_("executionErrorMessage") or []
        )

    def execution_error_number(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionErrorNumber") or [])

    def execution_id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionId") or [])

    def execution_result(self) -> list[Any]:
        return list(self.xa_elem.arrayByApplyingSelector_("executionResult") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def by_current_action(
        self, current_action: XAAutomatorAction
    ) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("currentAction", current_action.xa_elem)

    def by_execution_error_message(
        self, execution_error_message: str
    ) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("executionErrorMessage", execution_error_message)

    def by_execution_error_number(
        self, execution_error_number: int
    ) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("executionErrorNumber", execution_error_number)

    def by_execution_id(self, execution_id: str) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("executionId", execution_id)

    def by_execution_result(self, result: Any) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("result", result)

    def by_name(self, name: str) -> Union["XAAutomatorWorkflow", None]:
        return self.by_property("name", name)

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"


class XAAutomatorWorkflow(XAAutomatorDocument):
    """A class for managing and interacting with Automator workflows.

    .. seealso:: :class:`XAAutomatorApplication`

    .. versionadded:: 0.0.4
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def current_action(self) -> XAAutomatorAction:
        """The current or most recent action of the workflow."""
        return self._new_element(self.xa_elem.currentAction(), XAAutomatorAction)

    @property
    def execution_error_message(self) -> str:
        """The text error message generated by the most recent execution."""
        return self.xa_elem.executionErrorMessage()

    @property
    def execution_error_number(self) -> int:
        """The numeric error code generated by the most recent execution."""
        return self.xa_elem.executionErrorNumber()

    @property
    def execution_id(self) -> str:
        """The unique identifier for the current or most recent execution."""
        return self.xa_elem.executionId()

    @property
    def execution_result(self) -> Any:
        """The result of the most resent execution."""
        return self.xa_elem.executionResult().get()

    @property
    def name(self) -> str:
        """The name of the workflow."""
        return self.xa_elem.name()

    def execute(self) -> Any:
        """Executes the workflow.

        :return: The return value of the workflow after execution
        :rtype: Any

        .. versionadded:: 0.0.5
        """
        return self.xa_elem.execute()

    def automator_actions(
        self, filter: Union[dict, None] = None
    ) -> "XAAutomatorActionList":
        """Returns a list of actions, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter actions by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of actions
        :rtype: XAAutomatorActionList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.AutomatorActions(), XAAutomatorActionList, filter
        )

    def variables(self, filter: Union[dict, None] = None) -> "XAAutomatorVariableList":
        """Returns a list of variables, as PyXA objects, matching the given filter.

        :param filter: Keys and values to filter variables by, defaults to None
        :type filter: dict, optional
        :return: A PyXA list object wrapping a list of variables
        :rtype: XAAutomatorVariableList

        .. versionadded:: 0.0.4
        """
        return self._new_element(
            self.xa_elem.variables(), XAAutomatorVariableList, filter
        )

    def delete(self):
        """Closes the workflow.

        .. versionadded:: 0.0.4
        """
        self.xa_elem.delete()

    def save(self) -> "XAAutomatorWorkflow":
        """Saves the workflow to the disk at the location specified by :attr:`XAAutomatorWorkflow.path`, or in the downloads folder if no path has been specified.

        :return: The workflow object.
        :rtype: XAAutomatorWorkflow

        .. versionadded:: 0.0.5
        """
        self.xa_elem.saveAs_in_("workflow", self.path)
        return self

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"
