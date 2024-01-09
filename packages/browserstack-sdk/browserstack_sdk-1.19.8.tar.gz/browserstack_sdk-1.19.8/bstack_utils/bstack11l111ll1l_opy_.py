# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack111ll11_opy_ = 2048
bstack11l1ll1_opy_ = 7
def bstack11lllll_opy_ (bstack11ll11_opy_):
    global bstack11ll1l_opy_
    bstack11l1lll_opy_ = ord (bstack11ll11_opy_ [-1])
    bstack1l11111_opy_ = bstack11ll11_opy_ [:-1]
    bstack1l111ll_opy_ = bstack11l1lll_opy_ % len (bstack1l11111_opy_)
    bstack1l1l1l_opy_ = bstack1l11111_opy_ [:bstack1l111ll_opy_] + bstack1l11111_opy_ [bstack1l111ll_opy_:]
    if bstack1111l11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll11_opy_ - (bstack1llll11_opy_ + bstack11l1lll_opy_) % bstack11l1ll1_opy_) for bstack1llll11_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack111ll11_opy_ - (bstack1llll11_opy_ + bstack11l1lll_opy_) % bstack11l1ll1_opy_) for bstack1llll11_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l11l1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11l11l1_opy_:
    def __init__(self, handler):
        self._11l111llll_opy_ = {}
        self._11l11l1lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l111llll_opy_[bstack11lllll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬዄ")] = Module._inject_setup_function_fixture
        self._11l111llll_opy_[bstack11lllll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫዅ")] = Module._inject_setup_module_fixture
        self._11l111llll_opy_[bstack11lllll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ዆")] = Class._inject_setup_class_fixture
        self._11l111llll_opy_[bstack11lllll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭዇")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l111l1l1_opy_(bstack11lllll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩወ"))
        Module._inject_setup_module_fixture = self.bstack11l111l1l1_opy_(bstack11lllll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዉ"))
        Class._inject_setup_class_fixture = self.bstack11l111l1l1_opy_(bstack11lllll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዊ"))
        Class._inject_setup_method_fixture = self.bstack11l111l1l1_opy_(bstack11lllll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዋ"))
    def bstack11l11ll111_opy_(self, bstack11l111ll11_opy_, hook_type):
        meth = getattr(bstack11l111ll11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11l1lll_opy_[hook_type] = meth
            setattr(bstack11l111ll11_opy_, hook_type, self.bstack11l11l1l11_opy_(hook_type))
    def bstack11l11l1l1l_opy_(self, instance, bstack11l11l11ll_opy_):
        if bstack11l11l11ll_opy_ == bstack11lllll_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዌ"):
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧው"))
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤዎ"))
        if bstack11l11l11ll_opy_ == bstack11lllll_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢዏ"):
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨዐ"))
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥዑ"))
        if bstack11l11l11ll_opy_ == bstack11lllll_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤዒ"):
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣዓ"))
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧዔ"))
        if bstack11l11l11ll_opy_ == bstack11lllll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዕ"):
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧዖ"))
            self.bstack11l11ll111_opy_(instance.obj, bstack11lllll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤ዗"))
    @staticmethod
    def bstack11l11l1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧዘ"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫዙ")]:
            _11l11l1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1l11_opy_(self, hook_type):
        def bstack11l111lll1_opy_(arg=None):
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪዚ"))
            result = None
            exception = None
            try:
                self.bstack11l11l1ll1_opy_(hook_type, self._11l11l1lll_opy_[hook_type], (arg,))
                result = Result(result=bstack11lllll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫዛ"))
            except Exception as e:
                result = Result(result=bstack11lllll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬዜ"), exception=e)
                self.handler(hook_type, bstack11lllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬዝ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ዞ"), result)
        def bstack11l11l111l_opy_(this, arg=None):
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨዟ"))
            result = None
            exception = None
            try:
                self.bstack11l11l1ll1_opy_(hook_type, self._11l11l1lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11lllll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዠ"))
            except Exception as e:
                result = Result(result=bstack11lllll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዡ"), exception=e)
                self.handler(hook_type, bstack11lllll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪዢ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዣ"), result)
        if hook_type in [bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬዤ"), bstack11lllll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩዥ")]:
            return bstack11l11l111l_opy_
        return bstack11l111lll1_opy_
    def bstack11l111l1l1_opy_(self, bstack11l11l11ll_opy_):
        def bstack11l111l1ll_opy_(this, *args, **kwargs):
            self.bstack11l11l1l1l_opy_(this, bstack11l11l11ll_opy_)
            self._11l111llll_opy_[bstack11l11l11ll_opy_](this, *args, **kwargs)
        return bstack11l111l1ll_opy_