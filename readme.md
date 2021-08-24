# Deezeridu

Downloads songs, albums or playlists from deezer

# Install

`pip install deezeridu`

# Usage

```python
import deezeridu

api = deezeridu.API()
tracks = api.search_track("black metal ist krieg")
track = tracks["data"][0]
url = track["link"]

dz = deezeridu.Deezer(email="me@fakemail.com", password="supersafepassword")
dz.download(url, output_dir="songs")
```

# Credits

forked from https://pypi.org/project/deezloader