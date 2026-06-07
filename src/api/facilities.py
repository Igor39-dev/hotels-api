import json
from src.init import redis_manager

from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example
from src.api.dependencies import DBDep

from src.shemas import facilities
from src.shemas.facilities import FacilityAdd
from src.shemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache=}")

    if not facilities_from_cache:
        print("!!!No facilities in cache!!!")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts



@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
