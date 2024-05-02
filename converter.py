from PIL import Image
import os

class Converter:
    def __init__(self, input="./images", output="./webps") -> None:
        self.input = input
        self.output = output
        

    def start(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        files = os.listdir(self.input)
        for file in files:
            images = os.listdir(os.path.join(self.input, file))
            if not os.path.exists(os.path.join(self.output, file)):
                os.makedirs(os.path.join(self.output, str(file)))
            for image in images:
                if image.lower().endswith('.png') or image.lower().endswith('.jpg'):
                    img_path = os.path.join(self.input, file, image)
                    output_path = os.path.join(self.output, file, os.path.splitext(image)[0] + '.webp')
                    with Image.open(img_path) as img:
                        img.save(output_path, 'WEBP')


if __name__ == "__main__":
    conv = Converter()
    conv.start()
