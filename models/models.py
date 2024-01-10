from pydantic import BaseModel
from typing import Dict, Union

# Novel
class Novel(BaseModel):
    title: str
    noOfVolumes: int
    imageURL: str
    malLink: str
    rank: int
    trend: int
    genre: str
    author: str
    synopsis: str

class NovelInDB(Novel):
    _id: str

# Volume
class Volume(BaseModel):
    novelId: str
    volumeNumber: int
    noOfChapters: int

class VolumeInDB(Volume):
    _id: str

# Raw chapter
class Content(BaseModel):
    raw_content: str

class RawChapter(BaseModel):
  volumeId: str
  rawChaptersVolumeNumber: int
  chapters: Dict[str, Union[str, Content]]

class RawChapterInDB(RawChapter):
    _id:str

# Chapter
class Chapter(BaseModel):
  volumeId: str
  chapterNumber: int
  noOfPages: int

class ChapterInDB(Chapter):
  _id: str

# Page
class Page(BaseModel):
    chapterId: str
    pageNumber: int
    content: str

class PageInDB(Page):
    _id: str

