from fastapi import FastAPI
import uvicorn
from hotels import router as hotels_router


app = FastAPI()

app.include_router(hotels_router)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(): ...


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
