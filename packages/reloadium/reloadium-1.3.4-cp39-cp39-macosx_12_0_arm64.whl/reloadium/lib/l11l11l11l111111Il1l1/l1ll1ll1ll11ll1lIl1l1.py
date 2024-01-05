from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import ll1l11lllll1ll11Il1l1, l111ll1111ll1l11Il1l1, public, lll11111111lllllIl1l1, l1lll11111lll111Il1l1
from reloadium.corium.lll11ll1ll1l1ll1Il1l1 import lll1111lll1l11llIl1l1, llllllll111l1l1lIl1l1
from reloadium.corium.l111ll1111ll1l11Il1l1 import l1l11111l1l11111Il1l1, ll1l1ll11l1lllllIl1l1, l1111ll1l111lll1Il1l1
from reloadium.corium.l111ll1lll11l11lIl1l1 import llll1111l11llll1Il1l1
from reloadium.corium.l1llll11lllll1llIl1l1 import l1llll11lllll1llIl1l1
from reloadium.corium.ll1l11l111ll1l1lIl1l1 import l11111l1ll1ll111Il1l1
from reloadium.corium.l111lllll11l1ll1Il1l1 import l1llll11l11ll1llIl1l1, lll1ll11ll11l1llIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['llllllll11llll1lIl1l1', 'llll11l1l11ll111Il1l1', 'll1111ll111lll1lIl1l1']


ll1111111111111lIl1l1 = l1llll11lllll1llIl1l1.l11l1l1ll1l1lll1Il1l1(__name__)


class llllllll11llll1lIl1l1:
    @classmethod
    def l1ll11lllll1l111Il1l1(l1111l1llll1l1llIl1l1) -> Optional[FrameType]:
        llll1lll1l11l111Il1l1: FrameType = sys._getframe(2)
        lllll11111l111l1Il1l1 = next(l1lll11111lll111Il1l1.llll1lll1l11l111Il1l1.ll1l1lll11l111llIl1l1(llll1lll1l11l111Il1l1))
        return lllll11111l111l1Il1l1


class llll11l1l11ll111Il1l1(llllllll11llll1lIl1l1):
    @classmethod
    def l1llllllllll111lIl1l1(l1111llll11111llIl1l1, ll1lll111111llllIl1l1: List[Any], lll11lllllll1ll1Il1l1: Dict[str, Any], lll11111lll11l1lIl1l1: List[l1llll11l11ll1llIl1l1]) -> Any:  # type: ignore
        with ll1l1ll11l1lllllIl1l1():
            assert llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1
            llll1lll1l11l111Il1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1.l1l11l1lll1llll1Il1l1.ll1l11l1llllll11Il1l1()
            llll1lll1l11l111Il1l1.l1l111l1ll111ll1Il1l1()

            ll1lll11lll1l1l1Il1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.llll1llllllll11lIl1l1.ll1l111l11ll111lIl1l1(llll1lll1l11l111Il1l1.ll1llll1l11lll11Il1l1, llll1lll1l11l111Il1l1.lll1l111lll1lll1Il1l1.ll11l1ll11ll111lIl1l1())
            assert ll1lll11lll1l1l1Il1l1
            llll11l111ll111lIl1l1 = l1111llll11111llIl1l1.l1ll11lllll1l111Il1l1()

            for l1ll11ll11111111Il1l1 in lll11111lll11l1lIl1l1:
                l1ll11ll11111111Il1l1.l1111ll1111l1ll1Il1l1()

            for l1ll11ll11111111Il1l1 in lll11111lll11l1lIl1l1:
                l1ll11ll11111111Il1l1.l1ll111l11ll1111Il1l1()


        lllll11111l111l1Il1l1 = ll1lll11lll1l1l1Il1l1(*ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1);        llll1lll1l11l111Il1l1.l1ll1lll1ll1l1l1Il1l1.additional_info.pydev_step_stop = llll11l111ll111lIl1l1  # type: ignore

        return lllll11111l111l1Il1l1

    @classmethod
    async def l11l1l1l1l1l1lllIl1l1(l1111llll11111llIl1l1, ll1lll111111llllIl1l1: List[Any], lll11lllllll1ll1Il1l1: Dict[str, Any], lll11111lll11l1lIl1l1: List[lll1ll11ll11l1llIl1l1]) -> Any:  # type: ignore
        with ll1l1ll11l1lllllIl1l1():
            assert llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1
            llll1lll1l11l111Il1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1.l1l11l1lll1llll1Il1l1.ll1l11l1llllll11Il1l1()
            llll1lll1l11l111Il1l1.l1l111l1ll111ll1Il1l1()

            ll1lll11lll1l1l1Il1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.llll1llllllll11lIl1l1.ll1l111l11ll111lIl1l1(llll1lll1l11l111Il1l1.ll1llll1l11lll11Il1l1, llll1lll1l11l111Il1l1.lll1l111lll1lll1Il1l1.ll11l1ll11ll111lIl1l1())
            assert ll1lll11lll1l1l1Il1l1
            llll11l111ll111lIl1l1 = l1111llll11111llIl1l1.l1ll11lllll1l111Il1l1()

            for l1ll11ll11111111Il1l1 in lll11111lll11l1lIl1l1:
                await l1ll11ll11111111Il1l1.l1111ll1111l1ll1Il1l1()

            for l1ll11ll11111111Il1l1 in lll11111lll11l1lIl1l1:
                await l1ll11ll11111111Il1l1.l1ll111l11ll1111Il1l1()


        lllll11111l111l1Il1l1 = await ll1lll11lll1l1l1Il1l1(*ll1lll111111llllIl1l1, **lll11lllllll1ll1Il1l1);        llll1lll1l11l111Il1l1.l1ll1lll1ll1l1l1Il1l1.additional_info.pydev_step_stop = llll11l111ll111lIl1l1  # type: ignore

        return lllll11111l111l1Il1l1


