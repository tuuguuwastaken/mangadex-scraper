from converter import Converter
from api import Downloader

if __name__ == "__main__":
    url = input("enter Mangadex Link :")
    downloader = Downloader(url)
    converter = Converter()