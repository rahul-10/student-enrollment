from fastapi import FastAPI
import uvicorn

from app.api.v1.enrollments import router as enrollment_router
from app.api.v1.admin_timetables import router as admin_router
from app.core.config import settings
from app.core.exception_handlers import unhandled_exception_handler


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler
    )

    app.include_router(enrollment_router)
    app.include_router(admin_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.env == "local"
    )
