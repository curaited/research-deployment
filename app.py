import os
import asyncio
from flask import Flask, request, jsonify, render_template
import discord_bot
import threading
import atexit
import json
import random

#open JSOn file that stores the metadata fro the image library
with open('image_metadata.json') as f:
    image_metadata = json.load(f)

app = Flask(__name__, static_folder='static')

loop = None

#define the functions that select a random image with the mathcing tags
def select_image(room_type, style):
    matching_images = [image for image in image_metadata if image['room_type'] == room_type and image['style'] == style]
    selected_image = random.choice(matching_images)
    return selected_image['filename']

@app.before_first_request
def setup_event_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/generate-image", methods=["POST"])
def generate_image():
    global loop
    data = request.get_json()
    tags = data.get("tags", [])
    room_type, style = tags
    use_random_image = data.get("use_random_image", False)
    #determine if the discord bot should be called
    if use_random_image:
        #use the discord bot to generate the images_folder
        image_url = loop.run_until_complete(discord_bot.request_image_from_discord(tags))

    else:
        #use a local image (not that we will wan tto integrate cloud storage here)
        image_filename = select_image(room_type,style)
        image_url = f'/static/images/{image_filename}'
    return jsonify({"image_url": image_url})

if __name__ == '__main__':
    # Start the Discord bot in a separate thread
    bot_thread = threading.Thread(target=discord_bot.start_bot)
    bot_thread.start()

    # Run the Flask app
    app.run(debug=True)

    # Stop the Discord bot when the Flask app stops
    atexit.register(asyncio.run, discord_bot.stop_bot()) # There was a missing parenthesis here
