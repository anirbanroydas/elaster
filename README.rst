elaster
========

An in-app full-text Search Engine using Elasticsearch (a document store search engine based on Lucene), tornado as web server, sockjs in client(browser) side javascript library, sockjs-tornado as sockjs implementation on server side and elasticsearch-py as elasticsearch python client library.

**NOTE :** Still in developement. Not ready for release. Info added prior just for record purpose.

**NOTE :** Meanwhile, you can check the *Example - Webapp* images and static codes for an overview. 



Example - Webapp
-----------------

* **Welcome Page**

.. image:: img1.png 


* **Select app type**

.. image:: img2.png 


Documentation
--------------

**Link :** http://elaster.readthedocs.io/en/latest/


Project Home Page
--------------------

**Link :** https://www.github.com/anirbanroydas/elaster


Details
--------


:Author: Anirban Roy Das
:Email: anirban.nick@gmail.com
:Copyright(C): 2017, Anirban Roy Das <anirban.nick@gmail.com>

Check ``elaster/LICENSE`` file for full Copyright notice.



Overview
---------

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



Technical Specs
----------------


:sockjs-client (optional): Advanced Websocket Javascript Client used in **webapp example**
:Tornado: Async Python Web Library + Web Server
:sockjs-tornado: SockJS websocket server implementation for Tornado
:Elasticsearch: A document store search engine based on Lucene
:elasticsearch-py: Low-level elasticsearch python client
:pytest: Python testing library and test runner with awesome test discobery
:pytest-flask: Pytest plugin for flask apps, to test fask apps using pytest library.
:Uber\'s Test-Double: Test Double library for python, a good alternative to the `mock <https://github.com/testing-cabal/mock>`_ library
:Jenkins (Optional): A Self-hosted CI server
:Travis-CI (Optional): A hosted CI server free for open-source projecs 
:Docker: A containerization tool for better devops



Features
---------

* Search Engine
* in-app (Androi, iOS, website)
* Use as a standalone server or as a python library
* Suggestion based search 
* Autocomplete based search
* Add/Index your own dataset in json files
* Microservice
* Testing using Docker and Docker Compose
* CI servers like Jenkins, Travis-CI





Installation
------------

Prerequisite (Optional)
~~~~~~~~~~~~~~~~~~~~~~~

To safegurad secret and confidential data leakage via your git commits to public github repo, check ``git-secrets``.

This `git secrets <https://github.com/awslabs/git-secrets>`_ project helps in preventing secrete leakage by mistake.


Dependencies
~~~~~~~~~~~~~

1. Docker
2. Make (Makefile)

See, there are so many technologies used mentioned in the tech specs and yet the dependencies are just two. This is the power of Docker. 


Install
~~~~~~~~

* **Step 1 - Install Docker**

  Follow my another github project, where everything related to DevOps and scripts are mentioned along with setting up a development environemt to use Docker is mentioned.

    * Project: https://github.com/anirbanroydas/DevOps

  * Go to setup directory and follow the setup instructions for your own platform, linux/macos

* **Step 2 - Install Make**
  ::

      # (Mac Os)
      $ brew install automake

      # (Ubuntu)
      $ sudo apt-get update
      $ sudo apt-get install make

* **Step 3 - Install Dependencies**
  
  Install the following dependencies on your local development machine which will be used in various scripts.

  1. openssl
  2. ssh-keygen
  3. openssh




CI Setup
---------


If you are using the project in a CI setup (like travis, jenkins), then, on every push to github, you can set up your travis build or jenkins pipeline. Travis will use the ``.travis.yml`` file and Jenknis will use the ``Jenkinsfile`` to do their jobs. Now, in case you are using Travis, then run the Travis specific setup commands and for Jenkins run the Jenkins specific setup commands first. You can also use both to compare between there performance.

The setup keys read the values from a ``.env`` file which has all the environment variables exported. But you will notice an example ``env`` file and not a ``.env`` file. Make sure to copy the ``env`` file to ``.env`` and **change/modify** the actual variables with your real values.

The ``.env`` files are not commited to git since they are mentioned in the ``.gitignore`` file to prevent any leakage of confidential data.

After you run the setup commands, you will be presented with a number of secure keys. Copy those to your config files before proceeding.

**NOTE:** This is a one time setup.
**NOTE:** Check the setup scripts inside the ``scripts/`` directory to understand what are the environment variables whose encrypted keys are provided.
**NOTE:** Don't forget to **Copy** the secure keys to your ``.travis.yml`` or ``Jenkinsfile``

