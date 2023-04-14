### gifs are too big for mailtrap :(
import os
import imageio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import ssl

load_dotenv()

# .env
input_folder = os.getenv("SAVE_PATH")  # The folder containing the JPEG images
output_folder = os.getenv("GIF_PATH")  # The folder for the output GIF
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
email_password = os.getenv("EMAIL_PASSWORD")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

smtp_server = "smtp.mailtrap.io"
port = 587


def send_email(gif_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "New GIF Created"

    # Attach a text message
    text = "Please find the attached GIF."
    message.attach(MIMEText(text, "plain"))

    # Attach the GIF
    with open(gif_path, "rb") as gif:
        img = MIMEImage(gif.read(), name=os.path.basename(gif_path))
        message.attach(img)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(username, password)
        server.send_message(message)

    print(f"Email sent to {receiver_email} with the attached GIF.")


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

# Send an email with the created GIF
send_email(output_file)
