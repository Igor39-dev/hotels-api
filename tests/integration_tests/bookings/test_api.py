import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-08-10", "2026-08-20", 200),
    (1, "2026-08-11", "2026-08-21", 200),
    (1, "2026-08-12", "2026-08-22", 200),
    (1, "2026-08-13", "2026-08-23", 200),
    (1, "2026-08-14", "2026-08-24", 200),
    (1, "2026-08-15", "2026-08-25", 500),
    (1, "2026-08-26", "2026-08-30", 200),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,    
    db, authenticated_ac
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res
