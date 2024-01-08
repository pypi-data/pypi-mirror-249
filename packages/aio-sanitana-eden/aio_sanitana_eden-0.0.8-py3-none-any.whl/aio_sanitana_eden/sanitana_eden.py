"""Sanitana Eden API client."""
import asyncio
from collections.abc import Callable
from typing import Any

from .const import LOGGER, MAC, MAC0

CALLBACK_TYPE = Callable[[], None]


class SanitanaEden:
    """Controls a Sanitana Eden steam shower."""

    _POLLING_INTERVAL: float = 1.0
    _RECONNECT_INTERVAL: float = 30.0

    # State
    _available: bool = False
    _state: tuple[int, ...] = tuple(0 for _ in range(12))

    # Internal
    _task: asyncio.Task[None]
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    # Callbacks
    _listeners: dict[CALLBACK_TYPE, tuple[CALLBACK_TYPE, object | None]] = {}

    def __init__(self, host: str, port: int) -> None:
        """Initialize a SanitanaEden object."""

        # Connection information
        self._host = host
        self._port = port

        # States
        self.radio = SanitanaEdenRadio(self)
        self.bluetooth = SanitanaEdenBluetooth(self)
        self.light = SanitanaEdenLight(self)
        self.steam = SanitanaEdenSteam(self)

    # Async functions to setup/shutdown
    async def async_setup(self) -> None:
        """Start async runner."""
        self._task = asyncio.create_task(self._run())

    async def async_shutdown(self) -> None:
        """Shut down the SanitanaEden async infrastructure."""
        try:
            self._task.cancel()
            await self._task
        except asyncio.CancelledError:
            pass

    async def async_update(self) -> None:
        """Poll for state from Sanitana Eden."""
        await self._write(b"o")

    def async_add_listener(
        self, update_callback: CALLBACK_TYPE, context: Any = None
    ) -> CALLBACK_TYPE:
        """Listen for data updates."""

        def remove_listener() -> None:
            """Remove update listener."""
            self._listeners.pop(remove_listener)

        self._listeners[remove_listener] = (update_callback, context)
        return remove_listener

    async def _update_listeners(self) -> None:
        for update_callback, _ in list(self._listeners.values()):
            update_callback()

    # Exposed property for availability
    @property
    def available(self) -> bool:
        """Available."""
        return self._available

    def _setattr_if_changed(self, attr: str, value: Any) -> bool:
        if getattr(self, attr) == value:
            return False
        setattr(self, attr, value)
        return True

    async def _run(self):
        while True:
            try:
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self._run_data(tg))
            except ExceptionGroup as eg:
                LOGGER.exception(eg)
            except BaseExceptionGroup as beg:
                LOGGER.exception(beg)
            # Run again in 30 seconds
            dirty = self._setattr_if_changed("_available", False)
            if dirty:
                await self._update_listeners()
            await asyncio.sleep(self._RECONNECT_INTERVAL)

    async def _run_data(self, tg: asyncio.TaskGroup) -> None:
        reader, self._writer = await asyncio.open_connection(self._host, self._port)
        tg.create_task(self._poll())
        try:
            while True:
                b = await reader.readline()
                cmd, args = self._decode(b)
                if cmd is None:
                    continue
                if len(args) == 12:
                    dirty = self._setattr_if_changed("_available", True)
                    dirty = self._setattr_if_changed("_state", args) or dirty
                    # Notify subscribers
                    if dirty:
                        tg.create_task(self._update_listeners())
        finally:
            self._writer.close()
            await self._writer.wait_closed()

    async def _poll(self) -> None:
        while True:
            await self._write(b"o")
            if self._POLLING_INTERVAL <= 0:
                break
            await asyncio.sleep(self._POLLING_INTERVAL)

    def _encode(self, cmd: bytes, *args: int) -> bytes:
        result = b"".join(
            (
                b"@",
                MAC,
                MAC0,
                cmd,
                b" " if args else b"",
                b" ".join(str(a).encode("ascii") for a in args),
                b"*&\n",
            )
        )
        LOGGER.debug("=> %s", result)
        return result

    async def _write(self, cmd: bytes, *args: int) -> None:
        self._writer.write(self._encode(cmd, *args))

    def _decode(self, data: bytes) -> tuple[bytes | None, list[int] | list[str]]:
        LOGGER.debug("<= %s", data)
        if data[0:1] != b"@" or data[-3:] != b"*&\n":
            return (None, [])
        cmd = data[35:36]
        data2 = data[36:-3].decode()
        if cmd in [b"A"]:
            args = [a for a in data2.split("#") if a]
        else:
            args = [int(a) for a in data2.split(" ") if a]
        return (cmd, args)


