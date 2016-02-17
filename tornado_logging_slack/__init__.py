import os
import logging
import traceback
import json

from six.moves.urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient

SLACK_APIKEY = os.getenv('SLACK_APIKEY')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_USERNAME = os.getenv('SLACK_USERNAME')


class TornadoSlackHandler(logging.Handler):

    def __init__(self, api_key, channel, username, http_client=None):
        logging.Handler.__init__(self, level=logging.ERROR)

        self.api_key = api_key
        self.channel = channel
        self.username = username
        self.http_client = http_client or AsyncHTTPClient()

    def emit(self, record):
        data = {
            'token': self.api_key,
            'channel': self.channel,
            'text': str(record.getMessage()),
            'username': self.username,
            'icon_emoji': ':heavy_exclamation_mark:',
        }

        if record.exc_info:
            data['attachments'] = json.dumps([{
                'fallback': data['text'],
                'color': 'danger',
                'text': '\n'.join(
                    traceback.format_exception(*record.exc_info)),
            }])

        self.http_client.fetch(
            'https://slack.com/api/chat.postMessage',
            method='POST',
            body=urlencode(data),
            callback=self.callback,
        )

    def callback(self, response):
        if response.error:
            logging.warn('Failed to post error on slack: %s', response.error)


def auto_setup(logger_name=None):
    if not SLACK_APIKEY:
        return

    handler = TornadoSlackHandler(api_key=SLACK_APIKEY, channel=SLACK_CHANNEL,
                                  username=SLACK_USERNAME)
    logging.getLogger(logger_name).addHandler(handler)
