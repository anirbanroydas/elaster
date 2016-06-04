"""
The searchEngine module provides interface for the ElasticSearch client.

It provides classes to create elastic clients via elasticsearch-py and elasticsearh-dsl python libraries
to connect to ElasticSearch server, interact with , search, index, do CRUD, and many other complex functions.

"""


import json
import logging
import base64
import os
import elasticsearch




LOGGER = logging.getLogger(__name__)



# # utility temporary functions to check rather than using logging/LOGGER
# def pi(e): 
#     print '\n[ElasticsearchClient] Inside ' + e.upper() + '()\n'


# def pr(e):
#     print '\n[ElasticsearchClient] Returning from ' + e.upper() + '()\n'



class ElasticsearchClient(object):
    """
    This is a ElasticSearch Client class that will create an interface to connect to Elasticsearch.

    It provides methods for connecting, diconnecting, searching, indexing, do CRUD, and many other complex functions.

    """


    def __init__(self, conn=None, websocket_type='tornado'):
        """
        Create a new instance of the ElasticsearchClient class, passing in the conn object, websocket_type.

        :param  conn:               the connection pool object to Elasticsearch 
        :type   conn:               elasticsearch.Elasticsearch
        :param  websocket_type:     type of websocket connection established, sockjs or tornado
        :type   websocket_type:     string

        """

        # pi('__init__')

        self._websocket_type = websocket_type 
        self._conn = conn

        self.websocket = None

        # pr('__init__')




    def _genid(self):
        """ 
        Method that generates unique clientids by calling base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e').
        
        :return:        Returns a unique urlsafe id 
        :rtype:         string 

        """ 

        # pi('_genid')

        return base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e')




    def start(self):
        """
        Method to start the Elasticsearch client by initiating a connection  to Elasticsearchs.

        """

        # pi('start')

        LOGGER.info('[ElasticsearchClient] starting the Elasticsearch connection')

        self.setup_connection()
        self.setup_callbacks()
        
        # self._connection is the return code of the connection, success, failure, error. Success = 0
        self._connection = self.connect()

        # print '[ElasticsearchClient] self._connection : ', self._connection

        if self._connection == 0: 
            # Start paho-mqtt Elasticsearch Event/IO Loop
            LOGGER.info('[ElasticsearchClient] Startig IOLoop for client : %s ' % self)
            
            self.start_ioloop()

            # Start schedular for keeping the mqtt connection opening by chekcing keepalive, and request/response with PINGREQ/PINGRESP
            self.start_schedular()

        else:
            self._connecting = False 

            LOGGER.warning('[ElasticsearchClient] Connection for client :  %s  with broker Not Established ' % self)


        # pr('start')




    
    def setup_connection(self):
        """
        Method to setup the extra options like username,password, will set, tls_set etc 
        before starting the connection.

        """ 

        # pi('setup_connection')

        self._client = self.create_client()

        # setting up client username and password
        self._client.username_pw_set(self._username, self._password)
        
        

        # pr('setup_connection')





    
    def create_client(self):
        """
        Method to create the paho-mqtt Client object which will be used to connect 
        to Elasticsearch. 
        
        :return:        Returns a Elasticsearch mqtt client object 
        :rtype:         paho.mqtt.client.Client 

        """ 

        # pi('create_client')

        return mqtt.Client(client_id=self._clientid, clean_session=self._clean_session, userdata=self._userdata)





    def setup_callbacks(self):
        """
        Method to setup all callbacks related to the connection, like on_connect,
        on_disconnect, on_publish, on_subscribe, on_unsubcribe etc. 

        """ 

        # pi('setup_callbacks')

        self._client.on_connect = self.on_connect 
        self._client.on_disconnect = self.on_disconnect 


        # pr('setup_callbacks')





    def connect(self):
        """
        This method connects to Elasticsearch via returning the 
        connection return code.

        When the connection is established, the on_connect callback
        will be invoked by paho-mqtt.

        :return:        Returns a Elasticsearch mqtt connection return code, success, failure, error, etc 
        :rtype:         int

        """

        # pi('connect')

        if self._connecting:
            LOGGER.warning('[ElasticsearchClient] Already connecting to RabbitMQ')
            return

        self._connecting = True

        if self._connected: 
            LOGGER.warning('[ElasticsearchClient] Already connected to RabbitMQ')

        else:
            LOGGER.info('[ElasticsearchClient] Connecting to RabbitMQ on localhost:5672, Object: %s ' % self)

            # pr('connect')

            return self._client.connect(host=self._host, port=self._port, keepalive=self._keepalive, bind_address=self._bind_address)



    


    def on_connect(self, client, userdata, flags, rc): 
        """
        This is a Callback method and is called when the broker responds to our
        connection request. 

        :param      client:     the client instance for this callback 
        :param      userdata:   the private user data as set in Client() or userdata_set() 
        :param      flags:      response flags sent by the broker 
        :type       flags:      dict
        :param      rc:         the connection result 
        :type       rc:         int

        flags is a dict that contains response flags from the broker:

        flags['session present'] - this flag is useful for clients that are using clean session
        set to 0 only. If a client with clean session=0, that reconnects to a broker that it has
        previously connected to, this flag indicates whether the broker still has the session 
        information for the client. If 1, the session still exists. 

        The value of rc indicates success or not:

        0: Connection successful 1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 5: Connection refused - not authorised 
        6-255: Currently unused.

        """ 

        # pi('on_connect')

        if self._connection == 0:
            self._connected = True

            LOGGER.info('[ElasticsearchClient] Connection for client :  %s  with broker established, Return Code : %s ' % (client, str(rc)))

            # start subscribing to topics
            self.subscribe()

        else:
            self._connecting = False 

            LOGGER.warning('[ElasticsearchClient] Connection for client :  %s  with broker Not Established, Return Code : %s ' % (client, str(rc)))


        # pr('on_connect')








    def disconnect(self):   
        """
        Method to disconnect the mqqt connection with Elasticsearch broker.

        on_disconnect callback is called as a result of this method call. 

        """ 

        # pi('disconnect')

        if self._closing: 
            LOGGER.warning('[ElasticsearchClient] Connection for client :  %s  already disconnecting..' % self)

        else:
            self._closing = True 

            if self._closed:
                LOGGER.warning('[ElasticsearchClient] Connection for client :  %s  already disconnected ' % self)

            else:
                self._client.disconnect() 


        # pr('disconnect')



    



    def on_disconnect(self, client, userdata, rc):
        """
        This is a Callback method and is called when the client disconnects from
        the broker.

        """  

        # pi('on_disconnect')

        LOGGER.info('[ElasticsearchClient] Connection for client :  %s  with broker cleanly disconnected with return code : %s ' % (client, str(rc)))

        self._connecting = False 
        self._connected = False 
        self._closing = True
        self._closed = True

        
        # stopping ioloop - actually mqtt ioloop stopped, not the real torando ioloop, 
        # just removing handler from tornado ioloop
        self.stop_ioloop() 

        # stoppig shechular 
        self.stop_schedular()

        if self._ioloopClosed:
            self._sock = None


        # pr('on_disconnect')







    

    def addNewElasticsearchClient(self):
        """
        Method called after new mqtt connection is established and the client has started subsribing to 
        atleast some topics, called by on_subscribe callback. 

        """ 

        # pi('addNewMqttElasticsearchClient')

        mqttElasticsearchParticipants['count'] = mqttElasticsearchParticipants['count'] + 1

        # print '[ElasticsearchClient] mqttElasticsearchParticipants : ', mqttElasticsearchParticipants['count']
        
        return mqttElasticsearchParticipants['count']




    def sendMsgToWebsocket(self, msg): 
        """
        Method to send message to associated websocket. 

        :param      msg:        the message to be sent to the websocket 
        :type       msg:        string, unicode or json encoded string or a dict

        """ 

        # pi('sendMsgToWebsocket')

        # LOGGER.info('[ElasticsearchClient] Elasticsearch is sending msg to associated webscoket')

        if isinstance(msg, str) or isinstance(msg, unicode):
            payload = msg 
        else: 
            payload = json.dumps(msg)
        
        self.websocket.send(payload)   


        # pr('sendMsgToWebsocket')







    def publish(self, topic, msg=None, qos=2, retain=False):
        """
        If the class is not stopping, publish a message to ElasticsearchClient.

        on_publish callback is called after broker confirms the published message.
        
        :param  topic:  The topic the message is to published to
        :type   topic:  string 
        :param  msg:    Message to be published to broker
        :type   msg:    string 
        :param  qos:    the qos of publishing message 
        :type   qos:    int (0, 1 or 2) 
        :param  retain: Should the message be retained or not 
        :type   retain: bool

        """

        # pi('publish')

        # LOGGER.info('[ElasticsearchClient] Publishing message')

        # converting message to json, to pass the message(dict) in acceptable format (string)
        if isinstance(msg, str) or isinstance(msg, unicode):
            payload = msg
        else:
            payload = json.dumps(msg, ensure_ascii=False)

        self._client.publish(topic=topic, payload=payload, qos=qos, retain=retain)


        # pr('publish')



    
    
    def on_public_message(self, client, userdata, msg): 
        """
        This is a Callback method and is called  when a message has been received on a topic
        [public/msgs] that the client subscribes to.

        :param      client:         the client who initiated the publish method 
        :param      userdata:       the userdata associated with the client during its creation 
        :param      msg:            the message sent by the broker 
        :type       mid:            string or json encoded string 

        """

        # pi('on_public_message')

        # LOGGER.info('[ElasticsearchClient] Received message with mid : %s from topic : %s with qos :  %s and retain = %s ' % (str(msg.mid), msg.topic, str(msg.qos), str(msg.retain)))

        json_decoded_body = json.loads(msg.payload)
        stage = json_decoded_body['stage']

        if stage == 'new_participant':
            
            # print '[ElasticsearchClient] Received stage == new_participant'

            if json_decoded_body['msg']['clientid'] != self._clientid: 

                # print '[ElasticsearchClient] received stage == new_participant with != self._clientid, thus subscribing to its private status'
                
                topic_list = ('private/' + str(json_decoded_body['msg']['clientid']) + '/status', 2)
                
                # print 'ElasticsearchClient] topic_list to be sent : ', topic_list
                
                # subscribe the new participant's status topic
                self.subscribe(topic_list=topic_list)
            
            else:


                # pr('on_public_message')

                return



        if stage == 'stop' and self._clientid == json_decoded_body['msg']['clientid']:

            # print '[ElasticsearchClient] received stage == stop with == self._clientid, thus sending offline status to subscribers'
                
            # LOGGER.info('[ElasticsearchClient] skipping sending message to websocket since webscoket is closed.')
            # LOGGER.info('[ElasticsearchClient] initating closing of rabbitmq Client Connection...')

            # avoid sending the message to the corresponding websocket, since its already cloesed. 
            # rather sending the offline status message to the subscribers of its private/status topic
            self.send_offline_status()

        else:
            # print '[ElasticsearchClient] received stage != new_participant and != self._clientid, thus sendimg msg to corresponding websocket'
                
            # LOGGER.info('[ElasticsearchClient] sending the message to corresponsding websoket: %s ' % self.websocket)

            self.sendMsgToWebsocket(json_decoded_body)


        # pr('on_public_message')







    def delElasticsearchClient(self):
        """ Method called after an mqtt clinet unsubsribes to 
        atleast some topics, called by on_subscribe callback. 

        :return:    Returns update mqqt clients active 
        :rtype:     dict with update count 

        """ 

        # pi('delMqttElasticsearchClient')

        mqttElasticsearchParticipants['count'] = mqttElasticsearchParticipants['count'] - 1

        # print '[ElasticsearchClient] mqttElasticsearchParticipants : ', mqttElasticsearchParticipants['count']
        
        return mqttElasticsearchParticipants['count']




    

    def stop(self):
        """
        Cleanly shutdown the connection to Elasticsearch by disconnecting the mqtt client.

        When Elasticsearch confirms disconection, on_disconnect callback will be called.

        """

        # pi('stop')

        LOGGER.info('[ElasticsearchClient] Stopping ElasticsearchClient object... : %s ' % self)

        self.disconnect()

        # pr('stop')


    






