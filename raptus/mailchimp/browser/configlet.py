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
        portal_properties = getToolByName(self.context, 'portal_properties')
        props = portal_properties.raptus_mailchimp
        utils = getToolByName(self.context, 'plone_utils')
        connector = None
        self.values.update(dict(mailchimp_apikey=props.mailchimp_api_key))

        if 'mailchimp_save' in self.request.form:
            connector = IConnector(self.context)
            mailchimp_apikey = self.request.form.get('mailchimp_apikey')
            connector.setNewAPIKey(mailchimp_apikey)
            if connector.isValid:
                props.mailchimp_api_key = mailchimp_apikey
            else:
                msg = _(u'The provided MailChimp API key is not valid')
                self.errors.update(dict(mailchimp_apikey=msg))
                msg = _(u'The given API-Key for MailChimp is not valid')
                utils.addPortalMessage(msg, 'error')
            self.values.update(dict(mailchimp_apikey=mailchimp_apikey))

        if not connector:
            connector = IConnector(self.context)
        if connector.isValid:
            self.account_data = connector.getAccountDetails()

        return self.template()
