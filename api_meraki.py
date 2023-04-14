import httpx
import json


API_KEY = "144bb12832b630a6a4b5ed431b174c84ed50d197"
NETWORK_ID = "L_828099381482758539"
CAMERA_SERIAL = "Q2MV-KCHZ-2DBB"
SAVE_PATH = "./cam_shot"


# Retrieve a snapshot URL
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


async def main():
    snapshot_url = await get_snapshot_url(API_KEY, NETWORK_ID, CAMERA_SERIAL)

    if snapshot_url:
        print(f"Snapshot URL: {snapshot_url}")
    else:
        print("Failed to get the snapshot URL.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
