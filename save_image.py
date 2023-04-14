import httpx
import asyncio
import os
import io
from PIL import Image, UnidentifiedImageError
from datetime import datetime

API_KEY = "144bb12832b630a6a4b5ed431b174c84ed50d197"
NETWORK_ID = "L_828099381482758539"
CAMERA_SERIAL = "Q2MV-KCHZ-2DBB"
SAVE_PATH = "./cam_shot"


async def get_snapshot_url(api_key, network_id, camera_serial, timestamp=None):
    url = f"https://api.meraki.com/api/v0/networks/{network_id}/cameras/{camera_serial}/snapshot"

    headers = {"X-Cisco-Meraki-API-Key": api_key, "Content-Type": "application/json"}

    payload = {}

    if timestamp:
        payload["timestamp"] = timestamp

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code == 200 or response.status_code == 202:
        return response.json()["url"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


import time


async def save_image_from_url(url, save_path, max_retries=5, retry_interval=5):
    headers = {"Accept": "image/jpeg"}

    for retry_count in range(max_retries):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200 or 202:
            try:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))

                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                file_name = os.path.join(save_path, f"snapshot_{timestamp}.jpg")
                image.save(file_name)
                print(f"Snapshot saved to {file_name}")
                break
            except UnidentifiedImageError:
                if retry_count < max_retries - 1:
                    print(
                        f"Image not ready yet. Retrying in {retry_interval} seconds..."
                    )
                    await asyncio.sleep(retry_interval)
                else:
                    print("Failed to fetch the image after multiple retries.")
        else:
            print(f"Error {response.status_code}: {response.text}")
            break


async def main():
    snapshot_url = await get_snapshot_url(API_KEY, NETWORK_ID, CAMERA_SERIAL)

    if snapshot_url:
        print(f"Snapshot URL: {snapshot_url}")
        await save_image_from_url(snapshot_url, SAVE_PATH)
    else:
        print("Failed to get the snapshot URL.")


if __name__ == "__main__":
    asyncio.run(main())
