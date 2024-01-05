from contextlib import contextmanager
from pathlib import Path
import sys
import types
from threading import Timer, Thread
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, Set


import reloadium.lib.lllll1llll1l1ll1Il1l1.ll1l11lllll1lll1Il1l1
from reloadium.corium import lll1ll11l1lllll1Il1l1, ll1l11lllll1ll11Il1l1, l1lll11111lll111Il1l1
from reloadium.corium.lll1111ll11111llIl1l1 import l1l111l1ll111l11Il1l1
from reloadium.corium.ll11ll1lll1ll111Il1l1 import l11l1ll11lllll1lIl1l1, l1ll1lll1lll111lIl1l1
from reloadium.corium.lll11111111lllllIl1l1 import ll1ll11l11ll11l1Il1l1
from reloadium.corium.l1lll11111lll111Il1l1.l1ll1lll1ll1l1l1Il1l1 import lll1l11111lll11lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll11l11l111lllllIl1l1 import ll1lll1llllll111Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l111l111l1l111Il1l1 import ll111l111ll1111lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll11ll1ll1l11l11Il1l1 import l111111llll1111lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll111ll11l11ll1lIl1l1 import l111l1l11111ll11Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l11111l111l11111Il1l1 import ll1ll111lll1l1l1Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1llll1lll1l1l11Il1l1 import l1111ll1ll11llllIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll1l11l1l111l1l1Il1l1 import lllll1111ll1llllIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l111ll11lllll1llIl1l1 import ll1ll11ll111ll1lIl1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.ll1111l11ll1ll11Il1l1 import ll111111ll11lll1Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1ll1l1l1l1lll11Il1l1 import l11lll11l11l1lllIl1l1
from reloadium.corium.l1llll11lllll1llIl1l1 import l1llll11lllll1llIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.corium.l1l11lll111lllllIl1l1 import lllll11llll1llllIl1l1
    from reloadium.corium.l11111llllll1ll1Il1l1 import lll1lllll1l1lll1Il1l1


__RELOADIUM__ = True

ll1111111111111lIl1l1 = l1llll11lllll1llIl1l1.l11l1l1ll1l1lll1Il1l1(__name__)


