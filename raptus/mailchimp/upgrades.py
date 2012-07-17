from Products.CMFCore.utils import getToolByName


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-raptus.mailchimp:default')

