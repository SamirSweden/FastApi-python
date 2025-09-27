from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news

app = FastAPI(title="news proxy api")


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(news.router)
@app.get("/")
async def main():
    return {"message" : "hello backend works"}
