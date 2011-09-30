from zope.interface import Interface

class IOpenXJSInvocation(Interface):
    def code(zone, withtext=0, target='_blank'):
        """ """