class ll1111ll111lll1lIl1l1(llllllll11llll1lIl1l1):
    @classmethod
    def l1llllllllll111lIl1l1(l1111llll11111llIl1l1) -> Optional[ModuleType]:  # type: ignore
        with ll1l1ll11l1lllllIl1l1():
            assert llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1
            llll1lll1l11l111Il1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.l11l11l11l111111Il1l1.l1l11l1lll1llll1Il1l1.ll1l11l1llllll11Il1l1()

            ll1111ll1lll1l11Il1l1 = Path(llll1lll1l11l111Il1l1.ll1llll1lll11ll1Il1l1.f_globals['__spec__'].origin).absolute()
            lllll11llll11ll1Il1l1 = llll1lll1l11l111Il1l1.ll1llll1lll11ll1Il1l1.f_globals['__name__']
            llll1lll1l11l111Il1l1.l1l111l1ll111ll1Il1l1()
            ll11lllll111ll1lIl1l1 = llll1111l11llll1Il1l1.l1l11lll111lllllIl1l1.llll111lll1111l1Il1l1.ll1l1111lll1l11lIl1l1(ll1111ll1lll1l11Il1l1)

            if ( not ll11lllll111ll1lIl1l1):
                ll1111111111111lIl1l1.l1l111lll1l111llIl1l1('Could not retrieve src.', l1l11111l11ll11lIl1l1={'file': l11111l1ll1ll111Il1l1.ll1lll11l11ll11lIl1l1(ll1111ll1lll1l11Il1l1), 
'fullname': l11111l1ll1ll111Il1l1.lllll11llll11ll1Il1l1(lllll11llll11ll1Il1l1)})

            assert ll11lllll111ll1lIl1l1

        try:
            ll11lllll111ll1lIl1l1.l1l1ll1ll111111lIl1l1()
            ll11lllll111ll1lIl1l1.lll11111111l1l11Il1l1(l1111ll1lllll11lIl1l1=False)
            ll11lllll111ll1lIl1l1.l1llllllllll11llIl1l1(l1111ll1lllll11lIl1l1=False)
        except l1l11111l1l11111Il1l1 as l1lll11ll1ll1111Il1l1:
            llll1lll1l11l111Il1l1.l11lllll1111l1llIl1l1(l1lll11ll1ll1111Il1l1)
            return None

        import importlib.util

        l1ll11ll11111l11Il1l1 = llll1lll1l11l111Il1l1.ll1llll1lll11ll1Il1l1.f_locals['__spec__']
        l1l1lll11111llllIl1l1 = importlib.util.module_from_spec(l1ll11ll11111l11Il1l1)

        ll11lllll111ll1lIl1l1.l1111l1lllll11llIl1l1(l1l1lll11111llllIl1l1)
        return l1l1lll11111llllIl1l1


llllllll111l1l1lIl1l1.l1111llll1111ll1Il1l1(lll1111lll1l11llIl1l1.l1111l1ll1lllll1Il1l1, llll11l1l11ll111Il1l1.l1llllllllll111lIl1l1)
llllllll111l1l1lIl1l1.l1111llll1111ll1Il1l1(lll1111lll1l11llIl1l1.ll111l11l11l1l1lIl1l1, llll11l1l11ll111Il1l1.l11l1l1l1l1l1lllIl1l1)
llllllll111l1l1lIl1l1.l1111llll1111ll1Il1l1(lll1111lll1l11llIl1l1.l11l11lll1lllll1Il1l1, ll1111ll111lll1lIl1l1.l1llllllllll111lIl1l1)
