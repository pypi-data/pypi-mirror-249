Using this package
==================

Using the PasteDeploy entry point
---------------------------------
You can use the PasteDeploy entry point in your WSGI configuration file to
define a ``cheroot`` server:

.. code-block:: ini

   [server:main]
   use = egg:dataflake.wsgi.cheroot#main
   host = 127.0.0.1
   port = 8080

If you leave out the ``host`` specification, ``cheroot``  will listen on all
IPv4 interfaces (`0.0.0.0`). The default port, if none is given, is 8080.

``cheroot`` supports a wide range of configuration options that you can pass as
part of your WSGI configuration. Here's an example showing all options:

.. code-block:: ini

   [server:main]
   use = egg:dataflake.wsgi.cheroot#main
   host = 127.0.0.1
   port = 8080
   server_name = MyServer
   max = -1
   request_queue_size = 5
   timeout = 10
   shutdown_timeout = 5
   accepted_queue_size = -1
   accepted_queue_timeout = 10
   peercreds_enabled = False
   peercreds_resolve_enabled = False

The possible options are listed in the `cheroot documentation 
<https://cheroot.cherrypy.org/en/latest/pkg/cheroot.wsgi.html#cheroot.wsgi.Server>`_,
but a more detailed explanation is `in the code itself 
<https://github.com/cherrypy/cheroot/blob/master/cheroot/wsgi.py>`_, look for
the definition of the ``Server`` class ``__init__`` method.


Creating a basic WSGI configuration for Zope
--------------------------------------------
This package defines a console script named ``mkcherootinstance`` that works
just like Zope's own ``mkwsgiinstance``. It will ask you for a location, a
username and a password to create a basic Zope instance home with a WSGI
configuration, in this case it will be ``cheroot``-based as opposed to Zope's
default, ``waitress``.

.. note::

   Just like ``mkwsgiinstance``, the script will not overwrite an existing WSGI
   configuration file at ``etc/zope.ini``. You need to move the existing file
   to the side to get a fresh configuration.

.. code-block:: console

   $ bin/mkcherootinstance
   Please choose a directory in which you'd like to install
   Zope "instance home" files such as database files, configuration
   files, etc.
   
   Directory: .
   Please choose a username and password for the initial user.
   These will be the credentials you use to initially manage
   your new Zope instance.
   
   Username: admin
   Password: (enter password)
   Verify password: (re-enter password)
