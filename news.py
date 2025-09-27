from fastapi import FastAPI , APIRouter ,Query
from services import newsdata



router = APIRouter(prefix="/api/news",tags=["news"])


@router.get("/services")
async def sources():
    return await newsdata.get_sources()

@router.get("/")
async def news(
    category: str = Query(...),
    country: str = Query(...),
    page : int = Query(1)
):
    
    return await newsdata.get_news(category , country , page)
