from reloadium.corium.vendored import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import l1lll11111lll111Il1l1
from reloadium.corium.l1lll11111lll111Il1l1.l1ll1lll1ll1l1l1Il1l1 import lll1l11111lll11lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1
from reloadium.corium.l111ll1lll11l11lIl1l1 import llll1111l11llll1Il1l1
from reloadium.corium.l1llll11lllll1llIl1l1 import lll1111111lll1llIl1l1
from reloadium.corium.l11111llllll1ll1Il1l1 import lll1lllll1l1lll1Il1l1
from reloadium.corium.lll11111111lllllIl1l1 import lll11111111lllllIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.vendored.websocket_server import WebsocketServer


__RELOADIUM__ = True

__all__ = ['ll111l11ll1111llIl1l1']



ll11111ll11ll1llIl1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class ll111l11ll1111llIl1l1:
    ll11llll1lll1ll1Il1l1: str
    ll11111lllll1lllIl1l1: int
    ll1111111111111lIl1l1: lll1111111lll1llIl1l1

    ll1ll11l111ll111Il1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    lllll11lll1111l1Il1l1: str = field(init=False, default='')

    l11l1111ll111ll1Il1l1 = 'Reloadium page reloader'

    def l111l1111ll1l1l1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        l1111l1llll1l1llIl1l1.ll1111111111111lIl1l1.l11l1111ll111ll1Il1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(l1111l1llll1l1llIl1l1.ll11111lllll1lllIl1l1, '')]))

        l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1 = WebsocketServer(host=l1111l1llll1l1llIl1l1.ll11llll1lll1ll1Il1l1, port=l1111l1llll1l1llIl1l1.ll11111lllll1lllIl1l1)
        l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1.run_forever(threaded=True)

        l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1 = ll11111ll11ll1llIl1l1

        l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1 = l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1.replace('{info}', str(l1111l1llll1l1llIl1l1.l11l1111ll111ll1Il1l1))
        l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1 = l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1.replace('{port}', str(l1111l1llll1l1llIl1l1.ll11111lllll1lllIl1l1))
        l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1 = l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1.replace('{address}', l1111l1llll1l1llIl1l1.ll11llll1lll1ll1Il1l1)

    def l1l111ll111l11l1Il1l1(l1111l1llll1l1llIl1l1, ll111lll11l1l1l1Il1l1: str) -> str:
        lll1ll1llll1ll1lIl1l1 = ll111lll11l1l1l1Il1l1.find('<head>')
        if (lll1ll1llll1ll1lIl1l1 ==  - 1):
            lll1ll1llll1ll1lIl1l1 = 0
        lllll11111l111l1Il1l1 = ((ll111lll11l1l1l1Il1l1[:lll1ll1llll1ll1lIl1l1] + l1111l1llll1l1llIl1l1.lllll11lll1111l1Il1l1) + ll111lll11l1l1l1Il1l1[lll1ll1llll1ll1lIl1l1:])
        return lllll11111l111l1Il1l1

    def lllll1l111111ll1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        try:
            l1111l1llll1l1llIl1l1.l111l1111ll1l1l1Il1l1()
        except Exception as l1lll11ll1ll1111Il1l1:
            l1111l1llll1l1llIl1l1.ll1111111111111lIl1l1.l1ll1111l11l1111Il1l1('Could not start page reload server', l1l111l111llll11Il1l1=True)

    def l11l11lll11ll1l1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        if ( not l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.ll1111111111111lIl1l1.l11l1111ll111ll1Il1l1('Reloading page')
        l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1.send_message_to_all('reload')
        lll11111111lllllIl1l1.l111111l1ll11ll1Il1l1()

    def lllll1lll11l11llIl1l1(l1111l1llll1l1llIl1l1) -> None:
        if ( not l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.ll1111111111111lIl1l1.l11l1111ll111ll1Il1l1('Stopping reload server')
        l1111l1llll1l1llIl1l1.ll1ll11l111ll111Il1l1.shutdown()

    def l11l1111l1l1l111Il1l1(l1111l1llll1l1llIl1l1, l1l111ll111llll1Il1l1: float) -> None:
        def lll111lll11l1ll1Il1l1() -> None:
            time.sleep(l1l111ll111llll1Il1l1)
            l1111l1llll1l1llIl1l1.l11l11lll11ll1l1Il1l1()

        lll1l11111lll11lIl1l1(l1lll11l1111l1llIl1l1=lll111lll11l1ll1Il1l1, ll1111lll1ll1ll1Il1l1='page-reloader').start()


@dataclass
class l1ll11111ll11l1lIl1l1(l1l11111lll111l1Il1l1):
    ll11111ll11ll1llIl1l1: Optional[ll111l11ll1111llIl1l1] = field(init=False, default=None)

    l1l1111l11111lllIl1l1 = '127.0.0.1'
    l11l1ll111l1111lIl1l1 = 4512

    def lll1l111lll1l11lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l1l1l11lll111111Il1l1.ll11111l1111111lIl1l1('html')

    def l11llllll11l1l11Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path, lll1l11l11l1l111Il1l1: List[lll1lllll1l1lll1Il1l1]) -> None:
        if ( not l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
            return 

        from reloadium.corium.l11l11l11l111111Il1l1.ll111l1l111lllllIl1l1 import l1l11l1l1l1l111lIl1l1

        if ( not any((isinstance(l1l11l1l1l1ll11lIl1l1, l1l11l1l1l1l111lIl1l1) for l1l11l1l1l1ll11lIl1l1 in lll1l11l11l1l111Il1l1))):
            if (l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
                l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l11l11lll11ll1l1Il1l1()

    def ll11ll11llll111lIl1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        if ( not l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
            return 
        l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l11l11lll11ll1l1Il1l1()

    def l11ll1lll1l11111Il1l1(l1111l1llll1l1llIl1l1, ll11111lllll1lllIl1l1: int) -> ll111l11ll1111llIl1l1:
        while True:
            lll111llll11lll1Il1l1 = (ll11111lllll1lllIl1l1 + l1111l1llll1l1llIl1l1.l11l1ll111l1111lIl1l1)
            try:
                lllll11111l111l1Il1l1 = ll111l11ll1111llIl1l1(ll11llll1lll1ll1Il1l1=l1111l1llll1l1llIl1l1.l1l1111l11111lllIl1l1, ll11111lllll1lllIl1l1=lll111llll11lll1Il1l1, ll1111111111111lIl1l1=l1111l1llll1l1llIl1l1.lll111ll111l1111Il1l1)
                lllll11111l111l1Il1l1.lllll1l111111ll1Il1l1()
                l1111l1llll1l1llIl1l1.lll111ll11111l11Il1l1()
                break
            except OSError:
                l1111l1llll1l1llIl1l1.lll111ll111l1111Il1l1.l11l1111ll111ll1Il1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(lll111llll11lll1Il1l1, ''), ' port']))
                l1111l1llll1l1llIl1l1.l11l1ll111l1111lIl1l1 += 1

        return lllll11111l111l1Il1l1

    def lll111ll11111l11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        l1111l1llll1l1llIl1l1.lll111ll111l1111Il1l1.l11l1111ll111ll1Il1l1('Injecting page reloader')

    def l1ll1l1l11l1llllIl1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l1ll1l1l11l1llllIl1l1()

        if (l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
            l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.lllll1lll11l11llIl1l1()
