"""Sanitana Eden bluetooth controls."""
from .sanitana_eden import SanitanaEden


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
