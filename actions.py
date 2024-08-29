import configparser
import datetime

async def actions(message, bot):
    SETTINGS = configparser.ConfigParser()
    SETTINGS.read('preferences.ini')
    await logger(message, bot, SETTINGS)
    if SETTINGS['delete'] == 'True':
        await bot.delete_message(message.chat.id, message.id)
    else:
        None
    
    if SETTINGS['mode'] == 'ban':
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
    elif SETTINGS['mode'] == 'kick':
        await bot.ban_chat_member(message.chat.id, message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(seconds=SETTINGS['mute_time']))
    elif SETTINGS['mode'] == 'mute':
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(seconds=SETTINGS['mute_time']))
    else:
        None
    
async def logger(message, bot, SETTINGS):
    if SETTINGS['logs'] == True:
        await bot.send_message(SETTINGS['log_channel_id'] if SETTINGS['log_channel_id'] != 'default' else message.chat.id, 
                               f'''
                               Обнаружен спам от пользователя {message.from_user.first_name} (<@{message.from_user.id}>)  
                               ''')
    else:
        None