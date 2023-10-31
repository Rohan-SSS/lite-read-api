from pydantic import BaseModel
from database import db
from bson import ObjectId

### 65402f56b0ed2cc479a04653
import re
from slugify import slugify

class Novel(BaseModel):
    title: str
    noOfVolumes: int
    imageURL: str
    rank: int
    trend: int

class NovelInDB(Novel):
    _id: str

# create novel
def create_novel(novel: Novel):
    alt_value = slugify(novel.title)
    alt_value = ensure_unique_alt(alt_value)
    novel_dict = novel.dict()
    novel_dict["alt"] = alt_value
    result = db.novelCollection.insert_one(novel_dict)
    novel_dict["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return novel_dict  # Return the entire novel document

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


### Helper Fn

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