from io import StringIO
from contextlib import redirect_stdout
import asyncio
import tempfile
import os
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
#from ProjectDark.helper.basic import format_exc


async def _exec(client: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("Code to execute isn't provided!")
        return

    reply = message.reply_to_message

    code = message.text.split(maxsplit=1)[1]
    stdout = StringIO()

    await message.edit("Executing...")

    try:
        with redirect_stdout(stdout):
            exec(code)
        result = stdout.getvalue()
        if len(result) <= 4096:
            text = (
                f"<code>{code}</code>\n\n"
                "Result:\n"
                f"<code>{result}</code>"
            )
            if message.command[0] == "exnoedit":
                await message.reply(text)
            else:
                await message.edit(text)
        else:
            with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
                temp_file.write(result)
                temp_file_path = temp_file.name

            await message.reply_document(document=temp_file_path)

            os.remove(temp_file_path)
    except Exception as e:
        error_message = f"<code>{traceback.format_exc()}</code>"
        await message.edit(error_message)

@Client.on_message(filters.command(["ex", "exec"], cmd) & filters.me)
async def execute(client: Client, message: Message):
    await _exec(client, message)
    

@Client.on_message(filters.command("logs", cmd) & filters.me)
async def _logs(client: Client, message: Message):
    edit_msg = await message.edit("Sending...")
    
    if not os.path.exists("logs.txt"):
        await edit_msg.edit("None!")
        return
    
    await client.send_document(
        message.chat.id,
        "logs.txt",
        reply_to_message_id=message.id,
    )
    
    await message.delete()
