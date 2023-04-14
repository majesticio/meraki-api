# Meraki Camera Snapshot Downloader

This script downloads snapshots from a Meraki camera and saves them to the specified folder. It uses the Meraki API to get the snapshot URL and then downloads the image.

## Installation

1. Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed.

2. Clone this repository:

```
git clone https://github.com/majesticio/meraki-api.git
cd meraki-python
```

3. Install the required dependencies:

```
poetry install
```


4. Create a `.env` file with your Meraki API Key, Network ID, Camera Serial, and Save Path:

```bash
API_KEY=your_api_key
NETWORK_ID=your_network_id
CAMERA_SERIAL=your_camera_serial
SAVE_PATH=path/to/saved/image/folder
GIF_PATH=path/to/gif/folder
```


## Usage
> The script will download a snapshot from the specified camera and save it to the folder specified in the `.env` file.

1. Run the script with Poetry:
*example*
```
poetry run python save_image.py
```

## GIF maker
> *will take all the saved images and make a GIF!*
```
poetry run python gif_maker.py
```
