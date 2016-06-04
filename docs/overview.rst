Overview
=========

elaster is an in-app full-text Search Engine based on Elasticsearch which can be set up to search your app, website, etc. for any text.

All you have to do is add data to the index, just the data files, all mappings, indexing, settings are taken care by the elaster server.
You can start using the server right away without knowing anything about elasticsearch.

Even the cluster, nodes, etc. are taken care of.

If you want more power and control, change the configuration file at ``/usr/local/etc/elasticsearch/elasticsearch.yml``.

It uses the `Elasticsearch <https://www.elastic.co/products/elasticsearch>`_  to implement the real time full text search functionality. **Elasticsearch** is a search server based on `Lucene <http://lucene.apache.org/>`_. It provides a distributed, multitenant-capable full-text search engine with an HTTP web interface and schema-free JSON documents. Elasticsearch is developed in Java and is released as open source under the terms of the Apache License. Elasticsearch is the most popular enterprise search engine followed by `Apache Solr <https://en.wikipedia.org/wiki/Apache_Solr>`_, also based on Lucene.

A website example is given as builtin. For the website , the connection is created using the `sockjs <https://github.com/sockjs/sockjs-client>`_ protocol. **SockJS** is implemented in many languages, primarily in Javascript to talk to the servers in real time, which tries to create a duplex bi-directional connection between the **Client(browser)** and the **Server**. Ther server should also implement the **sockjs** protocol. Thus using the  `sockjs-tornado <https://github.com/MrJoes/sockjs-tornado>`_ library which exposes the **sockjs** protocol in `Tornado <http://www.tornadoweb.org/>`_ server.

It first tries to create a `Websocket <https://en.wikipedia.org/wiki/WebSocket>`_ connection, and if it fails then it fallbacks to other transport mechanisms, such as **Ajax**, **long polling**, etc. After the connection is established, the tornado server **(sockjs-tornado)** connects to **Elasticsearch** via using the **Elasticsearch Python Client Library**, `elasticsearch-py <https://pypi.python.org/pypi/elasticsearch>`_. 

Thus the connection is ``web-browser`` to ``tornado`` to ``elasticsearch`` and vice versa.

For any other **app (Android, iOS)**, use any android, iOS client library to connect to the elaster server. This software provides the website example builtin. Using command line ``elaster --example=webapp``, you start the elaster website example. But to use it in your person app(Anroid, iOS) or web app, use elaster as a general server.


