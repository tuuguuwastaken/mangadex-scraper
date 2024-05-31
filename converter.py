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

    def start(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        files = os.listdir(self.input_dir)
        tasks = []

        for file in files:
            images = os.listdir(os.path.join(self.input_dir, file))
            if not os.path.exists(os.path.join(self.output_dir, file)):
                os.makedirs(os.path.join(self.output_dir, file))

            for image in images:
                if image.lower().endswith('.png') or image.lower().endswith('.jpg'):
                    tasks.append((file, image))

        with ThreadPoolExecutor() as executor:
            executor.map(self.convert_image, tasks)

        return True

if __name__ == "__main__":
    conv = Converter()
    conv.start()
