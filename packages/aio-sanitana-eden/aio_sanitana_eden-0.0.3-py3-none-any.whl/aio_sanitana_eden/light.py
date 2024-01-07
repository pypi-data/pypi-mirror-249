"""Sanitana Eden light controls."""
from typing import Any
from .sanitana_eden import SanitanaEden


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
