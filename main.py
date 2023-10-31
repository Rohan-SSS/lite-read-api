from fastapi import FastAPI, HTTPException
from crud.crud_novel import *

app = FastAPI()

# create novel
@app.post("/novel/", response_model=NovelInDB)
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
@app.get("/novel/{alt}", response_model=NovelInDB)
async def read_novel_by_alt_endpoint(alt: str):
    novel = read_novel_by_alt(alt)
    if novel:
        return novel
    raise HTTPException(status_code=404, detail="Resource not found")

# update novel by alt
@app.put("/novel/alt/{alt}", response_model=NovelInDB)
async def update_novel_by_alt_endpoint(alt: str, novel: Novel):
    updated = update_novel_by_alt(alt, novel)
    if updated:
        updated_novel = read_novel_by_alt(alt)
        return updated_novel
    raise HTTPException(status_code=404, detail="Resource not found or couldn't be updated")

# delete novel by alt
@app.delete("/novel/alt/{alt}", response_model=dict)
async def delete_novel_by_alt_endpoint(alt: str):
    deleted = delete_novel_by_alt(alt)
    if deleted:
        return {"status": "success", "message": f"Novel {alt} deleted."}
    raise HTTPException(status_code=404, detail="Resource not found or couldn't be deleted")









# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Optional, List
# import time

# app = FastAPI()

# origins = ['http://localhost:3000']

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Message(BaseModel):
#     message: str

# @app.post("/api/chat")
# async def chat_endpoint(message: Message):
#     time.sleep(3)
#     return {"reply": f"Mock response for: {message.message}"}

# # Sample chapter data structure
# chapter_data = {
#     1: {
#         "pages": {
#             1: {
#                 "content": "Summary of page 1-3",
#                 "pageRange": "1-3"
#             },
#             2: {
#                 "content": "Summary of page 4-6",
#                 "pageRange": "4-6"
#             },
#             3: {
#                 "content": "Summary of page 7-9",
#                 "pageRange": "7-9"
#             }
#         }
#     },
#     2: {
#         "pages": {
#             4: {
#                 "content": "Summary of page 10-12",
#                 "pageRange": "10-12"
#             },
#             5: {
#                 "content": "Summary of page 13-15",
#                 "pageRange": "13-15"
#             }
#             # ... Add more chapters as needed
#         }
#     }
# }

# @app.get("/api/chapter-data")
# def get_chapter_data(page: int = 1):
#     for chapter, details in chapter_data.items():
#         if page in details["pages"]:
#             return {
#                 "chapter": chapter,
#                 "content": details["pages"][page]["content"],
#                 "pageRange": details["pages"][page]["pageRange"]
#             }
#     return {
#         "chapter": "Unknown",
#         "content": "Content not found",
#         "pageRange": "Unknown"
#     }

# @app.get("/api/pages", response_model=List[int])
# def get_pages():
#     pages = []
#     for details in chapter_data.values():
#         pages.extend(details["pages"].keys())
#     return pages

# @app.get("/api/story")
# def get_story(page: int = 1):
#     for chapter, details in chapter_data.items():
#         if page in details["pages"]:
#             return {
#                 "text": details["pages"][page]["content"]
#             }
#     return {
#         "text": "Content not found for this page."
#     }