# r3bot-webhook

This plugin (*Realhook*) provides your Limnoria bot with a simple webhook, which can be used to send messages to an (at the moment hardcoded) irc-channel vi a HTTP POST request.

### Warning

**Keep in mind:** The hook does not implement any form of authentication. The hook is exposed to anyone who has access to the server via http, thus allowing them to use it!

### Demo

A simple python client for the hook:

```python
import requests

HOOKURL = 'https://bots.realraum.at/realhook/'

requests.post(HOOKURL, data = 'hello world', headers={'content-type': 'text/plain;'})
```

At realraum we use(d) this to notify our irc-channel about zeromq events, [see demo code](https://gist.github.com/stefan2904/dba60622d5e9dbb06c70).
