from setuptools import setup

setup(
	name = "deezeridu",
	version = "0.0.1a3",
	description = "Downloads songs, albums or playlists from deezer",
	long_description_content_type = "text/markdown",
	license = "CC BY-NC-SA 4.0",
	python_requires = ">=3.8",
	author = "An0nimia",
	url = "https://github.com/OpenJarbas/deezeridu",
	packages = ["deezeridu", "deezeridu/models"],
	install_requires = [
		"mutagen", "pycryptodomex", "requests", "tqdm"
	]
)
