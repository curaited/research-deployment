import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="*", intents=discord.Intents.all())
ready_event = asyncio.Event()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    ready_event.set()

async def request_image_from_discord(tags):
    global client

    # Channel ID where the bot is located
    channel_id = 1095553899647205409

    # Send the command to the Discord bot
    channel = client.get_channel(channel_id)
    command = f'/imagine {" ".join(tags)}' # Update this line to join tags with a space
    sent_message = await channel.send(command)

    # Wait for the bot's response with the image
    def check_response(response):
        return response.author == sent_message.author and response.attachments

    response = await client.wait_for('message', check=check_response)

    # Return the image URL
    return response.attachments[0].url

async def start_bot():
    client.loop.create_task(client.start(discord_token))
    await ready_event.wait()

async def stop_bot():
    await client.close()
