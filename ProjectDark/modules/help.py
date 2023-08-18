# Part of PyroMan - 2022
# Kang by DarkPyro - 2023


from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER
from ProjectDark import CMD_HELP
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.helpers.utility import split_list

@Client.on_message(filters.command("help", CMD_HANDLER) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        help_message = "Available Modules:\n"
        for module in sorted(CMD_HELP.keys()):
            help_message += f"| `{module}` "
        await edit_or_reply(message, help_message)
        
    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"""
{str(help_arg)} Description
"""
            for cmd, function in commands.items():
                this_command += f"""
`{CMD_HANDLER}{cmd}`
    {function}
"""
            await edit_or_reply(message, this_command, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            await edit_or_reply(message, f"{help_arg} invalid module!")


def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict



@Client.on_message(filters.command("DISCLAIMER", CMD_HANDLER) & filters.me)
async def disclaimer(client: Client, message: Message):
    disclaimer = """
<b>DISCLAIMER (Indonesian)</b>

(A) Repo sepenuhnya bukan hasil karya kami, melainkan hanya meng-copy dari beberapa repo userbot yang ada.
(B) Kami tidak menyarankan Anda untuk menggunakan repo kami di akun utama.
(C) Hindari untuk menggunakan command gcast terlalu sering, jika memungkinkan jangan digunakan.

<b>Catatan:</b>
1) Kami tidak menambahkan daftar hitam,
2) Jika dikemudian hari akun Anda diban di beberapa grup dan mengalami limit oleh @SpamBot atau lebih fatalnya akun Anda dibanned oleh telegram (Silahkan baca kembali poin B, C).

<b>Tambahan:</b>
Kami menambahkan command <code>devil</code> [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/64e762f4e27aeed23a3109ac91ec3e99caa5d1d6/ProjectDark/modules/network.py#L27'>Read Code</a>] untuk memudahkan dalam mengecek user yang menggunakan userbot, dan hanya bekerja jika anda bergabung di grup support kami.
"""
    await edit_or_reply(message, disclaimer, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)


add_command_help(
    "DISCLAIMER",
    [
        ["DISCLAIMER",
        "Read disclaimer of userbot.",
        ],
    ],
)