from models.database import db
from models.models import Chapter
from bson import ObjectId

# create chapter
def create_chapter(volumeId: str, chapter: Chapter):
  chapter_dict = chapter.dict()
  chapter_dict["volumeId"] = ObjectId(volumeId)
  result = db.chapterCollection.insert_one(chapter_dict)
  chapter_dict["_id"] = str(result.inserted_id)
  chapter_dict["volumeId"] = str(chapter_dict["volumeId"])
  return chapter_dict

# read chapter by volume's novelId and volumeNumber and chapterNumber
def read_chapter_by_chapter_id(novel_alt:str, volumeNumber:int, chapterNumber:int):
  novel = db.novelCollection.find_one({"alt": novel_alt})
  if novel:
    volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
    if volume:
      return db.chapterCollection.find_one({"volumeId": volume["_id"], "chapterNumber": chapterNumber})
  return None

# update chapter by volume's novelId, volumeNumber and chapterNumber
def update_chapter_by_chapter_id(novel_alt:str, volumeNumber: int, chapterNumber:int, chapter: Chapter):
  chapter_data = read_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
  if chapter_data:
    update_data = chapter.dict(exclude={"volumeId"})
    result = db.chapterCollection.update_one({"_id":chapter_data["_id"]}, {"$set": update_data})
    return result.modified_count > 0
  return False

# delete chapter by volume's novelId, volumeNumber and chapterNumber
def delete_chapter_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber:int):
  chapter_data = read_chapter_by_chapter_id(novel_alt, volumeNumber, chapterNumber)
  if chapter_data:
    result = db.chapterCollection.delete_one({"_id":chapter_data["_id"]})
    return result.deleted_count > 0
  return False


