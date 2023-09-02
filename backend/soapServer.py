from http.server import HTTPServer
import logging
from pysimplesoap.server import SoapDispatcher, SOAPHandler, WSGISOAPHandler


dispatcher = SoapDispatcher(
'TransServer',
location = "http://127.0.0.1:8050/",
action = 'http://127.0.0.1:8050/', # SOAPAction
namespace = "http://example.com/sample.wsdl", prefix="ns0",
trace = True,
ns = True)

#Function
def settransactiondetails(sessionId,msisdn,amount,language):
    #Some Code here
    #And more code here
    return {'sessionId':sid,'responseCode':0}

# register the user function
dispatcher.register_function('InitiateTransfer', settransactiondetails,
    returns={'sessionId': str,'responseCode':int}, 
    args={'sessionId': str,'msisdn': str,'amount': str,'language': str})

logging.info("Starting server...")
httpd = HTTPServer(("", 8050),SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()