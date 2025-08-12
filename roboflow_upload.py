import os
import requests
from roboflow import Roboflow

# Replace with your API key, workspace ID, and project ID
ROBOFLOW_KEY = os.getenv("ROBOFLOW_KEY")  # Or hardcode
rf = Roboflow(api_key=ROBOFLOW_KEY)
project = rf.workspace("fieldsync-computer-vision").project("tower-properties-zragi")

# Path to folder with images
folder_path = r"C:\Users\LucyKien\Desktop\TESTFOLDER\bottom"

# Loop through files in the folder and upload them
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".json")):
        file_path = os.path.join(folder_path, file_name)
        print(f"Uploading {file_name}...")
        project.upload(file_path)