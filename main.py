from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from typing import List
from models.database import db

from crud.crud_novel import read_all_novels, read_novel_by_alt, read_novel_by_id, create_novel, update_novel_by_alt, delete_novel_by_alt
from crud.crud_volume import read_all_volumes, create_volume, read_volume_by_novel_and_volume, update_volume_by_novel_and_volume, delete_volume_by_novel_and_volume
from crud.crud_chapter import create_chapter, read_chapter_by_chapter_id, update_chapter_by_chapter_id, delete_chapter_by_chapter_id
from crud.crud_page import create_page, read_page_by_id, update_page_by_id, delete_page_by_id
from crud.crud_raw_chapter import create_raw_chapter, read_raw_chapter_by_volume_id

from models.models import Novel, NovelInDB, Volume, VolumeInDB, Chapter, ChapterInDB, Page, PageInDB, RawChapter, RawChapterInDB

app = FastAPI()

### CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### MAIN
# read all novels
@app.get("/novels", response_model=List[NovelInDB])
async def read_all_novels_endpoint():
    novels = read_all_novels()
    if novels:
        return novels
    raise HTTPException(status_code=404, detail="Resource not found")

# read all volumes
@app.get("/novel/{novel_alt}/volumes", response_model=List[VolumeInDB])
async def read_all_volumes_endpoint(novel_alt:str):
    volumes = read_all_volumes(novel_alt)
    if volumes:
        return volumes
    raise HTTPException(status_code=404, detail="Resource not found")


### PAGE
# create page
@app.post("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}/page", response_model=Page)
async def create_page_endpoint(novel_alt: str, volumeNumber: int, chapterNumber: int, page: Page):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
    if not volume:
        raise HTTPException(status_code=404, detail="Volume not found")
    chapter = db.chapterCollection.find_one({"volumeId": volume["_id"], "chapterNumber": chapterNumber})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    created_page = create_page(str(chapter["_id"]), page)
    return created_page

# read page
@app.get("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}/{pageNumber}", response_model=PageInDB)
async def read_page_by_id_endpoint(novel_alt: str, volumeNumber:int, chapterNumber:int, pageNumber:int):
    page = read_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
    if page:
        page["_id"] = str(page["_id"])
        page["chapterId"] = str(page["chapterId"])
        return page
    raise HTTPException(status_code=404, detail="Page not found")

# update page
@app.put("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}/{pageNumber}", response_model=Page)
async def update_page_by_id_endpoint(novel_alt:str, volumeNumber:int, chapterNumber:int, pageNumber:int, page:Page):
    updated = update_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber, page)
    if updated:
        updated_page = read_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
        updated_page["chapterId"] = str(updated_page["chapterId"])
        updated_page["_id"] = str(updated_page["_id"])
        return updated_page
    raise HTTPException(status_code=404, detail="Page not found or couldn't be updated")

# delete page
@app.delete("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}/{pageNumber}", response_model=dict)
async def delete_page_by_id_endpoint(novel_alt:str, volumeNumber:int, chapterNumber:int, pageNumber:int):
    deleted = delete_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
    if deleted:
        return {"status": "success", "message": f"Page {pageNumber} of Chapter {chapterNumber} in Volume {volumeNumber} of Novel {novel_alt} deleted."}
    raise HTTPException(status_code=404, detail="Page not found or couldn't be deleted")


