import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.corium.l1lll1ll1111ll1lIl1l1 import llll111ll1l1lll1Il1l1
from reloadium.lib.lllll1llll1l1ll1Il1l1.l1l1111llllllll1Il1l1 import l1l11111lll111l1Il1l1
from reloadium.lib import extensions_raw
from reloadium.corium.l111ll1lll11l11lIl1l1 import llll1111l11llll1Il1l1
from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class l11lll11l11l1lllIl1l1(l1l11111lll111l1Il1l1):
    ll1l111l11l11l11Il1l1 = 'Multiprocessing'

    lll1ll1ll1l1l111Il1l1 = True

    def __post_init__(l1111l1llll1l1llIl1l1) -> None:
        super().__post_init__()

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'multiprocessing.popen_spawn_posix')):
            l1111l1llll1l1llIl1l1.l11lll1l11111l1lIl1l1(l1l1lll11111llllIl1l1)

        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'multiprocessing.popen_spawn_win32')):
            l1111l1llll1l1llIl1l1.l111l1lll1111lllIl1l1(l1l1lll11111llllIl1l1)

    def l11lll1l11111l1lIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = extensions_raw.multiprocessing.posix_popen_launch  # type: ignore

    def l111l1lll1111lllIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = extensions_raw.multiprocessing.wind32_popen_launch  # type: ignore
