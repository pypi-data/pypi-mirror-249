from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.ll11ll1lll1ll111Il1l1 import l11l1ll11lllll1lIl1l1, ll1l1l11ll1l1lllIl1l1
from reloadium.corium.l1llll11lllll1llIl1l1 import lll1111111lll1llIl1l1, l1llll11lllll1llIl1l1
from reloadium.corium.l11111llllll1ll1Il1l1 import lll1lllll1l1lll1Il1l1, lllll1l111111111Il1l1
from reloadium.corium.l111lllll11l1ll1Il1l1 import l1llll11l11ll1llIl1l1, lll1ll11ll11l1llIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.lib.lllll1llll1l1ll1Il1l1.ll1ll1ll1l1lll1lIl1l1 import ll11111l1llll111Il1l1


__RELOADIUM__ = True

ll1111111111111lIl1l1 = l1llll11lllll1llIl1l1.l11l1l1ll1l1lll1Il1l1(__name__)


@dataclass
class l1l11111lll111l1Il1l1:
    ll1ll1ll1l1lll1lIl1l1: "ll11111l1llll111Il1l1"
    ll11ll1lll1ll111Il1l1: l11l1ll11lllll1lIl1l1

    ll1l111l11l11l11Il1l1: ClassVar[str] = NotImplemented
    l11lll111l1llll1Il1l1: bool = field(init=False, default=False)

    lll111ll111l1111Il1l1: lll1111111lll1llIl1l1 = field(init=False)

    lll1ll1l1l1l1ll1Il1l1: bool = field(init=False, default=False)

    lll1ll1ll1l1l111Il1l1 = False

    def __post_init__(l1111l1llll1l1llIl1l1) -> None:
        l1111l1llll1l1llIl1l1.lll111ll111l1111Il1l1 = l1llll11lllll1llIl1l1.l11l1l1ll1l1lll1Il1l1(l1111l1llll1l1llIl1l1.ll1l111l11l11l11Il1l1)
        l1111l1llll1l1llIl1l1.lll111ll111l1111Il1l1.l11l1111ll111ll1Il1l1('Creating extension')
        l1111l1llll1l1llIl1l1.ll1ll1ll1l1lll1lIl1l1.l1l11lll111lllllIl1l1.ll111l11lll1lll1Il1l1.l1lll11lll1ll111Il1l1(l1111l1llll1l1llIl1l1.l11llll1l11ll111Il1l1())
        l1111l1llll1l1llIl1l1.lll1ll1l1l1l1ll1Il1l1 = isinstance(l1111l1llll1l1llIl1l1.ll11ll1lll1ll111Il1l1, ll1l1l11ll1l1lllIl1l1)

    def l11llll1l11ll111Il1l1(l1111l1llll1l1llIl1l1) -> List[Type[lllll1l111111111Il1l1]]:
        lllll11111l111l1Il1l1 = []
        l11111llllll1ll1Il1l1 = l1111l1llll1l1llIl1l1.l111111ll11l1l11Il1l1()
        for lll11l1111l11ll1Il1l1 in l11111llllll1ll1Il1l1:
            lll11l1111l11ll1Il1l1.llll11l1llllll11Il1l1 = l1111l1llll1l1llIl1l1.ll1l111l11l11l11Il1l1

        lllll11111l111l1Il1l1.extend(l11111llllll1ll1Il1l1)
        return lllll11111l111l1Il1l1

    def l1ll1111lll11l1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        l1111l1llll1l1llIl1l1.l11lll111l1llll1Il1l1 = True

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def lll1lllll1l11l1lIl1l1(l1111llll11111llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> bool:
        if ( not hasattr(l1l1lll11111llllIl1l1, '__name__')):
            return False

        lllll11111l111l1Il1l1 = l1l1lll11111llllIl1l1.__name__.split('.')[0].lower() == l1111llll11111llIl1l1.ll1l111l11l11l11Il1l1.lower()
        return lllll11111l111l1Il1l1

    def l1ll1l1l11l1llllIl1l1(l1111l1llll1l1llIl1l1) -> None:
        ll1111111111111lIl1l1.l11l1111ll111ll1Il1l1(''.join(['Disabling extension ', '{:{}}'.format(l1111l1llll1l1llIl1l1.ll1l111l11l11l11Il1l1, '')]))

    @contextmanager
    def lll1lll1l1111111Il1l1(l1111l1llll1l1llIl1l1) -> Generator[None, None, None]:
        yield 

    def lll1l111lll1l11lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        pass

    def l1ll111ll1111l11Il1l1(l1111l1llll1l1llIl1l1, l111l1l1l1ll11llIl1l1: Exception) -> None:
        pass

    def l111ll1lll1111l1Il1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str, ll1llll1111l1l1lIl1l1: bool) -> Optional[l1llll11l11ll1llIl1l1]:
        return None

    async def ll1lll11l1111l1lIl1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str) -> Optional[lll1ll11ll11l1llIl1l1]:
        return None

    def l111ll1ll11lllllIl1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str) -> Optional[l1llll11l11ll1llIl1l1]:
        return None

    async def ll1ll11ll1llll1lIl1l1(l1111l1llll1l1llIl1l1, ll1111lll1ll1ll1Il1l1: str) -> Optional[lll1ll11ll11l1llIl1l1]:
        return None

    def ll11ll11llll111lIl1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        pass

    def l1llll1lll1ll1l1Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        pass

    def l11llllll11l1l11Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path, lll1l11l11l1l111Il1l1: List[lll1lllll1l1lll1Il1l1]) -> None:
        pass

    def __eq__(l1111l1llll1l1llIl1l1, llll11111lll11l1Il1l1: Any) -> bool:
        return id(llll11111lll11l1Il1l1) == id(l1111l1llll1l1llIl1l1)

    def l111111ll11l1l11Il1l1(l1111l1llll1l1llIl1l1) -> List[Type[lllll1l111111111Il1l1]]:
        return []

    def ll11ll1l11ll1l1lIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType, ll1111lll1ll1ll1Il1l1: str) -> bool:
        lllll11111l111l1Il1l1 = (hasattr(l1l1lll11111llllIl1l1, '__name__') and l1l1lll11111llllIl1l1.__name__ == ll1111lll1ll1ll1Il1l1)
        return lllll11111l111l1Il1l1


@dataclass(repr=False)
class l1111l111l1lll11Il1l1(l1llll11l11ll1llIl1l1):
    l1l1111llllllll1Il1l1: l1l11111lll111l1Il1l1

    def __repr__(l1111l1llll1l1llIl1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class l1lllll1l1111l1lIl1l1(lll1ll11ll11l1llIl1l1):
    l1l1111llllllll1Il1l1: l1l11111lll111l1Il1l1

    def __repr__(l1111l1llll1l1llIl1l1) -> str:
        return 'AsyncExtensionMemento'
