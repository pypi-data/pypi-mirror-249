"""Sanitana Eden API client."""
import asyncio
from collections.abc import Callable
from typing import Any

from .bluetooth import SanitanaEdenBluetooth
from .const import LOGGER, MAC, MAC0
from .light import SanitanaEdenLight
from .radio import SanitanaEdenRadio
from .steam import SanitanaEdenSteam

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
    _update: asyncio.Future[bool]

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
        """Poll for state from Sanitana Eden and await the next state update."""
        if not asyncio.isfuture(self._update) or self._update.done():
            self._update = asyncio.get_running_loop().create_future()

        await self._write(b"o")
        await self._update

    def async_add_listener(
        self, update_callback: CALLBACK_TYPE, context: Any = None
    ) -> CALLBACK_TYPE:
        """Listen for data updates."""

        def remove_listener() -> None:
            """Remove update listener."""
            self._listeners.pop(remove_listener)

        self._listeners[remove_listener] = (update_callback, context)
        return remove_listener

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
            # Unblock async_update
            if asyncio.isfuture(self._update) and not self._update.done():
                self._update.set_result(None)

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
                    # Unblock async_update
                    if asyncio.isfuture(self._update) and not self._update.done():
                        self._update.set_result(None)
        finally:
            self._writer.close()
            await self._writer.wait_closed()

    async def _update_listeners(self) -> None:
        for update_callback, _ in list(self._listeners.values()):
            update_callback()

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
