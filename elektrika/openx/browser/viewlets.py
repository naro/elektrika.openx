from zope.component import getUtility
from plone.app.layout.viewlets.common import ViewletBase
from elektrika.openx.interfaces import IOpenXJSInvocation

class OpenXBannerViewlet(ViewletBase):

    def code(self, zone, withText=False, target='_blank'):
        util = getUtility(IOpenXJSInvocation)
        return util.code(zone, withText, target)