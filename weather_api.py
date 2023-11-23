from api import API

class WeatherAPI(API):
    def __init__(self,key):
        super().__init__(key)

    async def get_weather(self,session,point):
        lat = point["lat"]
        lon = point["lng"]
        request_str = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.key}&units=metric"
        return await self.fetch(session,request_str)
