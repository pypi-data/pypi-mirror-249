import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l111ll1111ll1l11Il1l1 import ll1l1ll11l1lllllIl1l1
from reloadium.corium.l1lll11111lll111Il1l1.llll1l1l1l11l111Il1l1 import lll1ll1ll111l1l1Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1, l1111l111l1lll11Il1l1
from reloadium.corium.l111lllll11l1ll1Il1l1 import l1llll11l11ll1llIl1l1
from reloadium.corium.l1lll11111lll111Il1l1 import l1ll11111l1l1111Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class ll1lll111111ll11Il1l1(l1111l111l1lll11Il1l1):
    l1l1111llllllll1Il1l1: "ll111111ll11lll1Il1l1"
    ll11llll1lll1l1lIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def l11l1lll1ll11l1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().l11l1lll1ll11l1lIl1l1()

        l1l1l1111111ll1lIl1l1 = list(_sessions.values())

        for ll1lllllllll1l1lIl1l1 in l1l1l1111111ll1lIl1l1:
            if ( not ll1lllllllll1l1lIl1l1.is_active):
                continue

            llllll1ll1l111llIl1l1 = ll1lllllllll1l1lIl1l1.begin_nested()
            l1111l1llll1l1llIl1l1.ll11llll1lll1l1lIl1l1.append(llllll1ll1l111llIl1l1)

    def __repr__(l1111l1llll1l1llIl1l1) -> str:
        return 'DbMemento'

    def l1111ll1111l1ll1Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l1111ll1111l1ll1Il1l1()

        while l1111l1llll1l1llIl1l1.ll11llll1lll1l1lIl1l1:
            llllll1ll1l111llIl1l1 = l1111l1llll1l1llIl1l1.ll11llll1lll1l1lIl1l1.pop()
            if (llllll1ll1l111llIl1l1.is_active):
                try:
                    llllll1ll1l111llIl1l1.rollback()
                except :
                    pass

    def l1ll111l11ll1111Il1l1(l1111l1llll1l1llIl1l1) -> None:
        super().l1ll111l11ll1111Il1l1()

        while l1111l1llll1l1llIl1l1.ll11llll1lll1l1lIl1l1:
            llllll1ll1l111llIl1l1 = l1111l1llll1l1llIl1l1.ll11llll1lll1l1lIl1l1.pop()
            if (llllll1ll1l111llIl1l1.is_active):
                try:
                    llllll1ll1l111llIl1l1.commit()
                except :
                    pass


@dataclass
class ll111111ll11lll1Il1l1(l1l11111lll111l1Il1l1):
    ll1l111l11l11l11Il1l1 = 'Sqlalchemy'

    ll111ll1l1l1l11lIl1l1: List["Engine"] = field(init=False, default_factory=list)
    l1l1l1111111ll1lIl1l1: Set["Session"] = field(init=False, default_factory=set)
    ll1llllllll1111lIl1l1: Tuple[int, ...] = field(init=False)

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'sqlalchemy')):
            l1111l1llll1l1llIl1l1.l1ll1ll1l1lll111Il1l1(l1l1lll11111llllIl1l1)

        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'sqlalchemy.engine.base')):
            l1111l1llll1l1llIl1l1.ll1l1l11lll1l111Il1l1(l1l1lll11111llllIl1l1)

    def l1ll1ll1l1lll111Il1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: Any) -> None:
        l111lllll1llll1lIl1l1 = Path(l1l1lll11111llllIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l111lllll1llll1lIl1l1)[0]

        lll1111l1l11ll11Il1l1 = [int(l11l11ll11111l1lIl1l1) for l11l11ll11111l1lIl1l1 in __version__.split('.')]
        l1111l1llll1l1llIl1l1.ll1llllllll1111lIl1l1 = tuple(lll1111l1l11ll11Il1l1)

    def l111ll1lll1111l1Il1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str, ll1llll1111l1l1lIl1l1: bool) -> Optional["l1llll11l11ll1llIl1l1"]:
        lllll11111l111l1Il1l1 = ll1lll111111ll11Il1l1(ll1111lll1ll1ll1Il1l1=ll1111lll1ll1ll1Il1l1, l1l1111llllllll1Il1l1=l1111l1llll1l1llIl1l1)
        lllll11111l111l1Il1l1.l11l1lll1ll11l1lIl1l1()
        return lllll11111l111l1Il1l1

    def ll1l1l11lll1l111Il1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: Any) -> None:
        l111111ll11111l1Il1l1 = locals().copy()

        l111111ll11111l1Il1l1.update({'original': l1l1lll11111llllIl1l1.Engine.__init__, 'reloader_code': ll1l1ll11l1lllllIl1l1, 'engines': l1111l1llll1l1llIl1l1.ll111ll1l1l1l11lIl1l1})





        lllll1111ll111llIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        ll111lll1l11lll1Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (l1111l1llll1l1llIl1l1.ll1llllllll1111lIl1l1 <= (1, 3, 24, )):
            exec(lllll1111ll111llIl1l1, {**globals(), **l111111ll11111l1Il1l1}, l111111ll11111l1Il1l1)
        else:
            exec(ll111lll1l11lll1Il1l1, {**globals(), **l111111ll11111l1Il1l1}, l111111ll11111l1Il1l1)

        lll1ll1ll111l1l1Il1l1.llll1l1l1l11l111Il1l1(l1l1lll11111llllIl1l1.Engine, '__init__', l111111ll11111l1Il1l1['patched'])
