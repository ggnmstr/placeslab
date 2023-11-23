class API():
    def __init__(self,key):
        self.key = key

    async def fetch(self,session,request_str):
        async with session.get(request_str) as response:
            return await response.json()
