from models.database import db
from bson import ObjectId
from models.models import RawChapter


# create raw chapter
def create_raw_chapter(volumeId:str, raw_chapter: RawChapter):
    raw_chapter_dict = raw_chapter.dict()
    raw_chapter_dict["volumeId"] = ObjectId(volumeId)
    result = db.rawChapterCollection.insert_one(raw_chapter_dict)
    raw_chapter_dict["_id"] = str(result.inserted_id)
    raw_chapter_dict["volumeId"] = str(raw_chapter_dict["volumeId"])
    return raw_chapter_dict

# read raw chapter
def read_raw_chapter_by_volume_id(novel_alt:str, volumeNumber:int):
    novel = db.novelCollection.find_one({"alt":novel_alt})
    if novel:
        volume = db.volumeCollection.find_one({"novelId":ObjectId(novel["_id"]), "volumeNumber":volumeNumber})
        if volume:
            return db.rawChapterCollection.find_one({"volumeId":volume["_id"], "rawChaptersVolumeNumber":volumeNumber})
    return None

# update raw chapter
def update_raw_chapter_by_volume_id(novel_alt:str, volumeNumber:int, raw_chapter: RawChapter):
    raw_chapter_data = read_raw_chapter_by_volume_id(novel_alt, volumeNumber)
    if raw_chapter_data:
        update_raw_chapter = raw_chapter.dict(exclude={"volumeId"})
        result = db.rawChapterCollection.update_one({"_id":raw_chapter_data["_id"]}, {"$set": update_raw_chapter})
        return result.modified_count > 0
    return False

# delete raw chapter
def delete_chapter_by_volume_id(novel_alt:str, volumeNumber:int):
    raw_chapter_data = read_raw_chapter_by_volume_id(novel_alt, volumeNumber)
    if raw_chapter_data:
        result = db.rawChapterCollection.delete_one({"_id":raw_chapter_data["_id"]})
        return result.deleted_count > 0
    return False