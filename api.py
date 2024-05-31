import requests
import re
import json
import os

class Downloader:
    def __init__(self, url=None, output="./images") -> None:
        self.output = output
        self.url = url
        self.baseURLmanga = "https://api.mangadex.org/chapter?limit=100&manga={}"
        self.baseURLChapter = "https://api.mangadex.org/at-home/server/{}"

    def extractId(self, url):
        pattern = r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"
        uuid = re.search(pattern, url).group(1)
        print(uuid)
        return uuid

    def getChapterData(self, id):
        res = requests.get(self.baseURLmanga.format(id))
        data = res.json().get("data")
        print(json.dumps(data, indent=4))
        ids = []
        chapCount = 0
        seen_chapters = set()  # Set to track seen chapters
        try:
            for chapter in data:
                chapter_num = chapter.get("attributes").get("chapter")
                if chapter.get("attributes").get("translatedLanguage") == "en" and chapter_num not in seen_chapters:
                    seen_chapters.add(chapter_num)  # Mark this chapter as seen
                    ids.append(
                        {
                            "id": chapter.get("id"),
                            "name": f"Chapter {chapter_num or chapCount}",
                        }
                    )
                    chapCount += 1
            for id in ids:
                chapterResponse = requests.get(
                    self.baseURLChapter.format(id.get("id"))
                )
                baseURL = chapterResponse.json().get("baseUrl")
                hash = chapterResponse.json().get("chapter").get("hash")
                imgs = chapterResponse.json().get("chapter").get("data")

                imgUrl = "{}/data/{}/{}"
                count = 1
                for img in imgs:
                    url = imgUrl.format(baseURL, hash, img)
                    imgRes = requests.get(url)
                    img_data = imgRes.content
                    if imgRes.status_code != 200:
                        print(
                            "Failed to download image. Status code:",
                            imgRes.status_code,
                        )
                        return 0
                    output = os.path.join(self.output, id.get("name"))
                    if not os.path.exists(output):
                        os.makedirs(output)
                    image_filename = os.path.join(output, f"{count}.jpg")
                    with open(image_filename, "wb") as image_file:
                        print(
                            f"Downloaded {id.get('name')} : {count}/ {len(imgs)}"
                        )
                        image_file.write(img_data)
                    count += 1
        except Exception as e:
            return e
        return True

    def start(self, url=None):
        if not url:
            url = self.url
        if not url and not self.url:
            print("Please input the url")
            return

        mangaId = self.extractId(url)
        self.getChapterData(mangaId)


if __name__ == "__main__":
    api = Downloader(
        url="https://mangadex.org/title/adce0aea-3f6d-4fd2-9902-1107f59f94da/arafoo-kenja-no-isekai-seikatsu-nikki",
    )
    api.start()
