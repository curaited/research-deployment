import os
import json

# Set the path to the images folder
images_folder = 'static/images'

# List all the image files in the folder
image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg'))]

# Initialize an empty list to store image metadata
image_metadata = []

# Loop through the image files
for image_file in image_files:
    # Split the filename (without extension) into parts
    parts = os.path.splitext(image_file)[0].split('_')

    # Extract room type and style from the filename parts
    room_type = parts[0]
    style = parts[1]

    # Create a dictionary with the metadata for this image
    metadata = {
        'filename': image_file,
        'room_type': room_type,
        'style': style
    }

    # Add the metadata to the list
    image_metadata.append(metadata)

# Save the metadata list as a JSON file
with open('image_metadata.json', 'w') as f:
    json.dump(image_metadata, f, indent=2)
