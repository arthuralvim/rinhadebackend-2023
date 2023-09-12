from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.redis import get_redis
from app.routers import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the redis connection
    app.state.redis = await get_redis()
    yield
    # close redis connection and release the resources
    app.state.redis.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
    )


@app.get("/")
async def home():
    return {"hello": "welcome home"}


app.include_router(router, tags=["pessoas"])
