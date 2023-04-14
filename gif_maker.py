import os
import imageio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

input_folder = os.getenv("SAVE_PATH")  # The folder containing the JPEG images
output_folder = os.getenv("GIF_PATH")  # The folder for the output GIF

# Generate the timestamp string
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# Set the output file path with the timestamp
output_file = os.path.join(output_folder, f"giffed_on_{timestamp}.gif")

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

images = []

# Read all JPEG files in the input_folder
for file_name in sorted(os.listdir(input_folder)):
    if file_name.endswith(".jpg"):
        file_path = os.path.join(input_folder, file_name)
        images.append(imageio.imread(file_path))

# Create a GIF from the list of images
imageio.mimsave(output_file, images, format="GIF", duration=0.5)

print(f"GIF created and saved to {output_file}")
