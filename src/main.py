import uvicorn

from settings import uvicorn_settings

if __name__ == "__main__":
    uvicorn.run(app="app:app", **uvicorn_settings.model_dump())
