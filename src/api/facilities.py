from datetime import date
from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example
from src.api.dependencies import DBDep
from src.shemas.facilities import FacilityAdd
from src.shemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()
    


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
