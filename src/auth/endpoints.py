from fastapi import APIRouter, HTTPException, Depends, status
from src.auth.domain import Signup, Login, AccessToken
from src.db.dependencies import get_user_repository
from src.user.repository import UserRepository
from src.utils.logger import conf_logger as logger
from .jwt import create_access_jwt, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


logger = logger(__name__, log_level = "D")


@router.post("/signup", response_model=AccessToken, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: Signup,
    repository: UserRepository = Depends(get_user_repository),
) -> AccessToken:
    try:
        signup_data.password = get_password_hash(signup_data.password)
        user = repository.add(signup_data)
        return AccessToken(access_token=create_access_jwt(user.id))
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def login(
    login_data: Login,
    repository: UserRepository = Depends(get_user_repository),
) -> AccessToken:
    try:
        user = repository.get(email=login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )
        if not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
        return AccessToken(access_token=create_access_jwt(user.id))
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
