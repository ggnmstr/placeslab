import asyncio
from labclient import LabClient
graphhopper_api_key = "530458f9-9ebf-4fe3-840f-f205015423bf"
openweather_api_key = "986cbbc21481311f74653d40212c8d20"
opentripmap_api_key = "5ae2e3f221c38a28845f05b69c4535acdd87be331908743fb824dcab"

if __name__ == "__main__":
    labclient = LabClient(graphhopper_api_key,openweather_api_key,opentripmap_api_key)
    asyncio.run(labclient.run_lab())
