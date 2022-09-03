import os
from pyrogram import Client
from os import mkdir

app_id = int(os.environ.get("API_ID", "663122"))
app_key = os.environ.get('API_HASH', '23dac54b523173b5f83014ae566584bd')
token = os.environ.get('TG_BOT_TOKEN', '')

app = Client("zipBot", app_id, app_key, bot_token=token)


if __name__ == '__main__':

    try:
        mkdir("static")  # create static files folder
    except FileExistsError:
        pass

    app.run()
