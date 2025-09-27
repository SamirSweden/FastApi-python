import httpx
from models.config import  Config



cfg = Config()

async def get_sources():
    url = f"{cfg.base_url}/sources?apikey={cfg.api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    

async def get_news(category: str , country: str , page: int = 1):
    url = f"{cfg.base_url}/news"
    params = {
        "api_key" : cfg.api_key,
        "category" : category,
        "country" : country,
        "page" : page,
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url , params=params)
        res.raise_for_status()
        return res.json()
