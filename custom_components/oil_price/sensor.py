import logging
import aiohttp
import datetime
from bs4 import BeautifulSoup
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME, CONF_REGION

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(hours=8)
ICON = 'mdi:gas-station'

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up oil price sensors from config entry."""
    name = config_entry.data[CONF_NAME]
    region = config_entry.data[CONF_REGION]
    oil_types = ["92#", "95#", "98#", "0#"]

    sensors = [OilPriceSensor(name=f"{name} {oil_type}", region=region, oil_type=oil_type) for oil_type in oil_types]
    sensors.append(OilPriceHintSensor(name=f"{name} info", region=region))
    async_add_entities(sensors, True)


class OilPriceSensor(Entity):
    def __init__(self, name: str, region: str, oil_type: str):
        self._name = name
        self._region = region
        self._oil_type = oil_type
        self._state = None
        self._update_time = None

    async def async_update(self):
        """Fetch oil price data from the webpage."""
        url = f"http://www.qiyoujiage.com/{self._region}.shtml"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        self._parse_oil_price(text)
                    else:
                        _LOGGER.error(f"Failed to fetch data, status code: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error fetching oil price data: {e}")

    def _parse_oil_price(self, text):
        """Parse HTML content and extract specific oil type price."""
        soup = BeautifulSoup(text, "lxml")
        try:
            price_sections = soup.select("#youjia > dl")
            for section in price_sections:
                oil_type = section.select_one("dt").text.strip()
                price = section.select_one("dd").text.strip()
                if self._oil_type in oil_type:
                    self._state = price
                    self._update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    break
        except Exception as e:
            _LOGGER.error(f"Error parsing oil price data: {e}")

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
        return {
            "update_time": self._update_time,
        }


class OilPriceHintSensor(Entity):
    def __init__(self, name: str, region: str):
        self._name = name
        self._region = region
        self._state = None
        self._update_time = None

    async def async_update(self):
        """Fetch hint information from the webpage."""
        url = f"http://www.qiyoujiage.com/{self._region}.shtml"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        self._parse_hints(text)
                    else:
                        _LOGGER.error(f"Failed to fetch data, status code: {response.status}")
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Error fetching oil price hint data: {e}")

    def _parse_hints(self, text):
        """Parse HTML content and extract hint information."""
        soup = BeautifulSoup(text, "lxml")
        try:
            hint_section = soup.select_one("#youjiaCont > div:nth-of-type(2)")
            if hint_section:
                self._state = hint_section.text.strip()
                self._update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            _LOGGER.error(f"Error parsing hint data: {e}")

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
        return {
            "update_time": self._update_time,
        }
