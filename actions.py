import configparser
import datetime

async def actions(message, bot):
    SETTINGS = configparser.ConfigParser()
    SETTINGS.read('preferences.ini')
    if SETTINGS['delete'] == 'True':
        await bot.delete_message(message.chat.id, message.id)
    #elif SETTINGS['message_action'] == 'vote':
    #    await VOTE.vote(message.chat.id if SETTINGS['message_'] else SETTINGS['vote_chat_id'), message.from_user.id, message.id)
    else:
        None
    
    if SETTINGS['mode'] == 'ban':
        #await logger.log()
        await bot.ban_chat_member(message.chat.id, message.from_user.id)
    elif SETTINGS['mode'] == 'kick':
        #await logger.log()
        await bot.ban_chat_member(message.chat.id, message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(seconds=SETTINGS['mute_time']))
    elif SETTINGS['mode'] == 'mute':
        #await logger.log()
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=datetime.datetime.now() + datetime.timedelta(seconds=SETTINGS['mute_time']))
    #elif SETTINGS['mode') == 'vote':
    #    await VOTE.vote(message.chat.id if SETTINGS['mode_chat_id') else SETTINGS['vote_chat_id'), message.from_user.id, message.id)
    else:
        None
    
       