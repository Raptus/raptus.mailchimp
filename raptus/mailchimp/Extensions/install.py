from logging import getLogger

from Products.CMFCore.utils import getToolByName

logger = getLogger('raptus.mailchimp')

def uninstall(portal):
    configTool = getToolByName(portal, 'portal_controlpanel')
    try:
        configTool.unregisterConfiglet('MailchimpConfiglet')
    except:
        logger.error('unregistering MailchimpConfiglet failed')