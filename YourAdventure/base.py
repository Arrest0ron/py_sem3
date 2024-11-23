import UserManager
import asyncio
import aiomysql
import warnings
import random
from aiogram.utils.keyboard import KeyboardBuilder, InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.methods import *
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from user import SearchUser, User
from keyboards import *


DEBUG = False
pool = None
pool : aiomysql.Pool


async def create_database_async_pool():
    credentials = UserManager.get_credentials("ChatFreelyAdmin")
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
    
async def create_table_if_not_exists():
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_uid BIGINT PRIMARY KEY NOT NULL,
                    user_status ENUM('normal', 'connected', 'search', 'banned') DEFAULT 'normal',
                    INDEX (user_status),
                    rating INT DEFAULT 0,
                    registration TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_connections INT DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS search (
                    telegram_uid BIGINT PRIMARY KEY NOT NULL,
                    rating INT DEFAULT 0,
                    FOREIGN KEY (telegram_uid) REFERENCES users(telegram_uid) ON DELETE CASCADE
                );
                """)
            
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS connections (
                    telegram_uid_1 BIGINT PRIMARY KEY NOT NULL,
                    FOREIGN KEY (telegram_uid_1) REFERENCES users(telegram_uid) ON DELETE CASCADE, 
                    telegram_uid_2 BIGINT NOT NULL,
                    FOREIGN KEY (telegram_uid_2) REFERENCES users(telegram_uid) ON DELETE CASCADE, 
                    UNIQUE INDEX T_UID_2(telegram_uid_2)
                );
                """)
            
async def log_message(message : Message):
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
         
async def add_to_search(user : User):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                REPLACE INTO search
                (
                    telegram_uid,
                    rating
                )
                VALUES (%s,%s)
                ;
                """, (user.telegram_uid, user.rating))
            await conn.commit()
                      
async def drop_from_search(telegram_uid):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor

            await cursor.execute(
                """
                DELETE FROM search
                WHERE telegram_uid = %s
                """, (telegram_uid, ))
            await conn.commit()

async def add_to_connections(recipient, counterpart):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                REPLACE INTO connections
                (
                    telegram_uid_1,
                    telegram_uid_2
                )
                VALUES (%s,%s)
                ;
                """, (recipient, counterpart))
            await conn.commit()
                      
async def drop_from_connections(telegram_uid):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                DELETE FROM connections
                WHERE telegram_uid_1 = %s
                OR telegram_uid_2 = %s
                """, (telegram_uid, telegram_uid))
            await conn.commit()

async def update_status(uid : str, status : str):
    async with pool.acquire() as conn:
        conn : aiomysql.Connection
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                UPDATE users
                SET user_status = %s
                WHERE telegram_uid = %s
                """, (status,uid))
            await conn.commit()
                          
async def fetch_user(user_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            cursor: aiomysql.Cursor
            await cursor.execute(
                """
                SELECT * FROM users WHERE telegram_uid = %s
                """, (user_id,))
            if cursor.rowcount==0:
                warnings.warn(f"An attempt to fetch unknown user: {user_id}")
                return None
            data = await cursor.fetchone()
            return User(data)
    
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

API_TOKEN = UserManager.get_key()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)



@router.callback_query(F.data == 'profile')
@router.message(Command("profile"))
async def profile(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    data = await fetch_user(call.from_user.id)
    answer = f"""
Давай рассмотрим твой профиль:
Ваш рейтинг: {data.rating}
Всего диалогов: {data.total_connections}
Регистрация: {data.registration}
    """
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= answer, reply_markup=markup)
   
@router.message(Command("start"))
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await message.answer(f"Привет, {message.from_user.username}! Используй /menu, чтобы попасть в основное меню.", reply_markup=markup)

@router.callback_query(F.data == 'stop')
@router.message(Command("stop"))
async def stop_search(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)


    is_searching = is_in_search(call.from_user.id)
    if not is_searching:
        return await menu(call)
    
    await drop_from_search(call.from_user.id)
    await bot.send_message(chat_id = call.from_user.id, text= f"Вы остановили поиск собеседника!")
    await update_status(call.from_user.id, "normal")
    return await menu(call)


