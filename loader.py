from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from data.config import BOT_TOKEN, ADMINS

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()


# def scheduler_job():
#     scheduler.add_job(mailing, "interval", seconds=300, args=(dp,))


# async def mailing(dp):
#     users = session.query(User)
#     for direct in directions:
#         await mailing_direct(dp, users, direct)


# async def mailing_direct(dp, users, direct):
#     print(f'чекаю {direct}')
#     url = 'https://raitinglistpk.mospolytech.ru/rating_list_ajax.php'
#     params = {
#         'select1': '000000017_01',
#         'specCode': direct,
#         'eduForm': 'Очная',
#         'eduFin': 'Бюджетная основа'
#     }
#     zap = requests.post(url=url,
#                         verify=False,
#                         data=params
#                         )
#     soup = BeautifulSoup(zap.text, 'html.parser')
#     for line in soup.find(id='div4').table.find_all('tr')[1:]:
#         parametrs = []
#         for i in line.find_all('td')[:3]:
#             value = i.string
#             if value is None:
#                 value = i.find('font').string
#             parametrs.append(value.strip())
#         place = parametrs[1]
#         snils = parametrs[2]
#         user = users.filter(User.snils == snils).first()
#         print(user, place)
#         if place and user and user.place != int(place):
#             print(user)
#             user.place = int(place)
#             try:
#                 await dp.bot.send_message(text=f'Ваше место изменилось: {place}',
#                                           chat_id=user.user_id)
#             except BotBlocked:
#                 pass
#     session.commit()



