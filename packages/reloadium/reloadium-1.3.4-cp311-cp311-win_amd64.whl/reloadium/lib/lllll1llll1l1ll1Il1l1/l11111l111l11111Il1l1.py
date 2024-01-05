from dataclasses import dataclass, field
from types import CodeType, ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional
import inspect

from reloadium.lib.lllll1llll1l1ll1Il1l1.ll11111l1111l1llIl1l1 import l1ll11111ll11l1lIl1l1

if (TYPE_CHECKING):
    pass


__RELOADIUM__ = True


@dataclass
class ll1ll111lll1l1l1Il1l1(l1ll11111ll11l1lIl1l1):
    ll1l111l11l11l11Il1l1 = 'Numba'

    lll1ll1ll1l1l111Il1l1 = True

    def __post_init__(l1111l1llll1l1llIl1l1) -> None:
        super().__post_init__()

    def ll1ll1l11l1111llIl1l1(l1111l1llll1l1llIl1l1, l1l1lll11111llllIl1l1: ModuleType) -> None:
        if (l1111l1llll1l1llIl1l1.ll11ll1l11ll1l1lIl1l1(l1l1lll11111llllIl1l1, 'numba.core.bytecode')):
            l1111l1llll1l1llIl1l1.l1llllll1111ll11Il1l1()

    def l1llllll1111ll11Il1l1(l1111l1llll1l1llIl1l1) -> None:
        import numba.core.bytecode

        def l111l11ll1l1lll1Il1l1(l111ll111l1lll1lIl1l1) -> CodeType:  # type: ignore
            import ast
            lllll11111l111l1Il1l1 = getattr(l111ll111l1lll1lIl1l1, '__code__', getattr(l111ll111l1lll1lIl1l1, 'func_code', None))  # type: ignore

            if ('__rw_mode__' in lllll11111l111l1Il1l1.co_consts):  # type: ignore
                l11llll1ll1l111lIl1l1 = ast.parse(inspect.getsource(l111ll111l1lll1lIl1l1))
                l11llll111ll11llIl1l1 = l11llll1ll1l111lIl1l1.body[0]
                l11llll111ll11llIl1l1.decorator_list = []  # type: ignore

                ll1llll1l11lll11Il1l1 = compile(l11llll1ll1l111lIl1l1, filename=lllll11111l111l1Il1l1.co_filename, mode='exec')  # type: ignore
                lllll11111l111l1Il1l1 = ll1llll1l11lll11Il1l1.co_consts[0]

            return lllll11111l111l1Il1l1  # type: ignore

        numba.core.bytecode.get_code_object.__code__ = l111l11ll1l1lll1Il1l1.__code__
