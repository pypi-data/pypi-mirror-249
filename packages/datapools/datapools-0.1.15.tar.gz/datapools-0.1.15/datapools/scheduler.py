import asyncio
import copy

# import json
# import time
import traceback
from typing import Optional

from .common.backend_api import BackendAPI
from .common.logger import logger
from .common.queues import (
    GenericQueue,
    QueueMessage,
    QueueMessageType,
    QueueRole,
)
from .common.stoppable import Stoppable

# from .common.tasks_db import Hash
# from .common.tasks_db.redis import RedisTasksDB
from .common.types import (
    QUEUE_REPORTS,
    QUEUE_WORKER_TASKS,
    CrawlerHintURLStatus,
    SchedulerSettings,
)

# import httpx


class CrawlerScheduler(Stoppable):
    # 1. task:
    #   - get hint urls from the backend, put into tasks_db, status is changed at the backend at once
    #   - check "processing" tasks: ping worker. If it's dead then task is moved back to the queue
    # 2. api: get urls from workers, put into tasks_db
    #   tips:
    #   - reject existing urls: request redis by url hash
    # 3. api: worker gets a new task(s?) from queue:
    #   tips:
    #   - tasks_db: (redis) task should be moved into a separate key as "in progress", worker ID/IP/etc should be remembered to be able to ping
    # 4. api: worker notifies about finished task
    #    - remove task from "processing"
    #    - if it's a backend hint url, then update its status by calling backend api

    def __init__(self, cfg: Optional[SchedulerSettings] = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else SchedulerSettings()

        if self.cfg.CLI_HINT_URLS is None:
            self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)
        else:
            self.hints_done = asyncio.Event()
            self.hints = copy.copy(self.cfg.CLI_HINT_URLS)

        # self.tasks_db = RedisTasksDB(
        #     host=self.cfg.REDIS_HOST, port=self.cfg.REDIS_PORT
        # )
        self.todo_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=QUEUE_WORKER_TASKS,
        )
        logger.error("created publisher worker_tasks")
        self.reports_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=QUEUE_REPORTS,
        )
        logger.error("created receiver reports")

    async def wait(self):
        assert self.cfg.CLI_HINT_URLS is not None
        waiters = (self.hints_done.wait(), self.is_stopped())
        await asyncio.gather(*waiters)
        if not self.stop_event.is_set():
            # hints_done is set
            await self.todo_queue.until_empty()
            await self.reports_queue.until_empty()

    def run(self):
        self.tasks.append(asyncio.create_task(self.hints_loop()))
        self.tasks.append(asyncio.create_task(self.reports_loop()))
        self.todo_queue.run()
        self.reports_queue.run()
        super().run()

    async def stop(self):
        logger.info("scheduler stopping")
        await self.todo_queue.stop()
        logger.info("todo_queue stopped")
        await self.reports_queue.stop()
        logger.info("reports_queue stopped")
        await super().stop()
        logger.info("super stopped")

    async def _set_task_status(self, data):
        # hash, status: CrawlerHintURLStatus, contents
        logger.info(f"set_task_status: {data=}")
        task = data["task"]
        status = CrawlerHintURLStatus(data["status"])
        # contents = data[ 'contents' ]

        # if status == CrawlerHintURLStatus.Success:
        #     logger.info("------------------ task done --------------------")
        #     self.tasks_db.set_done(task["_hash"])

        if "id" in task:
            logger.info(f"--------------- set hint url status {status}")
            # this is hint url from server => have to update status on the backend
            if self.cfg.CLI_HINT_URLS is None:
                await self.api.set_hint_url_status(task["id"], status)

        # if contents:
        #     logger.info( f'----------------- pushing contents {contents=}' )
        #     await self.api.add_crawler_contents( contents )

    async def _add_task(self, task, ignore_existing=False, ignore_done=False):
        # puts task to the todo_queue if it does not exist in new/done list
        # hash = self.tasks_db.add(
        #     task, ignore_existing=ignore_existing, ignore_done=ignore_done
        # )
        # if hash:
        # task["_hash"] = hash
        # logger.info( 'pushing to worker_tasks')
        await self.todo_queue.push(
            QueueMessage(type=QueueMessageType.Task, data=task)
        )
        # logger.info( 'pushed')
        return True
        # return hash

    # return False

    async def _get_hint_urls(self):
        hints = None
        if self.cfg.CLI_HINT_URLS is None:
            # deployment mode
            try:
                hints = await self.api.get_hint_urls(limit=10)
            except Exception as e:
                logger.error(f"Failed get hints: {e}")
        else:
            # cli mode
            if len(self.hints) > 0:
                hints = [{"url": self.hints.pop()}]
            else:
                self.hints_done.set()
        return hints

    async def hints_loop(self):
        # infinitely fetching URL hints by calling backend api
        try:
            while not await self.is_stopped():
                if True:  # self.tasks_db.is_ready():
                    hints = await self._get_hint_urls()
                    if hints is not None:
                        for hint in hints:
                            logger.info(f"got hint: {hint}")

                            ignore_existing = True  # TODO: for tests only!
                            if not await self._add_task(
                                hint,
                                ignore_existing=ignore_existing,
                                ignore_done=True,
                            ):
                                if "id" in hint:
                                    await self.api.set_hint_url_status(
                                        hint["id"],
                                        CrawlerHintURLStatus.Rejected,
                                    )
                await asyncio.sleep(self.cfg.BACKEND_HINTS_PERIOD)
        except Exception as e:
            logger.error(
                f"!!!!!!! Exception in CrawlerScheduler::hints_loop() {e}"
            )
            logger.error(traceback.format_exc())

    async def reports_loop(self):
        # receive reports from workers
        try:
            while not await self.is_stopped():
                message = await self.reports_queue.pop(timeout=1)
                if message:
                    try:
                        qm = QueueMessage.decode(message.body)
                        if qm.type == QueueMessageType.Task:
                            logger.info("new task from worker")
                            # logger.info(f"{qm=}")
                            await self._add_task(qm.data, ignore_done=True)
                        elif qm.type == QueueMessageType.Report:
                            await self._set_task_status(qm.data)
                        else:
                            logger.error(f"Unsupported QueueMessage {qm=}")

                    except Exception as e:
                        logger.error(f"Failed decode process report")
                        logger.error(traceback.format_exc())

                    await self.reports_queue.mark_done(message)

        except Exception as e:
            logger.error(
                f"!!!!!!! Exception in CrawlerScheduler::reports_loop() {e}"
            )
            logger.error(traceback.format_exc())
