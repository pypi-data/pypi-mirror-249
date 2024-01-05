from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1
from reloadium.corium.l11111llllll1ll1Il1l1 import lll1lllll1l1lll1Il1l1
from reloadium.corium.l1lll11111lll111Il1l1 import l1ll11111l1l1111Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class lllll1111ll1llllIl1l1(l1l11111lll111l1Il1l1):
    ll1l111l11l11l11Il1l1 = 'PyGame'

    lll1ll1ll1l1l111Il1l1 = True

    ll11lllllll1111lIl1l1: bool = field(init=False, default=False)

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l11llll111ll1111Il1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l11llll111ll1111Il1l1, 'pygame.base')):
            l1111l1llll1l1llIl1l1.lll1llll11l1ll1lIl1l1()

    def lll1llll11l1ll1lIl1l1(l1111l1llll1l1llIl1l1) -> None:
        import pygame.display

        l1lll1ll1l1l1l1lIl1l1 = pygame.display.update

        def ll11l11l11l1llllIl1l1(*ll1lll111111llllIl1l1: Any, **lll11lllllll1ll1Il1l1: Any) -> None:
            if (l1111l1llll1l1llIl1l1.ll11lllllll1111lIl1l1):
                l1ll11111l1l1111Il1l1.llll1l1lllll1111Il1l1(0.1)
                return None
            else:
                return l1lll1ll1l1l1l1lIl1l1(*ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1)

        pygame.display.update = ll11l11l11l1llllIl1l1

    def l1llll1lll1ll1l1Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path) -> None:
        l1111l1llll1l1llIl1l1.ll11lllllll1111lIl1l1 = True

    def l11llllll11l1l11Il1l1(l1111l1llll1l1llIl1l1, ll1lll11l11ll11lIl1l1: Path, lll1l11l11l1l111Il1l1: List[lll1lllll1l1lll1Il1l1]) -> None:
        l1111l1llll1l1llIl1l1.ll11lllllll1111lIl1l1 = False

    def l1ll111ll1111l11Il1l1(l1111l1llll1l1llIl1l1, l111l1l1l1ll11llIl1l1: Exception) -> None:
        l1111l1llll1l1llIl1l1.ll11lllllll1111lIl1l1 = False
