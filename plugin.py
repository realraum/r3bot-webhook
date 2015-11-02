###
# Copyright (c) 2011, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

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

def query(path, args={}):
    args = dict([(x,y) for x,y in args.items() if y is not None])
    url = 'http://supybot.aperio.fr/api%s?%s' % (path, urlencode(args))
    data = utils.web.getUrl(url)
    if sys.version_info[0] >= 3:
        data = data.decode()
    return json.loads(data)

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
