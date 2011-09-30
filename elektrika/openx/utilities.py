import random
from zope.interface import implements
from zope.app.component.hooks import getSite 
from elektrika.openx.interfaces import IOpenXJSInvocation
import logging
logger = logging.getLogger('elektrika.openx')


class OpenXJSInvocation(object):
    implements(IOpenXJSInvocation)

    def code(self, zone, withtext=0, target='_blank', context=None):
        try:
            zone = int(zone)
        except ValueError:
            return ''

        # try to get ad server name
        if context is None:
            context = getSite()

        if getattr(context, 'getProperty', None) is None:
            # do not fail if site is not correctly determined (I experienced 
            # it eg. on inline validation)
            return
        server = context.getProperty('openx_server', '')
        
        if not server:
            logger.error("No OpenX server defined. Please set server URL in plone site property 'openx_server'. Do not include http:// in the server name!")
            return ''
            
        text = """
        <script type="text/javascript"><!--//<![CDATA[
           var m3_u = (location.protocol=='https:'?'https://%(server)s/www/delivery/ajs.php':'http://%(server)s/www/delivery/ajs.php');
           var m3_r = Math.floor(Math.random()*99999999999);
           if (!document.MAX_used) document.MAX_used = ',';
           document.write ("<scr"+"ipt type='text/javascript' src='"+m3_u);
        """ % {'server': server}
        subtext = 'document.write ("?zoneid=%s' % zone
        if withtext:
            subtext = subtext + '&amp;withtext=1'
        if target:
            subtext = subtext + '&amp;target=%s' % target
        subtext = subtext + '");' 
        text = text + subtext
        text = text + """  
           document.write ('&amp;cb=' + m3_r);
           if (document.MAX_used != ',') document.write ("&amp;exclude=" + document.MAX_used);
           document.write (document.charset ? '&amp;charset='+document.charset : (document.characterSet ? '&amp;charset='+document.characterSet : ''));
           document.write ("&amp;loc=" + escape(window.location));
           if (document.referrer) document.write ("&amp;referer=" + escape(document.referrer));
           if (document.context) document.write ("&context=" + escape(document.context));
           if (document.mmm_fo) document.write ("&amp;mmm_fo=1");
           document.write ("'><\/scr"+"ipt>");
        //]]>--></script>
        """
        rnd = random.randint(10000,99999)
        text = text + """<noscript><a href="http://%s/www/delivery/ck.php?n=acbe940d&amp;cb==%d" target="_blank"><img src="http://%s/www/delivery/avw.php?zoneid=%s&amp;cb=%d&amp;n=acbe940d" border="0" alt="" /></a></noscript>""" % (server, rnd, server, zone, rnd)

        return text
