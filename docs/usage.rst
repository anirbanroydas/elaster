Usage
=====

After having installed elaster, just run the following commands to use it:

Elaster Server
-----------------


1. *For* ``Mac`` *Users*
::

        # start normally
        $ elasticsearch
         
        # If you want to run in background
        $ elasticsearch -d 

        # start using brew services (doesn't work with tmux, athough there is a fix, mentioned in one of the pull requests and issues)
        $ brew services start elasticsearch


2. *For* ``Ubuntu/LInux`` *Users*
::

        # Go inside the elasticsearch extracted directory
        $ cd elasticsearch-2.3.0

        # start normally
        $ bin/elasticsearch

        # If you want to run in background
        $ bin/elasticsearch -d
           
          
Elaster Application
--------------------------

1. Start Server
   ::          
        
        $ elaster [options]
        
2. Options    
   
   :--port: Port number where the elaster search engine will start
   :--example: Example webapp to play with the server
   :--datapath: Dirctory containing the datasets in json format or the json file path itself.
   
   * **Example**
     :: 
             
          # Starting the server
          $ elaster --port=9191

          # Starting the server with the example webapp
          $ elaster --port=9191 --example=webapp

          # Starting the server with custom dataset 
          $ elaster --port --datapath=$HOME/project/xyz/data
          $ elaster --port --datapath=$HOME/project/xyz/data/photos.json
 

**NOTE** Cannot use both ``--example`` and ``--datapath`` together, for ``--example``, the dataset is automatically decided and indexed by the server itself.

             
3. Stop mosquittoChat Server
   
   Click ``Ctrl+C`` to stop the server.



