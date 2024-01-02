import json
import logging
from typing import Any, Tuple

import websockets
from websockets import ConnectionClosedError, WebSocketException

from .auth import Auth
from .const import HEATZY_APPLICATION_ID, HEATZY_PARAMS, HEATZY_WEBSOCKET
from .exception import WebSocketFailed

_LOGGER = logging.getLogger(__name__)
RETRY = 3


class WebSocket:
    """Websocket."""

    def __init__(self, username: str, password: str, auth_obj: Auth) -> None:
        self._ws: WebSocket | None = None
        self._access_token: Tuple[str, str] | None = None
        self._username = username
        self._password = password
        self._auth = auth_obj
        self._retry = RETRY
        self.ws_connected = False

    async def async_connect(self) -> None:
        """Websocket connection."""
        if self.ws_connected is False:
            try:
                bindings = await self._auth.request("bindings")
                params = bindings.get("devices", HEATZY_PARAMS)
                _LOGGER.debug(
                    "Websocket connect: %s %s", params[0]["host"], params[0]["ws_port"]
                )
                websocket = await websockets.connect(
                    HEATZY_WEBSOCKET.format(params[0]["host"], params[0]["ws_port"])
                )
                self._ws = websocket
                await self.async_login()
                self.ws_connected = True
                self._retry = RETRY
            except WebSocketException as error:
                raise WebSocketFailed(
                    "Error occurred while connect to Heatzy websocket."
                ) from error

    async def async_login(self):
        """Subscribe."""
        access_token = await self._auth.async_get_token()
        data = {
            "cmd": "login_req",
            "data": {
                "appid": HEATZY_APPLICATION_ID,
                "uid": access_token.get("uid"),
                "token": access_token.get("token"),
                "p0_type": "attrs_v4",
                "heartbeat_interval": 180,
                "auto_subscribe": True,
            },
        }
        _LOGGER.debug("Websocket login: %s", access_token.get("token"))
        await self._ws.send(json.dumps(data))
        rcv = await self._ws.recv()
        response = json.loads(rcv).get("data", {})
        _LOGGER.debug("Websocket login recv: %s", rcv)
        if response.get("error_code") or response.get("success") is not True:
            raise WebSocketFailed(
                f"Websocket login failed: {response.get('msg', response)}"
            )

    async def async_send(self, cmd: dict[str, Any]) -> dict[str, Any]:
        try:
            await self.async_connect()
            _LOGGER.debug("Websocket send: %s", cmd)
            await self._ws.send(json.dumps(cmd))
            rcv = await self._ws.recv()
            _LOGGER.debug("Websocket send recv: %s", rcv)
            response = json.loads(rcv).get("data", {})
            if response.get("error_code"):
                self.ws_connected = False
                if self._retry > 0:
                    self._retry -= 1
                    _LOGGER.debug("Websocket send retry")
                    return await self.async_send(cmd)
                raise WebSocketFailed(
                    f"Websocket send failed: {cmd} {response.get('msg', response)}"
                )
            return response
        except ConnectionClosedError:
            _LOGGER.debug("Websocket connection close")
            await self.async_close()
            self.ws_connected = False
            if self._retry > 0:
                self._retry -= 1
                _LOGGER.debug("Websocket connection close retry")
                return await self.async_send(cmd)
            raise WebSocketFailed("Websocket closed")

    async def async_close(self) -> None:
        """Close session."""
        await self._ws.close()
