from zope.interface import Interface

class IConnector(Interface):
    """ Provides all methods to connect on the MailChimp API
    """

    def __init__(self, context):
        """ Constructor
        """

    def getAccountDetails(self):
        """Retrieve lots of account information including payments made, plan info,
           some account stats, installed modules, contact info, and more.
        """
    def getLists(self):
        """Retrieve all of the lists defined for your user account
        """
    def addSubscribe(self, id, email_address, merge_vars={}, **kwargs):
        """Subscribe the provided email to a list.
           id is a list of ids
           If the optional parameters are None so its take this form portal_properties
           the full list: http://www.mailchimp.com/api/1.2/listsubscribe.func.php
           return a list of success subscriber and errors, no errors = empty list
        """
        return errors
        
    def cleanUpList(self, lists):
        """remove deleted list and return it
           used for updating vocabulary in list-widget
        """
        return []
        
    def setNewAPIKey(self):
        """override the apikey, this method is used to check a new apikey
        """
        
        
class IProperties(Interface):
    """ Provides all settings specified for a view
    """
    
    def getAvailableList (self):
        """ All mail-list that a user can subscribe for
        """