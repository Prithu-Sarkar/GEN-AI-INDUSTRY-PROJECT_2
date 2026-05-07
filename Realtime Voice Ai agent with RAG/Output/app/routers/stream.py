from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from bson import ObjectId
from app.database import get_database

router = APIRouter()

@router.post("/connect")
async def bot_connect(request: Request) -> Dict[str, Any]:
    """
    Returns WebSocket URL for the voice bot.
    Production: AWS ECS/ALB endpoint.
    Colab: localhost ws:// URL for demonstration.
    """
    try:
        body: Dict[str, Any] = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    equipment_id: str = body.get("equipment_id", "")
    if not equipment_id:
        raise HTTPException(status_code=400, detail="equipment_id is required")
    db = get_database()
    try:
        equipment = await db.equipment.find_one({"_id": ObjectId(equipment_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid equipment_id format")
    if not equipment:
        raise HTTPException(status_code=404, detail=f"Equipment {equipment_id} not found")
    ws_url = f"ws://localhost:8000/api/v1/stream/ws/{equipment_id}"
    logger.info(f"Generated WS URL: {ws_url}")
    return {"ws_url": ws_url}
