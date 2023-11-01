ObjectId = None

novel_collection = {
  "_id": ObjectId("someId1"),
  "title": "novelTitle",
  "noOfVolumes": "number",
  "imageURL":"link",
  "malLink":"link",
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
  "pageNumber":"number",
  "content":"content"
}