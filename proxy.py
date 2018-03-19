"""
This platform allows switch-like entities to be displayed as lights.

For more details about this platform, please refer to the documentation at
TBD
"""
import logging

import voluptuous as vol

from homeassistant.core import State, callback
import homeassistant.core as ha
from homeassistant.components import light
from homeassistant.const import (
    STATE_ON, ATTR_ENTITY_ID, CONF_NAME, STATE_UNAVAILABLE, CONF_ENTITY_ID,
    SERVICE_TURN_ON, SERVICE_TURN_OFF)
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.typing import HomeAssistantType, ConfigType
from homeassistant.components.light import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Light Proxy'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ENTITY_ID): cv.entity_id
})


async def async_setup_platform(hass: HomeAssistantType, config: ConfigType,
                               async_add_devices, discovery_info=None) -> None:
    """Initialize light.proxy platform."""
    async_add_devices([LightProxy(config[CONF_NAME],
                                  config[CONF_ENTITY_ID])])


class LightProxy(light.Light):
    """Representation of a light proxy."""

    def __init__(self, name: str, entity: str) -> None:
        """Initialize a light proxy."""
        self._name = name  # type: str
        self._entity = entity  # type: str
        self._is_on = False  # type: bool
        self._available = False  # type: bool
        self._async_unsub_state_changed = None

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        @callback
        def async_state_changed_listener(entity_id: str, old_state: State,
                                         new_state: State):
            """Handle entity updates."""
            self.async_schedule_update_ha_state(True)

        self._async_unsub_state_changed = async_track_state_change(
            self.hass, self._entity, async_state_changed_listener)
        await self.async_update()

    async def async_will_remove_from_hass(self):
        """Callback when removed from HASS."""
        if self._async_unsub_state_changed is not None:
            self._async_unsub_state_changed()
            self._async_unsub_state_changed = None

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return the on/off state of the light proxy."""
        return self._is_on

    @property
    def available(self) -> bool:
        """Return whether the light proxy is available."""
        return self._available

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return 0

    @property
    def should_poll(self) -> bool:
        """No polling needed for a light proxy."""
        return False

    async def async_turn_on(self, **kwargs):
        """Forward the turn_on command."""
        data = {ATTR_ENTITY_ID: self._entity}

        await self.hass.services.async_call(
            ha.DOMAIN, SERVICE_TURN_ON, data, blocking=True)

    async def async_turn_off(self, **kwargs):
        """Forward the turn_off command."""
        data = {ATTR_ENTITY_ID: self._entity}

        await self.hass.services.async_call(
            ha.DOMAIN, SERVICE_TURN_OFF, data, blocking=True)

    async def async_update(self):
        """Query all members and determine the light proxy state."""
        state = self.hass.states.get(self._entity)
        if state is None or state.state == STATE_UNAVAILABLE:
            self._available = False
            return
        self._available = True
        self._is_on = state.state == STATE_ON
