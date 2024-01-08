""".. versionadded:: 0.0.6

Control the macOS QuickTime application using JXA-like syntax.
"""
from typing import Any, Union

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath


class XAQuickTimeApplication(XABaseScriptable.XASBApplication, XACanOpenPath):
    """A class for managing and interacting with QuickTime.app.

    .. seealso:: :class:`XAQuickTimeWindow`, :class:`XAQuickTimeDocument`, :class:`XAQuickTimeAudioRecordingDevice`, :class:`XAQuickTimeVideoRecordingDevice`, :class:`XAQuickTimeAudioCompressionPreset`, :class:`XAQuickTimeMovieCompressionPreset`, :class:`XAQuickTimeScreenCompressionPreset`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAQuickTimeWindow

    @property
    def properties(self) -> dict:
        """Every property of the QuickTime application."""
        return self.xa_scel.properties()

    @property
    def name(self) -> str:
        """The name of the application."""
        return self.xa_scel.name()

    @property
    def frontmost(self) -> bool:
        """Whether QuickTime is the frontmost application."""
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def version(self) -> str:
        """The version of QuickTime.app."""
        return self.xa_scel.version()

    @property
    def current_document(self) -> "XAQuickTimeDocument":
        """The document currently open in the front window of QuickTime."""
        return self.front_window.document

    def open(self, path: Union[str, AppKit.NSURL]) -> "XAQuickTimeDocument":
        """Opens the file at the given filepath.

        :param target: The path of a file to open.
        :type target: Union[str, AppKit.NSURL]
        :return: A reference to the newly opened document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        if not isinstance(path, AppKit.NSURL):
            if "://" not in path:
                path = XABase.XAPath(path)
        self.xa_wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
            [path.xa_elem], self.xa_elem.bundleIdentifier(), 0, None, None
        )
        return self._new_element(self.front_window.document, XAQuickTimeDocument)

    def open_url(self, url: Union[str, AppKit.NSURL]) -> "XAQuickTimeDocument":
        """Opens the file at the given (remote) URL.

        :param target: The path of a file to stream.
        :type target: Union[str, NSURL]
        :return: A reference to the newly opened document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        if not isinstance(url, AppKit.NSURL):
            if "://" not in url:
                url = XABase.XAURL(url)
        self.xa_scel.openURL_(url)

    def new_audio_recording(self) -> "XAQuickTimeDocument":
        """Starts a new audio recording.

        :return: The newly created audio recording document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_scel.newAudioRecording()

    def new_movie_recording(self) -> "XAQuickTimeDocument":
        """Starts a new movie recording.

        :return: The newly created movie recording document.
        :rtype: XAQuickTimeDocument

        .. versionadded:: 0.0.6
        """
        return self.xa_scel.newMovieRecording()

    def new_screen_recording(self) -> "XAQuickTimeApplication":
        """Starts a new screen recording.

        :return: A reference to the application object.
        :rtype: XAQuickTimeApplication

        .. versionadded:: 0.0.6
        """
        self.xa_scel.newScreenRecording()
        return self

    def documents(self, filter: Union[dict, None] = None) -> "XAQuickTimeDocumentList":
        """Returns a list of documents, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have, or None
        :type filter: Union[dict, None]
        :return: The list of documents
        :rtype: XAQuickTimeDocumentList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.documents(), XAQuickTimeDocumentList, filter
        )

    def audio_recording_devices(
        self, filter: Union[dict, None] = None
    ) -> "XAQuickTimeAudioRecordingDeviceList":
        """Returns a list of audio recording devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned audio recording devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio recording devices
        :rtype: XAQuickTimeAudioRecordingDeviceList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.audioRecordingDevices(),
            XAQuickTimeAudioRecordingDeviceList,
            filter,
        )

    def video_recording_devices(
        self, filter: Union[dict, None] = None
    ) -> "XAQuickTimeVideoRecordingDeviceList":
        """Returns a list of video recording devices, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned video recording devices will have, or None
        :type filter: Union[dict, None]
        :return: The list of video recording devices
        :rtype: XAQuickTimeVideoRecordingDeviceList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.videoRecordingDevices(),
            XAQuickTimeVideoRecordingDeviceList,
            filter,
        )

    def audio_compression_presets(
        self, filter: Union[dict, None] = None
    ) -> "XAQuickTimeAudioCompressionPresetList":
        """Returns a list of audio compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned p[resets] will have, or None
        :type filter: Union[dict, None]
        :return: The list of audio compression presets
        :rtype: XAQuickTimeAudioCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.audioCompressionPresets(),
            XAQuickTimeAudioCompressionPresetList,
            filter,
        )

    def movie_compression_presets(
        self, filter: Union[dict, None] = None
    ) -> "XAQuickTimeMovieCompressionPresetList":
        """Returns a list of movie compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of movie compression presets
        :rtype: XAQuickTimeMovieCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.movieCompressionPresets(),
            XAQuickTimeMovieCompressionPresetList,
            filter,
        )

    def screen_compression_presets(
        self, filter: Union[dict, None] = None
    ) -> "XAQuickTimeScreenCompressionPresetList":
        """Returns a list of screen compression presets, as PyXA objects, matching the given filter.

        :param filter: A dictionary specifying property-value pairs that all returned presets will have, or None
        :type filter: Union[dict, None]
        :return: The list of screen compression presets
        :rtype: XAQuickTimeScreenCompressionPresetList

        .. versionadded:: 0.0.6
        """
        return self._new_element(
            self.xa_elem.screenCompressionPresets(),
            XAQuickTimeScreenCompressionPresetList,
            filter,
        )


class XAQuickTimeWindow(XABaseScriptable.XASBWindow):
    """A QuickTime window.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """Every property of a QuickTime window."""
        return self.xa_elem.properties()

    @property
    def document(self) -> "XAQuickTimeDocument":
        """The document currently displayed in the front window of QuickTime."""
        return self._new_element(self.xa_elem.document(), XAQuickTimeDocument)


