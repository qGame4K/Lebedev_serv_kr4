from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional

app = FastAPI(title="Task 10.2: Validation Error Handling")

# Модель Pydantic из задания [cite: 53, 54, 55, 56, 57, 58, 59]
class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

# Пользовательская обработка ошибок проверки [cite: 67]
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for err in exc.errors():
        formatted_errors.append({
            "field": " -> ".join(map(str, err.get("loc", []))),
            "error_detail": err.get("msg")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Data validation failed",
            "errors": formatted_errors
        },
    )

@app.post("/users/")
async def register_user(user: User):
    return {"message": "User successfully registered", "data": user}