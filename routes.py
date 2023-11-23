from fastapi import APIRouter, UploadFile
from name_matcher_service import (
    match_with_etalon,
    get_matching_table,
    update_matching_table,
    add_new_etalon,
    add_new_match
)
from fastapi import Body


router = APIRouter()

@router.post("/match_with_etalon/")
async def match_with_etalon_endpoint(file: UploadFile):
    return match_with_etalon(file)

@router.get("/get_matching_table/")
async def get_matching_table_endpoint():
    return get_matching_table()

@router.put("/update_matching_table/")
async def update_matching_table_endpoint(file: UploadFile):
    return update_matching_table(file)

@router.post("/add_new_etalon/")
async def add_new_etalon_endpoint(file: UploadFile):
    return add_new_etalon(file)

@router.post("/add_new_match/")
async def add_new_match_endpoint(file: UploadFile):
    return add_new_match(file)


@router.put("/change_specific_etalon/")
async def change_specific_etalon(etalon_id: int, new_values: dict = Body(...)):
    return change_specific_etalon(etalon_id, new_values)


@router.put("/change_specific_match/")
async def change_specific_match(match_id: int, new_values: dict = Body(...)):
    return change_specific_match(match_id, new_values)

