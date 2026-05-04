from fastapi import FastAPI
import uvicorn
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth


app = FastAPI(
    title="Hotels API",
    description="API для работы с отелями",
)

app.include_router(router_auth)
app.include_router(router_hotels)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(): ...


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=True)
