import asyncio
import aiohttp
from weather_api import WeatherAPI
from graphhopper_api import GraphhopperAPI
from opentripmap_api import OpenTripMapAPI
from labdata import LabData

# TODO: добавить тип места (туристическое, и тд) (osm key? ost key?)


class LabClient():
    def __init__(self, graphhopper_api_key, openweather_api_key, opentripmap_api_key):
        self.graphhopper_api = GraphhopperAPI(graphhopper_api_key)
        self.openweather_api = WeatherAPI(openweather_api_key)
        self.opentripmap_api = OpenTripMapAPI(opentripmap_api_key)
        self.data = LabData()

    async def procWeather(self, session, interesting_place):
        weather_json = await self.openweather_api.get_weather(session, interesting_place["point"])
        self.data.weather_json = weather_json
        print(
            f'Weather: {weather_json["weather"][0]["main"]}, {weather_json["weather"][0]["description"]}, {weather_json["main"]["temp"]}C, ',
            f'humidity: {weather_json["main"]["humidity"]}, pressure: {weather_json["main"]["pressure"]} hPa, wind speed: {weather_json["wind"]["speed"]} meter/sec, cloudness: {weather_json["clouds"]["all"]}%')

    async def procPlace(self, session, xid):
        info = await self.opentripmap_api.get_place_info(session, xid)
        self.data.places_info_json.append(info)
        if "name" in info and "wikipedia_extracts" in info:
            print(info["name"], "\n", info["wikipedia_extracts"]["text"])
        elif "name" in info:
            print(info["name"])

    async def procAllPlaces(self, session, interesting_place):
        places_json = await self.opentripmap_api.get_places(session, interesting_place["point"])
        self.data.places_json = places_json
        tasks = []
        for feature in places_json["features"]:
            xid = feature["properties"]["xid"]
            tasks.append(self.procPlace(session, xid))
        await asyncio.gather(*tasks)

    async def run_lab(self):
        print("Type the name of the place:")
        location = str(input())
        async with aiohttp.ClientSession() as session:
            locations_json = await self.graphhopper_api.get_locations(session, location)
            self.data.locations_json = locations_json
            print("Type in the number of the place you're interested in: ")
            for i, point in enumerate(locations_json["hits"]):
                things = [point["name"]]
                if "country" in point:
                    things.append(point["country"])
                if "city" in point:
                    things.append(point["city"])
                if "street" in point:
                    things.append(point["street"])
                if "osm_key" in point:
                    things.append(point["osm_key"])
                print(f'{i}) ', end='')
                print(*things, sep=", ")
            place_idx = int(input())
            interesting_place = locations_json["hits"][place_idx]
            task1 = self.procAllPlaces(session, interesting_place)
            task2 = self.procWeather(session, interesting_place)
            await asyncio.gather(task1, task2)
