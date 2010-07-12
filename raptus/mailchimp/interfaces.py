from zope.interface import Interface

class IConnector(Interface):
    """ Provides all methodes to connect on the MailChimp API
    """
    
    def ping(self, apikey):
        """"Ping" the MailChimp API - a simple method you can call 
            that will return a constant value as long as everything is good.
        """
    def getAccountDetails(self):
        """Retrieve lots of account information including payments made, plan info,
           some account stats, installed modules, contact info, and more.
        """