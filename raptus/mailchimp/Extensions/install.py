from logging import getLogger

from Products.CMFCore.utils import getToolByName

# Properties are defined here, because if they are defined in propertiestool.xml,
# all properties are re-set the their initial state if you reinstall product
# in the quickinstaller.

_PROPERTIES = [ dict(name='mailchimp_api_key', type_='string', value=''),
                dict(name='mailchimp_debug', type_='boolean', value=False),
                dict(name='mailchimp_ssl', type_='boolean', value=True),
                dict(name='mailchimp_cache_sec', type_='int', value=500),
                dict(name='mailchimp_available_fields', type_='lines', value=['subscriber_list','email']),
                
                dict(name='lists_email_type', type_='string', value='html'),
                dict(name='lists_double_optin', type_='boolean', value=True),
                dict(name='lists_update_existing', type_='boolean', value=False),
                dict(name='lists_replace_interests', type_='boolean', value=True),
                dict(name='lists_send_welcome', type_='boolean', value=False),
              ]

logger = getLogger('raptus.mailchimp')

def import_various(portal, reinstall=False):
    if not portal.readDataFile('raptus_mailchimp_import_various.txt'):
        return

    logger.info('set properties')
    props = getToolByName(portal, 'portal_properties').raptus_mailchimp
    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])
    
    logger.info('import_various finished')


def uninstall(portal):
    configTool = getToolByName(portal, 'portal_controlpanel')
    try:
        configTool.unregisterConfiglet('MailchimpConfiglet')
    except:
        logger.error('unregister MailchimpConfiglet fail')