@router.callback_query(F.data == 'quit')
@router.message(Command("quit"))
async def quit_dialogue(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    builder = InlineKeyboardBuilder()
    builder.add(*inline_dialogue_end_buttons_list)
    markup = builder.as_markup()
    counterpart = await get_connected_user(call.from_user.id)
    if counterpart is None:
        return await bot.send_message(chat_id = counterpart, text= f"Вы не находитесь в диалоге. Используйте /menu, чтобы попасть в меню, или /search, чтобы найти собеседника.", reply_markup=markup)
    await bot.send_message(chat_id = call.from_user.id, text= f"Вы остановили диалог с вашим собеседником. Используйте /search, чтобы найти нового собеседника, или /menu для возврата в меню.", reply_markup=markup)
    await drop_from_connections(call.from_user.id)
    await bot.send_message(chat_id = counterpart, text= f"Ваш собеседник остановил диалог. Используйте /search, чтобы найти нового собеседника, или /menu для возврата в меню.", reply_markup=markup)
    await update_status(call.from_user.id, "normal")
    await update_status(counterpart, "normal")


@router.callback_query(F.data == 'search')
@router.message(Command("search"))
async def search(call: CallbackQuery):
    usr = await fetch_user(call.from_user.id)
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    if usr.user_status != 'normal':
        return await menu(call)
    await update_status(call.from_user.id, "search")
    await bot.send_dice(chat_id = call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.add(*inline_search_buttons_list)
    # builder.adjust([1])
    markup = builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= f"Ищем для вас подходящего собеседника...", reply_markup=markup)
    counterpart = await get_counterpart(call.from_user.id)
    if counterpart is None:
        
        await add_to_search(usr)
        
    else:
        await drop_from_search(counterpart.telegram_uid)
        await update_status(call.from_user.id, "connected")
        await update_status(counterpart.telegram_uid, "connected")
        print(f"Found match for user {call.from_user.id}(@{call.from_user.username}), {counterpart.telegram_uid}")
        
        builder = InlineKeyboardBuilder()
        builder.add(*inline_connected_buttons_list)
        markup = builder.as_markup()
        
        await bot.send_message(chat_id = call.from_user.id, text= "Собеседник найден! Используйте /quit, чтобы прекратить диалог.", reply_markup=markup)
        await bot.send_message(chat_id = counterpart.telegram_uid, text= "Собеседник найден! Используйте /quit, чтобы прекратить диалог.", reply_markup=markup)
        await add_to_connections(call.from_user.id,counterpart.telegram_uid)
        
async def get_connected_user(telegram_uid : str):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            
            await cursor.execute(
                """
                SELECT * FROM connections WHERE telegram_uid_1 = %s OR telegram_uid_2 = %s;
                """, (telegram_uid, telegram_uid))
            if cursor.rowcount > 0:
                data = await cursor.fetchone()
                if data[0]==telegram_uid:
                    return data[1]
                return data[0]
            else:
                print(f"No user {telegram_uid} in connections.")
                return None

async def is_in_search(telegram_uid : str):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            
            cursor: aiomysql.Cursor
            user = await fetch_user(telegram_uid)
            user : User
            await cursor.execute(
                """
                SELECT * FROM search
                WHERE telegram_uid != %s
                """, (user.telegram_uid,))
            if cursor.rowcount > 0:
                return True

async def get_counterpart(telegram_uid : str):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            
            cursor: aiomysql.Cursor
            user = await fetch_user(telegram_uid)
            user : User
            await cursor.execute(
                """
                SELECT * FROM search
                WHERE telegram_uid != %s
                ORDER BY ABS(rating-%s);
                """, (user.telegram_uid, user.rating ))
            if await cursor.rowcount > 0:
                data = cursor.fetchone()
                return SearchUser(data)
            else:
                await asyncio.sleep(0.1)
                print(f"Match for {user.telegram_uid, user.rating } Not Found.")
                return None
        
@router.callback_query(F.data == 'menu')
@router.message(Command("menu"))
async def menu(call):
    if isinstance(call, CallbackQuery):
        await call.answer('', show_alert=False)
    await log_message(call)
    user = await fetch_user(call.from_user.id)
    status = user.user_status
    answer = "None"
    if  status == 'normal':
        answer = f"Добро пожаловать в главное меню, {call.from_user.full_name[:50]}!"
        buttons_list = inline_regular_buttons_list
    elif status == 'banned':
        answer = "Вы были заблокированы. Нажмите ниже, если хотите подать апелляцию."
        buttons_list = inline_banned_buttons_list
    elif status == 'search':
        buttons_list = inline_search_buttons_list
        answer = f"Вы в процессе поиска собеседника, {call.from_user.full_name[:50]}. Используйте /stop, чтобы прекратить поиск."
    elif status == 'connected':
        buttons_list = inline_connected_buttons_list
        answer = f"Вы находитесь в диалоге, {call.from_user.full_name[:50]}. Используйте /quit, чтобы прекратить диалог."
    
    if DEBUG:
        answer = f"We got your message: '{call.message.text}'\n, {call.from_user.username}(uid={user.telegram_uid})"
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(*buttons_list)
    keyboard_builder.adjust(*[1,2])
    menu_markup = keyboard_builder.as_markup()
    await bot.send_message(chat_id = call.from_user.id, text= answer, reply_markup=menu_markup)
     
@router.message()  
async def send_message(message : Message):
    connected = await get_connected_user(message.from_user.id)
    if connected is not None:
        # if message.sticker:
    
        await message.copy_to(chat_id=connected)
        # if message.document.file_size >  16777216:
        #     await bot.send_message(chat_id=message.from_user.id, text="Размер отправляемого файла не может превышать 16Мб.")
    else:
        await basic(message)

async def basic(message : Message):
    builder = InlineKeyboardBuilder()
    builder.add(*inline_to_menu_buttons_list)
    markup = builder.as_markup()
    await message.answer(text="Неизвестная команда. Используйте /menu, чтобы попасть в основное меню", reply_markup=markup)

async def main():
    global pool
    pool = await create_database_async_pool()
    if pool is None:
        raise BaseException("Could not resolve mysql database connection. Maybe check credentials/start db.")
    await create_table_if_not_exists()
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    if not DEBUG:
        warnings.filterwarnings("ignore", message="Table '.*' already exists")
    asyncio.run(main())
