from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users
from utils.jwt_handler import verify_token

# 整合 根据 Token 查询用户, 返回用户
async def get_current_user(
        authorization: str = Header(default=..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    # Bearer XXXXX
    # token = authorization.split(" ")[1]
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证格式错误，应使用 Bearer Token"
        )

    token = authorization.replace("Bearer ", "")

    payload = verify_token(token, token_type="access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌或令牌已过期"
        )

    user_id = payload.get("user_id")
    user = await users.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user






