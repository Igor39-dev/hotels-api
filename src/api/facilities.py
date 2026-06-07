import json
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.api.dependencies import DBDep
from src.shemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("!!!Going to DB!!!")
    return await db.facilities.get_all()



@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
