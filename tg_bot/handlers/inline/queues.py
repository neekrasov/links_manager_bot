from collections import OrderedDict

from aiogram import types
import json

from loguru import logger

from loader import dp


def read_json():
    global queues
    with open('data/queues.json') as f:
        queues = OrderedDict(json.loads(f.read()))
    for q in queues:
        queues[q] = OrderedDict(queues[q])


queues = OrderedDict()
read_json()


def write_json():
    with open('data/queues.json', 'w') as f:
        f.write(json.dumps(queues))


@dp.inline_handler(lambda chosen_inline_result: True)
async def get_msg(query: types.InlineQuery):
    """
    Срабатывает, когда пользователь вводит @bot_username <запрос>, предлагает варианты очередей с заданным запросом
    :param query: текст запроса
    """
    logger.debug(query)
    try:
        prepositions = ['на', 'в', 'за']
        answers = []

        for p in enumerate(prepositions):
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton(text='Встать в очередь',
                                               callback_data='enter_{}_{}'.format(p[1], query.query)))
            answers.append(types.InlineQueryResultArticle(id=str(p[0] + 1),
                                                          title='Создать очередь',
                                                          description='Очередь {} {}'.format(p[1], query.query),
                                                          input_message_content=types.InputTextMessageContent(
                                                              message_text='Очередь {} *{}*'.format(p[1], query.query),
                                                              parse_mode='Markdown'
                                                          ),
                                                          reply_markup=key))

        await dp.bot.answer_inline_query(query.id, answers)
    except Exception as e:
        logger.debug(e)
        print(e)


@dp.callback_query_handler(lambda call: call.data.startswith('enter'))
async def enter_queue(call: types.CallbackQuery):
    """
    Срабатывает при нажатии кнопки "Встать в очередь", не добавляет, если уже в очереди
    :param call: callback от кнопки
    """
    logger.debug(call.data.split('_'))
    if call.data.startswith('enter_'):
        prep = 'на'
    elif call.data.startswith('enter1_'):
        prep = 'в'
    else:
        prep = 'за'
    subj = call.data.split('_')[2]
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton('Встать в очередь', callback_data=call.data))
    if call.inline_message_id not in queues:  # проверка нахождения очереди в списке текущих очередей
        # если при нажатии кнопки очереди в списке не было, добавим в список очередь с первым человеком в ней
        # каждая очередь - словарь участников очереди. Каждый участник очереди - пара ключ-значение, где ключ - id в тг
        # значение - кортеж из его имени и фамилии
        queues[call.inline_message_id] = OrderedDict(
            [(str(call.from_user.id), (call.from_user.first_name, call.from_user.last_name))])
        last_name = '' if call.from_user.last_name is None else call.from_user.last_name  # не выводим фамилию если None
        text = 'Очередь {} *{}*\n1. {} {}'.format(prep, subj, call.from_user.first_name, last_name)
        write_json()
        await dp.bot.edit_message_text(text, inline_message_id=call.inline_message_id, reply_markup=key, parse_mode='Markdown')
    else:
        if str(call.from_user.id) not in queues[call.inline_message_id]:
            queues[call.inline_message_id].update({str(call.from_user.id): (call.from_user.first_name, call.from_user.last_name)})
            queues[call.inline_message_id].move_to_end(str(call.from_user.id))
            text = 'Очередь {} *{}*\n'.format(prep, subj)
            n = 1
            for i in queues[call.inline_message_id]:
                first_name, last_name = queues[call.inline_message_id][i][0], queues[call.inline_message_id][i][1]
                last_name = '' if last_name is None else last_name
                text += '{}. {} {}\n'.format(n, first_name, last_name)
                n += 1
            write_json()
            await dp.bot.edit_message_text(text, inline_message_id=call.inline_message_id, reply_markup=key, parse_mode='Markdown')
        else:
            await dp.answer_callback_query(call.id, 'Ты уже в очереди', False)