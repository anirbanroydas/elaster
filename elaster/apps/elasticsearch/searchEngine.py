"""
The searchEngine module provides interface for the ElasticSearch client.

It provides classes to create elastic clients via elasticsearch-py and elasticsearh-dsl python libraries
to connect to ElasticSearch server, interact with , search, index, do CRUD, and many other complex functions.

"""


import json
import logging
import base64
import os




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


    def __init__(self, conn=None):
        """
        Create a new instance of the ElasticsearchClient class, passing in the conn object, websocket_type.

        :param  conn:               the connection pool object to Elasticsearch 
        :type   conn:               elasticsearch.Elasticsearch

        """

        # pi('__init__')

        self._conn = conn

        self.websocket = None

        # pr('__init__')




    @staticmethod
    def _genid():
        """ 
        Method that generates unique clientids by calling base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e').
        
        :return:        Returns a unique urlsafe id 
        :rtype:         string 

        """ 

        # pi('_genid')

        return base64.urlsafe_b64encode(os.urandom(32)).replace('=', 'e')



    @staticmethod
    def prepare_index(conn=None, index=None):
        """
        Method to prepare ElasticSearch's index.

        :param  conn:   The elasticsearch connection object 
        :type   conn:   elasticsearch.Elasticsearch 
        :param  index:  The index to prepare elasticsearch for 
        :type   index:  string 

        """

        # pi('start')

        LOGGER.info('[ElasticsearchClient] Preparing Elasticsearch for indexing the index : %s ' % index)

        settings = ElasticsearchClient.add_settings(index)
        mappings = ElasticsearchClient.add_mappings(index)

        body = {
                    "settings": settings,
                    "mappings": mappings 
        }


        conn.create(index=index, body=body)

        # pr('start')




    @staticmethod
    def add_settings(index):
        """
        Method to add settings to Elasticssearch for index given as argument.

        :param  index:  The index to add settings into, in elasticsearch
        :type   index:  string  

        """ 

        # pi('setup_connection')

        LOGGER.info('[ElasticsearchClient] adding settings for index : %s ' % index)

        analyzer = ElasticsearchClient.add_analyzer(index) 

        settings = {
                    "number_of_shards": 1,
                    "analysis": analyzer
                }

        return settings

        # pr('setup_connection')



    @staticmethod
    def add_analyzer(index):
        """
        Method to add analyser to Elasticssearch for index given as argument.

        :param  index:  The index to add anlyzer to, in elasticsearch
        :type   index:  string  

        """ 

        # pi('setup_connection')

        LOGGER.info('[ElasticsearchClient] adding analyser for index : %s ' % index)

        analyser = {
                        "filter": 
                        {
                            "autocomplete_filter": 
                            {
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 20
                            }
                        },
                      
                        "analyzer": 
                        {
                            "autocomplete": 
                            {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": 
                                [
                                    "lowercase",
                                    "autocomplete_filter"
                                ]
                            }
                        }   
                 }      
        

        return analyser

        # pr('setup_connection')    



    @staticmethod
    def add_mappings(index):
        """
        Method to add mappings to Elasticssearch for index given as argument.

        :param  index:  The index to add mapping to, in elasticsearch 
        :type   index:  string  
        
        """

        # pi('create_client')

        mappings = {
                        "my_type": 
                        {
                            "properties": 
                            {
                                "name": 
                                {
                                    "type": "string",
                                    "analyzer": "autocomplete"
                                }
                            }
                        }
                    }



        return mappings





    @staticmethod
    def index_bulk(conn, index, data):
        """
        Method to index data  in Elasticsaerch connection object in bulk. 

        :param  conn:   The elasticsearch connection object 
        :type   conn:   elasticsearch.Elasticsearch 
        :param  index:  The index to bulk add into elasticsearch  
        :type   index:  string
        :param  data:   the data to index in bulk 
        :type   data:   string

        """ 

        # pi('setup_callbacks')

        json_decoded_data = json.loads(data)

        conn.bulk(body=json_decoded_data, index=index)        

        # pr('setup_callbacks')





    def search(self, index, msg):
        """
        The method to search Elasticsearch.

        :param  index:  The index to search elasticsearch for 
        :type   index:  string
        :param  msg:   the data to search for in given index 
        :type   msg:   string

        """

        # pi('connect')

        # prepare the search body
        search_body = self.prepare_search_body(msg)

        hits = self._conn.search(index=index, body=search_body)

        # prepaer the msg to be sent to websocket by sorting based on scores
        result = self.prepare_result(hits)

        self.sendmsgToWebsocket(result)

    




    def prepare_search_body(self, msg):
        """
        The method to prepare the Query DSL for searching the Elasticsearch for given index.

        :param  msg:   the data to search for in given index 
        :type   msg:   string

        """

        # pi('connect')

        # prepare the search body
        search_body = {
                        "query": 
                        {
                            "match": 
                            {
                                "name": 
                                {
                                    "query": msg,
                                    "analyzer": "standard" 
                                }
                            }
                        }
                    }


        return search_body







    def prepare_result(self, hits):
        """
        The method to prepare the result before sending in to websocket.

        :param  hits:   the hits result of searching the Elasticsearch
        :type   msg:    dict

        """

        # pi('connect')

        # prepare the hits result
        
        return hits







    def sendmsgToWebsocket(self, msg):
        """
        The method to send serach results to corresponding websocket.

        :param  msg:   the final msg after preparing it that is to be sent to corresponding websocket
        :type   msg:    dict

        """

        # pi('connect')

        res = json.dumps(msg)
        
        return res



