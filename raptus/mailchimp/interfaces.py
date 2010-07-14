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
    def setNewAPIKey(self):
        """override the apikey, this method is used to check a new apikey
        """
        
class IProperties(Interface):
    """ Provides all settings specified for a view
    """
    
    def getAvailableList (self):
        """ All mail-list that a user can subscribe for
        """