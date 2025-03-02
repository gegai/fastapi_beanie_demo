from fastapi import APIRouter
from src.application.services.scene_service import SceneService
from src.domain.entities.scenes import Scene

router = APIRouter(tags=["scenes"], prefix="/scenes")


@router.get("/")
async def get_scenes(
    text: str = None,
    scene_classification: str = None,
    agent_type: str = None,
    sort: str = None,
    reverse: bool = False,
    page: int = 1,
    per_page: int = 6,
):
    return await SceneService.get_scenes(text, scene_classification, agent_type, sort, reverse, page, per_page)
