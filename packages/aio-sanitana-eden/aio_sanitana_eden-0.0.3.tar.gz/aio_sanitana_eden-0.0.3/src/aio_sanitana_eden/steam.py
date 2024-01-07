"""Sanitana Eden steam functions."""
from .sanitana_eden import SanitanaEden


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
