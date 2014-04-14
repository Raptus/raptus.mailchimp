import time
import mailchimp

from zope import interface, component

from Products.CMFCore.utils import getToolByName

from plone.memoize import ram

from raptus.mailchimp.interfaces import IConnector
from raptus.mailchimp import MessageFactory as _


def cache_key(func, self):
    return (func.__name__, self.props.mailchimp_api_key, int(time.time()) / self.props.mailchimp_cache_sec)


class Connector(object):
    interface.implements(IConnector)
    component.adapts(interface.Interface)

    # check if the apikey is valid and the connector is ready to fetch data
    isValid = False

    def __init__(self, context):
        self.context = context
        self.mailChimp = None
        portal_properties = getToolByName(self.context, 'portal_properties')
        self.props = portal_properties.raptus_mailchimp

    @ram.cache(cache_key)
    def getAccountDetails(self):
        self.checkConnection()

        return self.mailChimp.helper.account_details()

    @ram.cache(cache_key)
    def getLists(self):
        self.checkConnection()

        if self.isValid:
            try:
                lists = self.mailChimp.lists.list()
                lists = lists.get('data')
                return lists
            except:
                pass
        return []

    def checkConnection(self):
        if self.mailChimp is None:
            self.setNewAPIKey(self.props.mailchimp_api_key)

    def subscribe(self, ids, email, merge_vars={}, **kwargs):
        self.checkConnection()

        defaults = dict(email_type=self.props.subscribe_email_type,
                        double_optin=self.props.subscribe_double_optin,
                        update_existing=self.props.subscribe_update_existing,
                        replace_interests=self.props.subscribe_replace_interests,
                        send_welcome=self.props.subscribe_send_welcome)
        defaults.update(kwargs)

        errors = []
        success = []

        for id in ids:
            if id in self.cleanUpLists(ids):
                list_name = self.getListName(id)
                try:
                    self.mailChimp.lists.subscribe(id=id,
                                                   email={'email':email},
                                                   merge_vars=merge_vars,
                                                   **defaults)
                    success.append(list_name)

                except mailchimp.Error, error:
                    mapping = dict(email=email, list_name=list_name)
                    error = self.translateError(error)
                    error.args = [_(msg, mapping=mapping)\
                                  for msg in error.args or [error.message]]
                    errors.append(error)

            else:
                msg = _(u'The chosen list is not available anymore.')
                errors.append(msg)

        return success, errors

    def unsubscribe(self, ids, email, **kwargs):
        self.checkConnection()

        defaults = dict(delete_member=self.props.unsubscribe_delete_member,
                        send_goodbye=self.props.unsubscribe_send_goodbye,
                        send_notify=self.props.unsubscribe_send_notify)
        defaults.update(kwargs)

        errors = []
        success = []

        for id in ids:
            if id in self.cleanUpLists(ids):
                list_name = self.getListName(id)
                try:
                    self.mailChimp.lists.unsubscribe(id=id,
                                                     email={'email':email},
                                                     **defaults)
                    success.append(list_name)

                except mailchimp.Error, error:
                    mapping = dict(email=email, list_name=list_name)
                    error = self.translateError(error)
                    error.args = [_(msg, mapping=mapping)\
                                  for msg in error.args or [error.message]]
                    errors.append(error)

            else:
                msg = _(u'The chosen list is not available anymore.')
                errors.append(msg)

        return success, errors

    def cleanUpLists(self, lists):
        return [li for li in lists if li in [i['id'] for i in self.getLists()]]

    def setNewAPIKey(self, apikey):
        self.mailChimp = mailchimp.Mailchimp(apikey, self.props.mailchimp_debug)
        try:
            self.isValid = self.mailChimp.helper.ping()
        except:
            self.isValid = False

    def getListName(self, list_id):
        list = self.mailChimp.lists.list(filters={'list_id':list_id}).get('data')
        return list[0].get('name', _(u'Error retrieving list name'))

    def translateError(self, error):
        errorname = error.__class__.__name__

        if errorname == 'ListAlreadySubscribedError':
            error.message = u'${email} is already subscribed to list ${list_name}.'

        error.args = [error.message]

        return error
