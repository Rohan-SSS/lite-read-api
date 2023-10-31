from fastapi import FastAPI, HTTPException
from crud.crud_novel import *
from crud.crud_volume import *

app = FastAPI()


### VOLUME
# create volume
@app.post("/novel/{novel_alt}/volume/", response_model=Volume)
async def create_volume_endpoint(novel_alt: str, volume: Volume):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")

    created_volume = create_volume(str(novel["_id"]), volume)
    return created_volume

# read volume by novel's alt and volumeNumber
@app.get("/novel/{novel_alt}/volume/{volumeNumber}", response_model=VolumeInDB)
async def read_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int):
    volume = read_volume_by_novel_and_volume(novel_alt, volumeNumber)
    if volume:
        volume["_id"] = str(volume["_id"])
        volume["novelId"] = str(volume["novelId"])
        return volume
    raise HTTPException(status_code=404, detail="Volume not found")

# update volume by novel's alt and volumeNumber
@app.put("/novel/{novel_alt}/volume/{volumeNumber}", response_model=Volume)
async def update_volume_by_novel_and_volume_endpoint(novel_alt: str, volumeNumber: int, volume: Volume):
    updated = update_volume_by_novel_and_volume(novel_alt, volumeNumber, volume)
    if updated:
        updated_volume = read_volume_by_novel_and_volume(novel_alt, volumeNumber)
        updated_volume["novelId"] = str(updated_volume["novelId"])
        updated_volume["_id"] = str(updated_volume["_id"])
        return updated_volume
    raise HTTPException(status_code=404, detail="Volume not found or couldn't be updated")

# delete volume by novel's alt and volumeNumber
@app.delete("/novel/{novel_alt}/volume/{volumeNumber}", response_model=dict)
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
