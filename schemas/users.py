from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
# from pydantic.mypy import from_attributes_callback


class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    #模型类配置
    model_config = ConfigDict(
        from_attributes=True #允许从ORM对象属性中获取
    )


#data数据类型
class UserAuthResponse(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(1800, description="过期时间（秒）")
    user_info: UserInfoResponse = Field(..., alias="userInfo")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="刷新令牌")

class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")



class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword",description="旧密码")
    new_password: str = Field(...,min_length=6 , alias="newPassword" , description="新密码")