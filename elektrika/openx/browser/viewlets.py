from zope.interface import implements
from zope.component import getMultiAdapter, getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import view

from elektrika.openx.interfaces import IOpenXJSInvocation
from elektrika.openx import eOpenXMessageFactory as _ 

class OpenXBannerViewlet(ViewletBase):

    def code(self, zone, withText=False, target='_blank'):
        util = getUtility(IOpenXJSInvocation)
        return util.code(zone, withText, target)
    
    

