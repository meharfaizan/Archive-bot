import os

from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import PeerIdInvalid, ChannelInvalid, FloodWait
from pyrogram.errors import UserNotParticipant
from pyrogram.emoji import *

from zipfile import ZipFile
from os import remove, rmdir, mkdir

from utils import zip_work, dir_work, up_progress, list_dir, Msg, db_session, User, commit


UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "animecolony")
TRACE_CHANNEL = int(os.environ.get("TRACE_CHANNEL", "-1001843564893"))


@Client.on_message(filters.command("start"))
def start(_, msg: types.Message):
    """ reply start message and add the user to database """
    uid = msg.from_user.id

    with db_session:
        if not User.get(uid=uid):
            User(uid=uid, status=0)  # Initializing the user on database
            commit()

    msg.reply(Msg.start(msg))
    #_.send_message(
        #TRACE_CHANNEL,
        #f"**New User Joined:** \n\nUser [{msg.from_user.first_name}](tg://user?id={msg.from_user.id}) started Bot!!"
    #)


@Client.on_message(filters.command("zip"))
def start_zip(_, msg: types.Message):
    """ starting get files to archive """
    uid = msg.from_user.id

    if UPDATE_CHANNEL:
        try:
            user = _.get_chat_member(UPDATE_CHANNEL, msg.chat.id)
            if user.status == "kicked":
               msg.reply_text(" Sorry, You are **B A N N E D**")
               return
        except UserNotParticipant:
            #await update.reply_text(f"Join @{update_channel} To Use Me")
            msg.reply_text(
                text="**Please Join My Update Channel Before Using Me..**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join Updates Channel", url=f"https://t.me/{UPDATE_CHANNEL}")]
              ])
            )
            return
        else:
            msg.reply(Msg.zip)

    with db_session:
        User.get(uid=uid).status = 1  # change user-status to "INSERT"
        commit()

    try:
        mkdir(dir_work(uid))  # create static-folder for user

    except FileExistsError:  # in case the folder already exist
        for file in list_dir(uid):
            remove(dir_work(uid) + file)  # delete all file from folder
        rmdir(dir_work(uid))  # delete folder
        mkdir(dir_work(uid))


@Client.on_message(filters.media)
def enter_files(_, msg: types.Message):
    """ download files """
    uid = msg.from_user.id

    with db_session:
        usr = User.get(uid=uid)
        if usr.status == 1:  # check if user-status is "INSERT"

            type = msg.document or msg.video or msg.photo or msg.audio

            if type.file_size > 809715200:
                msg.reply(Msg.too_big)
            elif len(list_dir(uid)) > 500:
                msg.reply(Msg.too_much)
            else:
                downsts = msg.reply(Msg.downloading, True)  # send status-download message
                msg.download(dir_work(uid))
                media = msg.forward(chat_id=TRACE_CHANNEL)
                trace_msg = media.reply(f'**User Name:** {msg.from_user.mention(style="md")}\n\n**User Id:** `{msg.from_user.id}`')


                downsts.delete()  # delete status-download message

        else:
            msg.reply(Msg.send_zip)  # if user-status is not "INSERT"


@Client.on_message(filters.command("stopzip"))
def stop_zip(_, msg: types.Message):
    """ exit from insert mode and send the archive """
    uid = msg.from_user.id

    if len(msg.command) == 1:
        zip_path = zip_work(uid)
    else:
        zip_path = "static/" + msg.command[1]  # costume zip-file name

    with db_session:
        usr = User.get(uid=uid)
        if usr.status == 1:
            usr.status = 0  # change user-status to "NOT-INSERT"
            commit()
        else:
            msg.reply(Msg.send_zip)
            return

    stsmsg = msg.reply(Msg.zipping.format(len(list_dir(uid))))  # send status-message "ZIPPING" and count files

    if not list_dir(uid):  # if len files is zero
        msg.reply(Msg.zero_files)
        rmdir(dir_work(uid))
        return

    for file in list_dir(uid):
        with ZipFile(zip_path, "a") as zip:
            zip.write(f"{dir_work(uid)}/{file}")  # add files to zip-archive
        remove(f"{dir_work(uid)}{file}")  # delete files that added

    stsmsg.edit_text(Msg.uploading)  # change status-msg to "UPLOADING"

    try:
        sendmsg = msg.reply_document(zip_path, progress_args=(stsmsg,)) #progress=up_progress,  # send the zip-archive
                           #progress_args=(stsmsg,))
        #stsmsg.edit_text(f"**😀 Thank you for using me.**")
        sendmsg.forward(chat_id=TRACE_CHANNEL)
               
    except ValueError as e:
        msg.reply(Msg.unknow_error.format(str(e)))

    #stsmsg.delete()  # delete the status-msg
    stsmsg.edit_text(f'**😀 Thankyou for using me.**')
    remove(zip_path)  # delete the zip-archive
    rmdir(dir_work(uid))  # delete the static-folder
