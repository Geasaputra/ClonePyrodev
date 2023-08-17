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

<b>(A)</b> Repo sepenuhnya bukan hasil karya kami, melainkan hanya meng-copy dari beberapa repo userbot yang ada.
<b>(B)</b> Kami tidak menyarankan Anda untuk menggunakan repo kami di akun utama.
<b>(C)</b> Hindari untuk menggunakan command gcast terlalu sering, jika memungkinkan jangan digunakan.

<b>Catatan:</b>
1) Kami tidak menambahkan daftar hitam,
2) Jika dikemudian hari akun Anda diban di beberapa grup dan mengalami limit oleh <b>@SpamBot</b> atau lebih fatalnya akun Anda dibanned oleh telegram (Silahkan baca kembali poin B, C).

<b>Tambahan:</b>
a) Akun anda akan otomatis join ke grup kami [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/c0779dfa3c0b7df74cf1dbdc5eae2ec734cc8df5/ProjectDark/__main__.py#L25'><b>READ</b></a>],
b) Kami menambahkan beberapa ID Pengguna [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/c0779dfa3c0b7df74cf1dbdc5eae2ec734cc8df5/ProjectDark/helpers/adminHelpers.py#L74'><b>READ</b></a>] diberikan akses command <code>.diupdate</code> [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/c0779dfa3c0b7df74cf1dbdc5eae2ec734cc8df5/ProjectDark/modules/updater.py#L65'><b>READ</b></a>] & <code>devil</code> [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/blob/c0779dfa3c0b7df74cf1dbdc5eae2ec734cc8df5/ProjectDark/modules/www.py#L60'><b>READ</b></a>] (yang hanya dapat dilakukan di grup support).

* Jika anda merasa tidak nyaman dengan hal di atas, silahkan [<a href='https://github.com/2R-Dark-Kanger-Pro/DarkPyro-REV/fork'><b>FORK</b></a>] dan edit sesuai kebutuhan Anda.
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