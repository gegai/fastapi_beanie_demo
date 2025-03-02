from .base import BaseDocument
from pydantic import Field
from typing import Optional


class Scene(BaseDocument):
    """
    场景信息
    """
    name: str = Field(..., description="场景名称")
    image: str = Field(..., description="场景图片")
    description: str = Field(..., description="场景描述")
    tags: list[str] = Field(..., description="场景标签")
    agent_type: str = Field(..., description="代理类型")
    classification: str = Field(..., description="场景分类")
    scene_name: str = Field(..., description="场景名称")
    map_name: str = Field(..., description="地图名称")
    applications: list[str] = Field(..., description="应用场景")

    class Settings:
        name = "scene"
