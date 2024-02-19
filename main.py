from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv
import os

from bot.routers import start_router, admin_router, user_router





load_dotenv()
ADMINS= os.getenv('ADMINS')
CHANEL_DATA_BASE = os.getenv('CHANEL_DATA_BASE')

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
            start_router.router,
            admin_router.router,
            user_router.router
        )
    

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

