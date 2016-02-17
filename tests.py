import logging
import json
import tornado_logging_slack
from mock import patch
from tornado.testing import AsyncTestCase, gen_test
from tornado.httpclient import AsyncHTTPClient, HTTPResponse, HTTPError
from six.moves import urllib


class MockHTTPClient(AsyncHTTPClient):

    def initialize(self, *args, **kwargs):
        super(MockHTTPClient, self).initialize(*args, **kwargs)
        self.called_requests = []
        self.error = None

    def fetch_impl(self, request, callback):
        self.called_requests.append(request)
        code = 200

        if self.error:
            code = self.error.code

        callback(HTTPResponse(request=request, code=code, error=self.error))

    @property
    def call_count(self):
        return len(self.called_requests)


class TornadoSlackHandlerTestCase(AsyncTestCase):

    maxDiff = None

    def setUp(self):
        AsyncTestCase.setUp(self)

        self.http_client = MockHTTPClient(force_instance=True)

        handler = tornado_logging_slack.TornadoSlackHandler(
            'my-key', 'my-channel', 'my-username',
            http_client=self.http_client
        )
        self.logger = logging.Logger('test')
        self.logger.addHandler(handler)

    def test_disabled_loglevels(self):
        self.logger.debug('debug message')
        self.logger.info('info message')
        self.logger.warn('warn message')

        self.assertEqual(self.http_client.call_count, 0)

    @gen_test
    def test_simple_error(self):
        self.logger.error('error message')
        self.assertEqual(self.http_client.call_count, 1)

        request = self.http_client.called_requests[0]
        self.assertEqual(request.url, 'https://slack.com/api/chat.postMessage')
        self.assertEqual(request.method, 'POST')

        form_data = urllib.parse.parse_qs(request.body.decode('utf-8'))
        self.assertEqual(form_data, {
            'text': ['error message'],
            'channel': ['my-channel'],
            'token': ['my-key'],
            'username': ['my-username'],
            'icon_emoji': [':heavy_exclamation_mark:'],
        })

    @gen_test
    def test_error_with_traceback(self):
        try:
            raise RuntimeError('My exception')
        except RuntimeError as err:
            self.logger.exception(err)

        self.assertEqual(self.http_client.call_count, 1)

        request = self.http_client.called_requests[0]
        self.assertEqual(request.url, 'https://slack.com/api/chat.postMessage')
        self.assertEqual(request.method, 'POST')

        form_data = urllib.parse.parse_qs(request.body.decode('utf-8'))
        self.assertEqual(form_data['text'][0], 'My exception')

        attachments = json.loads(form_data['attachments'][0])
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0]['color'], 'danger')
        self.assertEqual(attachments[0]['fallback'], 'My exception')
        self.assertRegexpMatches(attachments[0]['text'], 'Traceback')
        self.assertRegexpMatches(attachments[0]['text'], 'RuntimeError')

    @gen_test
    def test_error_posting_into_slack(self):
        self.http_client.error = HTTPError(500)

        self.logger.error('error message')
        self.assertEqual(self.http_client.call_count, 1)

    @patch('tornado_logging_slack.SLACK_APIKEY', new='my-api-key')
    @patch('tornado_logging_slack.SLACK_CHANNEL', new='my-channel')
    @patch('tornado_logging_slack.SLACK_USERNAME', new='my-username')
    def test_auto_setup_if_enabled(self):
        tornado_logging_slack.auto_setup('enabledLogger')

        logger = logging.getLogger('enabledLogger')
        self.assertEqual(len(logger.handlers), 1)

        handler = logger.handlers[0]
        self.assertIsInstance(
            handler, tornado_logging_slack.TornadoSlackHandler)

        self.assertEqual(handler.api_key, 'my-api-key')
        self.assertEqual(handler.channel, 'my-channel')
        self.assertEqual(handler.username, 'my-username')

    @patch('tornado_logging_slack.SLACK_APIKEY', new=None)
    def test_auto_setup_if_disabled(self):
        tornado_logging_slack.auto_setup('disabled')

        logger = logging.getLogger('disabledLogger')
        self.assertEqual(len(logger.handlers), 0)
