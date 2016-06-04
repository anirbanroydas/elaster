"""
This is the main view module which manages main tornado connections. This module
provides request handlers for managing simple HTTP requests as well as Websocket requests.

Although the websocket requests are actually sockJs requests which follows the sockjs protcol, thus it
provide interface to sockjs connection handlers behind the scene.

If using from non website app, like Android, iOs, or anyother websocket javascript library, then the websocket handler
will a different one and the websocket connection endpoint too.

For sockjs:

Handler : SearchSockjsHandler
Connection endpoint : /sockjs_search

For other websocket types:

Handler : SearchHandler
Connection endpoint : /search

"""




import tornado.web
import tornado.websocket
import tornado.escape
import logging



from sockjs.tornado import SockJSConnection
from elaster.apps.elasticsearch.searchEngine import ElasticsearchClient


LOGGER = logging.getLogger(__name__)



# Handles the general HTTP connections
class IndexHandler(tornado.web.RequestHandler):
    """This handler is a basic regular HTTP handler to serve the chatroom page.

    """

    def get(self):
        """
        This method is called when a client does a simple GET request,
        all other HTTP requests like POST, PUT, DELETE, etc are ignored.

        :return: Returns the rendered main requested page, in this case its the chat page, index.html

        """

        LOGGER.info('[IndexHandler] HTTP connection opened')

        self.render('index.html')

        LOGGER.info('[IndexHandler] index.html served')







# set of websocket connections
websocketParticipants = set()
# no. of mqtt clients
mqttClients = set()






# Handler for Websocket Connections or Sockjs Connections
class SearchSockjsHandler(SockJSConnection):
    """ Websocket Handler implementing the sockjs Connection Class which will
    handle the websocket/sockjs connections.
    """

    def on_open(self, info):
        """
        This method is called when a websocket/sockjs connection is opened for the first time.
        
        :param      self:  The object
        :param      info:  The information
        
        :return:    It returns the websocket object

        """

        LOGGER.info('[SearchSockjsHandler] Websocket connecition opened: %s ' % self)

        # adding new websocket connection to global websocketParcticipants set
        websocketParticipants.add(self)

        # Initialize new ElasticSearch connection client object for this websocket.
        # call with default values, also send the websocket_type to constructore
        self.es_client = ElasticsearchClient(conn=self.application.es_conn, websocket_type='sockjs')
        
        # Assign websocket object to a elasticsearch connection object.
        self.es_client.websocket = self
        
        # connect to elastic
        self.es_client.start()




    def on_message(self, message):
        """
        This method is called when a message is received via the websocket/sockjs connection
        created initially.
        
        :param      self:     The object
        :param      message:  The message received via the connection.
        :type       message: json string

        The message structure is:

        Eg:

        message = {
                    'index' : 'photo',
                    'msg'   : 'cath'
        }

        """

        # LOGGER.info('[SearchSockjsHandler] message received on Websocket: %s ' % self)

        res = tornado.escape.json_decode(message)

        # print '[SearchSockjsHandler] received msg : ', res

        msg = res['msg'] 
        index = res['index']

        self.es_client.search(index, msg)



    
    def on_close(self):
        """
        This method is called when a websocket/sockjs connection is closed.
        
        :param      self:  The object
        
        :return:     Doesn't return anything, except a confirmation of closed connection back to web app.
        
        """

        LOGGER.info('[SearchSockjsHandler] Websocket conneciton close event %s ' % self)

        self.es_client.stop()

        # removing the connection of global list
        websocketParticipants.remove(self)

        LOGGER.info('[SearchSockjsHandler] Websocket connection closed')









# Handler for Websocket Connections for general websockets
class SearchHandler(tornado.websocket.WebsocketHandler):
    """ Websocket Handler implementing the Tornado websocket WebsocketHandler Class which will
    handle the websocket connections.
    """

    def open(self):
        """
        This method is called when a websocket connection is opened for the first time.
        
        :param      self:  The object
        :param      info:  The information
        
        :return:    It returns the websocket object

        """

        LOGGER.info('[SearchHandler] Websocket connecition opened: %s ' % self)

        # adding new websocket connection to global websocketParcticipants set
        websocketParticipants.add(self)

        # Initialize new ElasticSearch connection client object for this websocket.
        # call with default values, also send the websocket_type to constructore
        self.es_client = ElasticsearchClient(conn=self.application.es_conn, websocket_type='tornado')
        
        # Assign websocket object to a elasticsearch connection object.
        self.es_client.websocket = self
        
        # connect to elastic
        self.es_client.start()




    def on_message(self, message):
        """
        This method is called when a message is received via the websocket connection
        created initially.
        
        :param      self:     The object
        :param      message:  The message received via the connection.
        :type       message: json string

        The message structure is:

        Eg: 

        message = {
                    'index' : 'photo',
                    'msg'   : 'cath'
        }


        """

        # LOGGER.info('[SearchHandler] message received on Websocket: %s ' % self)

        res = tornado.escape.json_decode(message)

        # print '[SearchHandler] received msg : ', res

        index = res['index']
        msg = res['msg']

        self.es_client.search(index, msg)



    
    def on_close(self):
        """
        This method is called when a websocketconnection is closed.
        
        :param      self:  The object
        
        :return:     Doesn't return anything, except a confirmation of closed connection back to web app.
        
        """

        LOGGER.info('[SearchHandler] Websocket conneciton close event %s ' % self)

        self.es_client.stop()

        # removing the connection of global list
        websocketParticipants.remove(self)

        LOGGER.info('[SearchHandler] Websocket connection closed')







