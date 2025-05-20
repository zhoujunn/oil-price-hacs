import logging
import aiohttp
import datetime
from bs4 import BeautifulSoup
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME, CONF_REGION
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, ICON, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_REGION): cv.string,
})

SCAN_INTERVAL = datetime.timedelta(seconds=DEFAULT_SCAN_INTERVAL)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config[CONF_NAME]
    region = config[CONF_REGION]
    oil_types = ["92#", "95#", "98#", "0#"]
    sensors = [OilPriceSensor(f"{name} {oil}", region, oil) for oil in oil_types]
    sensors.append(OilPriceHintSensor(f"{name} info", region))
    async_add_entities(sensors, True)


class OilPriceSensor(Entity):
    def __init__(self, name: str, region: str, oil_type: str):
        self._name = name
        self._region = region
        self._oil_type = oil_type
        self._state = None
        self._update_time = None

    async def async_update(self):
        url = f"http://www.qiyoujiage.com/{self._region}.shtml"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        self._parse(text)
                    else:
                        _LOGGER.error(f"Fetch failed: status {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Fetch exception: {e}")

    def _parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        sections = soup.select("#youjia > dl")
        for section in sections:
            oil = section.select_one("dt").text.strip()
            price = section.select_one("dd").text.strip()
            if self._oil_type in oil:
                self._state = price
                self._update_time = datetime.datetime.now().isoformat()
                break

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def extra_state_attributes(self):
        return {"update_time": self._update_time}


class OilPriceHintSensor(Entity):
    def __init__(self, name: str, region: str):
        self._name = name
        self._region = region
        self._state = None
        self._update_time = None

    async def async_update(self):
        url = f"http://www.qiyoujiage.com/{self._region}.shtml"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        self._parse(text)
                    else:
                        _LOGGER.error(f"Hint fetch failed: status {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Hint fetch exception: {e}")

    def _parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        section = soup.select_one("#youjiaCont > div:nth-of-type(2)")
        if section:
            self._state = section.text.strip()
            self._update_time = datetime.datetime.now().isoformat()

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:information-outline"

    @property
    def extra_state_attributes(self):
        return {"update_time": self._update_time}
