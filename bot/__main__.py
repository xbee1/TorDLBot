import shutil, psutil
import signal
import pickle
from pyrogram import idle
from bot import app
from os import execl, kill, path, remove
from sys import executable
from datetime import datetime
import pytz
import time
from telegram import ParseMode, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime, IMAGE_URL
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, anime, stickers, search, delete, speedtest, usage, mediainfo

now=datetime.now(pytz.timezone('Asia/Jakarta'))


@run_async
def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    current = now.strftime('%Y/%m/%d %I:%M:%S %p')
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>╭───┃🎖𝔹𝕆𝕋  𝕊𝕋𝔸𝕋𝕀𝕊𝕋𝕀ℂ𝕊🎖┃</b>\n' \
            f'<b>│</b>\n' \
            f'<b>├⏰𝐁𝐨𝐭𝐔𝐩𝐭𝐢𝐦𝐞:</b> {currentTime}\n' \
            f'<b>╰⏱𝐒𝐭𝐚𝐫𝐭𝐓𝐢𝐦𝐞:</b> {current}\n\n' \
            f'<b>╭─🧰𝐓𝐨𝐭𝐚𝐥𝐃𝐢𝐬𝐤 space:</b> {total}\n' \
            f'<b>├─📮𝐔𝐬𝐞𝐝:</b> {used}\n' \
            f'<b>╰─🏮𝐅𝐫𝐞𝐞:</b> {free}\n\n' \
            f'╭───┃🕹 𝐃𝐀𝐓𝐀 𝐔𝐒𝐀𝐆𝐄 🕹┃\n<b>├─🔺Upload:</b> {sent}\n' \
            f'<b>├─🔻𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝:</b> {recv}\n' \
            f'<b>├─📟𝐂𝐏𝐔:</b> {cpuUsage}%\n' \
            f'<b>├─💾𝐑𝐀𝐌:</b> {memory}%\n' \
            f'<b>├─💿𝐃𝐢𝐒𝐊:</b> {disk}%\n' \
            f'<b>│</b>\n' \
            f'<b>╰─┃🏆@ANonYmoUS_FriEND🏆┃</b>'
    update.effective_message.reply_photo(IMAGE_URL, stats, parse_mode=ParseMode.HTML)


@run_async
def start(update, context):
    start_string = f'''
𝚃𝚑𝚒𝚜 𝚋𝚘𝚝 𝚌𝚊𝚗 𝚖𝚒𝚛𝚛𝚘𝚛 𝚊𝚕𝚕 𝚢𝚘𝚞𝚛 𝚕𝚒𝚗𝚔𝚜 𝚝𝚘 𝙶𝚘𝚘𝚐𝚕𝚎 𝚍𝚛𝚒𝚟𝚎🔰❗️ 𝐄𝐍𝐆𝐢𝐍𝐄-𝐪𝐁𝐢𝐭𝐭𝐎𝐫𝐫𝐞𝐧𝐭⚡️
𝚝𝚢𝚙𝚎 /{BotCommands.HelpCommand} 𝚝𝚘 𝚐𝚎𝚝 𝚊 𝚕𝚒𝚜𝚝 𝚘𝚏 𝚊𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜😌
'''
    update.effective_message.reply_photo(IMAGE_URL, start_string, parse_mode=ParseMode.MARKDOWN)


@run_async
def repo(update, context):
    button = [
    [InlineKeyboardButton("🛠 𝕆𝕎ℕ𝔼ℝ 🛠", url=f"https://t.me/ANonYmoUS_FriEND")],
    [InlineKeyboardButton("🛠 𝐎𝐖𝐍𝐄𝐑 🛠", url=f"https://t.me/ANonYmoUS_FriEND")]]
    reply_markup = InlineKeyboardMarkup(button)
    update.effective_message.reply_photo(IMAGE_URL, reply_markup=reply_markup)


