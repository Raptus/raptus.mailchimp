from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _p

from raptus.mailchimp.interfaces import IConnector

class Configlet(BrowserView):
    template = ViewPageTemplateFile('configlet.pt')
    
    errors = {}
    values = {}
    account_data = []
    
    def __call__(self):
        props = getToolByName(context, 'portal_properties').raptus_mailchimp
        if self.request.form.has_key('mailchimp_save'):
            if self.connector.ping():
                props.mailchimp_api_key = self.values['mailchimp_apikey']
                
        self.connector = IConnector(self.context)
                
                
        return self.template()
    
    