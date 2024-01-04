# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll1ll_opy_ = 2048
bstack1l11l1l_opy_ = 7
def bstack111ll11_opy_ (bstack1111lll_opy_):
    global bstack111111_opy_
    bstack11l11l1_opy_ = ord (bstack1111lll_opy_ [-1])
    bstack1ll11l_opy_ = bstack1111lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack11l11l1_opy_ % len (bstack1ll11l_opy_)
    bstack1llllll_opy_ = bstack1ll11l_opy_ [:bstack1ll1lll_opy_] + bstack1ll11l_opy_ [bstack1ll1lll_opy_:]
    if bstack11111ll_opy_:
        bstack1l111l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1ll_opy_ - (bstack11111l_opy_ + bstack11l11l1_opy_) % bstack1l11l1l_opy_) for bstack11111l_opy_, char in enumerate (bstack1llllll_opy_)])
    else:
        bstack1l111l1_opy_ = str () .join ([chr (ord (char) - bstack1lll1ll_opy_ - (bstack11111l_opy_ + bstack11l11l1_opy_) % bstack1l11l1l_opy_) for bstack11111l_opy_, char in enumerate (bstack1llllll_opy_)])
    return eval (bstack1l111l1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l111l1ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111ll11_opy_:
    def __init__(self, handler):
        self._11l11l1l11_opy_ = {}
        self._11l111lll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l11l1l11_opy_[bstack111ll11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫዃ")] = Module._inject_setup_function_fixture
        self._11l11l1l11_opy_[bstack111ll11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዄ")] = Module._inject_setup_module_fixture
        self._11l11l1l11_opy_[bstack111ll11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዅ")] = Class._inject_setup_class_fixture
        self._11l11l1l11_opy_[bstack111ll11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ዆")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l111llll_opy_(bstack111ll11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ዇"))
        Module._inject_setup_module_fixture = self.bstack11l111llll_opy_(bstack111ll11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧወ"))
        Class._inject_setup_class_fixture = self.bstack11l111llll_opy_(bstack111ll11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧዉ"))
        Class._inject_setup_method_fixture = self.bstack11l111llll_opy_(bstack111ll11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዊ"))
    def bstack11l11l11l1_opy_(self, bstack11l111l1l1_opy_, hook_type):
        meth = getattr(bstack11l111l1l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l111lll1_opy_[hook_type] = meth
            setattr(bstack11l111l1l1_opy_, hook_type, self.bstack11l11l1ll1_opy_(hook_type))
    def bstack11l11l1l1l_opy_(self, instance, bstack11l11l11ll_opy_):
        if bstack11l11l11ll_opy_ == bstack111ll11_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧዋ"):
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦዌ"))
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣው"))
        if bstack11l11l11ll_opy_ == bstack111ll11_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨዎ"):
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧዏ"))
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤዐ"))
        if bstack11l11l11ll_opy_ == bstack111ll11_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣዑ"):
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢዒ"))
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦዓ"))
        if bstack11l11l11ll_opy_ == bstack111ll11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧዔ"):
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦዕ"))
            self.bstack11l11l11l1_opy_(instance.obj, bstack111ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣዖ"))
    @staticmethod
    def bstack11l111ll1l_opy_(hook_type, func, args):
        if hook_type in [bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭዗"), bstack111ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪዘ")]:
            _11l111l1ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1ll1_opy_(self, hook_type):
        def bstack11l11ll111_opy_(arg=None):
            self.handler(hook_type, bstack111ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩዙ"))
            result = None
            exception = None
            try:
                self.bstack11l111ll1l_opy_(hook_type, self._11l111lll1_opy_[hook_type], (arg,))
                result = Result(result=bstack111ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪዚ"))
            except Exception as e:
                result = Result(result=bstack111ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዛ"), exception=e)
                self.handler(hook_type, bstack111ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዜ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬዝ"), result)
        def bstack11l11l1111_opy_(this, arg=None):
            self.handler(hook_type, bstack111ll11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧዞ"))
            result = None
            exception = None
            try:
                self.bstack11l111ll1l_opy_(hook_type, self._11l111lll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack111ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨዟ"))
            except Exception as e:
                result = Result(result=bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩዠ"), exception=e)
                self.handler(hook_type, bstack111ll11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዡ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111ll11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪዢ"), result)
        if hook_type in [bstack111ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫዣ"), bstack111ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨዤ")]:
            return bstack11l11l1111_opy_
        return bstack11l11ll111_opy_
    def bstack11l111llll_opy_(self, bstack11l11l11ll_opy_):
        def bstack11l11l1lll_opy_(this, *args, **kwargs):
            self.bstack11l11l1l1l_opy_(this, bstack11l11l11ll_opy_)
            self._11l11l1l11_opy_[bstack11l11l11ll_opy_](this, *args, **kwargs)
        return bstack11l11l1lll_opy_