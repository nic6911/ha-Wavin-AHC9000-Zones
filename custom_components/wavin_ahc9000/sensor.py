from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import WavinCoordinator
from .entity import WavinParentEntity, WavinZoneEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: WavinCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([WavinRssiSensor(coordinator)])
    coordinator.register_platform("sensor", async_add_entities, _zone_sensors)


def _zone_sensors(coordinator: WavinCoordinator, zone: dict[str, Any]):
    entities = [WavinZoneTemperatureSensor(coordinator, zone)]
    if "floor_sensor" in zone:
        if zone.get("floor_sensor"):
            entities.append(WavinZoneFloorSensor(coordinator, zone))
    elif zone.get("floor") is not None:
        # Older AHC firmware did not publish an explicit floor-sensor flag.
        entities.append(WavinZoneFloorSensor(coordinator, zone))
    if "battery" in zone:
        entities.append(WavinZoneBatterySensor(coordinator, zone))
    if "humidity" in zone:
        entities.append(WavinZoneHumiditySensor(coordinator, zone))
    if "dewpoint" in zone:
        entities.append(WavinZoneDewPointSensor(coordinator, zone))
    return entities


class WavinZoneTemperatureSensor(WavinZoneEntity, SensorEntity):
    _attr_name = "Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _entity_key = "temperature"

    @property
    def native_value(self) -> float | None:
        value = self.zone.get("current")
        return float(value) if value is not None else None


class WavinZoneFloorSensor(WavinZoneEntity, SensorEntity):
    _attr_name = "Floor temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _entity_key = "floor_temperature"

    @property
    def native_value(self) -> float | None:
        value = self.zone.get("floor")
        return float(value) if value is not None else None


class WavinZoneBatterySensor(WavinZoneEntity, SensorEntity):
    _attr_name = "Battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0
    _entity_key = "battery"

    @property
    def native_value(self) -> int | None:
        value = self.zone.get("battery")
        return int(value) if value is not None else None


class WavinZoneHumiditySensor(WavinZoneEntity, SensorEntity):
    _attr_name = "Humidity"
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _entity_key = "humidity"

    @property
    def native_value(self) -> float | None:
        value = self.zone.get("humidity")
        return float(value) if value is not None else None


class WavinZoneDewPointSensor(WavinZoneEntity, SensorEntity):
    _attr_name = "Dew point"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _entity_key = "dewpoint"

    @property
    def native_value(self) -> float | None:
        value = self.zone.get("dewpoint")
        return float(value) if value is not None else None


class WavinRssiSensor(WavinParentEntity, SensorEntity):
    _attr_name = "RSSI"
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0
    _entity_key = "rssi"

    @property
    def native_value(self) -> int | None:
        if self.coordinator.rssi is None or self.coordinator.rssi == -127:
            return None
        return int(self.coordinator.rssi)
