from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME, CONF_REGION

async def async_setup_entry(hass, config_entry, async_add_entities):
    name = config_entry.data[CONF_NAME]
    region = config_entry.data[CONF_REGION]
    oil_types = ["92#", "95#", "98#", "0#"]

    sensors = [OilPriceSensor(name=f"{name} {oil_type}", region=region, oil_type=oil_type) for oil_type in oil_types]
    sensors.append(OilPriceHintSensor(name=f"{name} info", region=region))
    async_add_entities(sensors, True)
