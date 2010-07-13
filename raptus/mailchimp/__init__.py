import zope.i18nmessageid

MessageFactory = zope.i18nmessageid.MessageFactory('raptus.mailchimp')

def initialize(context):
    pass
#path is now done with collective.monkeypatcher


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
