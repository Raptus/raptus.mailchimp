from zope.formlib import form
from zope.app.form.browser import MultiCheckBoxWidget as MultiCheckBoxWidgetBase
from Products.Five.formlib.formbase import FormBase
from zope import interface, schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from raptus.mailchimp import MessageFactory as _
from raptus.mailchimp import interfaces

def subscriber_list(context):
    return context.getAvailableList()

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

    """
    merge_vars examples:
    
    
    FNAME = schema.TextLine(
        title=_('Name'))

    LNAME = schema.TextLine(
        title=_('Surname'))
    """
    

class SubscriberForm(FormBase):
    form_fields = form.Fields(ISubscriberForm, omit_readonly=True)
    template = ViewPageTemplateFile('subscriber.pt')
    

    def __init__(self, context, request):
        self.context, self.request = context, request
        self.connector = interfaces.IConnector(self.context)
        # change schema if there is only one list available
        if len(self.context.getAvailableList()) <= 1:
            self.form_fields = form.Fields(ISubscriberForm, omit_readonly=True).omit('subscriber_list')
        else:
            self.form_fields = form.Fields(ISubscriberForm, omit_readonly=True)
            self.form_fields['subscriber_list'].custom_widget = MultiCheckBoxWidget
        
    @form.action(_('Subscribe'))
    def subscribe(self, action, data):
        utils = getToolByName(self.context, 'plone_utils')
        
        email = data.pop('email')
        if (data.has_key('subscriber_list')):
            subscriber_list = data.pop('subscriber_list')
        else:
            subscriber_list = [li.token for li in self.context.getAvailableList()] 
        
        if len(subscriber_list) == 0:
            utils.addPortalMessage(_("You must choose at last one list."))
            return
        
        success, errors = self.connector.addSubscribe(subscriber_list, email, data)
        for err in errors:
            utils.addPortalMessage(' '.join(err.args),'error')
        if success:
            utils.addPortalMessage(_("You successfully subscribed for: ${lists}.", mapping=dict(lists=', '.join(success))))