### RAW CHAPTER
@app.post("/novel/{novel_alt}/{volumeNumber}/raw_chapter", response_model=RawChapter)
async def create_raw_chapter_endpoint(novel_alt:str, volumeNumber: int, raw_chapter:RawChapter):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if not novel:
        raise HTTPException(status_code=404, detail="Novel Not Found")
    volume = db.volumeCollection.find_one({"novelId":ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
    if not volume:
        raise HTTPException(status_code=404, detail="Volume Not Found")
    created_raw_chapter = create_raw_chapter(str(volume["_id"]), raw_chapter)
    return created_raw_chapter

@app.get("/novel/{novel_alt}/{volumeNumber}/raw_chapter/", response_model=RawChapterInDB)
async def read_raw_chapter_endpoint(novel_alt:str, volumeNumber:int):
    raw_chapter = read_raw_chapter_by_volume_id(novel_alt, volumeNumber)
    if raw_chapter:
        raw_chapter["_id"] = str(raw_chapter["_id"])
        raw_chapter["volumeId"] = str(raw_chapter["volumeId"])
        return raw_chapter
    raise HTTPException(status_code=404, detail="Resource not found")


### CHAPTER

# create chapter, when creating chapter number of chapters in volume collection needs to be updated
@app.post("/novel/{novel_alt}/{volumeNumber}/chapter", response_model=Chapter)
async def create_chapter_endpoint(novel_alt: str, volumeNumber: int, chapter: Chapter):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")
    volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
    if not volume:
        raise HTTPException(status_code=404, detail="Volume not found")
    created_chapter = create_chapter(str(volume["_id"]), chapter)
    return created_chapter

# read chapter
@app.get("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}", response_model=ChapterInDB)
async def read_chapter_by_id_endpoint(novel_alt: str, volumeNumber:int, chapterNumber:int):
    chapter = read_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
    if chapter:
        chapter["_id"] = str(chapter["_id"])
        chapter["volumeId"] = str(chapter["volumeId"])
        return chapter
    raise HTTPException(status_code=404, detail="Resource not found")

# update chapter
@app.put("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}", response_model=Chapter)
async def update_chapter_by_id_endpoint(novel_alt:str, volumeNumber:int, chapterNumber:int, chapter:Chapter):
    updated = update_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber, chapter)
    if updated:
        updated_chapter = read_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
        updated_chapter["volumeId"] = str(updated_chapter["volumeId"])
        updated_chapter["_id"] = str(updated_chapter["_id"])
        return updated_chapter
    raise HTTPException(status_code=404, detail="Resource not found")

# delete chapter
@app.delete("/novel/{novel_alt}/{volumeNumber}/{chapterNumber}", response_model=dict)
async def delete_chapter_by_id_endpoint(novel_alt:str, volumeNumber:int, chapterNumber:int):
    deleted = delete_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
    if deleted:
        return {"status": "success", "message": f"Chapter {chapterNumber} of Volume {volumeNumber} in Novel {novel_alt} deleted."}
    raise HTTPException(status_code=404, detail="Resource not found")


### VOLUME
# create volume
@app.post("/novel/{novel_alt}/", response_model=Volume)
async def create_volume_endpoint(novel_alt: str, volume: Volume):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")

    created_volume = create_volume(str(novel["_id"]), volume)
    return created_volume

# read volume by novel's alt and volumeNumber
@app.get("/novel/{novel_alt}/{volumeNumber}", response_model=VolumeInDB)
async def read_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int):
    volume = read_volume_by_novel_and_volume(novel_alt, volumeNumber)
    if volume:
        volume["_id"] = str(volume["_id"])
        volume["novelId"] = str(volume["novelId"])
        return volume
    raise HTTPException(status_code=404, detail="Volume not found")

# update volume by novel's alt and volumeNumber
@app.put("/novel/{novel_alt}/{volumeNumber}", response_model=Volume)
async def update_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int, volume: Volume):
    updated = update_volume_by_novel_and_volume(novel_alt, volumeNumber, volume)
    if updated:
        updated_volume = read_volume_by_novel_and_volume(novel_alt, volumeNumber)
        updated_volume["novelId"] = str(updated_volume["novelId"])
        updated_volume["_id"] = str(updated_volume["_id"])
        return updated_volume
    raise HTTPException(status_code=404, detail="Volume not found or couldn't be updated")

# delete volume by novel's alt and volumeNumber
@app.delete("/novel/{novel_alt}/{volumeNumber}", response_model=dict)
async def delete_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int):
    deleted = delete_volume_by_novel_and_volume(novel_alt, volumeNumber)
    if deleted:
        return {"status": "success", "message": f"Volume {volumeNumber} of Novel {novel_alt} deleted."}
    raise HTTPException(status_code=404, detail="Volume not found or couldn't be deleted")


### NOVEL
# create novel
@app.post("/novel/", response_model=Novel)
async def create_novel_endpoint(novel: Novel):
    created_novel = create_novel(novel)
    return created_novel

# read novel by MongoDB _id, gxz admin, and same url patterns fuck things LFI
@app.get("gxz/novel/{novel_id}", response_model=NovelInDB)
async def read_novel_by_id_endpoint(novel_id: str):
    novel = read_novel_by_id(novel_id)
    if novel:
        return novel
    raise HTTPException(status_code=404, detail="Resource not found")

# read novel by alt (slugified title)
@app.get("/novel/{alt}", response_model=Novel)
async def read_novel_by_alt_endpoint(alt: str):
    novel = read_novel_by_alt(alt)
    if novel:
        return novel
    raise HTTPException(status_code=404, detail="Resource not found")

# update novel by alt
@app.put("/novel/{alt}", response_model=Novel)
async def update_novel_by_alt_endpoint(alt: str, novel: Novel):
    updated = update_novel_by_alt(alt, novel)
    if updated:
        updated_novel = read_novel_by_alt(alt)
        return updated_novel
    raise HTTPException(status_code=404, detail="Resource not found or couldn't be updated")

# delete novel by alt
@app.delete("/novel/{alt}", response_model=dict)
async def delete_novel_by_alt_endpoint(alt: str):
    deleted = delete_novel_by_alt(alt)
    if deleted:
        return {"status": "success", "message": f"Novel {alt} deleted."}
    raise HTTPException(status_code=404, detail="Resource not found or couldn't be deleted")
