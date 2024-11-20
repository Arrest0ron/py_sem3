
import UserManager
import asyncio
import aiomysql
import warnings
import random
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
DEBUG = False


async def create_database_async_pool():
    credentials = UserManager.get_credentials("YourAdventureAdmin")
    if not credentials:
        return None
    try: 
        pool = await aiomysql.create_pool(
            user=credentials["username"],
            db=credentials["database"],
            password=credentials["password"],
            host=credentials["host"],
            minsize=1,
            maxsize=10,
            port=3306
        )
        return pool
    except aiomysql.Error as err:
        print("Error:", err.args)
        return None
    
async def create_table_if_not_exists(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_uid BIGINT PRIMARY KEY NOT NULL,
                    user_status ENUM('normal', 'connected', 'search', 'banned') DEFAULT 'normal',
                    INDEX (user_status),
                    connected_uid BIGINT NULL DEFAULT NULL,
                    rating INT DEFAULT NULL,
                    registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)

async def log_message(pool : aiomysql.Pool, message : Message):
    # print(f"Message {context} logged.")   
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                INSERT INTO users 
                (
                    telegram_uid
                )
                VALUES (%s)
                ON DUPLICATE KEY UPDATE
                last_update = CURRENT_TIMESTAMP
                """, (message.from_user.id,))
            await conn.commit()
            

async def update_status(pool : aiomysql.Pool, message : Message, status : str):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                INSERT INTO users 
                (
                    telegram_uid
                )
                VALUES (%s)
                ON DUPLICATE KEY UPDATE
                user_status = %s
                """, (message.from_user.id, status))
            await conn.commit()
            
        
async def fetch_user(pool, user_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                SELECT * FROM users WHERE telegram_uid = %s
                """, (user_id,))
            data = await cursor.fetchone()
            return data
    
async def get_message():
    sample_id = random.randint(1, 10)
    sample_context = random.sample(["A", "B", "C", "D", "E", "F"], k=4)
    context = {"Button": [i for i in sample_context]}
    if sample_id < 3:
        print("No message")
        return None
    await asyncio.sleep(3)
    print(f"User: {sample_id} sent: {sample_context}")
    return sample_id, context


API_TOKEN = '7655421976:AAEGxkW0TKEqNU6HPgsJGYW-fQjwyHxeJfs'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f"Привет, {message.from_user.username}!")

@router.message(Command("stop"))
async def send_welcome(message: Message):
    await message.answer(f"Вы остановили поиск собеседника!", reply_markup=None)
    await update_status(pool, message, "normal")
    return await menu(message)


@router.callback_query(F.data == 'search')
async def search(call: CallbackQuery):
    await call.answer('', show_alert=False)
    return await call.message.answer(text="found!")
    


@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer_dice()
    
    inline_kb_list = [
        [InlineKeyboardButton(text="Найти собеседника!", callback_data='search')],
        [InlineKeyboardButton(text="Мой профиль", callback_data='profile')],
        [InlineKeyboardButton(text="О боте", callback_data="about")]
    ]
    menu_markup = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    
    
    await log_message(pool, message)
    data = await fetch_user(pool, message.from_user.id)
    status = data[1]
    await message.delete()
    message.edit_reply_markup(reply_markup=None)
    
    answer = ""
    if  status == 'normal':
        answer = "Добро пожаловать в главное меню!"
    elif status == 'banned':
        answer = "Вы были заблокированы. Обратитесь в поддержку: @secondidentity, чтобы подать апелляцию."
        menu_markup = None
    elif status == "search":
        answer = "Вы в процессе поиска собеседника. Используйте /stop, чтобы прекратить поиск."
        stop_button = [[KeyboardButton(text="/stop")]]
        menu_markup = ReplyKeyboardMarkup(keyboard=stop_button)
    if DEBUG:
        answer = f"We got your message: '{message.text}'\n, {message.from_user.username}(uid={str(data[0])})"
    await message.answer(answer, reply_markup=menu_markup)
    

@router.message()  
async def basic(message : Message):
    start_buttons = [[KeyboardButton(text="/menu")]]
    start_markup = ReplyKeyboardMarkup(keyboard=start_buttons)
    await message.answer(text="Неизвестная команда. Используйте /menu, чтобы попасть в основное меню", reply_markup=start_markup)


pool = None

async def main():
    
    global pool
    pool = await create_database_async_pool()
    await create_table_if_not_exists(pool)
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="Table '.*' already exists")
    asyncio.run(main())