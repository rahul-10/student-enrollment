from fastapi import FastAPI
import uvicorn

from app.api.v1 import enrollments
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(enrollments.router)

print('settings: ', settings)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True
    )
