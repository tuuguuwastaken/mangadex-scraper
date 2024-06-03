from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor

class Converter:
    def __init__(self, input_dir="./images", output_dir="./webps") -> None:
        self.input_dir = input_dir
        self.output_dir = output_dir

    def convert_image(self, img_info):
        file, image = img_info
        img_path = os.path.join(self.input_dir, file, image)
        output_path = os.path.join(self.output_dir, file, os.path.splitext(image)[0] + '.webp')
        with Image.open(img_path) as img:
            img.save(output_path, 'WEBP')
        print(f"Converted {file}/{image}")

    def process_chapter(self, chapter):
        images = os.listdir(os.path.join(self.input_dir, chapter))
        if not os.path.exists(os.path.join(self.output_dir, chapter)):
            os.makedirs(os.path.join(self.output_dir, chapter))
        for image in images:
            if image.lower().endswith('.png') or image.lower().endswith('.jpg'):
                self.convert_image((chapter, image))

    def start(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        chapters = os.listdir(self.input_dir)
        
        with ThreadPoolExecutor(max_workers=40) as executor:
            executor.map(self.process_chapter, chapters)

        return True

if __name__ == "__main__":
    conv = Converter()
    conv.start()
