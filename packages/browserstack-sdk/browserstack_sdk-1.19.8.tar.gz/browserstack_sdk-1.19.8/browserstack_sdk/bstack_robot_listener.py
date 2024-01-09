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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111l11ll_opy_ import RobotHandler
from bstack_utils.capture import bstack1l11lll1ll_opy_
from bstack_utils.bstack1l11l1lll1_opy_ import bstack1l11l1l1ll_opy_, bstack1l11l111ll_opy_, bstack1l111l1ll1_opy_
from bstack_utils.bstack11l1ll11l_opy_ import bstack1ll1llll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1lllll1l11_opy_, bstack111l11lll_opy_, Result, \
    bstack1l11111lll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧക"): [],
        bstack11lllll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪഖ"): [],
        bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩഗ"): []
    }
    bstack1l111llll1_opy_ = []
    bstack1l11ll111l_opy_ = []
    @staticmethod
    def bstack1l11ll11ll_opy_(log):
        if not (log[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧഘ")] and log[bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨങ")].strip()):
            return
        active = bstack1ll1llll1l_opy_.bstack1l1111llll_opy_()
        log = {
            bstack11lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧച"): log[bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨഛ")],
            bstack11lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ജ"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"ࠫ࡟࠭ഝ"),
            bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഞ"): log[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧട")],
        }
        if active:
            if active[bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬഠ")] == bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ഡ"):
                log[bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩഢ")] = active[bstack11lllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪണ")]
            elif active[bstack11lllll_opy_ (u"ࠫࡹࡿࡰࡦࠩത")] == bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࠪഥ"):
                log[bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ദ")] = active[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧധ")]
        bstack1ll1llll1l_opy_.bstack1l11ll1111_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111ll1ll_opy_ = None
        self._1l1111l1ll_opy_ = None
        self._1l1l11111l_opy_ = OrderedDict()
        self.bstack1l1111ll1l_opy_ = bstack1l11lll1ll_opy_(self.bstack1l11ll11ll_opy_)
    @bstack1l11111lll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11llll1l_opy_()
        if not self._1l1l11111l_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫന")), None):
            self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬഩ"))] = {}
        bstack1l111lll1l_opy_ = bstack1l111l1ll1_opy_(
                bstack1l11lll111_opy_=attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭പ")),
                name=name,
                bstack1l1l111111_opy_=bstack111l11lll_opy_(),
                file_path=os.path.relpath(attrs[bstack11lllll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഫ")], start=os.getcwd()) if attrs.get(bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬബ")) != bstack11lllll_opy_ (u"࠭ࠧഭ") else bstack11lllll_opy_ (u"ࠧࠨമ"),
                framework=bstack11lllll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧയ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬര"), None)
        self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭റ"))][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧല")] = bstack1l111lll1l_opy_
    @bstack1l11111lll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11111l1l_opy_()
        self._1l11ll1l1l_opy_(messages)
        for bstack1l11lll1l1_opy_ in self.bstack1l111llll1_opy_:
            bstack1l11lll1l1_opy_[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧള")][bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬഴ")].extend(self.store[bstack11lllll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭വ")])
            bstack1ll1llll1l_opy_.bstack1l111l1111_opy_(bstack1l11lll1l1_opy_)
        self.bstack1l111llll1_opy_ = []
        self.store[bstack11lllll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧശ")] = []
    @bstack1l11111lll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l1111ll1l_opy_.start()
        if not self._1l1l11111l_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠩ࡬ࡨࠬഷ")), None):
            self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭സ"))] = {}
        driver = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪഹ"), None)
        bstack1l11l1lll1_opy_ = bstack1l111l1ll1_opy_(
            bstack1l11lll111_opy_=attrs.get(bstack11lllll_opy_ (u"ࠬ࡯ࡤࠨഺ")),
            name=name,
            bstack1l1l111111_opy_=bstack111l11lll_opy_(),
            file_path=os.path.relpath(attrs[bstack11lllll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ഻࠭")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1111ll11_opy_(attrs.get(bstack11lllll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫഼ࠧ"), None)),
            framework=bstack11lllll_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧഽ"),
            tags=attrs[bstack11lllll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧാ")],
            hooks=self.store[bstack11lllll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩി")],
            bstack1l11l11ll1_opy_=bstack1ll1llll1l_opy_.bstack1l11l1l1l1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11lllll_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨീ").format(bstack11lllll_opy_ (u"ࠧࠦࠢു").join(attrs[bstack11lllll_opy_ (u"࠭ࡴࡢࡩࡶࠫൂ")]), name) if attrs[bstack11lllll_opy_ (u"ࠧࡵࡣࡪࡷࠬൃ")] else name
        )
        self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠨ࡫ࡧࠫൄ"))][bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൅")] = bstack1l11l1lll1_opy_
        threading.current_thread().current_test_uuid = bstack1l11l1lll1_opy_.bstack1l11l1ll1l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11lllll_opy_ (u"ࠪ࡭ࡩ࠭െ"), None)
        self.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬേ"), bstack1l11l1lll1_opy_)
    @bstack1l11111lll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l1111ll1l_opy_.reset()
        bstack1l111l1l1l_opy_ = bstack1l11l1ll11_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬൈ")), bstack11lllll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ൉"))
        self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠧࡪࡦࠪൊ"))][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫോ")].stop(time=bstack111l11lll_opy_(), duration=int(attrs.get(bstack11lllll_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧൌ"), bstack11lllll_opy_ (u"ࠪ࠴്ࠬ"))), result=Result(result=bstack1l111l1l1l_opy_, exception=attrs.get(bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൎ")), bstack1l11lllll1_opy_=[attrs.get(bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൏"))]))
        self.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ൐"), self._1l1l11111l_opy_[attrs.get(bstack11lllll_opy_ (u"ࠧࡪࡦࠪ൑"))][bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൒")], True)
        self.store[bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭൓")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l11111lll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11llll1l_opy_()
        current_test_id = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬൔ"), None)
        bstack1l11llll11_opy_ = current_test_id if bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ൕ"), None) else bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨൖ"), None)
        if attrs.get(bstack11lllll_opy_ (u"࠭ࡴࡺࡲࡨࠫൗ"), bstack11lllll_opy_ (u"ࠧࠨ൘")).lower() in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൙"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ൚")]:
            hook_type = bstack1l111ll111_opy_(attrs.get(bstack11lllll_opy_ (u"ࠪࡸࡾࡶࡥࠨ൛")), bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ൜"), None))
            hook_name = bstack11lllll_opy_ (u"ࠬࢁࡽࠨ൝").format(attrs.get(bstack11lllll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭൞"), bstack11lllll_opy_ (u"ࠧࠨൟ")))
            if hook_type in [bstack11lllll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬൠ"), bstack11lllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬൡ")]:
                hook_name = bstack11lllll_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫൢ").format(bstack1l111l1lll_opy_.get(hook_type), attrs.get(bstack11lllll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൣ"), bstack11lllll_opy_ (u"ࠬ࠭൤")))
            bstack1l11ll1lll_opy_ = bstack1l11l111ll_opy_(
                bstack1l11lll111_opy_=bstack1l11llll11_opy_ + bstack11lllll_opy_ (u"࠭࠭ࠨ൥") + attrs.get(bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ൦"), bstack11lllll_opy_ (u"ࠨࠩ൧")).lower(),
                name=hook_name,
                bstack1l1l111111_opy_=bstack111l11lll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11lllll_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ൨")), start=os.getcwd()),
                framework=bstack11lllll_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ൩"),
                tags=attrs[bstack11lllll_opy_ (u"ࠫࡹࡧࡧࡴࠩ൪")],
                scope=RobotHandler.bstack1l1111ll11_opy_(attrs.get(bstack11lllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൫"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11ll1lll_opy_.bstack1l11l1ll1l_opy_()
            threading.current_thread().current_hook_id = bstack1l11llll11_opy_ + bstack11lllll_opy_ (u"࠭࠭ࠨ൬") + attrs.get(bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ൭"), bstack11lllll_opy_ (u"ࠨࠩ൮")).lower()
            self.store[bstack11lllll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൯")] = [bstack1l11ll1lll_opy_.bstack1l11l1ll1l_opy_()]
            if bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ൰"), None):
                self.store[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ൱")].append(bstack1l11ll1lll_opy_.bstack1l11l1ll1l_opy_())
            else:
                self.store[bstack11lllll_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ൲")].append(bstack1l11ll1lll_opy_.bstack1l11l1ll1l_opy_())
            if bstack1l11llll11_opy_:
                self._1l1l11111l_opy_[bstack1l11llll11_opy_ + bstack11lllll_opy_ (u"࠭࠭ࠨ൳") + attrs.get(bstack11lllll_opy_ (u"ࠧࡵࡻࡳࡩࠬ൴"), bstack11lllll_opy_ (u"ࠨࠩ൵")).lower()] = { bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ൶"): bstack1l11ll1lll_opy_ }
            bstack1ll1llll1l_opy_.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ൷"), bstack1l11ll1lll_opy_)
        else:
            bstack1l11l11l11_opy_ = {
                bstack11lllll_opy_ (u"ࠫ࡮ࡪࠧ൸"): uuid4().__str__(),
                bstack11lllll_opy_ (u"ࠬࡺࡥࡹࡶࠪ൹"): bstack11lllll_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬൺ").format(attrs.get(bstack11lllll_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧൻ")), attrs.get(bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ർ"), bstack11lllll_opy_ (u"ࠩࠪൽ"))) if attrs.get(bstack11lllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨൾ"), []) else attrs.get(bstack11lllll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫൿ")),
                bstack11lllll_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ඀"): attrs.get(bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫඁ"), []),
                bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫං"): bstack111l11lll_opy_(),
                bstack11lllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨඃ"): bstack11lllll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ඄"),
                bstack11lllll_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨඅ"): attrs.get(bstack11lllll_opy_ (u"ࠫࡩࡵࡣࠨආ"), bstack11lllll_opy_ (u"ࠬ࠭ඇ"))
            }
            if attrs.get(bstack11lllll_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧඈ"), bstack11lllll_opy_ (u"ࠧࠨඉ")) != bstack11lllll_opy_ (u"ࠨࠩඊ"):
                bstack1l11l11l11_opy_[bstack11lllll_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪඋ")] = attrs.get(bstack11lllll_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫඌ"))
            if not self.bstack1l11ll111l_opy_:
                self._1l1l11111l_opy_[self._1l11l11111_opy_()][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧඍ")].add_step(bstack1l11l11l11_opy_)
                threading.current_thread().current_step_uuid = bstack1l11l11l11_opy_[bstack11lllll_opy_ (u"ࠬ࡯ࡤࠨඎ")]
            self.bstack1l11ll111l_opy_.append(bstack1l11l11l11_opy_)
    @bstack1l11111lll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11111l1l_opy_()
        self._1l11ll1l1l_opy_(messages)
        current_test_id = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨඏ"), None)
        bstack1l11llll11_opy_ = current_test_id if current_test_id else bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪඐ"), None)
        bstack1l11lll11l_opy_ = bstack1l11l1ll11_opy_.get(attrs.get(bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨඑ")), bstack11lllll_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪඒ"))
        bstack1l11llllll_opy_ = attrs.get(bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫඓ"))
        if bstack1l11lll11l_opy_ != bstack11lllll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬඔ") and not attrs.get(bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ඕ")) and self._1l111ll1ll_opy_:
            bstack1l11llllll_opy_ = self._1l111ll1ll_opy_
        bstack1l11ll1ll1_opy_ = Result(result=bstack1l11lll11l_opy_, exception=bstack1l11llllll_opy_, bstack1l11lllll1_opy_=[bstack1l11llllll_opy_])
        if attrs.get(bstack11lllll_opy_ (u"࠭ࡴࡺࡲࡨࠫඖ"), bstack11lllll_opy_ (u"ࠧࠨ඗")).lower() in [bstack11lllll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ඘"), bstack11lllll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ඙")]:
            bstack1l11llll11_opy_ = current_test_id if current_test_id else bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ක"), None)
            if bstack1l11llll11_opy_:
                bstack1l111ll1l1_opy_ = bstack1l11llll11_opy_ + bstack11lllll_opy_ (u"ࠦ࠲ࠨඛ") + attrs.get(bstack11lllll_opy_ (u"ࠬࡺࡹࡱࡧࠪග"), bstack11lllll_opy_ (u"࠭ࠧඝ")).lower()
                self._1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඞ")].stop(time=bstack111l11lll_opy_(), duration=int(attrs.get(bstack11lllll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඟ"), bstack11lllll_opy_ (u"ࠩ࠳ࠫච"))), result=bstack1l11ll1ll1_opy_)
                bstack1ll1llll1l_opy_.bstack1l1111l11l_opy_(bstack11lllll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬඡ"), self._1l1l11111l_opy_[bstack1l111ll1l1_opy_][bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧජ")])
        else:
            bstack1l11llll11_opy_ = current_test_id if current_test_id else bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧඣ"), None)
            if bstack1l11llll11_opy_ and len(self.bstack1l11ll111l_opy_) == 1:
                current_step_uuid = bstack1lllll1l11_opy_(threading.current_thread(), bstack11lllll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪඤ"), None)
                self._1l1l11111l_opy_[bstack1l11llll11_opy_][bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪඥ")].bstack1l1l111l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11lllll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ඦ"), bstack11lllll_opy_ (u"ࠩ࠳ࠫට"))), result=bstack1l11ll1ll1_opy_)
            else:
                self.bstack1l11ll11l1_opy_(attrs)
            self.bstack1l11ll111l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11lllll_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨඨ"), bstack11lllll_opy_ (u"ࠫࡳࡵࠧඩ")) == bstack11lllll_opy_ (u"ࠬࡿࡥࡴࠩඪ"):
                return
            self.messages.push(message)
            bstack1l1l1111ll_opy_ = []
            if bstack1ll1llll1l_opy_.bstack1l1111llll_opy_():
                bstack1l1l1111ll_opy_.append({
                    bstack11lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩණ"): bstack111l11lll_opy_(),
                    bstack11lllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඬ"): message.get(bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩත")),
                    bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨථ"): message.get(bstack11lllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩද")),
                    **bstack1ll1llll1l_opy_.bstack1l1111llll_opy_()
                })
                if len(bstack1l1l1111ll_opy_) > 0:
                    bstack1ll1llll1l_opy_.bstack1l11ll1111_opy_(bstack1l1l1111ll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll1llll1l_opy_.bstack1l11l1111l_opy_()
    def bstack1l11ll11l1_opy_(self, bstack1l111ll11l_opy_):
        if not bstack1ll1llll1l_opy_.bstack1l1111llll_opy_():
            return
        kwname = bstack11lllll_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪධ").format(bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬන")), bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"࠭ࡡࡳࡩࡶࠫ඲"), bstack11lllll_opy_ (u"ࠧࠨඳ"))) if bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ප"), []) else bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩඵ"))
        error_message = bstack11lllll_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤබ").format(kwname, bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫභ")), str(bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ම"))))
        bstack1l111lll11_opy_ = bstack11lllll_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧඹ").format(kwname, bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧය")))
        bstack1l11l11l1l_opy_ = error_message if bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩර")) else bstack1l111lll11_opy_
        bstack1l1l111l11_opy_ = {
            bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ඼"): self.bstack1l11ll111l_opy_[-1].get(bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧල"), bstack111l11lll_opy_()),
            bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ඾"): bstack1l11l11l1l_opy_,
            bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ඿"): bstack11lllll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬව") if bstack1l111ll11l_opy_.get(bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧශ")) == bstack11lllll_opy_ (u"ࠨࡈࡄࡍࡑ࠭ෂ") else bstack11lllll_opy_ (u"ࠩࡌࡒࡋࡕࠧස"),
            **bstack1ll1llll1l_opy_.bstack1l1111llll_opy_()
        }
        bstack1ll1llll1l_opy_.bstack1l11ll1111_opy_([bstack1l1l111l11_opy_])
    def _1l11l11111_opy_(self):
        for bstack1l11lll111_opy_ in reversed(self._1l1l11111l_opy_):
            bstack1l1111l1l1_opy_ = bstack1l11lll111_opy_
            data = self._1l1l11111l_opy_[bstack1l11lll111_opy_][bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭හ")]
            if isinstance(data, bstack1l11l111ll_opy_):
                if not bstack11lllll_opy_ (u"ࠫࡊࡇࡃࡉࠩළ") in data.bstack1l1111l111_opy_():
                    return bstack1l1111l1l1_opy_
            else:
                return bstack1l1111l1l1_opy_
    def _1l11ll1l1l_opy_(self, messages):
        try:
            bstack1l11ll1l11_opy_ = BuiltIn().get_variable_value(bstack11lllll_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦෆ")) in (bstack1l11l111l1_opy_.DEBUG, bstack1l11l111l1_opy_.TRACE)
            for message, bstack1l111lllll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ෇"))
                level = message.get(bstack11lllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭෈"))
                if level == bstack1l11l111l1_opy_.FAIL:
                    self._1l111ll1ll_opy_ = name or self._1l111ll1ll_opy_
                    self._1l1111l1ll_opy_ = bstack1l111lllll_opy_.get(bstack11lllll_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ෉")) if bstack1l11ll1l11_opy_ and bstack1l111lllll_opy_ else self._1l1111l1ll_opy_
        except:
            pass
    @classmethod
    def bstack1l1111l11l_opy_(self, event: str, bstack1l111l11l1_opy_: bstack1l11l1l1ll_opy_, bstack1l11111ll1_opy_=False):
        if event == bstack11lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧ්ࠫ"):
            bstack1l111l11l1_opy_.set(hooks=self.store[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ෋")])
        if event == bstack11lllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬ෌"):
            event = bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ෍")
        if bstack1l11111ll1_opy_:
            bstack1l11l1l11l_opy_ = {
                bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ෎"): event,
                bstack1l111l11l1_opy_.bstack1l11l1l111_opy_(): bstack1l111l11l1_opy_.bstack1l11l11lll_opy_(event)
            }
            self.bstack1l111llll1_opy_.append(bstack1l11l1l11l_opy_)
        else:
            bstack1ll1llll1l_opy_.bstack1l1111l11l_opy_(event, bstack1l111l11l1_opy_)
class Messages:
    def __init__(self):
        self._1l1l1111l1_opy_ = []
    def bstack1l11llll1l_opy_(self):
        self._1l1l1111l1_opy_.append([])
    def bstack1l11111l1l_opy_(self):
        return self._1l1l1111l1_opy_.pop() if self._1l1l1111l1_opy_ else list()
    def push(self, message):
        self._1l1l1111l1_opy_[-1].append(message) if self._1l1l1111l1_opy_ else self._1l1l1111l1_opy_.append([message])
class bstack1l11l111l1_opy_:
    FAIL = bstack11lllll_opy_ (u"ࠧࡇࡃࡌࡐࠬා")
    ERROR = bstack11lllll_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧැ")
    WARNING = bstack11lllll_opy_ (u"࡚ࠩࡅࡗࡔࠧෑ")
    bstack1l11l1llll_opy_ = bstack11lllll_opy_ (u"ࠪࡍࡓࡌࡏࠨි")
    DEBUG = bstack11lllll_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪී")
    TRACE = bstack11lllll_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫු")
    bstack1l111l111l_opy_ = [FAIL, ERROR]
def bstack1l1111lll1_opy_(bstack1l111l1l11_opy_):
    if not bstack1l111l1l11_opy_:
        return None
    if bstack1l111l1l11_opy_.get(bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෕"), None):
        return getattr(bstack1l111l1l11_opy_[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪූ")], bstack11lllll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭෗"), None)
    return bstack1l111l1l11_opy_.get(bstack11lllll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧෘ"), None)
def bstack1l111ll111_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11lllll_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩෙ"), bstack11lllll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ේ")]:
        return
    if hook_type.lower() == bstack11lllll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫෛ"):
        if current_test_uuid is None:
            return bstack11lllll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪො")
        else:
            return bstack11lllll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬෝ")
    elif hook_type.lower() == bstack11lllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪෞ"):
        if current_test_uuid is None:
            return bstack11lllll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬෟ")
        else:
            return bstack11lllll_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ෠")