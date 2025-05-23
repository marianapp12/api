from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.core.exceptions import InvalidIDException, ResourceNotFoundException
from app.routes.Vino_router import Vino_router

app = FastAPI(
    title=" API",
    description=""
)


@app.exception_handler(InvalidIDException)
async def invalid_id_exception_handler(request, exc: InvalidIDException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(Vino_router)


@app.get('/')
def root():
    return {"message": "Go to http://127.0.0.1:8000/docs"}
