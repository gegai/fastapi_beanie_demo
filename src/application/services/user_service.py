from typing import List, Optional

from passlib.context import CryptContext
from beanie.operators import And, RegEx

from src.application.dto.user_dto import UserCreateDTO, UserUpdateDTO
from src.domain.entities.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def create_user(user_data: UserCreateDTO) -> User:
        user_dict = user_data.dict()
        user_dict["password"] = pwd_context.hash(user_dict["password"])
        user = User(**user_dict)
        await user.save()
        return user

    @staticmethod
    async def get_users(
        skip: int = 0,
        limit: int = 10,
        username: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> List[User]:
        # 创建基础查询条件
        filter_conditions = [User.is_deleted == False]  # noqa: E712

        # 动态添加模糊查询条件
        if username:
            filter_conditions.append(RegEx(User.username, f".*{username}.*", "i"))
        if email:
            filter_conditions.append(RegEx(User.email, f".*{email}.*", "i"))
        if phone:
            filter_conditions.append(RegEx(User.phone, f".*{phone}.*", "i"))

        # 执行查询
        users = await User.find(
            And(*filter_conditions)
        ).skip(skip).limit(limit).to_list()

        return users

    @staticmethod
    async def get_user_by_id(user_id: str) -> User:
        return await User.get(user_id)

    @staticmethod
    async def update_user(user: User, user_data: UserUpdateDTO) -> User:
        user_update_dict = user_data.dict(exclude_unset=True)
        for field, value in user_update_dict.items():
            setattr(user, field, value)
        await user.save()
        return user

    @staticmethod
    async def delete_user(user: User) -> None:
        user.is_deleted = True
        await user.save()
