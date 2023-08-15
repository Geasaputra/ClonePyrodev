# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

from pyrogram import Client, filters
from pyrogram.types import Message

from config import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply

from .help import add_command_help


@Client.on_message(filters.command("create", cmd) & filters.me)
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await edit_or_reply(
            message, f"Type `{cmd}help create` for more."
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    Dark = await edit_or_reply(message, "Processing...")
    desc = "Welcome to my" + ("group" if group_type == "gc" else "channel")
    if group_type == "gc":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id["id"])
        await Dark.edit(
            f"Successfully create group: [{group_name}]({link['invite_link']})",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id["id"])
        await Dark.edit(
            f"Successfully create channel: [{group_name}]({link['invite_link']})",
            disable_web_page_preview=True,
        )


add_command_help(
    "create",
    [
        ["create ch <tittle>",
        "Create a channel."
        ],
        
        ["create gc <tittle>",
        "Create a group."],
    ],
)
