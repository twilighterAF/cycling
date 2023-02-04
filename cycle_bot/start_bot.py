import threading

from loguru import logger

from tg_bot import bot_run
from time_loop import InnerCycle


if __name__ == '__main__':
    logger.add('logs/logfile.log', format='{time} | {level} | {message}', level='DEBUG',
               rotation='05:00', retention='7 days', compression='zip')
    logger.info('Start')
    threading.Thread(target=InnerCycle.start_loop, name='timeloop').start()
    InnerCycle.scheduler_run()
    bot_run()
