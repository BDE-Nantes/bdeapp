============
Installation
============

The project is developed in Python using the `Django framework`_. There are 3
sections below, focussing on developers, running the project using Docker and
hints for running the project in production.

.. _Django framework: https://www.djangoproject.com/


Development
===========


Prerequisites
-------------

You need the following libraries and/or programs:

* `Python`_ 3.9 or above
* Python `Virtualenv`_ and `Pip`_
* `PostgreSQL`_ 11 or above (14 recommended)
* If using Windows, you will need DDLs for libmagic. See `Installation instructions <https://github.com/ahupp/python-magic#windows>_`

.. _Python: https://www.python.org/
.. _Virtualenv: https://virtualenv.pypa.io/en/stable/
.. _Pip: https://packaging.python.org/tutorials/installing-packages/#ensure-pip-setuptools-and-wheel-are-up-to-date
.. _PostgreSQL: https://www.postgresql.org


Getting started
---------------

Developers can follow the following steps to set up the project on their local
development machine.

1. Navigate to the location where you want to place your project.

2. Get the code:

   .. code-block:: bash

       $ git clone git@github.com:BDE-Nantes/bdeapp.git
       $ cd bdeapp

3. Install all required (backend) libraries:

   .. code-block:: bash

       $ virtualenv env
       $ source env/bin/activate
       $ pip install -r requirements/dev.txt

4. Setup your PostgreSQL database (default user is ``bdeapp``, password is ``bdeapp``)

    .. code-block:: bash

        $ sudo -u postgres createuser --interactive --pwprompt
        $ sudo -u postgres createdb -O bdeapp bdeapp

5. Collect statics and create the initial database tables:

   .. code-block:: bash

       $ python src/manage.py collectstatic --link
       $ python src/manage.py migrate

6. Create a superuser to access the management interface:

   .. code-block:: bash

       $ python src/manage.py createsuperuser

7. You can now run your installation and point your browser to the address
   given by this command:

   .. code-block:: bash

       $ python src/manage.py runserver

8. Create a .env file with database settings. See dotenv.example for an example.

   .. code-block:: bash

       $ cp dotenv.example .env


**Note:** If you are making local, machine specific, changes, add them to
``src/bdeapp/conf/local.py``. You can base this file on the
example file included in the same directory.


Update installation
-------------------

When updating an existing installation:

1. Activate the virtual environment:

   .. code-block:: bash

       $ cd bdeapp
       $ source env/bin/activate

2. Update the code and libraries:

   .. code-block:: bash

       $ git pull
       $ pip install -r requirements/dev.txt

3. Update the statics and database:

   .. code-block:: bash

       $ python src/manage.py collectstatic --link
       $ python src/manage.py migrate


Testsuite
---------

To run the test suite:

.. code-block:: bash

    $ python src/manage.py test bdeapp

Configuration via environment variables
---------------------------------------

A number of common settings/configurations can be modified by setting
environment variables. You can persist these in your ``local.py`` settings
file or as part of the ``(post)activate`` of your virtualenv.

* ``SECRET_KEY``: the secret key to use. A default is set in ``dev.py``

* ``DB_NAME``: name of the database for the project. Defaults to ``bdeapp``.
* ``DB_USER``: username to connect to the database with. Defaults to ``bdeapp``.
* ``DB_PASSWORD``: password to use to connect to the database. Defaults to ``bdeapp``.
* ``DB_HOST``: database host. Defaults to ``localhost``
* ``DB_PORT``: database port. Defaults to ``5432``.


All settings for the project can be found in
``src/bdeapp/conf``.
The file ``local.py`` overwrites settings from the base configuration.


Commands
========

Commands can be executed using:

.. code-block:: bash

    $ python src/manage.py <command>

There are no specific commands for the project. See
`Django framework commands`_ for all default commands, or type
``python src/manage.py --help``.

.. _Django framework commands: https://docs.djangoproject.com/en/dev/ref/django-admin/#available-commands
