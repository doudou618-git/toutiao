from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest, RefreshTokenRequest

from config.db_conf import get_db
from crud import users
from utils.auth import get_current_user
from utils.response import success_response



router = APIRouter(prefix="/api/user", tags=["users"])
@router.post("/register")
async def register(user_data:UserRequest ,  db : AsyncSession = Depends(get_db)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    tokens = await users.create_tokens(db, user)
    response_data = UserAuthResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        expires_in=tokens["expires_in"],
        user_info=UserInfoResponse.model_validate(user)
    )
    return success_response(message="注册成功", data=response_data)



@router.post("/login")
async def login(user_data: UserRequest , db : AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或者密码错误")
    tokens = await users.create_tokens(db, user)
    response_data = UserAuthResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        expires_in=tokens["expires_in"],
        user_info=UserInfoResponse.model_validate(user)
    )
    return success_response(message="登录成功" ,data=response_data)


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """
    刷新 access token
    """
    result = await users.refresh_access_token(db, request.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    return success_response(message="Token刷新成功", data=result)
#查Token查用户 封装crud 功能整合成一个工具函数 路由导入使用，依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))


# 修改用户信息:验证Token → 更新(用户输入数据 put提交 → 请求体参数→定义Pydantic模型→修改跟新)

# 参数:用户输入的 + 验证Token的 + db(调用更新的方法)
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest , user: User = Depends(get_current_user),
                           db : AsyncSession = Depends(get_db)):
    user = await users.update_user(db, user.username, user_data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(
        password_data : UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db : AsyncSession = Depends(get_db)):
    res_change_pwd = await users.change_password(db , user , password_data.old_password , password_data.new_password )
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")
    return success_response(message="密码修改成功")