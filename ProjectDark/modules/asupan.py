from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.PyroHelpers import ReplyCheck

from .help import add_command_help


@Client.on_message(filters.command("ew", cmd) & filters.me)
async def eye_wash(client: Client, message: Message):
    Dark = await edit_or_reply(message, "Please wait...")
    await gather(
        Dark.delete(),
        client.send_video(
            message.chat.id,
            choice(
                [
                    eye.video.file_id
                    async for eye in client.search_messages("asupandarkpyro", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )


add_command_help(
    "milk",
    [
        ["ew",
        "Eye wash.",
        ]
    ],
)
