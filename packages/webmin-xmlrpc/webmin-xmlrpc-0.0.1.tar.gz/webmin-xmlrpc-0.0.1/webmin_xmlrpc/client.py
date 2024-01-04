"""The client for Webmin XML-RPC."""
from typing import Any

from aiohttp import ClientSession

from .xmlrpc import XMLRPCClient


class WebminInstance:
    """Represent a Webmin instance."""

    data: dict[str, Any]

    def __init__(self, session: ClientSession):
        """Initialize the WebMin instance."""
        self._client = XMLRPCClient(session)

    async def get_cpu_info(self) -> dict[str, Any]:
        """Retrieve the CPU load."""
        result = await self._client.call("proc.get_cpu_info")
        return {"load_1m": result[0], "load_5m": result[1], "load_15m": result[2]}

    async def get_memory_info(self) -> dict[str, Any]:
        """Retrieve memory info."""
        result = await self._client.call("proc.get_memory_info")
        return {
            "mem_total": result[0],
            "mem_free": result[1],
            "swap_total": result[2],
            "swap_free": result[3],
        }

    async def get_network_interfaces(self) -> dict[str, Any]:
        """Retrieve active network interfaces."""
        result = await self._client.call("net.active_interfaces")
        return {"active_interfaces": result}

    async def get_system_uptime(self) -> dict[str, Any]:
        """Retrieve uptime."""
        result = await self._client.call("proc.get_system_uptime")
        return {
            "uptime": {"days": result[0], "minutes": result[1], "seconds": result[2]}
        }

    async def local_disk_space(self) -> dict[str, Any]:
        """Retrieve local disk space."""
        result = await self._client.call("mount.local_disk_space")
        return {
            "total_space": result[0],
            "free_space": result[1],
            "fs": result[2],
            "used_space": result[3],
        }

    async def update(self) -> dict[str, Any]:
        """Retrieve the current data."""
        self.data = (
            (await self.get_cpu_info())
            | (await self.get_memory_info())
            | (await self.local_disk_space())
            | (await self.get_system_uptime())
            | (await self.get_network_interfaces())
        )
        return self.data
