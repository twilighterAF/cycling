import threading

from tg_bot.bot import bot_run
from time_loop.timeloop import start_loop


if __name__ == '__main__':
    threading.Thread(target=start_loop, name='timeloop', daemon=True)
    bot_run()
