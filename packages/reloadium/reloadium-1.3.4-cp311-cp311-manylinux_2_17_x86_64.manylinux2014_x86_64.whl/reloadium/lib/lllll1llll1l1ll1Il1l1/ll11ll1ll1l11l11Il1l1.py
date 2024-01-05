from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, cast
import types

from reloadium.corium.l1llll11lllll1llIl1l1 import l1llll11lllll1llIl1l1
from reloadium.corium.l1lll11111lll111Il1l1.llll1l1l1l11l111Il1l1 import lll1ll1ll111l1l1Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l111ll1111ll1l11Il1l1 import ll1l1ll11l1lllllIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll11111l1111l1llIl1l1 import l1ll11111ll11l1lIl1l1
from reloadium.corium.l11111llllll1ll1Il1l1 import ll111111l1l1l1l1Il1l1, lllll1l111111111Il1l1, l11llll1l11lll11Il1l1, ll1l11l1l1111l11Il1l1
from reloadium.corium.ll1lll11l1l11l1lIl1l1 import l1ll1l11111111llIl1l1
from dataclasses import dataclass, field

__RELOADIUM__ = True

ll1111111111111lIl1l1 = l1llll11lllll1llIl1l1.l11l1l1ll1l1lll1Il1l1(__name__)


@dataclass(**ll1l11l1l1111l11Il1l1)
class l1l11l1llll1l111Il1l1(l11llll1l11lll11Il1l1):
    l11ll111l11l1lllIl1l1 = 'FlaskApp'

    @classmethod
    def lllll111lllll1llIl1l1(l1111llll11111llIl1l1, ll1ll1l1l11ll11lIl1l1: l1ll1l11111111llIl1l1.ll1lll1ll1ll11l1Il1l1, ll1llll1lll11ll1Il1l1: Any, l11lllll111l1lllIl1l1: ll111111l1l1l1l1Il1l1) -> bool:
        import flask

        if (isinstance(ll1llll1lll11ll1Il1l1, flask.Flask)):
            return True

        return False

    def l111llll11l111l1Il1l1(l1111l1llll1l1llIl1l1) -> bool:
        return True

    @classmethod
    def ll11ll111l11llllIl1l1(l1111llll11111llIl1l1) -> int:
        return (super().ll11ll111l11llllIl1l1() + 10)


