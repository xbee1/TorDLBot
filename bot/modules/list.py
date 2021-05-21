from telegram.ext import CommandHandler, run_async
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
import threading
from bot.helper.telegram_helper.bot_commands import BotCommands

@run_async
def list_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"Searching: {search}")
        reply = sendMessage('🔍𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠..... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭🤚❗️', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
        else:
            editMessage('🚫𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭 𝐟𝐨𝐮𝐧𝐝🚫', reply, button)

    except IndexError:
        sendMessage('𝚂𝚎𝚗𝚍 𝚊 𝚜𝚎𝚊𝚛𝚌𝚑 𝚔𝚎𝚢 𝚊𝚕𝚘𝚗𝚐 𝚠𝚒𝚝𝚑 𝚌𝚘𝚖𝚖𝚊𝚗𝚍😏', context.bot, update)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(list_handler)
