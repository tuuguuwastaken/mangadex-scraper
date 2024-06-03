import requests
import re
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class Downloader:
    def __init__(self, url=None, output="./images", max_workers=5) -> None:
        self.output = output
        self.url = url
        self.baseURLmanga = "https://api.mangadex.org/chapter?limit=100&manga={}"
        self.baseURLChapter = "https://api.mangadex.org/at-home/server/{}"
        self.max_workers = max_workers

    def extractId(self, url):
        pattern = r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"
        uuid = re.search(pattern, url).group(1)
        print(uuid)
        return uuid

    def download_image(self, url, output_path, chapter_name, img_num, total_imgs):
        imgRes = requests.get(url)
        img_data = imgRes.content
        if imgRes.status_code != 200:
            print(f"Failed to download image {img_num} of {total_imgs} in {chapter_name}. Status code: {imgRes.status_code}")
            return False
        with open(output_path, "wb") as image_file:
            print(f"Downloaded {chapter_name} : {img_num}/{total_imgs}")
            image_file.write(img_data)
        return True

    def download_chapter(self, chapter):
        chapter_id = chapter.get("id")
        chapter_name = chapter.get("name")
        chapterResponse = requests.get(self.baseURLChapter.format(chapter_id))
        baseURL = chapterResponse.json().get("baseUrl")
        hash = chapterResponse.json().get("chapter").get("hash")
        imgs = chapterResponse.json().get("chapter").get("data")

        imgUrl = "{}/data/{}/{}"
        output_dir = os.path.join(self.output, chapter_name)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tasks = []
        with ThreadPoolExecutor(max_workers=len(imgs)) as executor:
            for count, img in enumerate(imgs, start=1):
                url = imgUrl.format(baseURL, hash, img)
                output_path = os.path.join(output_dir, f"{count}.jpg")
                tasks.append(executor.submit(self.download_image, url, output_path, chapter_name, count, len(imgs)))

            for task in as_completed(tasks):
                if not task.result():
                    print(f"An error occurred while downloading an image in {chapter_name}.")
        return True

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

            for chapter in ids:
                self.download_chapter(chapter)

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
