from logging import getLogger

from Products.CMFCore.utils import getToolByName

logger = getLogger('raptus.mailchimp')

def install(portal, reinstall=False):
    setup_tool = getToolByName(portal, 'portal_setup')

    logger.info('installing raptus.mailchimp')
    
    logger.info('running default profile')
    setup_tool.runAllImportStepsFromProfile('profile-raptus.mailchimp:default')
    logger.info('ran default profile')
    
    if not reinstall:
        logger.info('running install profile (initial install)')
        setup_tool.runAllImportStepsFromProfile('profile-raptus.mailchimp:install')
        logger.info('ran install profile')
    
    logger.info('installation finished')


def uninstall(portal):
    configTool = getToolByName(portal, 'portal_controlpanel')
    try:
        configTool.unregisterConfiglet('MailchimpConfiglet')
    except:
        logger.error('unregister configlet raptus.mailchimp fail')