@dataclass(**ll1l11l1l1111l11Il1l1)
class l1ll1l111111l1l1Il1l1(l11llll1l11lll11Il1l1):
    l11ll111l11l1lllIl1l1 = 'Request'

    @classmethod
    def lllll111lllll1llIl1l1(l1111llll11111llIl1l1, ll1ll1l1l11ll11lIl1l1: l1ll1l11111111llIl1l1.ll1lll1ll1ll11l1Il1l1, ll1llll1lll11ll1Il1l1: Any, l11lllll111l1lllIl1l1: ll111111l1l1l1l1Il1l1) -> bool:
        if (repr(ll1llll1lll11ll1Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def l111llll11l111l1Il1l1(l1111l1llll1l1llIl1l1) -> bool:
        return True

    @classmethod
    def ll11ll111l11llllIl1l1(l1111llll11111llIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class l111111llll1111lIl1l1(l1ll11111ll11l1lIl1l1):
    ll1l111l11l11l11Il1l1 = 'Flask'

    @contextmanager
    def lll1lll1l1111111Il1l1(l1111l1llll1l1llIl1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def ll11111ll11l1l11Il1l1(*ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> Any:
            def lll111ll1l1ll1llIl1l1(l111l111lll1l1l1Il1l1: Any) -> Any:
                return l111l111lll1l1l1Il1l1

            return lll111ll1l1ll1llIl1l1

        llllll111lll111lIl1l1 = FlaskLib.route
        FlaskLib.route = ll11111ll11l1l11Il1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = llllll111lll111lIl1l1  # type: ignore

    def l111111ll11l1l11Il1l1(l1111l1llll1l1llIl1l1) -> List[Type[lllll1l111111111Il1l1]]:
        return [l1l11l1llll1l111Il1l1, l1ll1l111111l1l1Il1l1]

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l11llll111ll1111Il1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l11llll111ll1111Il1l1, 'flask.app')):
            l1111l1llll1l1llIl1l1.llllll11llll1l1lIl1l1()
            l1111l1llll1l1llIl1l1.l1l1111lllll1lllIl1l1()
            l1111l1llll1l1llIl1l1.llll1llllll1lll1Il1l1()

        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l11llll111ll1111Il1l1, 'flask.cli')):
            l1111l1llll1l1llIl1l1.lll1111l1l1lll11Il1l1()


    def l11l1l11ll1ll1l1Il1l1(hostname: Any, port: Any, application: Any, use_reloader: Any = False, use_debugger: Any = False, use_evalex: Any = True, extra_files: Any = None, exclude_patterns: Any = None, reloader_interval: Any = 1, reloader_type: Any = 'auto', threaded: Any = False, processes: Any = 1, request_handler: Any = None, static_files: Any = None, passthrough_errors: Any = False, ssl_context: Any = None) -> Any:
        from typing import cast
        __rw_plugin__ = cast('Flask', globals().get('__rw_plugin__'))

        __rw_plugin__.ll11111ll11ll1llIl1l1 = __rw_plugin__.l11ll1lll1l11111Il1l1(port)  # type: ignore
        if (__rw_globals__['env'].page_reload_on_start):  # type: ignore
            __rw_plugin__.ll11111ll11ll1llIl1l1.l11l1111l1l1l111Il1l1(1.0)  # type: ignore
        __rw_orig__(hostname, port, application, use_reloader, use_debugger, use_evalex, extra_files, exclude_patterns, reloader_interval, reloader_type, threaded, processes, request_handler, static_files, passthrough_errors, ssl_context)  # type: ignore













    def llllll11llll1l1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        lll1ll1ll111l1l1Il1l1.l11l1l111lll1lllIl1l1(werkzeug.serving.run_simple, l1111l1llll1l1llIl1l1.l11l1l11ll1ll1l1Il1l1, llll11l1lll11lllIl1l1={'__rw_plugin__': l1111l1llll1l1llIl1l1})


    def llll1llllll1lll1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        l11l1ll11ll1llllIl1l1 = flask.app.Flask.__init__

        def ll11lll111llll1lIl1l1(l1111111l11lll1lIl1l1: Any, *ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> Any:
            l11l1ll11ll1llllIl1l1(l1111111l11lll1lIl1l1, *ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1)
            with ll1l1ll11l1lllllIl1l1():
                l1111111l11lll1lIl1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        lll1ll1ll111l1l1Il1l1.llll1l1l1l11l111Il1l1(flask.app.Flask, '__init__', ll11lll111llll1lIl1l1)

    def l1l1111lllll1lllIl1l1(l1111l1llll1l1llIl1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        l11l1ll11ll1llllIl1l1 = waitress.serve



        def ll11lll111llll1lIl1l1(*ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> Any:
            with ll1l1ll11l1lllllIl1l1():
                ll11111lllll1lllIl1l1 = lll11lllllll1ll1Il1l1.get('port')
                if ( not ll11111lllll1lllIl1l1):
                    ll11111lllll1lllIl1l1 = int(ll1lll111111llllIl1l1[1])

                ll11111lllll1lllIl1l1 = int(ll11111lllll1lllIl1l1)

                l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1 = l1111l1llll1l1llIl1l1.l11ll1lll1l11111Il1l1(ll11111lllll1lllIl1l1)
                if (env.page_reload_on_start):
                    l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l11l1111l1l1l111Il1l1(1.0)

            l11l1ll11ll1llllIl1l1(*ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1)

        lll1ll1ll111l1l1Il1l1.llll1l1l1l11l111Il1l1(waitress, 'serve', ll11lll111llll1lIl1l1)

    def lll1111l1l1lll11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll1lll11l111ll1lIl1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll1lll11l111ll1lIl1l1 = ll1lll11l111ll1lIl1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll1lll11l111ll1lIl1l1, cli.__dict__)

    def lll111ll11111l11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().lll111ll11111l11Il1l1()
        import flask.app

        l11l1ll11ll1llllIl1l1 = flask.app.Flask.dispatch_request

        def ll11lll111llll1lIl1l1(*ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> Any:
            lll111111l1ll11lIl1l1 = l11l1ll11ll1llllIl1l1(*ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1)

            if ( not l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
                return lll111111l1ll11lIl1l1

            if (isinstance(lll111111l1ll11lIl1l1, str)):
                lllll11111l111l1Il1l1 = l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l1l111ll111l11l1Il1l1(lll111111l1ll11lIl1l1)
                return lllll11111l111l1Il1l1
            elif ((isinstance(lll111111l1ll11lIl1l1, flask.app.Response) and 'text/html' in lll111111l1ll11lIl1l1.content_type)):
                lll111111l1ll11lIl1l1.data = l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l1l111ll111l11l1Il1l1(lll111111l1ll11lIl1l1.data.decode('utf-8')).encode('utf-8')
                return lll111111l1ll11lIl1l1
            else:
                return lll111111l1ll11lIl1l1

        flask.app.Flask.dispatch_request = ll11lll111llll1lIl1l1  # type: ignore
