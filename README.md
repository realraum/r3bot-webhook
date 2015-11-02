# r3bot-webhook

This plugin (*Realhook*) provides your Limnoria bot with a simple webhook, which can be used to send messages to an (at the moment hardcoded) irc-channel vi a HTTP POST request.

### Demo

A simple python client for the hook:

```python
import requests

HOOKURL = 'https://bots.realraum.at/realhook/'

requests.post(HOOKURL, data = 'hello world', headers={'content-type': 'text/plain;'})
```
