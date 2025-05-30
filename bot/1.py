import logging
logger = logging.getLogger(__name__)

import os
import datetime
#from ..config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied


#AUTH_USERS = [int(i) for i in os.environ.get("AUTH_USERS")]
#BANNED_USERS = [int(i) for i in os.environ.get("BANNED_USERS")]
FORCE_SUB = os.environ.get("FORCE_SUB")
    

@Client.on_message(filters.private & filters.incoming)
async def force_sub(c, m):
    if FORCE_SUB:
        try:
            chat = await c.get_chat_member(FORCE_SUB, m.from_user.id)
            if chat.status=='kicked':
                return await m.reply_text('Hai you are kicked from my updates channel. So, you are not able to use me',  quote=True)

        except UserNotParticipant:
            button = [[
                InlineKeyboardButton('join Updates channel', url=f'https://t.me/{FORCE_SUB}')
                ],[
                InlineKeyboardButton('🔄 Refresh 🔄', url=f'https://t.me/NewBotzTestBot?start')
            ]]
            markup = InlineKeyboardMarkup(button)
            return await m.reply_text(text="Hey join in my updates channel to use me.", parse_mode='markdown', reply_markup=markup, quote=True)

    await m.continue_propagation()
