import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l111ll1lll11l11lIl1l1 import llll1111l11llll1Il1l1
from reloadium.corium.ll11ll1lll1ll111Il1l1 import ll1l1l11ll1l1lllIl1l1
from reloadium.corium.l1lll11111lll111Il1l1.llll1l1l1l11l111Il1l1 import lll1ll1ll111l1l1Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l111ll1111ll1l11Il1l1 import ll1l1ll11l1lllllIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1111l111l1lll11Il1l1, l1lllll1l1111l1lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll11111l1111l1llIl1l1 import l1ll11111ll11l1lIl1l1
from reloadium.corium.l11111llllll1ll1Il1l1 import lll1lllll1l1lll1Il1l1, ll111111l1l1l1l1Il1l1, lllll1l111111111Il1l1, l11llll1l11lll11Il1l1, ll1l11l1l1111l11Il1l1
from reloadium.corium.l111lllll11l1ll1Il1l1 import l1llll11l11ll1llIl1l1, lll1ll11ll11l1llIl1l1
from reloadium.corium.ll1lll11l1l11l1lIl1l1 import l1ll1l11111111llIl1l1
from reloadium.corium.l1lll11111lll111Il1l1 import l1ll11111l1l1111Il1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**ll1l11l1l1111l11Il1l1)
class l1l1111111l1l1llIl1l1(l11llll1l11lll11Il1l1):
    l11ll111l11l1lllIl1l1 = 'Field'

    @classmethod
    def lllll111lllll1llIl1l1(l1111llll11111llIl1l1, ll1ll1l1l11ll11lIl1l1: l1ll1l11111111llIl1l1.ll1lll1ll1ll11l1Il1l1, ll1llll1lll11ll1Il1l1: Any, l11lllll111l1lllIl1l1: ll111111l1l1l1l1Il1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(ll1llll1lll11ll1Il1l1, 'field') and isinstance(ll1llll1lll11ll1Il1l1.field, Field))):
            return True

        return False

    def l11ll11ll11ll1llIl1l1(l1111l1llll1l1llIl1l1, ll11l1l11l111lllIl1l1: lllll1l111111111Il1l1) -> bool:
        return True

    @classmethod
    def ll11ll111l11llllIl1l1(l1111llll11111llIl1l1) -> int:
        return 200


