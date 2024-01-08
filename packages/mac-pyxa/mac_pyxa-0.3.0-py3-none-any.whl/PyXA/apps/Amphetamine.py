""".. versionadded:: 0.1.0

Control Amphetamine using JXA-like syntax.
"""

from typing import Literal, Union

from PyXA import XABaseScriptable


class XAAmphetamineApplication(XABaseScriptable.XASBApplication):
    """A class for managing and interacting with Amphetamine.app.

    .. versionadded:: 0.1.0
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether Amphetamine is the active application."""
        return self.xa_scel.frontmost()

    @property
    def version(self) -> str:
        """The version number of Amphetamine.app."""
        return self.xa_scel.version()

    @property
    def session_is_active(self) -> bool:
        """Whether there is an active session."""
        return self.xa_scel.sessionIsActive()

    @property
    def session_time_remaining(self) -> int:
        """The total seconds remaining in a session. 0 if session is of infinite duration. -1 is session is trigger-based. -2 is session is app-based or date-based. -3 if there is no active session."""
        return self.xa_scel.sessionTimeRemaining()

    @property
    def display_sleep_allowed(self) -> bool:
        """Whether display sleep is permitted.  If there is no active session, the state of the Preferences → Sessions → Allow Display Sleep checkbox is returned."""
        return self.xa_scel.displaySleepAllowed()

    @property
    def screen_saver_allowed(self) -> bool:
        """Whether screen saver activation is permitted. If there is no active session, the state of the Preferences → Sessions → Allow Screen Saver After checkbox is returned."""
        return self.xa_scel.screenSaverAllowed()

    @property
    def closed_display_mode_enabled(self) -> bool:
        """Whether closed-display mode is enabled. If there is no active session, the state of the Preferences → Sessions → Allow System to Sleep When Display is Closed checkbox is returned. Note: If this Mac does not support closed-display mode, false is always returned. Note: The UI button state for this feature will be the opposite of the return value for this call. For example, if the UI button's state is on/true, the return value for this call will be false."""
        return self.xa_scel.closedDisplayModeEnabled()

    @property
    def session_is_trigger(self) -> bool:
        """Whether the current session was started by a trigger. False boolean is always returned if there is no active session."""
        return self.xa_scel.sessionIsTrigger()

    @property
    def triggers_are_enabled(self) -> bool:
        """Whether trigger session activation is enabled."""
        return self.xa_scel.triggersAreEnabled()

    @property
    def drive_alive_is_enabled(self) -> bool:
        """Whether Drive Alive is enabled."""
        return self.xa_scel.driveAliveIsEnabled()

    def start_new_session(
        self,
        duration: Union[int, None] = None,
        interval: Union[Literal["hours", "minutes"], None] = None,
        display_sleep_allowed: Union[bool, None] = None,
    ):
        """Starts a new session. Options from Amphetamine's Preferences (default duration/display sleep allowed) are used if options are not explicitly supplied in command. Ends any existing sessions, including Trigger-based sessions before starting a new session.

        :param duration: The duration of the session
        :type duration: int
        :param interval: The time unit of the session, either hours or minutes, defaults to "minutes"
        :type interval: Literal['hours', 'minutes'], optional
        :param display_sleep_allowed: Whether display sleep is permitted during the session, defaults to False
        :type display_sleep_allowed: bool, optional

        .. versionadded:: 0.1.0
        """
        options = {}
        if duration != None:
            options["duration"] = duration
        if interval != None:
            options["interval"] = interval
        if display_sleep_allowed != None:
            options["displaySleepAllowed"] = display_sleep_allowed

        self.xa_scel.startNewSessionWithOptions_(options if options != {} else None)

    def end_session(self):
        """Ends the current session. Trigger sessions will also end with this command, but may immediately restart (this command does not disable Triggers).

        .. versionadded:: 0.1.0
        """
        self.xa_scel.endSession()

    def allow_display_sleep(self):
        """If there is an active session, the current session's properties are modified to display sleep. If no session is active, the global preference is set to allow display sleep for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.allow_display_sleep()
        >>> print(app.display_sleep_allowed)
        True

        .. versionadded:: 0.1.0
        """
        self.xa_scel.allowDisplaySleep()

    def prevent_display_sleep(self):
        """If there is an active session, the current session's properties are modified to prevent display sleep. If no session is active, the global preference is set to prevent display sleep for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.prevent_display_sleep()
        >>> print(app.display_sleep_allowed)
        False

        .. versionadded:: 0.1.0
        """
        self.xa_scel.preventDisplaySleep()

    def allow_screen_saver(self):
        """If there is an active session, the current session's properties are modified to allow screen saver activation. If no session is active, the global preference is set to allow screen saver activation for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration. If the Trigger session does not normally allow screen saver activation, a prompt is displayed to choose a delay before screen saver activation. This command should not be used for automation or if the Mac is otherwise unattended.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.allow_screen_saver()
        >>> print(app.screen_saver_allowed)
        True

        .. versionadded:: 0.1.0
        """
        self.xa_scel.allowScreenSaver()

    def prevent_screen_saver(self):
        """If there is an active session, the current session's properties are modified to prevent screen saver activation. If no session is active, the global preference is set to prevent screen saver activation for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.prevent_screen_saver()
        >>> print(app.screen_saver_allowed)
        False

        .. versionadded:: 0.1.0
        """
        self.xa_scel.preventScreenSaver()

    def enable_closed_display_mode(self):
        """If there is an active session, the current session's properties are modified to allow closed-display mode. If no session is active, the global preference is set to allow closed-display mode for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration. Note: When enabling this feature, a warning prompt appears. This prompt can be configured to not be show from within the prompt itself. Before making this call via AppleScript, you should visit Preferences → Sessions → Allow System to Sleep When Display is Closed and toggle on/off this feature. In the warning prompt that appears, select Do Not Show This Message Again.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.enable_closed_display_mode()
        >>> print(app.closed_display_mode_enabled)
        True

        .. versionadded:: 0.1.0
        """
        self.xa_scel.enableClosedDisplayMode()

    def disable_closed_display_mode(self):
        """If there is an active session, the current session's properties are modified to prevent closed-display mode. If no session is active, the global preference is set to prevent closed-display mode for future non-Trigger sessions. Note: If a Trigger session is active, only the current run of the Trigger session's properties are modified. Future runs of the Trigger session will use the Trigger's configuration.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.disable_closed_display_mode()
        >>> print(app.closed_display_mode_enabled)
        False

        .. versionadded:: 0.1.0
        """
        self.xa_scel.disableClosedDisplayMode()

    def enable_triggers(self):
        """Updates Amphetamine's preferences to enable Trigger session activation.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.enable_triggers()
        >>> print(app.triggers_are_enabled)
        True

        .. versionadded:: 0.1.0
        """
        self.xa_scel.enableTriggers()

    def disable_triggers(self):
        """Updates Amphetamine's preferences to disable Trigger session activation.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.disable_triggers()
        >>> print(app.triggers_are_enabled)
        False

        .. versionadded:: 0.1.0
        """
        self.xa_scel.disableTriggers()

    def enable_drive_alive(self):
        """Updates Amphetamine's preferences to enable Drive Alive.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.enable_drive_alive()
        >>> print(app.drive_alive_is_enabled)
        True

        .. versionadded:: 0.1.0
        """
        self.xa_scel.enableDriveAlive()

    def disable_drive_alive(self):
        """Updates Amphetamine's preferences to disable Drive Alive.

        :Example:

        >>> import PyXA
        >>> app = PyXA.Application("Amphetamine")
        >>> app.disable_drive_alive()
        >>> print(app.drive_alive_is_enabled)
        False

        .. versionadded:: 0.1.0
        """
        self.xa_scel.disableDriveAlive()

    def give_molecule(self):
        """Gives a molecule, as requested. You should not execute this command if you suffer from photosensitive epilepsy or are otherwise disturbed by flashing lights.

        .. versionadded:: 0.1.0
        """
        self.xa_scel.giveMolecule()
