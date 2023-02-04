import heapq
import time
from collections import namedtuple
from datetime import datetime
from tzlocal import get_localzone

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from cycle_bot.database import TablesHandler
from cycle_bot.models import UserCycle, User, Cycle


class InnerCycle:
    QUEUE = []  # main cycles priority queue
    QueueCycle = namedtuple('QueueCycle', ['user_id', 'cycle_num', 'end_time'])
    scheduler = BackgroundScheduler(timezone=str(get_localzone()))
    seconds_limit = 60

    @classmethod
    def cycling(cls):
        cycles = TablesHandler.sql_get_active_cycles()
        for user in cycles:
            cycle_data = UserCycle(**user)

            for cycle in cycle_data.cycles.values():
                time_diff = cycle.end_time - time.time()

                if all((time_diff < cls.seconds_limit, cycle.started, not cycle.paused)):
                    heap_unit = cls.QueueCycle(user['users'], cycle.cycle, cycle.end_time)
                    heapq.heappush(cls.QUEUE, heap_unit)

        logger.info(f'queue - {cls.QUEUE}')

    @classmethod
    def time_loop(cls):
        logger.info('Start time_loop')
        while True:

            if len(cls.QUEUE) > 0:
                closest_cycle = heapq.nsmallest(1, cls.QUEUE)
                cycle_time = closest_cycle[0][2]

                if not time.time() >= cycle_time:
                    time.sleep(0.1)

                else:
                    cycle = heapq.heappop(cls.QUEUE)  # send message to user
                    logger.debug(f' heappop {cycle}')
                    TablesHandler.sql_insert(*cls.change_cycle(cycle))

    @classmethod
    def change_cycle(cls, cycle: QueueCycle) -> tuple:
        user = cycle.user_id
        iterator = TablesHandler.sql_get_user(user)
        query = [cycles for cycles in iterator]
        model = User(**query[0])
        cycles = model.cycles
        status = InnerCycle.check_active_cycles(cycles)
        # check repeats and restart cycle
        stop_cycle = Cycle(
            cycle=cycle.cycle_num,
            start_time=0,
            end_time=0,
            started=False,
            paused=False,
            repeats=0
        )
        cycles[cycle.cycle_num] = stop_cycle
        cycle_to_dict = {key: value.dict() for (key, value) in cycles.items()}
        return user, status, cycle_to_dict

    @classmethod
    def check_active_cycles(cls, cycles: dict) -> bool:
        active = [cycle for cycle in cycles.values() if cycle.end_time > 0]
        return True if len(active) > 0 else False

    @classmethod
    def scheduler_run(cls):
        cls.scheduler.add_job(InnerCycle.cycling, 'interval', seconds=60, next_run_time=datetime.now())
        cls.scheduler.start()

    @classmethod
    def start_loop(cls):
        # TablesHandler.sql_delete_all_users()
        # for i in range(1000, 1003):
        #     TablesHandler.sql_insert(i, True, {
        #         1: {'cycle': 1, 'start_time': time.time(), 'end_time': time.time() + 15,
        #             'started': 'True', 'paused': 'False', 'repeats': 1},
        #
        #         2: {'cycle': 2, 'start_time': time.time(), 'end_time': time.time() + 55,
        #             'started': 'True', 'paused': 'False', 'repeats': 2},
        #
        #         3: {'cycle': 3, 'start_time': time.time(), 'end_time': time.time() + 60,
        #             'started': 'True', 'paused': 'True', 'repeats': 2},
        #                                        })
        InnerCycle.time_loop()
