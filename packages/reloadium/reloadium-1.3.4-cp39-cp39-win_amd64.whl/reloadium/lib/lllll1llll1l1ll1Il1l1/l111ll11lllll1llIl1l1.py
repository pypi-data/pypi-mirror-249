import dataclasses
import types
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1
from reloadium.fast.lllll1llll1l1ll1Il1l1.l111ll11lllll1llIl1l1 import l1l11llllll1ll1lIl1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class ll1ll11ll111ll1lIl1l1(l1l11111lll111l1Il1l1):
    ll1l111l11l11l11Il1l1 = 'Pytest'

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'pytest')):
            l1111l1llll1l1llIl1l1.l1111l11llllll1lIl1l1(l1l1lll11111llllIl1l1)

    def l1111l11llllll1lIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = l1l11llllll1ll1lIl1l1  # type: ignore

