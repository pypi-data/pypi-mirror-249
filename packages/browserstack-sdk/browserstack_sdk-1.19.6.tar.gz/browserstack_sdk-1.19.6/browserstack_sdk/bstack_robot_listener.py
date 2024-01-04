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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11ll1111_opy_ import RobotHandler
from bstack_utils.capture import bstack1l11lll1ll_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l11l11l11_opy_, bstack1l11lll1l1_opy_, bstack1l11l1l111_opy_
from bstack_utils.bstack1l1llll111_opy_ import bstack1l11ll1ll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1l1ll1_opy_, bstack1ll11ll1l_opy_, Result, \
    bstack1l1111l111_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ഔ"): [],
        bstack1lll11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩക"): [],
        bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨഖ"): []
    }
    bstack1l1111llll_opy_ = []
    bstack1l111l111l_opy_ = []
    @staticmethod
    def bstack1l111l1ll1_opy_(log):
        if not (log[bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഗ")] and log[bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧഘ")].strip()):
            return
        active = bstack1l11ll1ll_opy_.bstack1l11ll1l1l_opy_()
        log = {
            bstack1lll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ങ"): log[bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧച")],
            bstack1lll11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬഛ"): datetime.datetime.utcnow().isoformat() + bstack1lll11l_opy_ (u"ࠪ࡞ࠬജ"),
            bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬഝ"): log[bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ഞ")],
        }
        if active:
            if active[bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫട")] == bstack1lll11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬഠ"):
                log[bstack1lll11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨഡ")] = active[bstack1lll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩഢ")]
            elif active[bstack1lll11l_opy_ (u"ࠪࡸࡾࡶࡥࠨണ")] == bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩത"):
                log[bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬഥ")] = active[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ദ")]
        bstack1l11ll1ll_opy_.bstack1l11ll11l1_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111lll1l_opy_ = None
        self._1l11l1ll1l_opy_ = None
        self._1l1111l11l_opy_ = OrderedDict()
        self.bstack1l11111lll_opy_ = bstack1l11lll1ll_opy_(self.bstack1l111l1ll1_opy_)
    @bstack1l1111l111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l11ll11ll_opy_()
        if not self._1l1111l11l_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠧࡪࡦࠪധ")), None):
            self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫന"))] = {}
        bstack1l111lll11_opy_ = bstack1l11l1l111_opy_(
                bstack1l111llll1_opy_=attrs.get(bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬഩ")),
                name=name,
                bstack1l1l111l1l_opy_=bstack1ll11ll1l_opy_(),
                file_path=os.path.relpath(attrs[bstack1lll11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪപ")], start=os.getcwd()) if attrs.get(bstack1lll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫഫ")) != bstack1lll11l_opy_ (u"ࠬ࠭ബ") else bstack1lll11l_opy_ (u"࠭ࠧഭ"),
                framework=bstack1lll11l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭മ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫയ"), None)
        self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬര"))][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭റ")] = bstack1l111lll11_opy_
    @bstack1l1111l111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l1111l1ll_opy_()
        self._1l11l1ll11_opy_(messages)
        for bstack1l11ll1l11_opy_ in self.bstack1l1111llll_opy_:
            bstack1l11ll1l11_opy_[bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ല")][bstack1lll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫള")].extend(self.store[bstack1lll11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬഴ")])
            bstack1l11ll1ll_opy_.bstack1l1111lll1_opy_(bstack1l11ll1l11_opy_)
        self.bstack1l1111llll_opy_ = []
        self.store[bstack1lll11l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭വ")] = []
    @bstack1l1111l111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11111lll_opy_.start()
        if not self._1l1111l11l_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠨ࡫ࡧࠫശ")), None):
            self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬഷ"))] = {}
        driver = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩസ"), None)
        bstack1l11lllll1_opy_ = bstack1l11l1l111_opy_(
            bstack1l111llll1_opy_=attrs.get(bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧഹ")),
            name=name,
            bstack1l1l111l1l_opy_=bstack1ll11ll1l_opy_(),
            file_path=os.path.relpath(attrs[bstack1lll11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬഺ")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11l1l11l_opy_(attrs.get(bstack1lll11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ഻࠭"), None)),
            framework=bstack1lll11l_opy_ (u"ࠧࡓࡱࡥࡳࡹ഼࠭"),
            tags=attrs[bstack1lll11l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ഽ")],
            hooks=self.store[bstack1lll11l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨാ")],
            bstack1l111l11ll_opy_=bstack1l11ll1ll_opy_.bstack1l11llll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1lll11l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧി").format(bstack1lll11l_opy_ (u"ࠦࠥࠨീ").join(attrs[bstack1lll11l_opy_ (u"ࠬࡺࡡࡨࡵࠪു")]), name) if attrs[bstack1lll11l_opy_ (u"࠭ࡴࡢࡩࡶࠫൂ")] else name
        )
        self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"ࠧࡪࡦࠪൃ"))][bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫൄ")] = bstack1l11lllll1_opy_
        threading.current_thread().current_test_uuid = bstack1l11lllll1_opy_.bstack1l11l11ll1_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1lll11l_opy_ (u"ࠩ࡬ࡨࠬ൅"), None)
        self.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫെ"), bstack1l11lllll1_opy_)
    @bstack1l1111l111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11111lll_opy_.reset()
        bstack1l1l1111ll_opy_ = bstack1l11l1l1l1_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫേ")), bstack1lll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ൈ"))
        self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩ൉"))][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൊ")].stop(time=bstack1ll11ll1l_opy_(), duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ോ"), bstack1lll11l_opy_ (u"ࠩ࠳ࠫൌ"))), result=Result(result=bstack1l1l1111ll_opy_, exception=attrs.get(bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ്ࠫ")), bstack1l1l111l11_opy_=[attrs.get(bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൎ"))]))
        self.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ൏"), self._1l1111l11l_opy_[attrs.get(bstack1lll11l_opy_ (u"࠭ࡩࡥࠩ൐"))][bstack1lll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ൑")], True)
        self.store[bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ൒")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l1111l111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l11ll11ll_opy_()
        current_test_id = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ൓"), None)
        bstack1l11l11l1l_opy_ = current_test_id if bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬൔ"), None) else bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧൕ"), None)
        if attrs.get(bstack1lll11l_opy_ (u"ࠬࡺࡹࡱࡧࠪൖ"), bstack1lll11l_opy_ (u"࠭ࠧൗ")).lower() in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭൘"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ൙")]:
            hook_type = bstack1l111l11l1_opy_(attrs.get(bstack1lll11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ൚")), bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ൛"), None))
            hook_name = bstack1lll11l_opy_ (u"ࠫࢀࢃࠧ൜").format(attrs.get(bstack1lll11l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ൝"), bstack1lll11l_opy_ (u"࠭ࠧ൞")))
            if hook_type in [bstack1lll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫൟ"), bstack1lll11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫൠ")]:
                hook_name = bstack1lll11l_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪൡ").format(bstack1l111l1l1l_opy_.get(hook_type), attrs.get(bstack1lll11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪൢ"), bstack1lll11l_opy_ (u"ࠫࠬൣ")))
            bstack1l11l111l1_opy_ = bstack1l11lll1l1_opy_(
                bstack1l111llll1_opy_=bstack1l11l11l1l_opy_ + bstack1lll11l_opy_ (u"ࠬ࠳ࠧ൤") + attrs.get(bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ൥"), bstack1lll11l_opy_ (u"ࠧࠨ൦")).lower(),
                name=hook_name,
                bstack1l1l111l1l_opy_=bstack1ll11ll1l_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1lll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ൧")), start=os.getcwd()),
                framework=bstack1lll11l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ൨"),
                tags=attrs[bstack1lll11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ൩")],
                scope=RobotHandler.bstack1l11l1l11l_opy_(attrs.get(bstack1lll11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ൪"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l11l111l1_opy_.bstack1l11l11ll1_opy_()
            threading.current_thread().current_hook_id = bstack1l11l11l1l_opy_ + bstack1lll11l_opy_ (u"ࠬ࠳ࠧ൫") + attrs.get(bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ൬"), bstack1lll11l_opy_ (u"ࠧࠨ൭")).lower()
            self.store[bstack1lll11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ൮")] = [bstack1l11l111l1_opy_.bstack1l11l11ll1_opy_()]
            if bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭൯"), None):
                self.store[bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧ൰")].append(bstack1l11l111l1_opy_.bstack1l11l11ll1_opy_())
            else:
                self.store[bstack1lll11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ൱")].append(bstack1l11l111l1_opy_.bstack1l11l11ll1_opy_())
            if bstack1l11l11l1l_opy_:
                self._1l1111l11l_opy_[bstack1l11l11l1l_opy_ + bstack1lll11l_opy_ (u"ࠬ࠳ࠧ൲") + attrs.get(bstack1lll11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ൳"), bstack1lll11l_opy_ (u"ࠧࠨ൴")).lower()] = { bstack1lll11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൵"): bstack1l11l111l1_opy_ }
            bstack1l11ll1ll_opy_.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ൶"), bstack1l11l111l1_opy_)
        else:
            bstack1l11lll111_opy_ = {
                bstack1lll11l_opy_ (u"ࠪ࡭ࡩ࠭൷"): uuid4().__str__(),
                bstack1lll11l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ൸"): bstack1lll11l_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫ൹").format(attrs.get(bstack1lll11l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ൺ")), attrs.get(bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬൻ"), bstack1lll11l_opy_ (u"ࠨࠩർ"))) if attrs.get(bstack1lll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧൽ"), []) else attrs.get(bstack1lll11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪൾ")),
                bstack1lll11l_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫൿ"): attrs.get(bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪ඀"), []),
                bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪඁ"): bstack1ll11ll1l_opy_(),
                bstack1lll11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧං"): bstack1lll11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩඃ"),
                bstack1lll11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ඄"): attrs.get(bstack1lll11l_opy_ (u"ࠪࡨࡴࡩࠧඅ"), bstack1lll11l_opy_ (u"ࠫࠬආ"))
            }
            if attrs.get(bstack1lll11l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ඇ"), bstack1lll11l_opy_ (u"࠭ࠧඈ")) != bstack1lll11l_opy_ (u"ࠧࠨඉ"):
                bstack1l11lll111_opy_[bstack1lll11l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩඊ")] = attrs.get(bstack1lll11l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪඋ"))
            if not self.bstack1l111l111l_opy_:
                self._1l1111l11l_opy_[self._1l111lllll_opy_()][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ඌ")].add_step(bstack1l11lll111_opy_)
                threading.current_thread().current_step_uuid = bstack1l11lll111_opy_[bstack1lll11l_opy_ (u"ࠫ࡮ࡪࠧඍ")]
            self.bstack1l111l111l_opy_.append(bstack1l11lll111_opy_)
    @bstack1l1111l111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l1111l1ll_opy_()
        self._1l11l1ll11_opy_(messages)
        current_test_id = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧඎ"), None)
        bstack1l11l11l1l_opy_ = current_test_id if current_test_id else bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩඏ"), None)
        bstack1l111l1l11_opy_ = bstack1l11l1l1l1_opy_.get(attrs.get(bstack1lll11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧඐ")), bstack1lll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩඑ"))
        bstack1l1l111111_opy_ = attrs.get(bstack1lll11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪඒ"))
        if bstack1l111l1l11_opy_ != bstack1lll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫඓ") and not attrs.get(bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬඔ")) and self._1l111lll1l_opy_:
            bstack1l1l111111_opy_ = self._1l111lll1l_opy_
        bstack1l11ll1lll_opy_ = Result(result=bstack1l111l1l11_opy_, exception=bstack1l1l111111_opy_, bstack1l1l111l11_opy_=[bstack1l1l111111_opy_])
        if attrs.get(bstack1lll11l_opy_ (u"ࠬࡺࡹࡱࡧࠪඕ"), bstack1lll11l_opy_ (u"࠭ࠧඖ")).lower() in [bstack1lll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭඗"), bstack1lll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ඘")]:
            bstack1l11l11l1l_opy_ = current_test_id if current_test_id else bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬ඙"), None)
            if bstack1l11l11l1l_opy_:
                bstack1l11llllll_opy_ = bstack1l11l11l1l_opy_ + bstack1lll11l_opy_ (u"ࠥ࠱ࠧක") + attrs.get(bstack1lll11l_opy_ (u"ࠫࡹࡿࡰࡦࠩඛ"), bstack1lll11l_opy_ (u"ࠬ࠭ග")).lower()
                self._1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඝ")].stop(time=bstack1ll11ll1l_opy_(), duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬඞ"), bstack1lll11l_opy_ (u"ࠨ࠲ࠪඟ"))), result=bstack1l11ll1lll_opy_)
                bstack1l11ll1ll_opy_.bstack1l111l1lll_opy_(bstack1lll11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫච"), self._1l1111l11l_opy_[bstack1l11llllll_opy_][bstack1lll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ඡ")])
        else:
            bstack1l11l11l1l_opy_ = current_test_id if current_test_id else bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ජ"), None)
            if bstack1l11l11l1l_opy_ and len(self.bstack1l111l111l_opy_) == 1:
                current_step_uuid = bstack11l1l1ll1_opy_(threading.current_thread(), bstack1lll11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩඣ"), None)
                self._1l1111l11l_opy_[bstack1l11l11l1l_opy_][bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩඤ")].bstack1l11l11111_opy_(current_step_uuid, duration=int(attrs.get(bstack1lll11l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬඥ"), bstack1lll11l_opy_ (u"ࠨ࠲ࠪඦ"))), result=bstack1l11ll1lll_opy_)
            else:
                self.bstack1l11l1lll1_opy_(attrs)
            self.bstack1l111l111l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1lll11l_opy_ (u"ࠩ࡫ࡸࡲࡲࠧට"), bstack1lll11l_opy_ (u"ࠪࡲࡴ࠭ඨ")) == bstack1lll11l_opy_ (u"ࠫࡾ࡫ࡳࠨඩ"):
                return
            self.messages.push(message)
            bstack1l11ll1ll1_opy_ = []
            if bstack1l11ll1ll_opy_.bstack1l11ll1l1l_opy_():
                bstack1l11ll1ll1_opy_.append({
                    bstack1lll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨඪ"): bstack1ll11ll1l_opy_(),
                    bstack1lll11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧණ"): message.get(bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨඬ")),
                    bstack1lll11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧත"): message.get(bstack1lll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨථ")),
                    **bstack1l11ll1ll_opy_.bstack1l11ll1l1l_opy_()
                })
                if len(bstack1l11ll1ll1_opy_) > 0:
                    bstack1l11ll1ll_opy_.bstack1l11ll11l1_opy_(bstack1l11ll1ll1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l11ll1ll_opy_.bstack1l11ll111l_opy_()
    def bstack1l11l1lll1_opy_(self, bstack1l11l1111l_opy_):
        if not bstack1l11ll1ll_opy_.bstack1l11ll1l1l_opy_():
            return
        kwname = bstack1lll11l_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩද").format(bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫධ")), bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠬࡧࡲࡨࡵࠪන"), bstack1lll11l_opy_ (u"࠭ࠧ඲"))) if bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬඳ"), []) else bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨප"))
        error_message = bstack1lll11l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣඵ").format(kwname, bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪබ")), str(bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬභ"))))
        bstack1l11111l1l_opy_ = bstack1lll11l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦම").format(kwname, bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ඹ")))
        bstack1l1111ll11_opy_ = error_message if bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨය")) else bstack1l11111l1l_opy_
        bstack1l1111ll1l_opy_ = {
            bstack1lll11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫර"): self.bstack1l111l111l_opy_[-1].get(bstack1lll11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭඼"), bstack1ll11ll1l_opy_()),
            bstack1lll11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫල"): bstack1l1111ll11_opy_,
            bstack1lll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ඾"): bstack1lll11l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ඿") if bstack1l11l1111l_opy_.get(bstack1lll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ව")) == bstack1lll11l_opy_ (u"ࠧࡇࡃࡌࡐࠬශ") else bstack1lll11l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ෂ"),
            **bstack1l11ll1ll_opy_.bstack1l11ll1l1l_opy_()
        }
        bstack1l11ll1ll_opy_.bstack1l11ll11l1_opy_([bstack1l1111ll1l_opy_])
    def _1l111lllll_opy_(self):
        for bstack1l111llll1_opy_ in reversed(self._1l1111l11l_opy_):
            bstack1l11l111ll_opy_ = bstack1l111llll1_opy_
            data = self._1l1111l11l_opy_[bstack1l111llll1_opy_][bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬස")]
            if isinstance(data, bstack1l11lll1l1_opy_):
                if not bstack1lll11l_opy_ (u"ࠪࡉࡆࡉࡈࠨහ") in data.bstack1l111ll111_opy_():
                    return bstack1l11l111ll_opy_
            else:
                return bstack1l11l111ll_opy_
    def _1l11l1ll11_opy_(self, messages):
        try:
            bstack1l111ll1l1_opy_ = BuiltIn().get_variable_value(bstack1lll11l_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥළ")) in (bstack1l111l1111_opy_.DEBUG, bstack1l111l1111_opy_.TRACE)
            for message, bstack1l11llll1l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1lll11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ෆ"))
                level = message.get(bstack1lll11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෇"))
                if level == bstack1l111l1111_opy_.FAIL:
                    self._1l111lll1l_opy_ = name or self._1l111lll1l_opy_
                    self._1l11l1ll1l_opy_ = bstack1l11llll1l_opy_.get(bstack1lll11l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ෈")) if bstack1l111ll1l1_opy_ and bstack1l11llll1l_opy_ else self._1l11l1ll1l_opy_
        except:
            pass
    @classmethod
    def bstack1l111l1lll_opy_(self, event: str, bstack1l11lll11l_opy_: bstack1l11l11l11_opy_, bstack1l11l1l1ll_opy_=False):
        if event == bstack1lll11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ෉"):
            bstack1l11lll11l_opy_.set(hooks=self.store[bstack1lll11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ්࠭")])
        if event == bstack1lll11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ෋"):
            event = bstack1lll11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭෌")
        if bstack1l11l1l1ll_opy_:
            bstack1l1l11111l_opy_ = {
                bstack1lll11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ෍"): event,
                bstack1l11lll11l_opy_.bstack1l111ll1ll_opy_(): bstack1l11lll11l_opy_.bstack1l111ll11l_opy_(event)
            }
            self.bstack1l1111llll_opy_.append(bstack1l1l11111l_opy_)
        else:
            bstack1l11ll1ll_opy_.bstack1l111l1lll_opy_(event, bstack1l11lll11l_opy_)
class Messages:
    def __init__(self):
        self._1l11111ll1_opy_ = []
    def bstack1l11ll11ll_opy_(self):
        self._1l11111ll1_opy_.append([])
    def bstack1l1111l1ll_opy_(self):
        return self._1l11111ll1_opy_.pop() if self._1l11111ll1_opy_ else list()
    def push(self, message):
        self._1l11111ll1_opy_[-1].append(message) if self._1l11111ll1_opy_ else self._1l11111ll1_opy_.append([message])
class bstack1l111l1111_opy_:
    FAIL = bstack1lll11l_opy_ (u"࠭ࡆࡂࡋࡏࠫ෎")
    ERROR = bstack1lll11l_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭ා")
    WARNING = bstack1lll11l_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭ැ")
    bstack1l1l1111l1_opy_ = bstack1lll11l_opy_ (u"ࠩࡌࡒࡋࡕࠧෑ")
    DEBUG = bstack1lll11l_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩි")
    TRACE = bstack1lll11l_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪී")
    bstack1l1111l1l1_opy_ = [FAIL, ERROR]
def bstack1l11l11lll_opy_(bstack1l11l1llll_opy_):
    if not bstack1l11l1llll_opy_:
        return None
    if bstack1l11l1llll_opy_.get(bstack1lll11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨු"), None):
        return getattr(bstack1l11l1llll_opy_[bstack1lll11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෕")], bstack1lll11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬූ"), None)
    return bstack1l11l1llll_opy_.get(bstack1lll11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭෗"), None)
def bstack1l111l11l1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1lll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨෘ"), bstack1lll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬෙ")]:
        return
    if hook_type.lower() == bstack1lll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪේ"):
        if current_test_uuid is None:
            return bstack1lll11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩෛ")
        else:
            return bstack1lll11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫො")
    elif hook_type.lower() == bstack1lll11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩෝ"):
        if current_test_uuid is None:
            return bstack1lll11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫෞ")
        else:
            return bstack1lll11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ෟ")