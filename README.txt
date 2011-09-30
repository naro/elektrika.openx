Introduction
============

Package integrates open source `OpenX ad server`_ with Plone. It is possible to
show banner from any OpenX "zone" in portlet, define custom viewlet and show
banners in viewlet or invoke banner from any template using public openx_view
Browser view.

Package supports Javascript invocation only. 

Configuration
=============

You must manually add new property openx_server to the Plone site root and set
domain name of your OpenX server **without scheme**. 'ad.domain.com' is
correct value, but 'http://ad.domain.com' is wrong!

Usage
=====

Portlet
-------

Use Manage portlets interface and add "OpenX portlet". You must specify OpenX
zone number and you may set additional properties.

Viewlet
-------

You must define your own viewlet in your own product. There is no default viewlet available for end-users. Example viewlet registration code::

    <browser:viewlet
        name="YOUR VIEWLET NAME EG. banner-top-468"
        for="*"
        manager="plone.app.layout.viewlets.interfaces.IPortalTop" - CHANGE MANAGER IPortalTop or IPortalHeader etc.
        class="elektrika.openx.browser.viewlets.OpenXBannerViewlet"
        template="banner.pt"  - change template, copy contents of banner.pt there and don't forget to set "ZONE" parameter inside template 
        layer=".interfaces.IThemeSpecific"  - specify your Layer or remove this line
        permission="zope.Public"
        />              

Common template
---------------

If you want to invoke OpenX banner from any other template, eg. customized
main_template or customized footer etc., you may use openx_view Browser view::

    <div tal:define="openx context/openx_view"
         tal:replace="structure python:openx.code(38)" />

'code' method supports parameters::
    
    openx_view.code(zone, withText=False, target='_blank')


.. _`OpenX ad server`: http://openx.org