@dataclass(repr=False)
class ll1lll111111ll11Il1l1(l1111l111l1lll11Il1l1):
    l1l11l1ll1l1111lIl1l1: "Atomic" = field(init=False)

    l1l1111lll111111Il1l1: bool = field(init=False, default=False)

    def l11l1lll1ll11l1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l11l1lll1ll11l1lIl1l1()
        from django.db import transaction

        l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1 = transaction.atomic()
        l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__enter__()

    def l1111ll1111l1ll1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l1111ll1111l1ll1Il1l1()
        if (l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__exit__(None, None, None)

    def l1ll111l11ll1111Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l1ll111l11ll1111Il1l1()

        if (l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1 = True
        l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__exit__(None, None, None)

    def __repr__(l1111l1llll1l1llIl1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class lll1111lll11l11lIl1l1(l1lllll1l1111l1lIl1l1):
    l1l11l1ll1l1111lIl1l1: "Atomic" = field(init=False)

    l1l1111lll111111Il1l1: bool = field(init=False, default=False)

    async def l11l1lll1ll11l1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        await super().l11l1lll1ll11l1lIl1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1 = transaction.atomic()


        with llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.ll11ll1lll11llllIl1l1.l1l1l11llllllll1Il1l1(False):
            await sync_to_async(l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__enter__)()

    async def l1111ll1111l1ll1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l1111ll1111l1ll1Il1l1()
        if (l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1 = True
        from django.db import transaction

        def ll1lll1lllll1l1lIl1l1() -> None:
            transaction.set_rollback(True)
            l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__exit__(None, None, None)
        with llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.ll11ll1lll11llllIl1l1.l1l1l11llllllll1Il1l1(False):
            await sync_to_async(ll1lll1lllll1l1lIl1l1)()

    async def l1ll111l11ll1111Il1l1(l1111l1llll1l1llIl1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l1ll111l11ll1111Il1l1()

        if (l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1):
            return 

        l1111l1llll1l1llIl1l1.l1l1111lll111111Il1l1 = True
        with llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.ll11ll1lll11llllIl1l1.l1l1l11llllllll1Il1l1(False):
            await sync_to_async(l1111l1llll1l1llIl1l1.l1l11l1ll1l1111lIl1l1.__exit__)(None, None, None)

    def __repr__(l1111l1llll1l1llIl1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class ll1lll1llllll111Il1l1(l1ll11111ll11l1lIl1l1):
    ll1l111l11l11l11Il1l1 = 'Django'

    ll11l1ll11ll11l1Il1l1: Optional[int] = field(init=False)
    l111l1lll111111lIl1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    ll1l11lllll1ll1lIl1l1: Any = field(init=False, default=None)
    l11l11lll11l1111Il1l1: Any = field(init=False, default=None)
    ll1l111lll111ll1Il1l1: Any = field(init=False, default=None)

    lll1ll1ll1l1l111Il1l1 = True

    def __post_init__(l1111l1llll1l1llIl1l1) -> None:
        super().__post_init__()
        l1111l1llll1l1llIl1l1.ll11l1ll11ll11l1Il1l1 = None

    def l111111ll11l1l11Il1l1(l1111l1llll1l1llIl1l1) -> List[Type[lllll1l111111111Il1l1]]:
        return [l1l1111111l1l1llIl1l1]

    def lll1l111lll1l11lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        super().lll1l111lll1l11lIl1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'django.core.management.commands.runserver')):
            l1111l1llll1l1llIl1l1.ll1lllll1l1111l1Il1l1()
            if ( not l1111l1llll1l1llIl1l1.lll1ll1l1l1l1ll1Il1l1):
                l1111l1llll1l1llIl1l1.l11111l11l1l1l11Il1l1()

    def l1ll1l1l11l1llllIl1l1(l1111l1llll1l1llIl1l1) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = l1111l1llll1l1llIl1l1.ll1l11lllll1ll1lIl1l1
        django.core.management.commands.runserver.Command.get_handler = l1111l1llll1l1llIl1l1.ll1l111lll111ll1Il1l1
        django.core.handlers.base.BaseHandler.get_response = l1111l1llll1l1llIl1l1.l11l11lll11l1111Il1l1

    def l111ll1lll1111l1Il1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str, ll1llll1111l1l1lIl1l1: bool) -> Optional["l1llll11l11ll1llIl1l1"]:
        if (l1111l1llll1l1llIl1l1.lll1ll1l1l1l1ll1Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (ll1llll1111l1l1lIl1l1):
            return None
        else:
            lllll11111l111l1Il1l1 = ll1lll111111ll11Il1l1(ll1111lll1ll1ll1Il1l1=ll1111lll1ll1ll1Il1l1, l1l1111llllllll1Il1l1=l1111l1llll1l1llIl1l1)
            lllll11111l111l1Il1l1.l11l1lll1ll11l1lIl1l1()

        return lllll11111l111l1Il1l1

    async def ll1lll11l1111l1lIl1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str) -> Optional["lll1ll11ll11l1llIl1l1"]:
        if (l1111l1llll1l1llIl1l1.lll1ll1l1l1l1ll1Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        lllll11111l111l1Il1l1 = lll1111lll11l11lIl1l1(ll1111lll1ll1ll1Il1l1=ll1111lll1ll1ll1Il1l1, l1l1111llllllll1Il1l1=l1111l1llll1l1llIl1l1)
        await lllll11111l111l1Il1l1.l11l1lll1ll11l1lIl1l1()
        return lllll11111l111l1Il1l1

    def ll1lllll1l1111l1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        import django.core.management.commands.runserver

        l1111l1llll1l1llIl1l1.ll1l11lllll1ll1lIl1l1 = django.core.management.commands.runserver.Command.handle

        def ll11lll111llll1lIl1l1(*ll1lll111111llllIl1l1: Any, **l1l111l1lll11ll1Il1l1: Any) -> Any:
            with ll1l1ll11l1lllllIl1l1():
                ll11111lllll1lllIl1l1 = l1l111l1lll11ll1Il1l1.get('addrport')
                if ( not ll11111lllll1lllIl1l1):
                    ll11111lllll1lllIl1l1 = django.core.management.commands.runserver.Command.default_port

                ll11111lllll1lllIl1l1 = ll11111lllll1lllIl1l1.split(':')[ - 1]
                ll11111lllll1lllIl1l1 = int(ll11111lllll1lllIl1l1)
                l1111l1llll1l1llIl1l1.ll11l1ll11ll11l1Il1l1 = ll11111lllll1lllIl1l1

            return l1111l1llll1l1llIl1l1.ll1l11lllll1ll1lIl1l1(*ll1lll111111llllIl1l1, **l1l111l1lll11ll1Il1l1)

        lll1ll1ll111l1l1Il1l1.llll1l1l1l11l111Il1l1(django.core.management.commands.runserver.Command, 'handle', ll11lll111llll1lIl1l1)

    def l11111l11l1l1l11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        import django.core.management.commands.runserver

        l1111l1llll1l1llIl1l1.ll1l111lll111ll1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def ll11lll111llll1lIl1l1(*ll1lll111111llllIl1l1: Any, **l1l111l1lll11ll1Il1l1: Any) -> Any:
            with ll1l1ll11l1lllllIl1l1():
                assert l1111l1llll1l1llIl1l1.ll11l1ll11ll11l1Il1l1
                l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1 = l1111l1llll1l1llIl1l1.l11ll1lll1l11111Il1l1(l1111l1llll1l1llIl1l1.ll11l1ll11ll11l1Il1l1)
                if (env.page_reload_on_start):
                    l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l11l1111l1l1l111Il1l1(2.0)

            return l1111l1llll1l1llIl1l1.ll1l111lll111ll1Il1l1(*ll1lll111111llllIl1l1, **l1l111l1lll11ll1Il1l1)

        lll1ll1ll111l1l1Il1l1.llll1l1l1l11l111Il1l1(django.core.management.commands.runserver.Command, 'get_handler', ll11lll111llll1lIl1l1)

    def lll111ll11111l11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().lll111ll11111l11Il1l1()

        import django.core.handlers.base

        l1111l1llll1l1llIl1l1.l11l11lll11l1111Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def ll11lll111llll1lIl1l1(l1l1111ll1111lllIl1l1: Any, l11l11lll1l111l1Il1l1: Any) -> Any:
            lll111111l1ll11lIl1l1 = l1111l1llll1l1llIl1l1.l11l11lll11l1111Il1l1(l1l1111ll1111lllIl1l1, l11l11lll1l111l1Il1l1)

            if ( not l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1):
                return lll111111l1ll11lIl1l1

            l1l1l1l1ll11llllIl1l1 = lll111111l1ll11lIl1l1.get('content-type')

            if (( not l1l1l1l1ll11llllIl1l1 or 'text/html' not in l1l1l1l1ll11llllIl1l1)):
                return lll111111l1ll11lIl1l1

            l111lllll1llll1lIl1l1 = lll111111l1ll11lIl1l1.content

            if (isinstance(l111lllll1llll1lIl1l1, bytes)):
                l111lllll1llll1lIl1l1 = l111lllll1llll1lIl1l1.decode('utf-8')

            ll1ll11lll1l11llIl1l1 = l1111l1llll1l1llIl1l1.ll11111ll11ll1llIl1l1.l1l111ll111l11l1Il1l1(l111lllll1llll1lIl1l1)

            lll111111l1ll11lIl1l1.content = ll1ll11lll1l11llIl1l1.encode('utf-8')
            lll111111l1ll11lIl1l1['content-length'] = str(len(lll111111l1ll11lIl1l1.content)).encode('ascii')
            return lll111111l1ll11lIl1l1

        django.core.handlers.base.BaseHandler.get_response = ll11lll111llll1lIl1l1  # type: ignore

    def l1llll1lll1ll1l1Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        super().l1llll1lll1ll1l1Il1l1(ll1lll11l11ll11lIl1l1)

        from django.apps.registry import Apps

        l1111l1llll1l1llIl1l1.l111l1lll111111lIl1l1 = Apps.register_model

        def l1lll1l11111l111Il1l1(*ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> Any:
            pass

        Apps.register_model = l1lll1l11111l111Il1l1

    def l11llllll11l1l11Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path, lll1l11l11l1l111Il1l1: List[lll1lllll1l1lll1Il1l1]) -> None:
        super().l11llllll11l1l11Il1l1(ll1lll11l11ll11lIl1l1, lll1l11l11l1l111Il1l1)

        if ( not l1111l1llll1l1llIl1l1.l111l1lll111111lIl1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = l1111l1llll1l1llIl1l1.l111l1lll111111lIl1l1
