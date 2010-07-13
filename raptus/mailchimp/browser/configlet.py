from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from raptus.mailchimp import MessageFactory as _

from raptus.mailchimp.interfaces import IConnector

class Configlet(BrowserView):
    template = ViewPageTemplateFile('configlet.pt')
    
    errors = {}
    values = {}
    account_data = None
    
    def __call__(self):
        props = getToolByName(self.context, 'portal_properties').raptus_mailchimp
        utils = getToolByName(self.context, 'plone_utils')
        connector= None
        self.values.update(dict(mailchimp_apikey = props.mailchimp_api_key))

        if self.request.form.has_key('mailchimp_save'):
            connector = IConnector(self.context)
            connector.setNewAPIKey(self.request.form.get('mailchimp_apikey'))
            if connector.isValid:
                props.mailchimp_api_key = self.request.form.get('mailchimp_apikey')
            else:
                self.errors.update(dict(mailchimp_apikey=_(u'The given API-Key for MailChimp is not valid')))
                utils.addPortalMessage(_(u'The given API-Key for MailChimp is not valid'),'error')
            self.values.update(dict(mailchimp_apikey = self.request.form.get('mailchimp_apikey')))
        
        if not connector:
            connector = IConnector(self.context)
        if connector.isValid:
            self.account_data = connector.getAccountDetails()
                
                
        return self.template()
    
    