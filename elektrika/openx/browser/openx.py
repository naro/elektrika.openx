from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize import view

from elektrika.openx.interfaces import IOpenXJSInvocation

class OpenXView(BrowserView):
    """ This view may be used from any template 

        <div tal:define="openx context/openx_view"
             tal:replace="structure python:openx.code(38)" />

    """
    def code(self, zone, withText=False, target='_blank'):
        util = getUtility(IOpenXJSInvocation)
        return util.code(zone, withText, target)
