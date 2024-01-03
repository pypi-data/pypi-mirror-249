import json
import time
from datetime import datetime
from typing import List

import pytest

from tickthon import Task, ExpenseLog
from tickthon import TicktickClient
from tickthon._config import get_ticktick_ids
from tickthon.data.ticktick_id_keys import TicktickIdKeys as tik, TicktickFolderKeys as tfK


@pytest.fixture(scope="module")
def ticktick_client(ticktick_info):
    return TicktickClient(ticktick_info["username"], ticktick_info["password"])


def test_get_project_list(ticktick_client, data_folder_path):
    expected_project_lists = {"test-project-1": "90as8dfa09sd8f90asdf809",
                              "test-project-2": "90as8dfa0as23dfsdf809",
                              "test-project-3": "90as8df23f2390asdf809",
                              "test-project-4": "90as823fw3sd8f90asdf809",
                              "test-project-5": "90as8dfa23432fdsasdf809",
                              "test-project-6": "90as8df324fds8f90asdf809",
                              "test-project-7": "90as8d234sdf9sd8f90asdf809"}
    with open(data_folder_path / "project_profiles.json") as f:
        lists = json.load(f)

    project_lists = ticktick_client._get_folder_lists(lists)

    assert project_lists == expected_project_lists


def test_get_active_tasks(ticktick_client):
    active_tasks = ticktick_client.get_active_tasks()

    assert len(active_tasks) > 0
    assert len(ticktick_client.all_active_tasks) >= len(active_tasks)


def test_get_completed_tasks(ticktick_client):
    completed_tasks = ticktick_client.get_completed_tasks()
    assert len(completed_tasks) > 0


def test_get_expense_logs(ticktick_client):
    id_expense_log = ticktick_client.create_task(Task(title="$100 test expense log", created_date="2099-09-09",
                                                      ticktick_id="test-id", ticktick_etag="test-etag"))

    expense_logs = ticktick_client.get_expense_logs()

    assert len(expense_logs) > 0
    assert (isinstance(expense_logs, List) and
            all(isinstance(i[0], Task) and isinstance(i[1], ExpenseLog) for i in expense_logs))
    time.sleep(3)
    ticktick_client.complete_task(ticktick_client.get_task(id_expense_log))


def test_get_day_logs(ticktick_client):
    day_logs_project_id = get_ticktick_ids()[tik.LIST_IDS.value].get(tfK.DAY_LOGS.value)
    id_day_log = ticktick_client.create_task(Task(title="Test daily log", created_date="2099-09-09",
                                                  ticktick_id="test-id", ticktick_etag="test-etag",
                                                  project_id=day_logs_project_id))

    day_logs = ticktick_client.get_day_logs()

    assert len(day_logs) > 0
    assert (isinstance(day_logs, List))
    time.sleep(3)
    ticktick_client.complete_task(ticktick_client.get_task(id_day_log))


def test_complete_task(ticktick_client):
    task_id = ticktick_client.create_task(Task(title="test-task", created_date="2099-09-09",
                                               ticktick_id="test-id", ticktick_etag="test-etag"))

    task_to_complete = ticktick_client.get_task(task_id)

    ticktick_client.complete_task(task_to_complete)

    completed_task = ticktick_client.get_task(task_to_complete.ticktick_id)
    assert completed_task.status == 2


def test_get_overall_focus_time(ticktick_client):
    date = datetime.now().strftime("%Y-%m-%d")
    focus_time = ticktick_client.get_overall_focus_time(date)

    assert isinstance(focus_time, float)
    assert focus_time >= 0

# TODO: Create a test for get_deleted_tasks
# TODO: Create a test for get_abandoned_tasks
