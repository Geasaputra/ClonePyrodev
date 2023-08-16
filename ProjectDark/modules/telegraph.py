# Part of PyroMan - 2022
# Kang by DarkPyro - 2023


from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, exceptions, upload_file

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply, get_text
from ProjectDark.helpers.tools import *

from .help import *

telegraph = Telegraph()
r = telegraph.create_account(short_name="DarkPyro-Userbot")
auth_url = r["auth_url"]


@Client.on_message(filters.command("tgraph", cmd) & filters.me)
async def uptotelegraph(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Processing...")
    if not message.reply_to_message:
        await Dark.edit(
            "Reply to message!"
        )
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await Dark.edit(f"{exc}")
            os.remove(m_d)
            return
        U_done = (
            f"[Successfully](https://telegra.ph/{media_url[0]})!"
        )
        await Dark.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await Dark.edit(f"{exc}")
            return
        wow_graph =f"[Successfully](https://telegra.ph/{response['path']})!"
        await Dark.edit(wow_graph)


add_command_help(
    "telegraph",
    [
        ["tgraph",
        "Reply to Text or media to upload it to the telegraph.",
        ],
    ],
)
