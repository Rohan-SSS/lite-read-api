from models.database import db
from models.models import Volume
from bson import ObjectId


### MAIN
def read_all_volumes(novel_alt:str):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    volumes_cursor = db.volumeCollection.find({"novelId":ObjectId(novel["_id"])})
    volumes = []
    for volume in volumes_cursor:
        volume["_id"] = str(volume["_id"])
        volume["novelId"] = str(volume["novelId"])
        volumes.append(volume)
    return volumes


### CRUD
# create volume
def create_volume(novelId: str, volume: Volume):
    volume_dict = volume.dict()
    volume_dict["novelId"] = ObjectId(novelId)
    result = db.volumeCollection.insert_one(volume_dict)
    volume_dict["_id"] = str(result.inserted_id)
    volume_dict["novelId"] = str(volume_dict["novelId"])
    return volume_dict

# read volume by novel's alt and volumeNumber
def read_volume_by_novel_and_volume(novel_alt: str, volumeNumber: int):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if novel:
        return db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
    return None

# update volume by novel's alt and volumeNumber
def update_volume_by_novel_and_volume(novel_alt: str, volumeNumber: int, volume: Volume):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if novel:
        update_data = volume.dict(exclude={"novelId"})
        result = db.volumeCollection.update_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber}, {"$set": update_data})
        return result.modified_count > 0
    return False

# delete volume by novel's alt and volumeNumber
def delete_volume_by_novel_and_volume(novel_alt: str, volumeNumber: int):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if novel:
        result = db.volumeCollection.delete_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
        return result.deleted_count > 0
    return False
