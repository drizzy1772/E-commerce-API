




from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": "HTTPException",
            "message": exc.detail,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Validation errors"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error": "Validation error",
            "message": message,
        }
    )