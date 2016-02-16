import os
import logging

from concurrent.futures import ThreadPoolExecutor
from slacker_log_handler import SlackerLogHandler
from tornado.concurrent import run_on_executor

SLACK_APIKEY = os.getenv('SLACK_APIKEY')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_USERNAME = os.getenv('SLACK_USERNAME')


class TornadoSlackHandler(SlackerLogHandler):

    _thread_pool = ThreadPoolExecutor(1)

    @run_on_executor(executor='_thread_pool')
    def emit(self, message):
        super(TornadoSlackHandler, self).emit(message)


def setup():
    if not SLACK_APIKEY:
        return

    handler = TornadoSlackHandler(api_key=SLACK_APIKEY, channel=SLACK_CHANNEL,
                                  username=SLACK_USERNAME)
    handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(handler)
