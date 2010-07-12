from zope import interface, component
from raptus.mailchimp.interfaces import IConnector
import greatape

class Connector(object):

    interface.implements(IManageable)
    component.adapts(interface.Interface)

    def __init__(self):
        self.conn = greateape('here comms the api key')
        
    def ping(self, apikey):
        temp_conn = greateape(apikey)
        return conn(method='ping')

    def getAccountDetails(self):
        return conn(method='getAccountDetails')