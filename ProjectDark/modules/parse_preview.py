# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils.sections import section

from .help import add_command_help


@Client.on_message(filters.command("parse", cmd) & filters.me)
async def parse(client: Client, message: Message):
    r = message.reply_to_message
    has_wpp = False
    if not r:
        return await edit_or_reply(message, "Reply to a message with a webpage.")
    m_ = await edit_or_reply(message, "Parsing...")
    if not r.web_page:
        text = r.text or r.caption
        if text:
            m = await client.send_message("me", text)
            await sleep(1)
            await m.delete()
            if m.web_page:
                r = m
                has_wpp = True
    else:
        has_wpp = True
    if not has_wpp:
        return await m_.edit(
            "Replied message has no webpage preview.",
        )
    wpp = r.web_page
    body = {
        "Title": [wpp.title or "null"],
        "Description": [(wpp.description[:50] + "...") if wpp.description else "null"],
        "URL": [wpp.display_url or "null"],
        "Author": [wpp.author or "null"],
        "Site Name": [wpp.site_name or "null"],
        "Type": wpp.type or "null",
    }
    text = section("Preview", body)
    t = wpp.type
    if t == "Photo":
        media = wpp.photo
        func = client.send_photo
    elif t == "Audio":
        media = wpp.audio
        func = client.send_audio
    elif t == "Video":
        media = wpp.video
        func = client.send_video
    elif t == "Document":
        media = wpp.document
        func = client.send_document
    else:
        media = None
        func = None
    if media and func:
        await m_.delete()
        return await func(
            m_.chat.id,
            media.file_id,
            caption=text,
        )
    await m_.edit(text, disable_web_page_preview=True)


add_command_help(
    "parse",
    [
        ["parse",
        "Parse a preview link.",
        ],
    ],
)