@run_async
def restart(update, context):
    restart_message = sendMessage("🤯Restarting, Please wait❗️", context.bot, update)
    LOGGER.info(f'Restarting the Bot...')
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("𝕊𝕥𝕒𝕣𝕥𝕚𝕟𝕘 ℙ𝕚𝕟𝕘🖲", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help(update, context):
    help_string_adm = f'''
/{BotCommands.HelpCommand}: To get this message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the link to Google Drive.

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link]: Starts mirroring and if downloaded file is any archive, extracts it to Google Drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Start mirroring and upload the archived (.tar) version of the download

/{BotCommands.CloneCommand}: Copy file/folder to Google Drive

/{BotCommands.DeleteCommand} [link]: Delete file from Google Drive (Only Owner & Sudo)

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror}: Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the downloads

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google Drive, if found replies with the link

/{BotCommands.StatsCommand}: Show Stats of the machine the bot is hosted on

/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Can only be invoked by Owner & Sudo of the bot)

/{BotCommands.AuthorizedUsersCommand}: Show authorized users (Only Owner & Sudo)

/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner)

/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner)

/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports

/{BotCommands.UsageCommand}: To see Heroku Dyno Stats (Owner & Sudo only).

/{BotCommands.SpeedCommand}: Check Internet Speed of the Host

/{BotCommands.RepoCommand}: Get the bot repo.

/shell: Run commands in Shell (Terminal).

/mediainfo: Get detailed info about replied media.

/tshelp: Get help for Torrent search module.

/weebhelp: Get help for Anime, Manga, and Character module.

/stickerhelp: Get help for Stickers module.
'''

    help_string = f'''
/{BotCommands.HelpCommand}: To get this message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the link to Google Drive.

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link]: Starts mirroring and if downloaded file is any archive, extracts it to Google Drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Start mirroring and upload the archived (.tar) version of the download

/{BotCommands.CloneCommand}: Copy file/folder to Google Drive

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror}: Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the downloads

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google Drive, if found replies with the link

/{BotCommands.StatsCommand}: Show Stats of the machine the bot is hosted on

/{BotCommands.SpeedCommand}: Check Internet Speed of the Host

/{BotCommands.RepoCommand}: Get the bot repo.

/mediainfo: Get detailed info about replied media.

/tshelp: Get help for Torrent search module.

/weebhelp: Get help for Anime, Manga, and Character module.

/stickerhelp: Get help for Stickers module.
'''

    if CustomFilters.sudo_user(update) or CustomFilters.owner_filter(update):
        sendMessage(help_string_adm, context.bot, update)
    else:
        sendMessage(help_string, context.bot, update)


botcmds = [
BotCommand(f'{BotCommands.MirrorCommand}', 'Start Mirroring'),
BotCommand(f'{BotCommands.TarMirrorCommand}','Upload tar (zipped) file'),
BotCommand(f'{BotCommands.UnzipMirrorCommand}','Extract files'),
BotCommand(f'{BotCommands.CloneCommand}','Copy file/folder to Drive'),
BotCommand(f'{BotCommands.WatchCommand}','Mirror YT-DL support link'),
BotCommand(f'{BotCommands.TarWatchCommand}','Mirror Youtube playlist link as tar'),
BotCommand(f'{BotCommands.CancelMirror}','Cancel a task'),
BotCommand(f'{BotCommands.CancelAllCommand}','Cancel all tasks'),
BotCommand(f'{BotCommands.DeleteCommand}','Delete file from Drive'),
BotCommand(f'{BotCommands.ListCommand}',' [query] Searches files in G-Drive'),
BotCommand(f'{BotCommands.StatusCommand}','Get Mirror Status message'),
BotCommand(f'{BotCommands.StatsCommand}','Bot Usage Stats'),
BotCommand(f'{BotCommands.HelpCommand}','Get Detailed Help'),
BotCommand(f'{BotCommands.SpeedCommand}','Check Speed of the host'),
BotCommand(f'{BotCommands.LogCommand}','Bot Log [owner only]'),
BotCommand(f'{BotCommands.RestartCommand}','Restart bot [owner only]'),
BotCommand(f'{BotCommands.RepoCommand}','Get the bot repo')]


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("😎𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲❗")
        LOGGER.info('Restarted Successfully!')
        remove('restart.pickle')
    bot.set_my_commands(botcmds)

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
    repo_handler = CommandHandler(BotCommands.RepoCommand, repo,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(repo_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
