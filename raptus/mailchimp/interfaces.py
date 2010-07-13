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
    def setNewAPIKey(self):
        """override the apikey, this method is used to check a new apikey
        """