import os
import logging
import traceback
import json

from six.moves.urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient

SLACK_APIKEY = os.getenv('SLACK_APIKEY')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')
SLACK_USERNAME = os.getenv('SLACK_USERNAME')

SLACK_PROXY_HOST = os.getenv('SLACK_PROXY_HOST')
SLACK_PROXY_PORT = int(os.getenv('SLACK_PROXY_PORT', '3128'))
SLACK_PROXY_USERNAME = os.getenv('SLACK_PROXY_USERNAME')
SLACK_PROXY_PASSWORD = os.getenv('SLACK_PROXY_PASSWORD')


class TornadoSlackHandler(logging.Handler):

    def __init__(self, api_key, channel, username, http_client=None,
                 proxy_host=None, proxy_port=None, proxy_username=None,
                 proxy_password=None):

        logging.Handler.__init__(self, level=logging.ERROR)

        self.api_key = api_key
        self.channel = channel
        self.username = username
        self.http_client = http_client or AsyncHTTPClient()

        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password

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
            proxy_host=self.proxy_host,
            proxy_port=self.proxy_port if self.proxy_host else None,
            proxy_username=self.proxy_username,
            proxy_password=self.proxy_password,
        )

    def callback(self, response):
        if response.error:
            logging.warn('Failed to post error on slack: %s', response.error)


def auto_setup(logger_name=None):
    if not SLACK_APIKEY:
        return

    handler = TornadoSlackHandler(
        api_key=SLACK_APIKEY, channel=SLACK_CHANNEL, username=SLACK_USERNAME,
        proxy_host=SLACK_PROXY_HOST, proxy_port=SLACK_PROXY_PORT,
        proxy_username=SLACK_PROXY_USERNAME,
        proxy_password=SLACK_PROXY_PASSWORD,
    )
    logging.getLogger(logger_name).addHandler(handler)
