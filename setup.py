from cx_Freeze import setup, Executable

setup(
    name="Mangadex download and converter",
    version="1.0",
    description="Description of your application",
    executables=[Executable("mangadex-downloader.py")],
)
