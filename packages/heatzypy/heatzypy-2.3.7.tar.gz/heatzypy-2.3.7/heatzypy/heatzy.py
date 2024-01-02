"""Heatzy API."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientSession  # pylint: disable=import-error

from .auth import Auth
from .websocket import WebSocket

_LOGGER = logging.getLogger(__name__)


class HeatzyClient:
    """Heatzy Client data."""

    def __init__(
        self,
        username: str,
        password: str,
        session: ClientSession | None = None,
        time_out: int = 120,
    ) -> None:
        """Load parameters."""
        self._auth = Auth(session, username, password, time_out)
        self._ws = WebSocket(username, password, self._auth)
        self.request = self._auth.request
        self.ws_send = self._ws.async_send

    async def async_bindings(self) -> dict[str, dict[str, Any]]:
        """Fetch all configured devices."""
        return await self.request("bindings")

    async def async_get_devices(self) -> dict[str, Any]:
        """Fetch all configured devices."""
        response = await self.async_bindings()
        devices = response.get("devices", {})
        devices_with_datas = [
            await self._async_merge_with_device_data(device)  # type: ignore
            for device in devices
        ]
        dict_devices_with_datas = {
            device["did"]: device for device in devices_with_datas
        }
        return dict_devices_with_datas

    async def async_get_device(self, device_id: str) -> dict[str, Any]:
        """Fetch device with given id."""
        device = await self.request(f"devices/{device_id}")
        return await self._async_merge_with_device_data(device)

    async def _async_merge_with_device_data(
        self, device: dict[str, Any]
    ) -> dict[str, Any]:
        """Fetch detailed data for device and merge it with the device information."""
        device_data = await self.async_get_device_data(device["did"])
        if device_data.get("attrs"):  # Websocket return attrs instead of attr
            device_data["attr"] = device_data.pop("attrs")
        return {**device, **device_data}

    async def async_get_device_data(self, device_id: str) -> dict[str, Any]:
        """Fetch detailed data for device with given id."""
        return await self.ws_send({"cmd": "c2s_read", "data": {"did": f"{device_id}"}})
        # Fix github.com/cyr-ius/hass-heatzy/issues/50
        # return await self.request(f"devdata/{device_id}/latest")

    async def async_control_device(
        self, device_id: str, payload: dict[str, Any]
    ) -> None:
        """Control state of device with given id."""
        await self.request(f"control/{device_id}", method="POST", json=payload)

    async def async_close(self) -> None:
        """Close session."""
        await self._auth.async_close()
        await self._ws.async_close()
