from api import API

class OpenTripMapAPI(API):
    def __init__(self, key):
        super().__init__(key)

    async def get_places(self, session,point):
        lat = point["lat"]
        lon = point["lng"]
        request_str = f"https://api.opentripmap.com/0.1/en/places/radius?radius=2000&lon={lon}&lat={lat}&apikey={self.key}"
        return await self.fetch(session,request_str)

    async def get_place_info(self,session, xid):
        request_str = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey={self.key}"
        return await self.fetch(session,request_str)

    async def get_place_info_text(self, session,xid):
        request_str = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey={self.key}"
        async with session.get(request_str) as response:
            place_info = await response.json()
            text = place_info.get("wikipedia_extracts", {}).get("text", "")
            return text
