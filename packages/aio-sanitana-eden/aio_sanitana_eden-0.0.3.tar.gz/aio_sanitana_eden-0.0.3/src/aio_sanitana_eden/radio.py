"""Sanitana Eden radio controls."""
from .sanitana_eden import SanitanaEden


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
