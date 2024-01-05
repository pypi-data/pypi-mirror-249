Installation 
=============

The easiest way to use geometron is to install it with pip (or tools based on pip such as pipenv)

.. code-block:: bash

    $ pip install geometron

For contributing, you will need to clone the repository and setup the environment for using this project
:

.. code-block:: bash

   $ git clone git@gfa-gitlab.umons.ac.be:kaufmanno/geometron.git
   $ cd geometron/
   $ pipenv shell
   $ pipenv install

To view installed dependencies, see the
`Pipfile <https://gfa-gitlab.umons.ac.be/kaufmanno/geometron/blob/master/Pipfile>`__.
Be aware that using *pipfile install* actually installs from the
Pipfile.lock file. Use the –skip-lock option if you want to use the
Pipfile instead.
