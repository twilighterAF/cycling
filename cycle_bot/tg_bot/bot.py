from os import getenv

from aiogram import Bot, Dispatcher, executor, types
from loguru import logger
from dotenv import load_dotenv


load_dotenv(dotenv_path='./.env')
bot = Bot(token=str(getenv('BOT_TOKEN')))
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Hello')


@dispatcher.message_handler(commands='run')
async def start(message: types.Message):
    await message.reply('Run cycles')


@dispatcher.message_handler(commands='stop')
async def stop(message: types.Message):
    await message.reply('Stop cycles')


def format_time(time: str) -> int:
    hours, minutes, seconds = 0, 0, 0
    number = ''

    for char in time:

        if char.isdigit():
            number += char

        elif char == 'h':
            hours = int(number)
            number = ''
        elif char == 'm':
            minutes = int(number)
            number = ''
        elif char == 's':
            seconds = int(number)
            number = ''

    result = seconds + (minutes * 60) + (hours * 3600)

    return result


def format_repeats(repeats: list) -> int:
    result = 0
    if repeats:
        result = int(repeats[0].split('x')[1])
    return result


@dispatcher.message_handler(regexp='^(\s?[1-5]\s'  # cycle number
                                   '(\d{1,2}[h, m, s]){1,3}'  # time format - 23h59m59s
                                   '\s(x\d+)?'  # repeat count format - x2
                                   '\s?\/){1,5}')  # slash divider at the end
async def cycles_input(message: types.Message):
    result = {}
    cmds = message.text.split('/')

    for cycle in cmds:

        if len(cycle) > 0:
            string = cycle.strip().split(' ')
            cycle_number = string[0]
            cycle_time = string[1].lower()
            cycle_repeats = string[2:]
            seconds = format_time(cycle_time)
            repeats = format_repeats(cycle_repeats)
            result[cycle_number] = {'time': seconds, 'repeats': repeats}

    await message.answer('match')


def bot_run():
    executor.start_polling(dispatcher, skip_updates=True)
