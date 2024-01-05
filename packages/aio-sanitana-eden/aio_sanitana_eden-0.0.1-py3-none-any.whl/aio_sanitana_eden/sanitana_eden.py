from asyncio import CancelledError, Future, StreamReader, StreamWriter, Task, TaskGroup, create_task, get_running_loop, isfuture, open_connection, sleep
from collections.abc import Callable
from typing import Any

from .const import LOGGER

class SanitanaEden:
    """Controls a Sanitana Eden steam shower."""

    _POLLING_INTERVAL: float = 1.0
    _RECONNECT_INTERVAL: float = 30.0

    _STATES = ("light", "radio", "bluetooth", "steam")

    def __init__(self, host: str, port: int) -> None:
        """Initialize a SanitanaEden object."""

        # Connection information
        self._host = host
        self._port = port

        # States
        self._available = False
        self._light: tuple[int, ...] = (0, 0, 0)
        self._radio: tuple[int, ...] = (0, 0)
        self._bluetooth: tuple[int, ...] = (0,)
        self._steam: tuple[int, ...] = (0, 0)

        # Callbacks
        self._subscribers: set[Callable] = set()

        # Internal
        self._task: Task | None = None
        self._reader: StreamReader | None = None
        self._writer: StreamWriter | None = None
        self._update: Future | None = None

    # Async functions to setup/shutdown
    async def async_setup(self) -> None:
        """Start async runner."""
        self._task = create_task(self._run())

    async def async_shutdown(self) -> None:
        """Shut down the SanitanaEden async infrastructure."""
        try:
            self._task.cancel()
            await self._task
        except CancelledError:
            pass

    async def async_update(self) -> None:
        """Poll for state from Sanitana Eden and await the next state update."""
        if not isfuture(self._update) or self._update.done():
            self._update = get_running_loop().create_future()

        await self._write(b"o")
        await self._update

    # Subscribe and unsubscribe functions
    def subscribe(self, cb: Callable) -> None:
        """Subscribe to state update notifications."""
        self._subscribers.add(cb)

    def unsubscribe(self, cb: Callable) -> None:
        """Unsubscribe from state update notifications."""
        self._subscribers.discard(cb)

    # Exposed property for availability
    @property
    def available(self) -> bool:
        """Available."""
        return bool(self._available)

    # Exposed properties for state
    @property
    def light_rgb_color(self) -> tuple[int, int, int]:
        """Light RGB color."""
        return self._light

    @property
    def radio_is_on(self) -> bool:
        """Radio on/off state."""
        return bool(self._radio[0])

    @property
    def radio_frequency(self) -> int:
        """Radio tuned frequency in units of 10kHz."""
        return self._radio[1]

    @property
    def radio_volume(self) -> int:
        """Radio volume (range 0-63."""
        return self._radio[2]

    @property
    def bluetooth_is_on(self) -> bool:
        """Bluetooth on/off state."""
        return bool(self._bluetooth[0])

    @property
    def steam_is_on(self) -> bool:
        """Steam generator on/off state."""
        return self._steam[0] != 0 or self._steam[1] != 0

    @property
    def steam_temperature(self) -> int:
        """Temperature for running steam program in degrees Celcius."""
        return self._steam[0]

    @property
    def steam_remaining(self) -> int:
        """Percentage of steam program still remaining, counting down from 1024."""
        return self._steam[1]

    def _setattr_if_changed(self, attr: str, value: Any) -> bool:
        if getattr(self, attr) == value:
            return False
        setattr(self, attr, value)
        return True

    # Service functions

    async def async_light_turn_on(self, rgb_color: tuple[int, int, int]) -> None:
        """Turn light on."""
        await self._write(b"m", *rgb_color)

    async def async_light_turn_off(self) -> None:
        """Turn light off."""
        await self._write(b"m", 0, 0, 0)

    async def async_radio_turn_on(self) -> None:
        """Turn radio on."""
        await self._write(b"j", 1, self._radio[1], self._radio[2])

    async def async_radio_turn_off(self) -> None:
        """Turn radio off."""
        await self._write(b"j", 0, self._radio[1], self._radio[2])

    async def async_radio_set_frequency(self, frequency: int) -> None:
        """Turn radio on."""
        await self._write(b"j", self._radio[0], frequency, self._radio[2])

    async def async_radio_set_volume(self, volume: float) -> None:
        """Turn radio on."""
        await self._write(b"j", self._radio[0], self._radio[1], volume)

    async def async_bluetooth_turn_on(self) -> None:
        """Turn bluetooth on."""
        await self._write(b"r", 1)

    async def async_bluetooth_turn_off(self) -> None:
        """Turn bluetooth off."""
        await self._write(b"r", 0)

    async def async_steam_turn_on(self, temperature: int, minutes: int) -> None:
        """Turn on steam generator."""
        await self._write(b"n", temperature, minutes)

    async def async_steam_turn_on_low(self) -> None:
        """Turn on steam generator - low setting."""
        await self._write(b"n", 35, 10)

    async def async_steam_turn_on_high(self) -> None:
        """Turn on steam generator - high setting."""
        await self._write(b"n", 50, 15)

    async def async_steam_turn_off(self):
        """Turn steam generator off."""
        await self._write(b"n", 0, 0)

    async def _run(self):
        while True:
            try:
                async with TaskGroup() as tg:
                    tg.create_task(self._run_data(tg))
            except ExceptionGroup as eg:
                LOGGER.exception(eg)
            except BaseExceptionGroup as beg:
                LOGGER.exception(beg)
            # Run again in 30 seconds
            dirty=self._setattr_if_changed("_available", False)
            if dirty:
                tg.create_task(self._run_subscribers())
            # Unblock async_update
            if isfuture(self._update) and not self._update.done():
                self._update.set_result(None)

            await sleep(self._RECONNECT_INTERVAL)

    async def _run_data(self, tg: TaskGroup) -> None:
        reader, self._writer = await open_connection(self._host, self._port)
        tg.create_task(self._poll())
        try:
            while True:
                b = await reader.readline()
                cmd, args = self._decode(b)
                if cmd is None:
                    continue
                if len(args) == 12:
                    dirty = False
                    for k, v in [
                        ("_available", True),
                        ("_radio", args[0:3]),
                        ("_bluetooth", args[3:4]),
                        ("_light", args[4:7]),
                        ("_steam", args[7:9]),
                    ]:
                        dirty = self._setattr_if_changed(k, v) or dirty
                    # Notify subscribers
                    if dirty:
                        tg.create_task(self._run_subscribers())
                    # Unblock async_update
                    if isfuture(self._update) and not self._update.done():
                        self._update.set_result(None)
        finally:
            self._writer.close()
            await self._writer.wait_closed()

    async def _run_subscribers(self):
        for fn in self._subscribers:
            fn()

    async def _poll(self) -> None:
        while True:
            await self._write(b"o")
            if self._POLLING_INTERVAL <= 0:
                break
            await sleep(self._POLLING_INTERVAL)

    def _encode(self, cmd: bytes, *args: int) -> bytes:
        result = (
            b"@11:22:33:44:55:6600:00:00:00:00:00"
            + cmd
            + (b" " if args else b"")
            + (" ".join(str(a) for a in args)).encode("ascii")
            + b"*&\n"
        )
        LOGGER.debug("=> %s", result)
        return result

    async def _write(self, cmd: bytes, *args: int) -> None:
        self._writer.write(self._encode(cmd, *args))

    def _decode(self, data: bytes) -> tuple[bytes | None, list[int | str] | None]:
        LOGGER.debug("<= %s", data)
        if data[0:1] != b"@" or data[-3:] != b"*&\n":
            return (None, None)
        cmd = data[35:36]
        data = data[36:-3].decode()
        if cmd in [b"A"]:
            args = [a for a in data.split("#") if a]
        else:
            args = [int(a) for a in data.split(" ") if a]
        return (cmd, args)
