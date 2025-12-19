from fastapi import APIRouter

router = APIRouter()

@router.get("/player/{player_id}")
async def get_player(player_id: int):
    return {"player_id": player_id}

@router.get("/team/{team_id}")
async def get_team(team_id: int):
    return {"team_id": team_id}

@router.get("/search")
async def search_stats(query: str):
    return {"team_id": query}

