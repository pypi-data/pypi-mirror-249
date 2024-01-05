import sys

from reloadium.corium.l1lll11111lll111Il1l1.ll11lll1l11lll1lIl1l1 import l111l1lll1lll1l1Il1l1

__RELOADIUM__ = True

l111l1lll1lll1l1Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class l11l11l1lll11111Il1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = l11l11l1lll11111Il1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
