from setuptools import setup

setup(
	name = "deezeridu",
	version = "0.0.1a2",
	description = "Downloads songs, albums or playlists from deezer",
	long_description_content_type = "text/markdown",
	license = "CC BY-NC-SA 4.0",
	python_requires = ">=3.8",
	author = "An0nimia",
	author_email = "An0nimia@protonmail.com",
	url = "https://github.com/An0nimia/deezloader",
	packages = ["deezeridu", "deezeridu/models"],

	install_requires = [
		"mutagen", "pycryptodomex", "requests", "tqdm"
	]
)
