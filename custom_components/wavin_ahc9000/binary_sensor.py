from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WavinCoordinator
from .entity import WavinZoneEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: WavinCoordinator = hass.data[DOMAIN][entry.entry_id]
    coordinator.register_platform("binary_sensor", async_add_entities, _zone_binary_sensors)


def _zone_binary_sensors(coordinator: WavinCoordinator, zone: dict[str, Any]):
    entities = []
    if "battery_low" in zone:
        entities.append(
            WavinZoneBinarySensor(
                coordinator, zone, "Low battery", "battery_low", BinarySensorDeviceClass.BATTERY
            )
        )
    if "warning" in zone:
        entities.append(
            WavinZoneBinarySensor(
                coordinator, zone, "Warning", "warning", BinarySensorDeviceClass.PROBLEM
            )
        )
    if "error" in zone:
        entities.append(
            WavinZoneBinarySensor(
                coordinator, zone, "Error", "error", BinarySensorDeviceClass.PROBLEM
            )
        )
    return entities


class WavinZoneBinarySensor(WavinZoneEntity, BinarySensorEntity):
    def __init__(
        self,
        coordinator: WavinCoordinator,
        zone: dict[str, Any],
        name: str,
        key: str,
        device_class: BinarySensorDeviceClass,
    ) -> None:
        self._zone_key = key
        self._entity_key = key
        super().__init__(coordinator, zone)
        self._attr_name = name
        self._attr_device_class = device_class

    @property
    def is_on(self) -> bool:
        return bool(self.zone.get(self._zone_key))
