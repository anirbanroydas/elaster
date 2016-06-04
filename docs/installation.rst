Installation
=============

Prerequisites
~~~~~~~~~~~~~

1. python 2.7+
2. tornado
3. sockjs-tornado 
4. sockjs-client (optional, just for example webapp)
5. elasticsearch-py (python low-level client library for Elasticsearch)
6. Elasticsearch (The search-engine)


Install
~~~~~~~
::

        $ pip install elaster

If above dependencies do not get installed by the above command, then use the below steps to install them one by one.

 **Step 1 - Install pip**

 Follow the below methods for installing pip. One of them may help you to install pip in your system.

 * **Method 1 -**  https://pip.pypa.io/en/stable/installing/

 * **Method 2 -** http://ask.xmodulo.com/install-pip-linux.html

 * **Method 3 -** If you installed python on MAC OS X via ``brew install python``, then **pip** is already installed along with python.


 **Step 2 - Install tornado**
 ::

         $ pip install tornado

 **Step 3 - Install sockjs-tornado**
 ::

         $ pip install sockjs-tornado


 **Step 4 - Install elasticsearch-py**
 ::

         $ pip install elasticsearch


 **Step 5 - Install Elasticsearch**
 
 * *For* ``Mac`` *Users*
 
   1. Install Java 8 (if not instlled already)
   ::

          # Tap Caskroom to install java from caskroom
          $ brew tap caskroom/cask 

          # Install brew-cask to use brew cask command (new homebrew doesn't need this, hence you can use brew cask just by tapping Caskroom)
          $ brew install brew-cask

          # Install java
          $ brew cask install java



   2. Brew Install Elasticsearch
   ::

         $ brew install elasticsearch

   3. Configure elasticsearch, by modifying the file at ``/usr/local/etc/elasticsearch/elasticsearch.yml``.

 * *For* ``Ubuntu/Linux`` *Users*

   1. Follow this link, `here <https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html>`_.

   

   2. Also, you can follow this link, `here <https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04>`_.
   


   4. Configure elasticsearch, by modifying the file at ``/usr/local/etc/elasticsearch/elasticsearch.yml``.




