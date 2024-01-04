from __future__ import annotations

from hikari import Snowflake, GatewayBot, UndefinedOr, UNDEFINED, VoiceEvent
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from .errors import (
    SessionNotStartedException,
    PlayerQueueException,
    PlayerSettingException,
    PlayerException,
)
from .abc.track import Track
from .abc.events import TrackEndEvent, PlayerQueueEmptyEvent
from .abc.player import PlayerVoice

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")


class Player(VoiceConnection):
    @classmethod
    async def initialize(  # type: ignore
        cls,
        channel_id: Snowflake,
        endpoint: str,
        guild_id: Snowflake,
        on_close: t.Any,  # type: ignore TODO: This needs to be fixed, or I need to make my own player.
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: Snowflake,
        *,
        bot: GatewayBot,
        ongaku: Ongaku,
    ):
        """
        Initialise the player.

        Initialise the player so that the player can be changed.
        """

        init_player = Player(
            bot=bot,
            ongaku=ongaku,
            channel_id=channel_id,
            endpoint=endpoint,
            guild_id=guild_id,
            on_close=on_close,
            owner=owner,
            session_id=session_id,
            shard_id=shard_id,
            token=token,
            user_id=user_id,
        )

        return init_player

    def __init__(
        self,
        *,
        bot: GatewayBot,
        ongaku: Ongaku,
        channel_id: Snowflake,
        endpoint: str,
        guild_id: Snowflake,
        on_close: t.Awaitable[None],  # type: ignore TODO: This needs to be fixed, or I need to make my own player.
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: Snowflake,
    ) -> None:
        """
        Base player class

        The class that allows the player, to play songs, and more.
        """
        self._bot = bot
        self._ongaku = ongaku
        self._channel_id = channel_id
        self._endpoint = endpoint
        self._guild_id = guild_id
        self._on_close = on_close
        self._owner = owner
        self._session_id = session_id
        self._shard_id = shard_id
        self._token = token
        self._user_id = user_id

        self._is_paused = True
        self._connected = False

        self._queue: list[Track] = []

        bot.subscribe(TrackEndEvent, self._track_end_event)

    @property
    def channel_id(self) -> Snowflake:
        """
        ID of the voice channel this voice connection is currently in.
        """
        return self._channel_id

    @property
    def guild_id(self) -> Snowflake:
        """
        ID of the guild this voice connection is in.
        """
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """
        Whether the current connection is alive.
        """
        return self._is_alive

    @property
    def shard_id(self) -> int:
        """
        ID of the shard that requested the connection.
        """
        return self._shard_id

    @property
    def owner(self) -> VoiceComponent:
        """
        Return the component that is managing this connection.
        """
        return self._owner

    @property
    def is_paused(self) -> bool:
        """
        Returns whether the bot is currently paused.
        """
        return self._is_paused

    @property
    def queue(self) -> tuple[Track, ...]:
        """
        Returns a queue, of the current tracks that are waiting to be played. The top one is the currently playing one.
        """
        return tuple(self._queue)

    @property
    def connected(self) -> bool:
        return self._connected

    async def _connect(self) -> None:
        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()
        
        voice = PlayerVoice(
            self._token, self._endpoint[6:], self._session_id
        )
        
        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            voice=voice,
            no_replace=False,
        )

        self._connected = True

    async def play(self, track: t.Optional[Track] = None) -> None:
        """
        Play a track

        Allows for the user to play a track.
        The current track will be stopped, and this will replace it.

        Parameters
        ----------
        track: t.Optional[abc.Track]
            the track you wish to play. If empty, it will pull from the queue.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.
        PlayerQueueException
            The queue is empty and no track was given, so it cannot play songs.
        """

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if len(self.queue) > 0 and track == None:
            raise PlayerQueueException("Empty Queue. Cannot play nothing.")

        if track != None:
            self._queue.insert(0, track)

        if self._connected == False:
            await self._connect()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=self.queue[0],
            no_replace=False,
        )

        self._is_paused = False

    async def pause(self, value: UndefinedOr[bool] = UNDEFINED) -> None:
        """
        Pause the current track

        Allows for the user to pause the currently playing track.

        Parameters
        ----------
        value : hikari.UndefinedOr[bool]
            How you wish to pause the bot.

        !!! INFO
            `True` will force pause the bot, `False` will force unpause the bot, and `undefined` will toggle.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.

        """
        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if value == UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku.internal.session_id, paused=self.is_paused
        )

    async def add(self, tracks: t.Sequence[Track]) -> None:
        """
        Add tracks

        Add tracks to the queue. This will not automatically start playing the songs.

        Parameters
        ----------
        tracks : list[abc.Track]
            The list of tracks you wish to add to the queue.
        """
        self._queue.extend(tracks)

    async def remove(self, value: Track | int) -> None:
        """
        Remove track.

        Removes the track, or the track in that position.

        Parameters
        ----------
        value : abc.Track | int
            Remove a selected track. If `abc.Track`, then it will remove the first occurrence of that track. If `int`, it will remove the track at that number (starts at 0).

        Raises
        ------
        PlayerSettingException
            The queue is empty.
        SessionNotStartedException
            No session id provided, or the session id is null.
        """
        if len(self.queue) == 0:
            raise PlayerSettingException("Queue is empty.")

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if isinstance(value, Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except Exception as e:
            raise PlayerException(f"Failed to remove a song: {e}")

        if index == 0:
            if len(self.queue) == 0:
                await self._ongaku.rest.internal.player.update_player(
                    self.guild_id, self._ongaku.internal.session_id, track=None
                )
            else:
                await self.play()

    async def skip(self, amount: int = 1) -> None:
        """
        skip songs

        skip a selected amount of songs.

        Parameters
        ----------
        amount : int
            The amount of songs you wish to skip.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.
        PlayerSettingException
            The amount was 0 or a negative number.
        PlayerQueueException
            The queue is already empty, so no songs can be skipped.
        """
        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if amount <= 0:
            raise PlayerSettingException(
                f"Skip amount cannot be 0 or negative. Value: {amount}"
            )
        if len(self.queue) == 0:
            raise PlayerQueueException("No tracks in queue.")

        for _ in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) == 0:
            await self._ongaku.rest.internal.player.update_player(
                self.guild_id,
                self._ongaku.internal.session_id,
                track=None,
            )
            return

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=self._queue[0],
            no_replace=False,
        )

    async def volume(self, volume: int) -> None:
        """
        change the volume

        The volume you wish to set for the bot.

        Parameters
        ----------
        volume : int
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        SessionNotStartedException
            The session has not been yet started.
        PlayerSettingException
            Raised if the value is above, or below 0, or 1000.
        """

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if volume < 0:
            raise PlayerSettingException(
                f"Volume cannot be below zero. Volume: {volume}"
            )
        if volume > 1000:
            raise PlayerSettingException(
                f"Volume cannot be above 1000. Volume: {volume}"
            )

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            volume=volume,
            no_replace=False,
        )

    async def clear(self) -> None:
        """
        Clear the queue

        Clear the current queue, and also stop the audio from the bot.

        Raises
        ------
        SessionNotStarted
            The session is not yet started.
        """
        self._queue.clear()

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=None,
            no_replace=False,
        )

    async def position(self, value: int) -> None:
        """
        Change the track position

        Change the current track position

        Parameters
        ----------
        value : int
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionNotStartedException
            The session is not yet started.
        PlayerSettingException
            When the track position selected is not a valid position.
        PlayerSettingException
            The queue is empty.
        """
        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if self.queue[0].info.length < value:
            raise PlayerSettingException(
                "Length is longer than currently playing song!"
            )

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku.internal.session_id, position=value
        )

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        print("Player disconnecting...")
        self._is_alive = False
        self._connected = False
        await self.clear()

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        await self._ongaku.rest.internal.player.delete_player(
            self._ongaku.internal.session_id, self._guild_id
        )

        if self._bot.cache.get_voice_state(self.guild_id, self._bot.get_me().id) != None: #type: ignore
            await self._bot.voice.disconnect(self.guild_id)

        

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""
        print("Player connecting...")
        voice = PlayerVoice(
            self._token, self._endpoint[6:], self._session_id
        )

        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=self.queue[0],
            voice=voice,
            no_replace=False,
        )
        await self._bot.update_voice_state(self.guild_id, self.channel_id)

    async def notify(self, event: VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""
        print("notifying?")

    async def _track_end_event(self, event: TrackEndEvent):
        if self._ongaku.internal.session_id == None:
            raise SessionNotStartedException()

        if int(event.guild_id) == int(self.guild_id):
            try:
                await self.remove(0)
            except:
                await self._bot.dispatch(
                    PlayerQueueEmptyEvent(self._bot, self.guild_id)
                )
                return

            if len(self.queue) == 0:
                await self._bot.dispatch(
                    PlayerQueueEmptyEvent(self._bot, self.guild_id)
                )
                return

            await self._ongaku.rest.internal.player.update_player(
                self.guild_id,
                self._ongaku.internal.session_id,
                track=self._queue[0],
                no_replace=False,
            )
