from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import inspect

from app.models import Base
from app.config import engine
from app.routers import router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
    )


@app.get("/")
async def home():
    return {"hello": "welcome home"}


@router.get("/ready")
async def ready():
    try:
        table_exists = inspect(engine).has_table("pessoas")
    except Exception as e:
        table_exists = False
    return {"ready": table_exists}


app.include_router(router, tags=["pessoas"])
