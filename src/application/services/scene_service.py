from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from beanie.operators import RegEx, And, In, NotIn
from src.domain.entities.scenes import Scene
from datetime import datetime


class SceneResponse(BaseModel):
    """用户信息响应模型"""
    id: str = Field(alias="id", description="用户ID")
    name: str = Field(description="场景名称")
    scene_name: str = Field(description="场景名称UE")
    map_name: str = Field(description="场景地图名称")
    description: str = Field(description="场景描述")
    image: str = Field(description="场景图片")
    applications: List[str] = Field(default=[], description="项目信息")
    agent_type: str = Field(description="被测智能体类型")
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
    def response(cls, data: Scene) -> "SceneResponse":
        return cls(
            id=str(data.id),
            name=data.name,
            scene_name=data.scene_name,
            map_name=data.map_name,
            description=data.description,
            image=data.image,
            applications=data.applications,
            agent_type=data.agent_type,
            create_time=data.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            update_time=data.update_time.strftime("%Y-%m-%d %H:%M:%S")
        )

class SceneService:

    @classmethod
    async def get_scenes(cls, text=None, scene_classification=None, agent_type=None, sort=None, reverse: bool = False,
                         page: int = 1, per_page: int = 6, tags=None, application_id=None, include_in_application=None):
        # 构建查询条件，不使用 is_deleted
        filter_conditions = [Scene.is_deleted == False]  # noqa: E712
        # filter_conditions = []

        # 文本搜索
        if ObjectId.is_valid(text):
            filter_conditions.append(Scene._id == ObjectId(text))
        elif text:
            filter_conditions.append(RegEx(Scene.name, text))

        # 场景分类筛选
        if scene_classification:
            filter_conditions.append(Scene.scene_classification == scene_classification)

        # 智能体类型筛选
        if agent_type:
            filter_conditions.append(Scene.agent_type == agent_type)

        # 标签筛选
        if tags:
            filter_conditions.append(Scene.tags.all(tags))

        # 项目相关筛选
        if application_id and include_in_application:
            filter_conditions.append(In(Scene.applications, application_id))
        elif application_id and not include_in_application:
            filter_conditions.append(NotIn(Scene.applications, application_id))

        # 创建查询对象
        find_query = Scene.find(And(*filter_conditions))

        # 排序处理
        if sort:
            sort_direction = -1 if reverse else 1
            find_query = find_query.sort((sort, sort_direction))

        # 分页
        skip = (page - 1) * per_page

        # 执行查询
        total = await find_query.count()
        scenes = await find_query.skip(skip).limit(per_page).to_list()
        response = [SceneResponse.response(scene) for scene in scenes]
        return {
            "total": total,
            "items": response,
            "page": page,
            "per_page": per_page
        }
