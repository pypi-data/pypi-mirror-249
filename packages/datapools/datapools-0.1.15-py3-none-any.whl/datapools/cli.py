import asyncio
import logging
import os
from typing import List

import click

from datapools.common.logger import logger, setup_logger
from datapools.common.types import (
    BaseProducerSettings,
    SchedulerSettings,
    WorkerSettings,
)
from datapools.producer import BaseProducer
from datapools.scheduler import CrawlerScheduler
from datapools.worker import CrawlerWorker


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop("not_required_if")
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + " NOTE: This argument is mutually exclusive with %s"
            % self.not_required_if
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`"
                    % (self.name, self.not_required_if)
                )
            else:
                self.prompt = None

        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


scheduler = None
worker = None
producer = None


async def cli_main():
    cli_init(standalone_mode=False)
    logger.info("cli_init done")
    await cli_wait()
    logger.info("cli_wait done")


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(cli_main())
    except KeyboardInterrupt as e:
        logger.info("exiting")

    loop.run_until_complete(cli_stop())


@click.group(invoke_without_command=True)
@click.option(
    "-l",
    "--loglevel",
    type=str,
    default="info",
    help="info, debug, error, warning}}",
)
@click.option("--google-api-key", type=str, help="todo")
@click.option(
    "--worker-storage-path",
    type=str,
    help="todo",
    default="/tmp/worker_storage",
)
@click.option("--worker-todo-queue-size", type=int, help="todo", default=1)
@click.option(
    "--producer-storage-path",
    type=str,
    help="todo",
    default="/tmp/producer_storage",
)
@click.option("-u", "--hint-url", type=str, multiple=True)
@click.option("-p", "--plugin", type=str, multiple=True)
@click.option("--hint-urls-file", type=str)
@click.pass_context
def cli_init(ctx, **kwargs):
    global scheduler
    global worker
    global producer

    level = logging.getLevelName(kwargs.get("loglevel").upper())
    setup_logger(level)
    # print(logger)

    # TODO: exclusive options should be processed by click
    hint_url = kwargs.get("hint_url")
    if hint_url:
        hint_urls = set(hint_url)
    else:
        hint_urls_file = kwargs.get("hint_urls_file")
        if hint_urls_file:
            with open(hint_urls_file, "r") as f:
                lines = f.readlines()
                hint_urls = set()
                for line in lines:
                    line = line.strip()
                    if len(line):
                        hint_urls.add(line)
        else:
            raise Exception("hint_urls")

    cfg = SchedulerSettings()
    cfg.CLI_HINT_URLS = hint_urls
    scheduler = CrawlerScheduler(cfg)
    scheduler.run()

    cfg = WorkerSettings()
    cfg.GOOGLE_DRIVE_API_KEY = kwargs.get("google_api_key")
    cfg.STORAGE_PATH = kwargs.get("worker_storage_path")
    if not os.path.exists(cfg.STORAGE_PATH):
        os.mkdir(cfg.STORAGE_PATH)
    cfg.TODO_QUEUE_SIZE = kwargs.get("worker_todo_queue_size")
    cfg.CLI_MODE = True
    plugins = kwargs.get("plugin")
    if plugins:
        cfg.USE_ONLY_PLUGINS = plugins
        cfg.ADDITIONAL_PLUGINS = plugins

    worker = CrawlerWorker(cfg)
    worker.run()

    cfg = BaseProducerSettings()
    cfg.STORAGE_PATH = kwargs.get("producer_storage_path")
    if not os.path.exists(cfg.STORAGE_PATH):
        os.mkdir(cfg.STORAGE_PATH)
    cfg.WORKER_STORAGE_PATH = kwargs.get("worker_storage_path")
    cfg.CLI_MODE = True
    producer = BaseProducer(cfg)
    producer.run()


async def cli_stop():
    global scheduler
    global worker
    global producer

    await asyncio.gather(scheduler.stop(), worker.stop(), producer.stop())


async def cli_wait():
    global scheduler
    global worker
    global producer

    await asyncio.gather(scheduler.wait(), worker.wait(), producer.wait())
