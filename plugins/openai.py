import os
import pyrogram
from pyrogram import Client, filters
import openai
import re

# Set your OpenAI API key here
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

# Authentication code filter
def is_authenticated(client, message):
    return client.get_chat_member(message.chat.id, message.from_user.id).status in ("member", "admin", "creator")

# OpenAI command handler
@Client.on_message(filters.command("openai"))
async def openai_command(client, message):
    text = " ".join(message.text.split(" ")[1:])  # Join the text parts after the command

    # Try to generate a completion from OpenAI
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text,
            max_tokens=4000,
            temperature=0.9,
            top_p=9,
            frequency_penalty=0.5,
            presence_penalty=0.2,
        )
    except Exception as e:
        # If an error occurs, send a message to the user
        await message.reply(f"Error: {e}")
    else:
        # If the completion was successful, send the completion to the user
        if response and response.choices:
            await message.reply(response.choices[0].text)
        else:
            await message.reply("OpenAI failed to generate a completion.")

