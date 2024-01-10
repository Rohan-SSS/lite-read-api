from models.database import db
from models.models import Page
from bson import ObjectId


# create page
def create_page(chapterId: str, page: Page):
    page_dict = page.dict()
    page_dict["chapterId"] = ObjectId(chapterId)
    result = db.pageCollection.insert_one(page_dict)
    page_dict["_id"] = str(result.inserted_id)
    page_dict["chapterId"] = str(page_dict["chapterId"])
    return page_dict

# read page by chapter's novelId, volumeNumber, chapterNumber, and pageNumber
def read_page_by_id(novel_alt:str, volumeNumber:int, chapterNumber:int, pageNumber:int):
    novel = db.novelCollection.find_one({"alt": novel_alt})
    if novel:
        volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
        if volume:
            chapter = db.chapterCollection.find_one({"volumeId": volume["_id"], "chapterNumber": chapterNumber})
            if chapter:
                return db.pageCollection.find_one({"chapterId": chapter["_id"], "pageNumber": pageNumber})
    return None

# update page by chapter's novelId, volumeNumber, chapterNumber, and pageNumber
def update_page_by_id(novel_alt:str, volumeNumber: int, chapterNumber:int, pageNumber:int, page: Page):
    page_data = read_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
    if page_data:
        update_data = page.dict(exclude={"chapterId"})
        result = db.pageCollection.update_one({"_id": page_data["_id"]}, {"$set": update_data})
        return result.modified_count > 0
    return False

# delete page by chapter's novelId, volumeNumber, chapterNumber, and pageNumber
def delete_page_by_id(novel_alt: str, volumeNumber: int, chapterNumber:int, pageNumber:int):
    page_data = read_page_by_id(novel_alt, volumeNumber, chapterNumber, pageNumber)
    if page_data:
        result = db.pageCollection.delete_one({"_id": page_data["_id"]})
        return result.deleted_count > 0
    return False

























# from pydantic import BaseModel
# from database import db
# from bson import ObjectId


# # db schema
# class Page(BaseModel):
#   chapterId: str
#   pages: dict

# class PageInDB(Page):
#   _id: str


# # create page
# def create_page_by_chapter_id(chapterId:str, pages:dict):
#   pages_dict = pages.dict()
#   pages_dict["chapterId"]:ObjectId(chapterId)
#   result = db.pageCollection.insert_one(pages_dict)
#   pages_dict["_id"] = str(result.inserted_id)
#   pages_dict["chapterId"] = str(pages_dict["chapterId"])
#   return pages_dict

# # read a specific page inside the pages dictionary for a given chapterId
# def read_specific_page_by_chapter_id(novel_alt:str, volumeNumber:int, chapterNumber:int, pageNumber:int):
#   novel = db.novelCollection.find_one({"alt":novel_alt})
#   if novel:
#     volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber":volumeNumber})
#     if volume:
#       chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber":chapterNumber})
#       if chapter:
#         page = db.pageCollection.find_one({"chapterId": ObjectId(chapter["_id"])})
#         if page:
#           return page["pages"].get(str(pageNumber))
#   return None

# # read the whole dictionary for a given chapterId
# def read_pages_collection_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber: int):
#     novel = db.novelCollection.find_one({"alt": novel_alt})
#     if novel:
#         volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
#         if volume:
#             chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber": chapterNumber})
#             if chapter:
#                 page_data = db.pageCollection.find_one({"chapterId": ObjectId(chapter["_id"])})
#                 if page_data:
#                     page_data["_id"] = str(page_data["_id"])
#                     page_data["chapterId"] = str(page_data["chapterId"])
#                     return page_data
#     return None

# # update a specific page inside the pages dictionary for a given chapterId
# def update_specific_page_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber: int, pageNumber: int, content: str):
#     novel = db.novelCollection.find_one({"alt": novel_alt})
#     if novel:
#         volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
#         if volume:
#             chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber": chapterNumber})
#             if chapter:
#                 update_key = f"pages.{pageNumber}"
#                 result = db.pageCollection.update_one({"chapterId": ObjectId(chapter["_id"])}, {"$set": {update_key: content}})
#                 return result.modified_count > 0
#     return False

# # update the whole dictionary for a given chapterId
# def update_page_collection_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber: int, pages: dict):
#     novel = db.novelCollection.find_one({"alt": novel_alt})
#     if novel:
#         volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
#         if volume:
#             chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber": chapterNumber})
#             if chapter:
#                 result = db.pageCollection.update_one({"chapterId": ObjectId(chapter["_id"])}, {"$set": {"pages": pages}})
#                 return result.modified_count > 0
#     return False

# # delete a specific page inside the pages dictionary for a given chapterId
# def delete_specific_page_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber: int, pageNumber: int):
#     novel = db.novelCollection.find_one({"alt": novel_alt})
#     if novel:
#         volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
#         if volume:
#             chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber": chapterNumber})
#             if chapter:
#                 delete_key = f"pages.{pageNumber}"
#                 result = db.pageCollection.update_one({"chapterId": ObjectId(chapter["_id"])}, {"$unset": {delete_key: ""}})
#                 return result.modified_count > 0
#     return False

# # delete the whole dictionary for a given chapterId
# def delete_pages_collection_by_chapter_id(novel_alt: str, volumeNumber: int, chapterNumber: int):
#     novel = db.novelCollection.find_one({"alt": novel_alt})
#     if novel:
#         volume = db.volumeCollection.find_one({"novelId": ObjectId(novel["_id"]), "volumeNumber": volumeNumber})
#         if volume:
#             chapter = db.chapterCollection.find_one({"volumeId": ObjectId(volume["_id"]), "chapterNumber": chapterNumber})
#             if chapter:
#                 result = db.pageCollection.delete_one({"chapterId": ObjectId(chapter["_id"])})
#                 return result.deleted_count > 0
#     return False