from Products.CMFCore.utils import getToolByName
from zope import interface, component
from raptus.mailchimp.interfaces import IConnector
import greatape

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

    def setNewAPIKey(self, apikey):
        self.mailChimp = greatape.MailChimp(apikey, self.props.mailchimp_ssl, self.props.mailchimp_debug)
        try:
            self.isValid = self.mailChimp(method='ping')
        except:
            self.isValid = False
