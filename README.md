# Tornado logging slack
Log tornado in slack chat without block eventloop, based on [mathiasose/slacker_log_handler](https://github.com/mathiasose/slacker_log_handler)

## Install

with pip:

```bash
pip install tornado-logging-slack
```
## Usage
```python

import tornado_logging_slack

if __name__ == '__main__':
    tornado_logging_slack.setup()
    IOLoop.current().start()
```

## Enviroment variables

- SLACK_APIKEY: Generate a key at https://api.slack.com;
- SLACK_CHANNEL: Set which channel you want to post to;
- SLACK_USERNAME: The username that will post to Slack;


## Contributing
Fork, patch, and send a pull request.
