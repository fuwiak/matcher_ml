from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, UploadFile, File

from name_matcher_service import (
    match_with_etalon,
    get_matching_table,
    update_matching_table,
    add_new_etalon,
    add_new_match
)

router = APIRouter()

@router.post("/match_with_etalon/")
async def match_with_etalon_endpoint(file: UploadFile):
    return match_with_etalon(file)
@router.get("/get_matching_table/")
async def get_matching_table_endpoint():
    return get_matching_table()

@router.put("/update_matching_table/")
async def update_matching_table_endpoint(updates: dict):
    return update_matching_table(updates)

@router.post("/add_new_etalon/")
async def add_new_etalon_endpoint(etalon: dict):
    return add_new_etalon(etalon)

@router.post("/add_new_match/")
async def add_new_match_endpoint(match_data: dict):
    return add_new_match(match_data)
