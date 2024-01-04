"""Definition of the audio service backends base classes.

These classes can be used to create an Audioservice plugin extending
OpenVoiceOS's media playback options.
"""
from abc import ABCMeta, abstractmethod

from ovos_utils import classproperty
from ovos_utils.fakebus import FakeBus
from ovos_utils.process_utils import RuntimeRequirements


class AudioBackend(metaclass=ABCMeta):
    """Base class for all audio backend implementations.

    Arguments:
        config (dict): configuration dict for the instance
        bus (MessageBusClient): OpenVoiceOS messagebus emitter
    """

    def __init__(self, config=None, bus=None):
        self._track_start_callback = None
        self.supports_mime_hints = False
        self.config = config or {}
        self.bus = bus or FakeBus()

    @classproperty
    def runtime_requirements(self):
        """ skill developers should override this if they do not require connectivity
         some examples:
         IOT plugin that controls devices via LAN could return:
            scans_on_init = True
            RuntimeRequirements(internet_before_load=False,
                                 network_before_load=scans_on_init,
                                 requires_internet=False,
                                 requires_network=True,
                                 no_internet_fallback=True,
                                 no_network_fallback=False)
         online search plugin with a local cache:
            has_cache = False
            RuntimeRequirements(internet_before_load=not has_cache,
                                 network_before_load=not has_cache,
                                 requires_internet=True,
                                 requires_network=True,
                                 no_internet_fallback=True,
                                 no_network_fallback=True)
         a fully offline plugin:
            RuntimeRequirements(internet_before_load=False,
                                 network_before_load=False,
                                 requires_internet=False,
                                 requires_network=False,
                                 no_internet_fallback=True,
                                 no_network_fallback=True)
        """
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=False,
                                   requires_internet=False,
                                   requires_network=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True)

    @property
    def playback_time(self):
        return 0

    @abstractmethod
    def supported_uris(self):
        """List of supported uri types.

        Returns:
            list: Supported uri's
        """

    @abstractmethod
    def clear_list(self):
        """Clear playlist."""

    @abstractmethod
    def add_list(self, tracks):
        """Add tracks to backend's playlist.

        Arguments:
            tracks (list): list of tracks.
        """

    @abstractmethod
    def play(self, repeat=False):
        """Start playback.

        Starts playing the first track in the playlist and will contiune
        until all tracks have been played.

        Arguments:
            repeat (bool): Repeat playlist, defaults to False
        """

    @abstractmethod
    def stop(self):
        """Stop playback.

        Stops the current playback.

        Returns:
            bool: True if playback was stopped, otherwise False
        """

    def set_track_start_callback(self, callback_func):
        """Register callback on track start.

        This method should be called as each track in a playlist is started.
        """
        self._track_start_callback = callback_func

    def pause(self):
        """Pause playback.

        Stops playback but may be resumed at the exact position the pause
        occured.
        """

    def resume(self):
        """Resume paused playback.

        Resumes playback after being paused.
        """

    def next(self):
        """Skip to next track in playlist."""

    def previous(self):
        """Skip to previous track in playlist."""

    def lower_volume(self):
        """Lower volume.

        This method is used to implement audio ducking. It will be called when
        OpenVoiceOS is listening or speaking to make sure the media playing isn't
        interfering.
        """

    def restore_volume(self):
        """Restore normal volume.

        Called when to restore the playback volume to previous level after
        OpenVoiceOS has lowered it using lower_volume().
        """

    def get_track_length(self):
        """
        getting the duration of the audio in milliseconds
        NOTE: not yet supported by mycroft-core
        """

    def get_track_position(self):
        """
        get current position in milliseconds
        NOTE: not yet supported by mycroft-core
        """

    def set_track_position(self, milliseconds):
        """
        go to position in milliseconds
        NOTE: not yet supported by mycroft-core
          Args:
                milliseconds (int): number of milliseconds of final position
        """

    def seek_forward(self, seconds=1):
        """Skip X seconds.

        Arguments:
            seconds (int): number of seconds to seek, if negative rewind
        """

    def seek_backward(self, seconds=1):
        """Rewind X seconds.

        Arguments:
            seconds (int): number of seconds to seek, if negative jump forward.
        """

    def track_info(self):
        """Get info about current playing track.

        Returns:
            dict: Track info containing atleast the keys artist and album.
        """
        ret = {}
        ret['artist'] = ''
        ret['album'] = ''
        return ret

    def shutdown(self):
        """Perform clean shutdown.

        Implements any audio backend specific shutdown procedures.
        """
        self.stop()


class RemoteAudioBackend(AudioBackend):
    """Base class for remote audio backends.

    RemoteAudioBackends will always be checked after the normal
    AudioBackends to make playback start locally by default.

    An example of a RemoteAudioBackend would be things like Chromecasts,
    mopidy servers, etc.
    """