class XAQuickTimeDocumentList(XABase.XAList):
    """A wrapper around lists of themes that employs fast enumeration techniques.

    All properties of themes can be called as methods on the wrapped list, returning a list containing each theme's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeDocument, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def audio_volume(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("audioVolume") or [])

    def current_time(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("currentTime") or [])

    def data_rate(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("dataRate") or [])

    def data_size(self) -> list[int]:
        return list(self.xa_elem.arrayByApplyingSelector_("dataSize") or [])

    def duration(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("duration") or [])

    def looping(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("looping") or [])

    def muted(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("muted") or [])

    def natural_dimensions(self) -> list[tuple[int, int]]:
        return list(self.xa_elem.arrayByApplyingSelector_("naturalDimensions") or [])

    def playing(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("playing") or [])

    def rate(self) -> list[float]:
        return list(self.xa_elem.arrayByApplyingSelector_("rate") or [])

    def presenting(self) -> list[bool]:
        return list(self.xa_elem.arrayByApplyingSelector_("presenting") or [])

    def current_microphone(self) -> "XAQuickTimeAudioRecordingDeviceList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentMicrophone") or []
        return self._new_element(ls, XAQuickTimeAudioRecordingDeviceList)

    def current_camera(self) -> "XAQuickTimeVideoRecordingDeviceList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentCamera") or []
        return self._new_element(ls, XAQuickTimeVideoRecordingDeviceList)

    def current_audio_compression(self) -> "XAQuickTimeAudioCompressionPresetList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentAudioCompression") or []
        return self._new_element(ls, XAQuickTimeAudioCompressionPresetList)

    def current_movie_compression(self) -> "XAQuickTimeMovieCompressionPresetList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentMovieCompression") or []
        return self._new_element(ls, XAQuickTimeMovieCompressionPresetList)

    def current_screen_compression(self) -> "XAQuickTimeScreenCompressionPresetList":
        ls = self.xa_elem.arrayByApplyingSelector_("currentScreenCompression") or []
        return self._new_element(ls, XAQuickTimeScreenCompressionPresetList)

    def by_properties(self, properties: dict) -> "XAQuickTimeDocument":
        return self.by_property("properties", properties)

    def by_audio_volume(self, audio_volume: float) -> "XAQuickTimeDocument":
        return self.by_property("audioVolume", audio_volume)

    def by_current_time(self, current_time: float) -> "XAQuickTimeDocument":
        return self.by_property("currentTime", current_time)

    def by_data_rate(self, data_rate: int) -> "XAQuickTimeDocument":
        return self.by_property("dataRate", data_rate)

    def by_data_size(self, data_size: int) -> "XAQuickTimeDocument":
        return self.by_property("dataSize", data_size)

    def by_duration(self, duration: float) -> "XAQuickTimeDocument":
        return self.by_property("duration", duration)

    def by_looping(self, looping: bool) -> "XAQuickTimeDocument":
        return self.by_property("looping", looping)

    def by_muted(self, muted: bool) -> "XAQuickTimeDocument":
        return self.by_property("muted", muted)

    def by_natural_dimensions(
        self, natural_dimensions: tuple[int, int]
    ) -> "XAQuickTimeDocument":
        return self.by_property("naturalDimensions", natural_dimensions)

    def by_playing(self, playing: bool) -> "XAQuickTimeDocument":
        return self.by_property("playing", playing)

    def by_rate(self, rate: float) -> "XAQuickTimeDocument":
        return self.by_property("rate", rate)

    def by_presenting(self, presenting: bool) -> "XAQuickTimeDocument":
        return self.by_property("presenting", presenting)

    def by_current_microphone(self, current_microphone: float) -> "XAQuickTimeDocument":
        return self.by_property("currentMicrophone", current_microphone.xa_elem)

    def by_current_camera(self, current_camera: float) -> "XAQuickTimeDocument":
        return self.by_property("currentCamera", current_camera.xa_elem)

    def by_current_audio_compression(
        self, current_audio_compression: float
    ) -> "XAQuickTimeDocument":
        return self.by_property(
            "currentAudioCompression", current_audio_compression.xa_elem
        )

    def by_current_movie_compression(
        self, current_movie_compression: float
    ) -> "XAQuickTimeDocument":
        return self.by_property(
            "currentMovieCompression", current_movie_compression.xa_elem
        )

    def by_current_screen_compression(
        self, current_screen_compression: float
    ) -> "XAQuickTimeDocument":
        return self.by_property(
            "currentScreenCompression", current_screen_compression.xa_elem
        )


class XAQuickTimeDocument(XABase.XAObject):
    """A class for managing and interacting with documents in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document."""
        return self.xa_elem.properties()

    @property
    def audio_volume(self) -> float:
        """The volume of the movie from 0 to 1 (0 to 100%)."""
        return self.xa_elem.audioVolume()

    @audio_volume.setter
    def audio_volume(self, audio_volume: float):
        self.set_property("audioVolume", audio_volume)

    @property
    def current_time(self) -> float:
        """The current time of the movie in seconds."""
        return self.xa_elem.currentTime()

    @current_time.setter
    def current_time(self, current_time: float):
        self.set_property("currentTime", current_time)

    @property
    def data_rate(self) -> int:
        """The data rate of the movie in bytes per second."""
        return self.xa_elem.dataRate()

    @property
    def data_size(self) -> int:
        """The data size of the movie in bytes."""
        return self.xa_elem.dataSize()

    @property
    def duration(self) -> float:
        """The duration of the movie in seconds."""
        return self.xa_elem.duration()

    @property
    def looping(self) -> bool:
        """Whether the movie plays in a loop."""
        return self.xa_elem.looping()

    @looping.setter
    def looping(self, looping: bool):
        self.set_property("looping", looping)

    @property
    def muted(self) -> bool:
        """Whether the movie is muted."""
        return self.xa_elem.muted()

    @muted.setter
    def muted(self, muted: bool):
        self.set_property("muted", muted)

    @property
    def natural_dimensions(self) -> tuple[int, int]:
        """The national dimensions of the movie."""
        return self.xa_elem.naturalDimensions()

    @property
    def playing(self) -> bool:
        """Whether the movie is currently playing."""
        return self.xa_elem.playing()

    @property
    def rate(self) -> float:
        """The current rate of the movie."""
        return self.xa_elem.rate()

    @rate.setter
    def rate(self, rate: float):
        self.set_property("rate", rate)

    @property
    def presenting(self) -> bool:
        """Whether the movie is presented in full screen."""
        return self.xa_elem.presenting()

    @presenting.setter
    def presenting(self, presenting: bool):
        self.set_property("presenting", presenting)

    @property
    def current_microphone(self) -> "XAQuickTimeAudioRecordingDevice":
        """The currently previewing audio device."""
        return self._new_element(
            self.xa_elem.currentMicrophone(), XAQuickTimeAudioRecordingDevice
        )

    @current_microphone.setter
    def current_microphone(self, current_microphone: "XAQuickTimeAudioRecordingDevice"):
        self.set_property("currentMicrophone", current_microphone.xa_elem)

    @property
    def current_camera(self) -> "XAQuickTimeVideoRecordingDevice":
        """The currently previewing video device."""
        return self._new_element(
            self.xa_elem.currentCamera(), XAQuickTimeVideoRecordingDevice
        )

    @current_camera.setter
    def current_camera(self, current_camera: "XAQuickTimeVideoRecordingDevice"):
        self.set_property("currentCamera", current_camera.xa_elem)

    @property
    def current_audio_compression(self) -> "XAQuickTimeAudioCompressionPreset":
        """The current audio compression preset."""
        return self._new_element(
            self.xa_elem.currentAudioCompression(), XAQuickTimeAudioCompressionPreset
        )

    @current_audio_compression.setter
    def current_audio_compression(
        self, current_audio_compression: "XAQuickTimeAudioCompressionPreset"
    ):
        self.set_property("currentAudioCompression", current_audio_compression.xa_elem)

    @property
    def current_movie_compression(self) -> "XAQuickTimeMovieCompressionPreset":
        """The current movie compression preset."""
        return self._new_element(
            self.xa_elem.currentMovieCompression(), XAQuickTimeMovieCompressionPreset
        )

    @current_movie_compression.setter
    def current_movie_compression(
        self, current_movie_compression: "XAQuickTimeMovieCompressionPreset"
    ):
        self.set_property("currentMovieCompression", current_movie_compression.xa_elem)

    @property
    def current_screen_compression(self) -> "XAQuickTimeScreenCompressionPreset":
        """The current screen compression preset."""
        return self._new_element(
            self.xa_elem.currentScreenCompression(), XAQuickTimeScreenCompressionPreset
        )

    @current_screen_compression.setter
    def current_screen_compression(
        self, current_screen_compression: "XAQuickTimeScreenCompressionPreset"
    ):
        self.set_property(
            "currentScreenCompression", current_screen_compression.xa_elem
        )

    def play(self) -> "XAQuickTimeDocument":
        self.xa_elem.play()
        return self

    def start(self) -> "XAQuickTimeDocument":
        self.xa_elem.start()
        return self

    def pause(self) -> "XAQuickTimeDocument":
        self.xa_elem.pause()
        return self

    def resume(self) -> "XAQuickTimeDocument":
        self.xa_elem.resume()
        return self

    def stop(self) -> "XAQuickTimeDocument":
        self.xa_elem.stop()
        return self

    def step_backward(self, num_steps: int) -> "XAQuickTimeDocument":
        self.xa_elem.stepBackwardBy_(num_steps)
        return self

    def step_forward(self, num_steps: int) -> "XAQuickTimeDocument":
        self.xa_elem.stepForwardBy_(num_steps)
        return self

    def trim(self, start_time: float, end_time: float) -> "XAQuickTimeDocument":
        self.xa_elem.trimFrom_to_(start_time, end_time)
        return self

    def present(self) -> "XAQuickTimeDocument":
        self.xa_elem.present()
        return self


class XAQuickTimeAudioRecordingDeviceList(XABase.XAList):
    """A wrapper around lists of audio recording devices that employs fast enumeration techniques.

    All properties of audio recording devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeAudioRecordingDevice, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ID") or [])


