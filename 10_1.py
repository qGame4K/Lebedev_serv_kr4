from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task 10.1: Custom Exceptions")


class ErrorResponseModel(BaseModel):
    error_type: str
    message: str

class CustomExceptionA(Exception):
    def __init__(self, message: str):
        self.message = message

class CustomExceptionB(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=400,
        content=ErrorResponseModel(error_type="Validation Error", message=exc.message).model_dump()
    )

@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=404,
        content=ErrorResponseModel(error_type="Not Found Error", message=exc.message).model_dump()
    )

@app.get("/check-condition")
async def trigger_exception_a(is_valid: bool = False):
    if not is_valid:
        raise CustomExceptionA("Condition is not met. Please pass is_valid=true.") # [cite: 44]
    return {"message": "Success!"}

@app.get("/resource/{resource_id}")
async def trigger_exception_b(resource_id: int):
    if resource_id != 1:
        raise CustomExceptionB(f"Resource with id {resource_id} not found.") # [cite: 44]
    return {"message": "Resource found!"}