@dataclass
class ll11111l1llll111Il1l1:
    l1l11lll111lllllIl1l1: "lllll11llll1llllIl1l1"

    lllll1llll1l1ll1Il1l1: List[l1l11111lll111l1Il1l1] = field(init=False, default_factory=list)

    ll1ll1l1l1l1llllIl1l1: List[types.ModuleType] = field(init=False, default_factory=list)

    l11ll111111ll111Il1l1: List[Type[l1l11111lll111l1Il1l1]] = field(init=False, default_factory=lambda :[l111111llll1111lIl1l1, l1111ll1ll11llllIl1l1, ll1lll1llllll111Il1l1, ll111111ll11lll1Il1l1, lllll1111ll1llllIl1l1, l111l1l11111ll11Il1l1, ll1ll11ll111ll1lIl1l1, l11lll11l11l1lllIl1l1, ll111l111ll1111lIl1l1, ll1ll111lll1l1l1Il1l1])




    ll1l1l111lll1111Il1l1: List[Type[l1l11111lll111l1Il1l1]] = field(init=False, default_factory=list)
    l1ll1l1ll1ll1111Il1l1 = (1 if l1l111l1ll111l11Il1l1().l11ll1l1ll11l1l1Il1l1 in [ll1ll11l11ll11l1Il1l1.llllll11ll1l1111Il1l1, ll1ll11l11ll11l1Il1l1.ll11l1ll11l1111lIl1l1] else 5)

    def __post_init__(l1111l1llll1l1llIl1l1) -> None:
        if (l1l111l1ll111l11Il1l1().ll1l1lll11lll1llIl1l1.l1l11llllll11ll1Il1l1):
            l1111l1llll1l1llIl1l1.l11ll111111ll111Il1l1.remove(ll1ll11ll111ll1lIl1l1)

        lll1l11111lll11lIl1l1(l1lll11l1111l1llIl1l1=l1111l1llll1l1llIl1l1.l11l11l11ll1l11lIl1l1, ll1111lll1ll1ll1Il1l1='show-forbidden-dialog').start()

    def l11l11l11ll1l11lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        l1lll11111lll111Il1l1.l1ll11111l1l1111Il1l1.llll1l1lllll1111Il1l1(l1111l1llll1l1llIl1l1.l1ll1l1ll1ll1111Il1l1)

        l1111l1llll1l1llIl1l1.l1l11lll111lllllIl1l1.l11ll1l1ll1l1111Il1l1.l1ll1lll1l1lllllIl1l1()

        if ( not l1111l1llll1l1llIl1l1.ll1l1l111lll1111Il1l1):
            return 

        lllll1llll1l1ll1Il1l1 = [l1lll11ll1ll1111Il1l1.ll1l111l11l11l11Il1l1 for l1lll11ll1ll1111Il1l1 in l1111l1llll1l1llIl1l1.ll1l1l111lll1111Il1l1]
        l1111l1llll1l1llIl1l1.l1l11lll111lllllIl1l1.l1lllll111ll1lllIl1l1.lll1111111l1ll1lIl1l1(l1ll1lll1lll111lIl1l1.l1ll11l1l111l1llIl1l1, ll1l11lllll1ll11Il1l1.lll11l1lll1ll1l1Il1l1.l111l11l1l1l1ll1Il1l1(lllll1llll1l1ll1Il1l1), 
ll11l11111ll1l1lIl1l1='')

    def lllll111111ll111Il1l1(l1111l1llll1l1llIl1l1, l1111l1l1ll11l11Il1l1: types.ModuleType) -> None:
        for l1l1l11lll11l1llIl1l1 in l1111l1llll1l1llIl1l1.l11ll111111ll111Il1l1.copy():
            if (l1l1l11lll11l1llIl1l1.lll1lllll1l11l1lIl1l1(l1111l1l1ll11l11Il1l1)):
                if (( not l1l1l11lll11l1llIl1l1.lll1ll1ll1l1l111Il1l1 and l1111l1llll1l1llIl1l1.l1l11lll111lllllIl1l1.l1lllll111ll1lllIl1l1.ll11ll1lll1ll111Il1l1.l1l1l11l11ll11llIl1l1([l1l1l11lll11l1llIl1l1.ll1l111l11l11l11Il1l1]) is False)):
                    l1111l1llll1l1llIl1l1.ll1l1l111lll1111Il1l1.append(l1l1l11lll11l1llIl1l1)
                    l1111l1llll1l1llIl1l1.l11ll111111ll111Il1l1.remove(l1l1l11lll11l1llIl1l1)
                    continue
                l1111l1llll1l1llIl1l1.l1l111ll1llll11lIl1l1(l1l1l11lll11l1llIl1l1)

        if (l1111l1l1ll11l11Il1l1 in l1111l1llll1l1llIl1l1.ll1ll1l1l1l1llllIl1l1):
            return 

        for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy():
            l1l1l111111ll1l1Il1l1.ll1ll1l11l1111llIl1l1(l1111l1l1ll11l11Il1l1)

        l1111l1llll1l1llIl1l1.ll1ll1l1l1l1llllIl1l1.append(l1111l1l1ll11l11Il1l1)

    def l1l111ll1llll11lIl1l1(l1111l1llll1l1llIl1l1, l1l1l11lll11l1llIl1l1: Type[l1l11111lll111l1Il1l1]) -> None:
        l11lll1l1l1ll111Il1l1 = l1l1l11lll11l1llIl1l1(l1111l1llll1l1llIl1l1, l1111l1llll1l1llIl1l1.l1l11lll111lllllIl1l1.l1lllll111ll1lllIl1l1.ll11ll1lll1ll111Il1l1)

        l1111l1llll1l1llIl1l1.l1l11lll111lllllIl1l1.l1l11l11ll11lll1Il1l1.l1l1l1lll111l11lIl1l1.l11l11l11111lll1Il1l1(lll1ll11l1lllll1Il1l1.ll1l1l1ll1llll1lIl1l1(l11lll1l1l1ll111Il1l1))
        l11lll1l1l1ll111Il1l1.lll1l111lll1l11lIl1l1()
        l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.append(l11lll1l1l1ll111Il1l1)

        if (l1l1l11lll11l1llIl1l1 in l1111l1llll1l1llIl1l1.l11ll111111ll111Il1l1):
            l1111l1llll1l1llIl1l1.l11ll111111ll111Il1l1.remove(l1l1l11lll11l1llIl1l1)

    @contextmanager
    def lll1lll1l1111111Il1l1(l1111l1llll1l1llIl1l1) -> Generator[None, None, None]:
        l1111l11ll1lllllIl1l1 = [l1l1l111111ll1l1Il1l1.lll1lll1l1111111Il1l1() for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy()]

        for ll11l1111l1l1ll1Il1l1 in l1111l11ll1lllllIl1l1:
            ll11l1111l1l1ll1Il1l1.__enter__()

        yield 

        for ll11l1111l1l1ll1Il1l1 in l1111l11ll1lllllIl1l1:
            ll11l1111l1l1ll1Il1l1.__exit__(*sys.exc_info())

    def l1llll1lll1ll1l1Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy():
            l1l1l111111ll1l1Il1l1.l1llll1lll1ll1l1Il1l1(ll1lll11l11ll11lIl1l1)

    def ll11ll11llll111lIl1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy():
            l1l1l111111ll1l1Il1l1.ll11ll11llll111lIl1l1(ll1lll11l11ll11lIl1l1)

    def l1ll111ll1111l11Il1l1(l1111l1llll1l1llIl1l1, l111l1l1l1ll11llIl1l1: Exception) -> None:
        for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy():
            l1l1l111111ll1l1Il1l1.l1ll111ll1111l11Il1l1(l111l1l1l1ll11llIl1l1)

    def l11llllll11l1l11Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path, lll1l11l11l1l111Il1l1: List["lll1lllll1l1lll1Il1l1"]) -> None:
        for l1l1l111111ll1l1Il1l1 in l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.copy():
            l1l1l111111ll1l1Il1l1.l11llllll11l1l11Il1l1(ll1lll11l11ll11lIl1l1, lll1l11l11l1l111Il1l1)

    def ll1111111lllll1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        l1111l1llll1l1llIl1l1.lllll1llll1l1ll1Il1l1.clear()
