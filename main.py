import platform
import asyncio
import sys
from telebot.async_telebot import AsyncTeleBot
from concurrent.futures import ThreadPoolExecutor
from model import Model
from actions import actions

os_name = platform.system()
executor = ThreadPoolExecutor(max_workers=10)

if os_name in ('Linux', 'Darwin'):
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        uvloop.install()
    except ImportError:
        print("uvloop is not installed, falling back to default asyncio event loop. Please, report this as an issue in Github, as it is not a normal behaviour during standart installation process")
else:
    print('uvloop not supported, falling back to default event loop. Consider using dedicated server for this bot')

with open('run/secrets/api_token', 'r') as secret:
    API_TOKEN = secret.read().strip()    
    
bot = AsyncTeleBot(API_TOKEN)
model = Model('RUSpam/spamNS_v1')

@bot.message_handler(func=lambda message: True)
async def detect_spam(message):
    loop = asyncio.get_event_loop()
    spam_score = await loop.run_in_executor(executor, model.check, message.text)
    if spam_score > 0.5:
        await actions(message, bot)
            
if __name__ == '__main__':
    try:
        asyncio.run(bot.infinity_polling())
    except KeyboardInterrupt:
        sys.exit(0)