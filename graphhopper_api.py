from api import API

class GraphhopperAPI(API):
    def __init__(self, key):
        super().__init__(key)

    async def get_locations(self,session, location):
        request_str = f"https://graphhopper.com/api/1/geocode?q={location}&locale=en&key={self.key}&type=json&limit=10"
        return await super().fetch(session,request_str)
