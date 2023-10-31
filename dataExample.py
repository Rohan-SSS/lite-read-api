
ObjectId = None

novel_collection = {
  "_id": ObjectId("someId1"),
  "title": "novelTitle",
  "novelId": "number",
  "noOfVolumes": "number",
  "imageURL":"link",
  "alt":"novelTitleSluged",
  "rank":"number",
  "trend":"number"
}

volumes_collection={
  "_id": ObjectId("someId2"),
  "novelId": ObjectId("someId1"),
  "volumeNumber": "number",
  "noOfChapters": "number"
}

chpaters_volume={
  "_id": ObjectId("someId3"),
  "volumeId": ObjectId("someId2"),
  "chapterNumber": "number",
  "noOfPages": "number"
}

pages_collection={
  "_id": ObjectId("someId4"),
  "chapterId": ObjectId("someId3"),
  "pages": {
    "1": "V2 C1 Page 1 content ...",
    "2": "V2 C1 Page 2 content ..."
  }
}