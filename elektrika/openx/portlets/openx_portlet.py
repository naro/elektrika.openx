import random 
from zope import schema 
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form 
from zope.interface import implements 
from plone.app.portlets.portlets import base 
from plone.memoize.instance import memoize 
from plone.portlets.interfaces import IPortletDataProvider 
from DateTime import DateTime 
from Acquisition import aq_inner 
from Products.CMFCore.interfaces import ICatalogTool 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile 
from Products.CMFCore.utils import getToolByName 

from elektrika.openx.interfaces import IOpenXJSInvocation
from elektrika.openx import eOpenXMessageFactory as _ 

class IOpenXPortlet(IPortletDataProvider): 
    zone = schema.Int(title=_(u'Zone number'), 
                      description=_(u'Enter zone number'), 
                      required=True) 
                       
    showBorder = schema.Bool(title=_(u"Show portlet border?"), 
                           description=u"", 
                           required=False,
                           default=False) 

    withText = schema.Bool(title=_(u"Append text to the banner?"), 
                           description=_(u"If enabled, there will be text of banner appended to the banner image"), 
                           required=False,
                           default=False) 
                           
    target = schema.TextLine(title=_(u"Target frame"), 
                             description=_(u"_blank, _new, nothing, frame name, ..."), 
                             required=False,
                             default=u'_blank') 

    cssClass = schema.TextLine(title=_(u"CSS class"), 
                             description=_(u"Enter css class for portlet. More than one class may be separated by space. Default is 'portlet portletOpenX'"), 
                             required=True,
                             default=u'portlet portletOpenX') 

    cssId = schema.TextLine(title=_(u"CSS ID"), 
                             description=_(u"Enter CSS ID for this portlet. This text must be unique around the page. Default is blank."), 
                             required=False,
                             default=u'') 

class Assignment(base.Assignment): 
    implements(IOpenXPortlet) 
    def __init__(self, zone=None, showBorder=False, withText=False, target=u'_blank', cssClass=None, cssId=None): 
        self.zone = zone 
        self.showBorder = showBorder
        self.withText = withText 
        self.target = target
        self.cssClass = cssClass
        self.cssId = cssId
         
    @property 
    def title(self): 
        return _(u"OpenX banner") 

class Renderer(base.Renderer): 
    render = ViewPageTemplateFile('openx_portlet.pt') 
    
    @property 
    def available(self): 
        return True
        
    @property
    def cssId(self):
        if self.data.cssId:
            return self.data.cssId
        else:
            return None

    @property
    def cssClass(self):
        return self.data.cssClass

    @property
    def showBorder(self):
        return self.data.showBorder
        
    def code(self): 
        util = getUtility(IOpenXJSInvocation)
        return util.code(self.data.zone, self.data.withText, self.data.target)
                       
class AddForm(base.AddForm): 
    form_fields = form.Fields(IOpenXPortlet) 
    label = _(u"Add OpenX portlet") 
    description = _(u"This portlet displays ad banners") 
    
    def create(self, data): 
        assignment = Assignment() 
        form.applyChanges(assignment, self.form_fields, data) 
        return assignment 
        
class EditForm(base.EditForm): 
    form_fields = form.Fields(IOpenXPortlet) 
    label = _(u"Edit OpenX portlet") 
    description = _(u"This portlet displays ad banners.") 

