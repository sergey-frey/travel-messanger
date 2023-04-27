from backend.app.users import auth_backend, fastapi_users
from backend.dto.user import UserCreate, UserRead, UserUpdate
from . import chat, user, post
from fastapi import APIRouter


router = APIRouter()

router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"],
)
router.include_router(
    post.router,
    prefix="/post",
    tags=["post"],
)
router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"],
)
router.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
)
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/auth",
    tags=["auth"],
)
