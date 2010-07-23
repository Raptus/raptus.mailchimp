from zope.formlib import form
from zope import schema, component
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from raptus.mailchimp import MessageFactory as _
from raptus.mailchimp import interfaces


def available_list(context):
    connector = interfaces.IConnector(context)
    lists = connector.getLists()
    if hasattr(context,'data'):
        context.data.available_list = connector.cleanUpLists(context.data.available_list)
    return SimpleVocabulary([SimpleTerm(value=li['id'], title=li['name']) for li in lists])

def errorMessage(context):
    if not interfaces.IConnector(context).isValid:
        utils = getToolByName(context, 'plone_utils')
        utils.addPortalMessage(_('API key entry required for editing this portlet.'),'error')

class IMailChimpPortlet(IPortletDataProvider):
    """A Mailchimp portlet"""

    name = schema.TextLine(
    title=_(u'Title'),
    description=_(u'Title of the portlet'))
    
    available_list = schema.List(
    title=_(u'Available lists'),
    description=_(u'Select available lists to subscribe to.'),
    required=True,
    min_length=1,
    value_type=schema.Choice(source='raptus.mailchimp.available_list'))

class Assignment(base.Assignment):
    """Portlet assignment"""
    
    implements(IMailChimpPortlet, interfaces.IProperties)

    _all_lists = {}
    
    def __init__(self, name=u'', available_list=[]):
        self.name = name
        self.available_list = available_list

    @property
    def title(self):
        return _(u"MailChimp")
    
    def getAvailableList(self):
        return self.available_list

class Renderer(base.Renderer):
    """Portlet renderer"""
    
    render = ViewPageTemplateFile('portlet.pt')
    
    def form(self):
        return getMultiAdapter((self.data, self.request), name='raptus.mailchimp.subscriberForm')()

    @property
    def name(self):
        return self.data.name or _(u"Subscribe to newsletter")

    @property
    def available(self):
        return len(component.getUtility(IVocabularyFactory,'raptus.mailchimp.subscriber_list')(self.data))

class AddForm(base.AddForm):
    """Portlet add form"""
    form_fields = form.Fields(IMailChimpPortlet)
    
    def update(self):
        errorMessage(self.context)
        super(AddForm, self).update()
    
    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form"""
    def __call__(self):
        errorMessage(self.context)
        return super(EditForm, self).__call__()
    form_fields = form.Fields(IMailChimpPortlet)
