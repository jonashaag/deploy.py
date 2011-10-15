./deploy.py
===========

Deploys tox_-generated virtualenvs using uWSGI_, nginx_ and supervisord_
within seconds. Based on fabric_.

System Setup
------------
Follow the instructions in ``etc/*``.

Setup & Initial Deploy
----------------------
In your project directory, do ::

   cp /path/to/deploy/fabfile.py .
   ln -s /path/to/deploy/deploy.py

   vim fabfile.py
   ./deploy.py

On the remote host, do ::

   sudo supervisorctl reread
   sudo supervisorctl update
   sudo /etc/(rc.d|init.d|...)/nginx reload

Subsequent Deploys
------------------
::

   ./deploy.py


.. _tox: http://tox.readthedocs.org
.. _uWSGI: http://projects.unbit.it/uwsgi/
.. _nginx: http://wiki.nginx.org
.. _supervisord: http://supervisord.org
.. _fabric: http://fabfile.org
