import httpx


class Bruce_async_httpx():

    async def fetch_data(self,url:str,timeout:float=None)->dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url,timeout=timeout)
            return response.json()

    async def fetch_data_post(self,url:str,req_data:dict,timeout:float=None)->dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(url,data=req_data,timeout=timeout)
            return response.json()

