import time
from zope import interface, schema, component
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.formlib import form
from zope.schema.interfaces import IVocabularyFactory
from zope.app.form.browser import MultiCheckBoxWidget as MultiCheckBoxWidgetBase
from plone.memoize import ram
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.formlib.formbase import FormBase
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from raptus.mailchimp import MessageFactory as _
from raptus.mailchimp import interfaces

def _render_cachekey(fun, self):
    # raise ram.DontCache
    props = getToolByName(self.context, 'portal_properties').raptus_mailchimp
    key = '-'.join(self.data.getAvailableList())
    key += str(int(time.time()) / props.mailchimp_cache_sec) # cache for at most 100 seconds
    return key

@ram.cache(_render_cachekey)
def subscriber_list(context):
    import logging
    logging.info('call of cache function')
    connector = interfaces.IConnector(context)
    lists = connector.getLists()
    simpleTerms = []
    for li in context.getAvailableList():
        for dli in lists:
            if li == dli['id']:
                simpleTerms.append(SimpleTerm(value=dli['id'], title=dli['name']))
                break
    return SimpleVocabulary(simpleTerms)

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class InvalidEmailAddress(schema.ValidationError):
    __doc__ = _(u"Invalid email address")

class MultiCheckBoxWidget(MultiCheckBoxWidgetBase):
    """ because the form machinery expects to instantiate widgets with two parameters
        we need to override the constructor.
    """
    def __init__(self, field, request):
        MultiCheckBoxWidgetBase.__init__(self, field, field.value_type.vocabulary, request)

class ISubscriberForm(interface.Interface):
    """ The schema of subscriber view
        feel free to extend this schema and define your own.
        all possible fields you can find on mailchimp.com/api
    """

    subscriber_list = schema.List(
        title=_(u'Choose a List you want subscribe for'),
        required=True,
        value_type=schema.Choice(source='raptus.mailchimp.subscriber_list'))

    email = schema.TextLine(
        title=_(u'Email'),
        constraint=validateaddress)

    FNAME = schema.TextLine(
        title=_('Name'))

    LNAME = schema.TextLine(
        title=_('Surname'))
    

class SubscriberForm(FormBase):
    form_fields = form.Fields(ISubscriberForm, omit_readonly=True)
    template = ViewPageTemplateFile('subscriber.pt')
    

    def __init__(self, context, request):
        self.context, self.request = context, request
        self.subscriber_list_voc = component.getUtility(IVocabularyFactory,'raptus.mailchimp.subscriber_list')(self.context)
        
        props = getToolByName(self.context, 'portal_properties').raptus_mailchimp
        
        # hidde all fields they are not found in properties
        hidde = [field.field.getName() for field in self.form_fields if field.field.getName() not in props.mailchimp_available_fields]
        # change schema if there is only one list available
        if len(self.context.getAvailableList()) <= 1:
            hidde.append('subscriber_list')
            self.form_fields = form.Fields(ISubscriberForm, omit_readonly=True).omit(*hidde)
        else:
            self.form_fields = form.Fields(ISubscriberForm, omit_readonly=True).omit(*hidde)
            self.form_fields['subscriber_list'].custom_widget = MultiCheckBoxWidget
            
    @form.action(_('Subscribe'))
    def subscribe(self, action, data):
        connector = interfaces.IConnector(self.context)
        utils = getToolByName(self.context, 'plone_utils')
        
        email = data.pop('email')
        if (data.has_key('subscriber_list')):
            subscriber_list = data.pop('subscriber_list')
        else:
            subscriber_list = [li.token for li in self.subscriber_list_voc] 
        
        if len(subscriber_list) == 0:
            utils.addPortalMessage(_("You must choose at last one list."))
            return
        
        success, errors = connector.addSubscribe(subscriber_list, email, data)
        for err in errors:
            utils.addPortalMessage(' '.join(err.args),'error')
        if success:
            utils.addPortalMessage(_("You successfully subscribed for: ${lists}.", mapping=dict(lists=', '.join(success))))