class XAQuickTimeAudioRecordingDevice(XABase.XAObject):
    """A class for managing and interacting with microphones in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the device."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the device."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the device."""
        return self.xa_elem.ID()


class XAQuickTimeVideoRecordingDeviceList(XABase.XAList):
    """A wrapper around lists of video recording devices that employs fast enumeration techniques.

    All properties of video recording devices can be called as methods on the wrapped list, returning a list containing each devices's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeVideoRecordingDevice, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ID") or [])


class XAQuickTimeVideoRecordingDevice(XABase.XAObject):
    """A class for managing and interacting with cameras in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the device."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the device."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the device."""
        return self.xa_elem.ID()


class XAQuickTimeAudioCompressionPresetList(XABase.XAList):
    """A wrapper around lists of audio compression presets that employs fast enumeration techniques.

    All properties of audio compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeAudioCompressionPreset, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ID") or [])


class XAQuickTimeAudioCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with audio compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the preset."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the preset."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the preset."""
        return self.xa_elem.ID()


class XAQuickTimeMovieCompressionPresetList(XABase.XAList):
    """A wrapper around lists of movie compression presets that employs fast enumeration techniques.

    All properties of movie compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeMovieCompressionPreset, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ID") or [])


class XAQuickTimeMovieCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with movie compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the preset."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the preset."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the preset."""
        return self.xa_elem.ID()


class XAQuickTimeScreenCompressionPresetList(XABase.XAList):
    """A wrapper around lists of screen compression presets that employs fast enumeration techniques.

    All properties of screen compression presets can be called as methods on the wrapped list, returning a list containing each presets's value for the property.

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAQuickTimeScreenCompressionPreset, filter)

    def properties(self) -> list[dict]:
        return list(self.xa_elem.arrayByApplyingSelector_("properties") or [])

    def name(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("name") or [])

    def id(self) -> list[str]:
        return list(self.xa_elem.arrayByApplyingSelector_("ID") or [])


class XAQuickTimeScreenCompressionPreset(XABase.XAObject):
    """A class for managing and interacting with screen compression presets in QuickTime.app.

    .. seealso:: :class:`XAQuickTimeApplication`

    .. versionadded:: 0.0.6
    """

    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the preset."""
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the preset."""
        return self.xa_elem.name()

    @property
    def id(self) -> str:
        """The unique identifier for the preset."""
        return self.xa_elem.ID()
