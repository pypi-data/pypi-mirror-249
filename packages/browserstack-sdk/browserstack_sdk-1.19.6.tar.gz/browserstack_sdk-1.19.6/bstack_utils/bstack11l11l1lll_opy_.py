# coding: UTF-8
import sys
bstack1l1ll_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1l1ll1l_opy_ = 7
def bstack1lll11l_opy_ (bstack1ll11_opy_):
    global bstack11llll_opy_
    bstack1111ll1_opy_ = ord (bstack1ll11_opy_ [-1])
    bstack1111111_opy_ = bstack1ll11_opy_ [:-1]
    bstack1ll1_opy_ = bstack1111ll1_opy_ % len (bstack1111111_opy_)
    bstack1l11lll_opy_ = bstack1111111_opy_ [:bstack1ll1_opy_] + bstack1111111_opy_ [bstack1ll1_opy_:]
    if bstack1l1ll_opy_:
        bstack1ll1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack11ll11l_opy_ + bstack1111ll1_opy_) % bstack1l1ll1l_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack1ll1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack11ll11l_opy_ + bstack1111ll1_opy_) % bstack1l1ll1l_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack1ll1l11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _11l11ll11l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l111llll_opy_:
    def __init__(self, handler):
        self._11l11l1l1l_opy_ = {}
        self._11l111ll1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._11l11l1l1l_opy_[bstack1lll11l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪዂ")] = Module._inject_setup_function_fixture
        self._11l11l1l1l_opy_[bstack1lll11l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዃ")] = Module._inject_setup_module_fixture
        self._11l11l1l1l_opy_[bstack1lll11l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩዄ")] = Class._inject_setup_class_fixture
        self._11l11l1l1l_opy_[bstack1lll11l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫዅ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack11l111ll11_opy_(bstack1lll11l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ዆"))
        Module._inject_setup_module_fixture = self.bstack11l111ll11_opy_(bstack1lll11l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭዇"))
        Class._inject_setup_class_fixture = self.bstack11l111ll11_opy_(bstack1lll11l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ወ"))
        Class._inject_setup_method_fixture = self.bstack11l111ll11_opy_(bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨዉ"))
    def bstack11l11l1ll1_opy_(self, bstack11l11l1111_opy_, hook_type):
        meth = getattr(bstack11l11l1111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l111ll1l_opy_[hook_type] = meth
            setattr(bstack11l11l1111_opy_, hook_type, self.bstack11l11l1l11_opy_(hook_type))
    def bstack11l111l1ll_opy_(self, instance, bstack11l11l11ll_opy_):
        if bstack11l11l11ll_opy_ == bstack1lll11l_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦዊ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥዋ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢዌ"))
        if bstack11l11l11ll_opy_ == bstack1lll11l_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧው"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦዎ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣዏ"))
        if bstack11l11l11ll_opy_ == bstack1lll11l_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢዐ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨዑ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥዒ"))
        if bstack11l11l11ll_opy_ == bstack1lll11l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦዓ"):
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥዔ"))
            self.bstack11l11l1ll1_opy_(instance.obj, bstack1lll11l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢዕ"))
    @staticmethod
    def bstack11l111lll1_opy_(hook_type, func, args):
        if hook_type in [bstack1lll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬዖ"), bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ዗")]:
            _11l11ll11l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1l11_opy_(self, hook_type):
        def bstack11l11ll111_opy_(arg=None):
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨዘ"))
            result = None
            exception = None
            try:
                self.bstack11l111lll1_opy_(hook_type, self._11l111ll1l_opy_[hook_type], (arg,))
                result = Result(result=bstack1lll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዙ"))
            except Exception as e:
                result = Result(result=bstack1lll11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዚ"), exception=e)
                self.handler(hook_type, bstack1lll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪዛ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫዜ"), result)
        def bstack11l11l11l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1lll11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ዝ"))
            result = None
            exception = None
            try:
                self.bstack11l111lll1_opy_(hook_type, self._11l111ll1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1lll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧዞ"))
            except Exception as e:
                result = Result(result=bstack1lll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዟ"), exception=e)
                self.handler(hook_type, bstack1lll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨዠ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩዡ"), result)
        if hook_type in [bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪዢ"), bstack1lll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧዣ")]:
            return bstack11l11l11l1_opy_
        return bstack11l11ll111_opy_
    def bstack11l111ll11_opy_(self, bstack11l11l11ll_opy_):
        def bstack11l11l111l_opy_(this, *args, **kwargs):
            self.bstack11l111l1ll_opy_(this, bstack11l11l11ll_opy_)
            self._11l11l1l1l_opy_[bstack11l11l11ll_opy_](this, *args, **kwargs)
        return bstack11l11l111l_opy_