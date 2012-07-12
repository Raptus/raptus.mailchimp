import time
import greatape

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
        if self.mailChimp is None:
            self.setNewAPIKey(self.props.mailchimp_api_key)
        return self.mailChimp(method='getAccountDetails')

    @ram.cache(cache_key)
    def getLists(self):
        if self.mailChimp is None:
            self.setNewAPIKey(self.props.mailchimp_api_key)
        if self.isValid:
            try:
                return self.mailChimp(method='lists')
            except:
                pass
        return []

    def addSubscribe(self, ids, email_address, merge_vars={}, **kwargs):
        if self.mailChimp is None:
            self.setNewAPIKey(self.props.mailchimp_api_key)
        defaults = dict(email_type=self.props.lists_email_type,
                        double_optin=self.props.lists_double_optin,
                        update_existing=self.props.lists_update_existing,
                        replace_interests=self.props.lists_replace_interests,
                        send_welcome=self.props.lists_send_welcome)
        defaults.update(kwargs)

        # quick fix if merge_vars are empty
        if not len(merge_vars):
            merge_vars = dict(dummy='dummy')

        errors = []
        success = []
        lists = self.getLists()
        for id in ids:
            if id in [li['id'] for li in lists]:
                name = [i for i in lists if i['id'] == id][0]['name']
                try:
                    self.mailChimp(method='listSubscribe',
                                   id=id,
                                   email_address=email_address,
                                   merge_vars=merge_vars,
                                   **defaults)
                    success.append(name)
                except KeyError, error:
                    # special error for non-ascii chars
                    # backward compatibility
                    error.args = getattr(error, 'args', tuple())
                    error.args = [_('Invalid character: ${char}',
                                    mapping=dict(char=msg))\
                                  for msg in error.args or [error.msg]]
                    errors.append(error)
                except Exception, error:
                    mapping = dict(email=email_address, list=name)
                    # backward compatibility
                    error.args = getattr(error, 'args', tuple())
                    error.args = [_(msg.replace(email_address, '${email}')\
                                    .replace(name, '${list}'),
                                    mapping=mapping)\
                                  for msg in error.args or [error.msg]]
                    errors.append(error)
            else:
                msg = _(u'The chosen list is not available anymore.')
                errors.append(greatape.MailChimpError(msg))
        return success, errors

    def cleanUpLists(self, lists):
        return [li for li in lists if li in [i['id'] for i in self.getLists()]]

    def setNewAPIKey(self, apikey):
        self.mailChimp = greatape.MailChimp(apikey, self.props.mailchimp_ssl,
                                            self.props.mailchimp_debug)
        try:
            self.isValid = self.mailChimp(method='ping')
        except:
            self.isValid = False
