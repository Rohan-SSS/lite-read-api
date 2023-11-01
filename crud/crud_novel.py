### NOTE
# For admin controls a different api needed
# update needs all fields


from pydantic import BaseModel
from database import db
from bson import ObjectId

import re
from slugify import slugify


### DB SCHEMA
class Novel(BaseModel):
    title: str
    noOfVolumes: int
    imageURL: str
    malLink: str
    rank: int
    trend: int

class NovelInDB(Novel):
    _id: str


### MAIN
# read all novels
def read_all_novels():
    novels_cursor = db.novelCollection.find()
    novels = []

    for novel in novels_cursor:
        novel["_id"] = str(novel["_id"])
        novels.append(novel)
    return novels


### CRUD
# create novel
def create_novel(novel: Novel):
    alt_value = slugify(novel.title)
    alt_value = ensure_unique_alt(alt_value)
    novel_dict = novel.dict()
    novel_dict["alt"] = alt_value
    result = db.novelCollection.insert_one(novel_dict)
    novel_dict["_id"] = str(result.inserted_id)
    return novel_dict

# read novel by MongoDB _id
def read_novel_by_id(novel_id: str):
    novel = db.novelCollection.find_one({"_id": ObjectId(novel_id)})
    if novel:
        novel["_id"] = str(novel["_id"])
        return novel
    return None

# read novel by alt (slugified title)
def read_novel_by_alt(alt: str):
    return db.novelCollection.find_one({"alt": alt})

# update novel by alt
def update_novel_by_alt(alt: str, novel: Novel):
    result = db.novelCollection.update_one({"alt": alt}, {"$set": novel.dict()})
    return result.modified_count > 0

# delete novel by alt
def delete_novel_by_alt(alt: str):
    result = db.novelCollection.delete_one({"alt": alt})
    return result.deleted_count > 0


### HELPER

def ensure_unique_alt(alt: str) -> str:
    """
    Ensure that the alt is unique in the collection.
    If not, append a number to it and check again.
    """
    count = 1
    original_alt = alt
    while db.novelCollection.find_one({"alt": alt}):
        alt = f"{original_alt}-{count}"
        count += 1
    return alt