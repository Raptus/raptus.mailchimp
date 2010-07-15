from Products.CMFCore.utils import getToolByName
from zope import interface, component
import greatape
from raptus.mailchimp.interfaces import IConnector
from raptus.mailchimp import MessageFactory as _

class Connector(object):

    interface.implements(IConnector)
    component.adapts(interface.Interface)
    
    # check if the apikey is valid and the connector is ready to fetch data
    isValid = False

    def __init__(self, context):
        self.context = context
        self.props = getToolByName(self.context, 'portal_properties').raptus_mailchimp
        self.setNewAPIKey(self.props.mailchimp_api_key)

    def getAccountDetails(self):
        return self.mailChimp(method='getAccountDetails')

    def getLists(self):
        return self.mailChimp(method='lists')

    def addSubscribe(self, ids, email_address, merge_vars={}, **kwargs):
        defaults = dict(email_type = self.props.lists_email_type,
                        double_optin = self.props.lists_double_optin,
                        update_existing = self.props.lists_update_existing,
                        replace_interests = self.props.lists_replace_interests,
                        send_welcome = self.props.lists_send_welcome)
        defaults.update(kwargs)
        
        errors = []
        success =[]
        lists = self.getLists()
        for id in ids:
            if id in [li['id'] for li in lists]:
                try:
                    self.mailChimp(method='listSubscribe',id=id, email_address=email_address, merge_vars=merge_vars,**defaults)
                    success.append([i for i in lists if i['id']==id][0]['name'])
                except Exception, error:
                    errors.append(error)
            else:
                errors.append(greatape.MailChimpError(_('The chosen list is not more available')))
        return success, errors
            
    def cleanUpLists(self, lists):
        return [li for li in lists if li in [i['id'] for i in self.getLists()]]
        
            
    def setNewAPIKey(self, apikey):
        self.mailChimp = greatape.MailChimp(apikey, self.props.mailchimp_ssl, self.props.mailchimp_debug)
        try:
            self.isValid = self.mailChimp(method='ping')
        except:
            self.isValid = False
