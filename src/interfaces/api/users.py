from datetime import datetime
from typing import List, Optional, Dict

from fastapi import APIRouter, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field
from bson import ObjectId

from src.application.dto.user_dto import UserCreateDTO, UserUpdateDTO
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.entities.base import PyObjectId


router = APIRouter(tags=["users"], prefix="/users")


class UserResponse(BaseModel):
    """用户信息响应模型"""
    id: str = Field(description="用户ID")
    username: str = Field(description="用户名")
    email: str = Field(description="电子邮箱")
    phone: Optional[str] = Field(None, description="电话号码")
    is_active: bool = Field(description="是否激活")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }
        populate_by_name = True
        arbitrary_types_allowed = True
        from_attributes = True

    @classmethod
    def from_mongo(cls, data: User) -> "UserResponse":
        return cls(
            id=str(data.id),
            username=data.username,
            email=data.email,
            phone=data.phone,
            is_active=data.is_active,
            create_time=data.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            update_time=data.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )


class DeleteResponse(BaseModel):
    """删除操作响应模型"""
    message: str = Field(description="操作结果消息")


@router.post(
    "/",
    response_model=UserResponse,
    summary="创建新用户",
    description="创建一个新的用户账号",
    response_description="返回创建的用户信息"
)
async def create_user(
    user_data: UserCreateDTO = Body(..., description="用户创建信息")
) -> UserResponse:
    """
    创建新用户

    - **username**: 用户名 (3-50字符)
    - **email**: 电子邮箱 (有效的邮箱格式)
    - **password**: 密码 (最少6个字符)
    - **phone**: 电话号码 (可选，需符合国际格式)
    """
    user = await UserService.create_user(user_data)
    return UserResponse.from_mongo(user)


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="获取用户列表",
    description="获取所有未删除的用户列表",
    response_description="返回用户列表"
)
async def get_users(
    skip: int = Query(0, description="跳过的记录数", ge=0),
    limit: int = Query(10, description="返回的记录数", ge=1, le=100),
    username: Optional[str] = Query(None, description="用户名"),
    email: Optional[str] = Query(None, description="电子邮箱"),
    phone: Optional[str] = Query(None, description="电话号码")
) -> List[UserResponse]:
    """
    获取用户列表，支持分页

    - **skip**: 跳过的记录数（默认0）
    - **limit**: 返回的记录数（默认10，最大100）
    """
    users = await UserService.get_users(skip, limit, username, email, phone)
    return [UserResponse.from_mongo(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="获取用户详情",
    description="根据用户ID获取用户详细信息",
    response_description="返回用户详细信息"
)
async def get_user(
    user_id: str = Path(..., description="用户ID", example="507f1f77bcf86cd799439011")
) -> UserResponse:
    """
    获取指定用户的详细信息

    - **user_id**: 用户ID（MongoDB ObjectId）
    """
    user = await UserService.get_user_by_id(user_id)
    if not user or user.is_delete:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_mongo(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="更新用户信息",
    description="更新指定用户的信息",
    response_description="返回更新后的用户信息"
)
async def update_user(
    user_id: str = Path(..., description="用户ID", example="507f1f77bcf86cd799439011"),
    user_data: UserUpdateDTO = Body(..., description="用户更新信息")
) -> UserResponse:
    """
    更新用户信息

    - **user_id**: 用户ID
    - **username**: 新用户名 (可选，3-50字符)
    - **email**: 新电子邮箱 (可选，有效的邮箱格式)
    - **phone**: 新电话号码 (可选，需符合国际格式)
    """
    user = await UserService.get_user_by_id(user_id)
    if not user or user.is_delete:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await UserService.update_user(user, user_data)
    return UserResponse.from_mongo(updated_user)


@router.delete(
    "/{user_id}",
    response_model=DeleteResponse,
    summary="删除用户",
    description="软删除指定用户",
    response_description="返回删除操作结果"
)
async def delete_user(
    user_id: str = Path(..., description="用户ID", example="507f1f77bcf86cd799439011")
) -> Dict[str, str]:
    """
    删除用户（软删除）

    - **user_id**: 要删除的用户ID
    """
    user = await UserService.get_user_by_id(user_id)
    if not user or user.is_delete:
        raise HTTPException(status_code=404, detail="User not found")
    await UserService.delete_user(user)
    return {"message": "User deleted successfully"}
