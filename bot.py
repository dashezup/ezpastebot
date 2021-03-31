from pyrogram import Client, idle

app = Client("ezpastebot")
app.start()
print('>>> BOT STARTED')
idle()
app.stop()
print('\n>>> BOT STOPPED')
