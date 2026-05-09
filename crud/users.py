import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest

from utils.jwt_handler import hash_password, verify_password, create_access_token, create_refresh_token, verify_token


#根据用户名查询数据库
async def get_user_by_username(db : AsyncSession, username : str):
     query = select(User).where(User.username == username)
     result = await db.execute(query)
     return result.scalar_one_or_none()



async def get_user_by_id(db: AsyncSession, user_id: int):
     """
     根据用户ID查询用户
     """
     query = select(User).where(User.id == user_id)
     result = await db.execute(query)
     return result.scalar_one_or_none()


#创建用户
async def create_user(db : AsyncSession, user_data : UserRequest):
     hashed_password = hash_password(user_data.password)
     user = User(username=user_data.username, password=hashed_password)
     db.add(user)
     await db.commit()
     await db.refresh(user)
     return user

# #生成token
# #生成Token + 设置过期时间 +查询数据库当前用户是否有token  有就更新，没有就添加
# async def create_token(db : AsyncSession, user_id: int):
#      token = str(uuid.uuid4())
#      expire_at = datetime.now() + timedelta(days=7)
#      query = select(UserToken).where(UserToken.user_id == user_id)
#      result = await db.execute(query)
#      user_token = result.scalar_one_or_none()
#      if user_token:
#           user_token.token = token
#           user_token.expire_at = expire_at
#      else:
#           user_token = UserToken(user_id=user_id, token=token, expires_at=expire_at)
#           db.add(user_token)
#           await db.commit()
#      return token


async def create_tokens(db: AsyncSession, user: User):
     """
     创建 JWT tokens（access + refresh）
     返回字典包含 tokens 和用户信息
     """
     access_token = create_access_token(
          data={"sub": user.username, "user_id": user.id}
     )
     refresh_token = create_refresh_token(
          data={"sub": user.username, "user_id": user.id}
     )

     return {
          "access_token": access_token,
          "refresh_token": refresh_token,
          "token_type": "bearer",
          "expires_in": 1800  # 30分钟
     }



async def authenticate_user(db : AsyncSession, username: str, password: str):
     user = await get_user_by_username(db, username)
     if not user:
          return None
     if not verify_password(password, user.password):
          return None
     return user


# async def get_user_by_token(db : AsyncSession, token: str):
#      query = select(UserToken).where(UserToken.token == token)
#      result = await db.execute(query)
#      db_token = result.scalar_one_or_none()
#
#      if not db_token or db_token.expires_at < datetime.now():
#           return None
#
#      query = select(User).where(User.id == db_token.user_id)
#      result = await db.execute(query)
#      return result.scalar_one_or_none()


async def refresh_access_token(db: AsyncSession, refresh_token: str):
     """
     使用 refresh token 获取新的 access token
     """
     payload = verify_token(refresh_token, token_type="refresh")
     if not payload:
          return None

     user_id = payload.get("user_id")
     user = await get_user_by_id(db, user_id)

     if not user:
          return None

     new_access_token = create_access_token(
          data={"sub": user.username, "user_id": user.id}
     )

     return {
          "access_token": new_access_token,
          "token_type": "bearer",
          "expires_in": 1800
     }


#更新用户信息; update更新 检查是否命中 获取更新后的用户返回
#update(User).where(User.username == username).values(字段=值)
#user_data 是一个pydantic类型 得到字典 -**解包
#没有设置的值不更新
async def update_user(db : AsyncSession, username : str, user_data : UserUpdateRequest):
     query = update(User).where(User.username == username).values(**user_data.model_dump(
          exclude_unset=True,
          exclude_none=True,
     ))
     result = await db.execute(query)
     await db.commit()

     #检查更新
     if result.rowcount == 0:
          raise HTTPException(status_code=404, detail="用户不存在")

     #获取一下更新后的用户
     updated_user = await get_user_by_username(db,username)
     return updated_user

#修改密码 验证旧密码 新密码加密 修改密码
async def change_password(db : AsyncSession, user: User , old_password : str, new_password : str):
     if not verify_password(old_password, user.password):
          return False

     hashed_new_pwd = hash_password(new_password)
     user.password = hashed_new_pwd
     db.add(user)  #更新：由SQLAlchemy真正接管这个User对象 确保可以commit 规避session过期或关闭导致的不能提交的问题
     await db.commit()
     await db.refresh(user)
     return True






