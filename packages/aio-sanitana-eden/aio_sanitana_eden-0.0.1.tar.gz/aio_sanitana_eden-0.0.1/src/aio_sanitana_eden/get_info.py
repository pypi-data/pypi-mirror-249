
from asyncio import TaskGroup, get_running_loop, timeout
from .exceptions import DeviceConnectionError
from .protocols import _QueuedDatagramProtocol

async def async_get_info(host: str) -> None:
    """Retrieve information on a Sanitana Eden through its UDP socket."""

    result = {}
    loop = get_running_loop()
    disconnect = loop.create_future()

    def _parse(data: bytes, _) -> list[str]:
        """Parse AT+ response from USR-WIFI232-G2 used in Sanitana Eden."""
        str_data = data.decode().rstrip("\n\r")
        if str_data.startswith("+ERR="):
            return None
        if str_data.startswith("+ok="):
            str_data = str_data[4:]
        return str_data.split(",")

    async with TaskGroup() as tg:
        try:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: _QueuedDatagramProtocol(tg, disconnect),
                remote_addr=(host, 48899),
            )
        except Exception as e:
            raise DeviceConnectionError from e

        try:
            async with timeout(3):
                if data := _parse(*await protocol.send_receive(b"HF-A11ASSISTHREAD")):
                    result["mac_used"] = data[1]
                    result["model"] = data[2]
                try:
                    async with timeout(0.1):
                        await protocol.send(b"+ok")
                        await protocol.receive()
                except TimeoutError:
                    pass
                if data := _parse(*await protocol.send_receive(b"AT+NETP\r")):
                    result["protocol"] = data[0]
                    result["mode"] = data[1]
                    result["port"] = int(data[2])
                if data := _parse(*await protocol.send_receive(b"AT+WAMAC\r")):
                    result["mac_ap"] = data[0]
                if data := _parse(*await protocol.send_receive(b"AT+WSMAC\r")):
                    result["mac_sta"] = data[0]
                return result
        except Exception as e:
            raise DeviceConnectionError from e
        finally:
            transport.close()
            await disconnect

