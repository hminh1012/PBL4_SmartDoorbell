import time
import names
import firebase
import cloudinary
import cloudinary.uploader
import datetime

thoigian = datetime.datetime.now()



# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name="dyrabqcno",
    secure = True,
    api_key="885437657119333",
    api_secret="JrlYz1bz-cKtqwtLJ7RYxetVLmU"
)

# Upload the image
response = cloudinary.uploader.upload(
    "example.jpg",  # Path to your image
    public_id = names.get_full_name(),        # Optional: specify a unique ID for the file
    overwrite=True            # Optional: overwrite if the same public ID exists
)

# Print the response
print("Uploaded Successfully!")
print(f"URL: {response['secure_url']}")




# Configure Cloudinary using environment variables
cloudinary.config(
    cloud_name="dyrabqcno",
    secure = True,
    api_key="885437657119333",
    api_secret="JrlYz1bz-cKtqwtLJ7RYxetVLmU"
)

# Upload the image
response = cloudinary.uploader.upload(
    "buglarly.jpg",  # Path to your image
    public_id=names.get_full_name(),        # Optional: specify a unique ID for the file
    overwrite=True            # Optional: overwrite if the same public ID exists
)

# Print the response
print("Uploaded Successfully!")
print(f"URL: {response['secure_url']}")


# Firebase configuration
config = {
  "apiKey": "AIzaSyAamS-omT7i-1fFFuwHr5k8_ILt0ptNl3E",
  "authDomain": "pidrowsiness-277a4.firebaseapp.com",
  "databaseURL": "https://pidrowsiness-277a4-default-rtdb.firebaseio.com",
  "projectId": "pidrowsiness-277a4",
  "storageBucket": "pidrowsiness-277a4.appspot.com",
  "messagingSenderId": "443787716450",
  "appId": "1:443787716450:web:c7033070895e50b0e56e3b",
  "measurementId": "G-KBBZSE34Y3"
}

# Instantiates a Firebase app
app = firebase.initialize_app(config)

db = app.database()

# File to store in storage
file_path = '/home/pi/PBL4/buglarly.jpg'



data = {"Link_Jitsi_Meet": "",
"Link_image": response['secure_url'],
"Time": thoigian.strftime("%c")}
db.child("Status").set(data)
# Add a 5-second delay between pushes
time.sleep(0.1)
print(data)
