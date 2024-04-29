from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.exceptions import LoginFailedError, UsernameAlreadyTakenError
from app.routes.auth.get_user import get_current_user
from app.routes.serializers import User, LoginUserData, RegisterUserData

router = APIRouter(prefix="/auth")


@router.get("/me")
async def get_user(current_user: User = Depends(get_current_user)):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"email": current_user.email})


@router.post("/register")
async def register(user_data: RegisterUserData):
    from app.entrypoint import app

    try:
        result = app.user_service.register(user_data)
    except UsernameAlreadyTakenError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": "User with this email already exists in the system"}
        )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)


@router.post("/login")
def login(user_data: LoginUserData):
    from app.entrypoint import app

    try:
        result = app.user_service.login(user_data)
    except LoginFailedError:
        return JSONResponse(
            content={"errors": "Username and/or password are incorrect"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
