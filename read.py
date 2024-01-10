from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from crud.crud_novel import read_all_novels, read_novel_by_alt
from crud.crud_volume import read_volume_by_novel_and_volume, read_all_volumes
from crud.crud_chapter import read_chapter_by_chapter_id
from crud.crud_page import read_page_by_id

from models.models import Novel, NovelInDB, VolumeInDB,  ChapterInDB, PageInDB

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Novel
# read all novels for homepage
@app.get("/novels", response_model=List[NovelInDB])
async def read_all_novels_endpoint():
    novels = read_all_novels()
    if novels:
        return novels
    raise HTTPException(status_code=404, detail="Resource not found")

# read novel
@app.get("/novel/{novel_alt}/", response_model=Novel)
async def read_novel_by_alt_endpoint(novel_alt:str):
    novel = read_novel_by_alt(novel_alt)
    if novel:
        return novel
    raise HTTPException(status_code=404, detail="Resource not found")

# Volume
# read volume by novel's alt and volumeNumber
@app.get("/novel/{novel_alt}/{volumeNumber}", response_model=VolumeInDB)
async def read_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int):
    volume = read_volume_by_novel_and_volume(novel_alt, volumeNumber)
    if volume:
        volume["_id"] = str(volume["_id"])
        volume["novelId"] = str(volume["novelId"])
        return volume
    raise HTTPException(status_code=404, detail="Volume not found")


# Chapter
# read chapter
@app.get("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}", response_model=ChapterInDB)
async def read_chapter_by_id_endpoint(novel_alt: str, volumeNumber:int, chapterNumber:int):
    chapter = read_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
    if chapter:
        chapter["_id"] = str(chapter["_id"])
        chapter["volumeId"] = str(chapter["volumeId"])
        return chapter
    raise HTTPException(status_code=404, detail="Resource not found")


# Page
# read a page
@app.get("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}/{pageNumber}", response_model=PageInDB)
async def read_page_by_id_endpoint(novel_alt: str, volumeNumber:int, chapterNumber:int, pageNumber:int):
    page = read_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
    if page:
        page["_id"] = str(page["_id"])
        page["chapterId"] = str(page["chapterId"])
        return page
    raise HTTPException(status_code=404, detail="Page not found")

