from __future__ import annotations

import logging

import snap7
import voluptuous as vol
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_DEVICES, CONF_NAME, CONF_ADDRESS
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import (PLATFORM_SCHEMA, LightEntity)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_STATE_ADDRESS = "state_address"
CONF_BYTE = "byte"
CONF_BIT = "bit"

ADDRESS_SCHEMA = vol.Schema({
    vol.Required(CONF_BIT): int,
    vol.Required(CONF_BYTE): int
})

LIGHT_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_STATE_ADDRESS): ADDRESS_SCHEMA
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional("lib"): cv.string,
    vol.Optional(CONF_DEVICES): vol.All(
        cv.ensure_list, [LIGHT_SCHEMA]
    )
})

def setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    host = config[CONF_HOST]
    lib = config.get("lib", None)
    client = snap7.client.Client(lib)
    client.connect(host, 0, 1)

    if not client.get_connected():
        _LOGGER.error("Couldn't connect to simatic")
        return

    devices: list[dict] = config[CONF_DEVICES]

    lamps = []

    for device in devices:
        _LOGGER.error(f"Setting up {device}")
        name = device[CONF_NAME]
        state_byte = device[CONF_STATE_ADDRESS][CONF_BYTE]
        state_bit = device[CONF_STATE_ADDRESS][CONF_BIT]

        lamp = SimaticLight(client, name, (state_byte, state_bit))
        lamps.append(lamp)

    add_entities(lamps)


class SimaticLight(LightEntity):

    def __init__(self, client: snap7.client.Client, name: str, state_address: tuple[int, int]) -> None:
        self._client = client
        self._state_address = state_address
        self._name = name
        self._state = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        _LOGGER.debug(f"turn on lamp {self._name}")

    def turn_off(self, **kwargs: Any) -> None:
        _LOGGER.debug(f"turn off lamp {self._name}")


    def update(self) -> None:
        _LOGGER.error(f"Updating State for lamp {self._name}")
        byte, bit = self._state_address

        res = self._client.db_read(10, byte, 1)[0]
        res_bit = (res >> bit) & 1
        self._state = bool(res_bit)
