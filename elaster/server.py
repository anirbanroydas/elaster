""" 
The server module starts the elaster server and initiates the elasticsearch connection. 
It also takes addtional option example parameter to initiate the example indices. 

"""




import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options
import logging
import os
from elasticsearch import Elasticsearch 

from urls import urls
from settings import settings
from elaster.apps.elasticsearch.searchEngine import ElasticsearchClient


define("port", default=9091, help="run on the given port", type=int)
define("example", default=None, help='the example app to run in elaster server', type=str)
define("datapath", default=None, help='the path to data to be indexed into elasticsearch for searching over it', type=str)


LOGGER = logging.getLogger(__name__)


class Application(tornado.web.Application):
    """ 
    Application Class initiates the elaster server app with proper settings and providing methods to create
    the elasticsearch connection and start the tornado server. 

    It subclasses tornado.web.Application.

    """


    def __init__(self, example=None, data_path=None):
        """ 
        Initialization method for the application. 

        :param  example:   The example to be used.
        :type   example:    string or default is None 

        """ 

        # connect to  Elasticsearch using elasticsearch python client library's Elasticsearch method
        self.es_conn = Elasticsearch()



        if example is not None:
            tpath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples', example))
            spath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'examples', example, 'static'))
            dpath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_example_datasets'))
            settings['template_path'] = tpath
            settings['static_path'] = spath

            # create the example dataset index with the created ElasticSearch conn
            self._createDataIndex(self.es_conn, dpath)
        
        else: 
            # create the dataset index from the give path 
            self._createDataIndex(self.es_conn, data_path)

        tornado.web.Application.__init__(self, urls, **settings)


    def _createDataIndex(self, path):
        """ 
        Method to create the Data Index into Elasticsearch to search over it from the give path.

        It checks the path, and if its a file, it indexes it directly, and if its a dirctory, it indexes
        all the individual files inside the directory to upto 1 level down. So, all the data should be in 
        the same directory as the path.

        :param  path:   the directory path to data, or the file itself to be indexed (the files should be JSON files.)
        :type   path:   string

        """ 

        
        if os.path.isfile(path): 
            if path.endswith('.json'): 
                    with open(path, 'rb') as f:
                        data = f.read()
                        index = f[:-5] 
                        ElasticsearchClient.prepare_index(self.es_conn, index)
                        ElasticsearchClient.index_bulk(self.es_conn, index, data)

        else:
            for f in os.listdir(path): 
                if os.path.isfile(f): 
                    if f.endswith('.json'): 
                        with open(f, 'rb') as f:
                            data = f.read()
                            index = f[:-5] 
                            ElasticsearchClient.prepare_index(self.es_conn, index)
                            ElasticsearchClient.index_bulk(self.es_conn, index, data)
         
        
    




def main():
    """ 
    The main methos starts the server by accepting the Application object.
    It starts the server at the given port extracted from options.port otherwise it
    takes a default value of 9091.
    
    """ 

    tornado.options.parse_command_line()
    app = Application(example=options.example, data_path=options.datapath)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    LOGGER.info('[server.main] Starting Elaster on http://127.0.0.1:%s', options.port)

    try:
        LOGGER.info("\n[server.main] Elaster server Started.\n")

        tornado.ioloop.IOLoop.current().start()
        
    except KeyboardInterrupt:
        LOGGER.error('\n[server.main] EXCEPTION KEYBOARDINTERRUPT INITIATED\n')
        LOGGER.info("[server.main] Stopping Server....")
        LOGGER.info('[server.main] closing all websocket connections objects and corresponsding mqtt client objects')
        LOGGER.info('Stopping elaster\'s Tornado\'s main iolooop')
        
        # Stopping main thread's ioloop, not to be confused with current thread's ioloop
        # which is ioloop.IOLoop.current()
        tornado.ioloop.IOLoop.instance().stop()

        LOGGER.info("\n[server.main] Elaster server Stopped.")






if __name__ == "__main__":
    main()

