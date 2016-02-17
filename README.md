[![Build Status](https://travis-ci.org/globocom/tornado-logging-slack.png?branch=master)](https://travis-ci.org/globocom/tornado-logging-slack)
[![Coverage Status](https://coveralls.io/repos/github/globocom/tornado-logging-slack/badge.svg?branch=master)](https://coveralls.io/github/globocom/tornado-logging-slack?branch=master)

# Tornado logging slack
Log tornado errors in slack chat without block eventloop, based on [mathiasose/slacker_log_handler](https://github.com/mathiasose/slacker_log_handler)

## Install

with pip:

```bash
pip install tornado-logging-slack
```
## Usage
```python

import tornado_logging_slack

if __name__ == '__main__':
    tornado_logging_slack.auto_setup()
    IOLoop.current().start()
```

## Enviroment variables

- SLACK_APIKEY: Generate a key at https://api.slack.com;
- SLACK_CHANNEL: Set which channel you want to post to;
- SLACK_USERNAME: The username that will post to Slack;

- SLACK_PROXY_HOST: HTTP proxy hostname if you use a proxy;
- SLACK_PROXY_PORT: HTTP proxy port, default: 3128;
- SLACK_PROXY_USERNAME: HTTP proxy username;
- SLACK_PROXY_PASSWORD: HTTP proxy password;

## Contributing
Fork, patch, test and send a pull request.
