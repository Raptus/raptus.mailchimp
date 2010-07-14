from zope.formlib import form
from zope.app.form.browser import MultiCheckBoxWidget as MultiCheckBoxWidgetBase
from Products.Five.formlib.formbase import FormBase
from zope import interface, schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from raptus.mailchimp import MessageFactory as _


def subscriber_list(context):
    return context.getAvailableList()

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
        title=_(u'Choose a List you want subscriber for'),
        description=_(u'Select available lists as subscribe in'),
        required=True,
        value_type=schema.Choice(source='raptus.mailchimp.subscriber_list'))

    
    email = schema.TextLine(
        title=_(u'Email'))
    

class SubscriberForm(FormBase):
    form_fields = form.Fields(ISubscriberForm, omit_readonly=True)
    template = ViewPageTemplateFile('subscriber.pt')
    
    form_fields['subscriber_list'].custom_widget = MultiCheckBoxWidget

    def __init__(self, context, request):
        self.context, self.request = context, request
        
    @form.action(_("Subscibe"))
    def subscibe(self, action, data):
        import logging
        logging.info(data)
        pass
        
