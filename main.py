import os
from pyrogram import Client
from os import mkdir

app_id = int(os.environ.get("API_ID", "6534707"))
app_key = os.environ.get('API_HASH', '4bcc61d959a9f403b2f20149cbbe627a')
token = os.environ.get('BOT_TOKEN', '5421870037:AAFUp2szK2uhVcBLk8WhNcbFBqYLrfB-TlQ')

app = Client("zipBot", app_id, app_key, bot_token=token)


if __name__ == '__main__':

    try:
        mkdir("static")  # create static files folder
    except FileExistsError:
        pass

    app.run()
