import datetime
import time
import traceback
import uuid
from threading import Thread
from typing import List, Dict, Any, Tuple

from pydantic import BaseModel, ValidationError

from lemon_scheduler.lemon_runtime.models import ScheduleTaskTab
from lemon_scheduler.lemon_runtime.wrappers import lemon
from lemon_scheduler.scheduler.funcs import name_to_func_mapping


def get_next_task_round_unit() -> int:
    return 60


def get_tasks_in_next_round(start_time: int, end_time: int) -> List[ScheduleTaskTab]:
    return list(
        ScheduleTaskTab
        .select()
        .where(
            ScheduleTaskTab.expected_execute_time.between(start_time, end_time),
            ScheduleTaskTab.executed == False
        )
        .order_by(
            ScheduleTaskTab.expected_execute_time
        )
    )


def execute_func_by_name(func_name, *args, **kwargs):
    func_wrapper = name_to_func_mapping.get(func_name)
    lemon.utils.run_in_atomic(func_wrapper, *args, **kwargs)


class FuncArgs(BaseModel):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


def execute_tasks(tasks: List[ScheduleTaskTab]):
    for task in tasks:
        now = int(time.time())
        if task.expected_execute_time > now:
            time.sleep(task.expected_execute_time - now)
            (ScheduleTaskTab
            .update(**{"execution_resulting": "执行中"})
            .where(
                ScheduleTaskTab.id == task.id,
                ScheduleTaskTab.execution_result == "等待中"
            ))
            update_dict = {'execution_result': '成功', "real_execution_time": int(time.time())}
            try:
                a = FuncArgs.parse_raw(task.task_arguments)
                execute_func_by_name(task.task_function, *a.args, **a.kwargs)
            except ValidationError as e:
                update_dict['execution_result'] = "失败"
                update_dict['execution_output'] = traceback.format_exc()
            except Exception as e:
                update_dict['execution_result'] = "失败"
                update_dict['execution_output'] = traceback.format_exc()
            finally:
                update_dict.update({"execution_finish_time": int(time.time())})
                (ScheduleTaskTab
                 .update(**update_dict)
                 .where(ScheduleTaskTab.id == task.id)
                 .execute())
            pass


def search_and_execute_tasks():
    last_execute_ts = 0
    while True:
        try:
            unit = get_next_task_round_unit()
            next_round_end_ts = int(time.time()) + unit
            tasks = get_tasks_in_next_round(last_execute_ts, next_round_end_ts)
            last_execute_ts = next_round_end_ts
            #
            execute_tasks(tasks)
        except Exception as e:
            pass


def start_task_loop():
    Thread(target=search_and_execute_tasks).start()


class Task:
    def __init__(self, func_name: str, *args, **kwargs):
        if func_name not in name_to_func_mapping:
            raise KeyError(f"func [{func_name}] not existed.")
        self.args = FuncArgs(args=args, kwargs=kwargs)
        self.func_name: str = ""

    def delay(self, delay_seconds: int):
        ScheduleTaskTab.create(**{
            "task_function": self.func_name,
            "task_arguments": self.args,
            "task_id": uuid.uuid4().hex,
            "expected_execute_time": int(time.time()) + delay_seconds,
            "executed": False,
            "execution_result": "等待中",
            "execution_output": "",
        })

    def delay_utils(self, target_time: datetime.datetime):
        return self.delay((target_time - datetime.datetime.now()).seconds)