**NOTE:** If you don't want to do the copy of ``env`` to ``.env`` file and change the variable values in ``.env`` with your real values then you can just edit the ``travis-setup.sh`` or ``jenknis-setup.sh`` script and update the values their directly. The scripts are in the ``scripts/`` project level directory.


**IMPORTANT:** You have to run the ``travis-setup.sh`` script or the ``jenkins-setup.sh`` script in your local machine before deploying to remote server.
 

Travis Setup
~~~~~~~~~~~~~~~~~

These steps will encrypt your environment variables to secure your confidential data like api keys, docker based keys, deploy specific keys.
::

  $ make travis-setup



Jenkins Setup
~~~~~~~~~~~~~~~~~~~

These steps will encrypt your environment variables to secure your confidential data like api keys, docker based keys, deploy specific keys.
::

  $ make jenkins-setup





Usage
-----

After having installed the above dependencies, and ran the **Optional** (If not using any CI Server) or **Required** (If using any CI Server) **CI Setup** Step, then just run the following commands to use it:


You can run and test the app in your local development machine or you can run and test directly in a remote machine. You can also run and test in a production environment. 



Run
~~~~

The below commands will start everythin in development environment. To start in a production environment, suffix ``-prod`` to every **make** command.

For example, if the normal command is ``make start``, then for production environment, use ``make start-prod``. Do this modification to each command you want to run in production environment. 

**Exceptions:** You cannot use the above method for test commands, test commands are same for every environment. Also the  ``make system-prune`` command is standalone with no production specific variation (Remains same in all environments).

* **Start Applcation**
  ::

      $ make clean
      $ make build
      $ make start

      # OR

      $ docker-compose up -d


    
  
* **Stop Application**
  ::

      $ make stop

      # OR

      $ docker-compose stop


* **Remove and Clean Application**
  ::

      $ make clean

      # OR

      $ docker-compose rm --force -v
      $ echo "y" | docker system prune


* **Clean System**
  ::

      $ make system-prune

      # OR

      $ echo "y" | docker system prune






Logging
~~~~~~~~


* To check the whole application Logs
  ::

      $ make check-logs

      # OR

      $ docker-compose logs --follow --tail=10



* To check just the python app\'s logs
  ::

      $ make check-logs-app

      # OR

      $ docker-compose logs --follow --tail=10 identidock





Test
~~~~

Now, testing is the main deal of the project. You can test in many ways, namely, using ``make`` commands as mentioned in the below commands, which automates everything and you don't have to know anything else, like what test library or framework is being used, how the tests are happening, either directly or via ``docker`` containers, or may be different virtual environments using ``tox``. Nothing is required to be known.

On the other hand if you want fine control over the tests, then you can run them directly, either by using ``pytest`` commands, or via ``tox`` commands to run them in different python environments or by using ``docker-compose`` commands to run differetn tests. 

But running the make commands is lawasy the go to strategy and reccomended approach for this project.

**NOTE:** Tox can be used directly, where ``docker`` containers will not be used. Although we can try to run ``tox`` inside our test contianers that we are using for running the tests using the ``make`` commands, but then we would have to change the ``Dockerfile`` and install all the ``python`` dependencies like ``python2.7``, ``python3.x`` and then run ``tox`` commands from inside the ``docker`` containers which then run the ``pytest`` commands which we run now to perform our tests inside the current test containers. 

**CAVEAT:** The only caveat of using the make commands directly and not using ``tox`` is we are only testing the project in a single ``python`` environment, nameley ``python 3.6``.


* To Test everything
  ::

      $ make test


  Any Other method without using make will involve writing a lot of commands. So use the make command preferrably


* To perform Unit Tests
  ::

      $ make test-unit


* To perform Component Tests
  ::

      $ make test-component


* To perform Contract Tests
  ::

      $ make test-contract


* To perform Integration Tests
  ::

      $ make test-integration


* To perform End To End (e2e) or System or UI Acceptance or Functional Tests
  ::

      $ make test-e2e

      # OR

      $ make test-system

      # OR  

      $ make test-ui-acceptance

      # OR

      $ make test-functional






Todo
-----

1. Add Blog post regarding this topic.
2. Add Contract Tests using pact
3. Add integration tests
4. Add e2d tests