class SanitanaEdenRadio:
    """Represent the radio functions of a Sanitana Eden."""

    def __init__(self, se: SanitanaEden):
        """Initialize."""
        self._se = se

    @property
    def _radio(self) -> tuple[int, ...]:
        return self._se._state[0:3]

    @property
    def is_on(self) -> bool:
        """Return True if the radio is on."""
        return bool(self._radio[0])

    @property
    def frequency(self) -> float:
        """Return the frequency in MHz the radio is tuned to (range 87.5-108, step 0.01)."""
        return float(self._radio[1]) / 100.0

    @property
    def volume(self) -> float:
        """Return the volume of the radio (range 0-63, step 1)."""
        return float(self._radio[2])

    async def async_turn_on(self, **_) -> None:
        """Turn radio on."""
        await self._se._write(b"j", 1, self._radio[1], self._radio[2])

    async def async_turn_off(self, **_) -> None:
        """Turn radio off."""
        await self._se._write(b"j", 0, self._radio[1], self._radio[2])

    async def async_set_frequency(self, frequency: float) -> None:
        """Set the frequency the radio is tuned to."""
        await self._se._write(
            b"j", self._radio[0], int(frequency * 100.0), self._radio[2]
        )

    async def async_set_volume(self, volume: float) -> None:
        """Set the radio volume."""
        await self._se._write(b"j", self._radio[0], self._radio[1], int(volume))


class SanitanaEdenBluetooth:
    """Represent the bluetooth functions of a Sanitana Eden."""

    def __init__(self, se: SanitanaEden):
        """Initialize."""
        self._se = se

    @property
    def _bluetooth(self) -> tuple[int, ...]:
        return self._se._state[3:4]

    @property
    def is_on(self) -> bool:
        """Return True if the entity is on."""
        return bool(self._bluetooth[0])

    async def async_turn_on(self, **_) -> None:
        """Turn bluetooth on."""
        await self._se._write(b"r", 1)

    async def async_turn_off(self, **_) -> None:
        """Turn bluetooth off."""
        await self._se._write(b"r", 0)


class SanitanaEdenLight:
    """Represent the light functions on a Sanitana Eden."""

    def __init__(self, se: SanitanaEden):
        """Initialize a SantanaEdenLight."""
        self._se = se

    @property
    def _light(self) -> tuple[int, ...]:
        return self._se._state[4:7]

    @property
    def brightness(self) -> int:
        """Return the brightness of the light (0..255)."""
        return max(self._light)

    @property
    def is_on(self) -> bool:
        """Return True if the light is on."""
        return self.brightness != 0

    @property
    def rgb_color(self) -> tuple[int, ...]:
        """Return the RGB color of the light as a tuple[int,int,int]."""
        brightness = self.brightness
        if brightness == 0:
            return (255, 255, 255)

        return tuple(int(x * 255 / brightness) for x in self._light)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn light on."""
        rgb_color: tuple[int, ...] = kwargs.get("rgb_color") or self.rgb_color
        brightness: int = kwargs.get("brightness") or self.brightness or 255
        rgb_color = tuple(int(x * brightness / 255) for x in rgb_color)
        await self._se._write(b"m", *rgb_color)

    async def async_turn_off(self, **_) -> None:
        """Turn light off."""
        await self._se._write(b"m", 0, 0, 0)


class SanitanaEdenSteam:
    """Represent the steam functions of a Sanitana Eden."""

    def __init__(self, se: SanitanaEden):
        """Initialize."""
        self._se = se

    @property
    def _steam(self) -> tuple[int, ...]:
        return self._se._state[4:7]

    @property
    def is_on(self) -> bool:
        """Return True if the steam generator is on."""
        return self._steam[0] != 0 or self._steam[1] != 0

    @property
    def temperature(self) -> float:
        """Return the temperature in degrees Celcius of the steam program."""
        return float(self._steam[0])

    @property
    def remaining(self) -> int:
        """Percentage of steam program still remaining, counting down from 1024."""
        return self._steam[1]

    async def async_turn_on(self, temperature: int, minutes: int) -> None:
        """Turn on steam generator."""
        await self._se._write(b"n", temperature, minutes)

    async def async_turn_off(self):
        """Turn steam generator off."""
        await self._se._write(b"n", 0, 0)
