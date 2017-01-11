.. image:: https://img.shields.io/pypi/v/librarypaste.svg
   :target: https://pypi.org/project/librarypaste

.. image:: https://img.shields.io/pypi/pyversions/librarypaste.svg

.. image:: https://img.shields.io/pypi/dm/librarypaste.svg

.. image:: https://img.shields.io/travis/yougov/librarypaste/master.svg
   :target: http://travis-ci.org/yougov/librarypaste

License
=======

License is indicated in the project metadata (typically one or more
of the Trove classifiers). For more details, see `this explanation
<https://github.com/jaraco/skeleton/issues/1>`_.

Usage
=====

Launch with the ``librarypaste``
command or with ``python -m librarypaste``. The library will host the service
on ``[::0]:8080`` by default. Pass cherrypy config files on the command line
to customize behaivor.

By default, the server saves pastes to the file system  in ``./repo`` using the
JSON store, but there is support for a MongoDB backend as well.

See also `lpaste <https://pypi.org/project/lpaste>`_ for a Python-based
client (including a clipboard helper) and Mac OS X App.
