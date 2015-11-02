import re
import sys
import json
import supybot.world as world
import supybot.utils as utils
from supybot import httpserver
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

if sys.version_info[0] < 3:
    from urllib import urlencode
else:
    from urllib.parse import urlencode

_ = PluginInternationalization('Realhook')

class RealhookCallback(httpserver.SupyHTTPServerCallback):
    name = 'Realraum website callback'
    defaultResponse = _("""
    You shouldn't be there, this subfolder is not for you. Go back to the
    index and try out other plugins (if any).""")
    def doPost(self, handler, path, form):
        try:
            self.plugin.announce.onPayload(form)
        except Exception as e:
            raise e
        finally:
            self.send_response(200)
            self.end_headers()

instance = None

bold = ircutils.bold

@internationalizeDocstring
class Realhook(callbacks.Plugin):
    """Add the help for "@plugin help Website" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        global instance
        self.__parent = super(Realhook, self)
        callbacks.Plugin.__init__(self, irc)
        instance = self

        callback = RealhookCallback()
        callback.plugin = self
        httpserver.hook('realhook', callback)

    class announce(callbacks.Commands):
        def onPayload(self, form):
            for irc in world.ircs:
                if irc.network == 'oftc':
                    text = form#['text'].value            
                    irc.queueMsg(ircmsgs.privmsg('#realraum', text))


    def die(self):
        self.__parent.die()
        httpserver.unhook('realhook')

Class = Realhook


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
