======
Stilpy
======


.. image:: https://img.shields.io/pypi/v/stilpy.svg
        :target: https://pypi.python.org/pypi/stilpy

.. image:: https://img.shields.io/travis/fesanmar/stilpy.svg
        :target: https://travis-ci.org/fesanmar/stilpy

.. image:: https://readthedocs.org/projects/stilpy/badge/?version=latest
        :target: https://stilpy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/fesanmar/Stilpy/shield.svg
     :target: https://pyup.io/repos/github/fesanmar/Stilpy/
     :alt: Updates



Stilpy creates time intervals from records and manage them for you.


* Free software: MIT license
* Documentation: https://stilpy.readthedocs.io.


Features
--------

* Sorted time intervals iterator created from a collection of records
* List, tuples, dicts and dict like objects supported as the items inside the collection of records
* `sqlite3.Row objects`_ supported as well
* Records grouping supported so you can create intervals applying grouping conditions
* datetime strings dynamically casted to datetime_ format
* Sum the durations of your time intervals if they can be sum
* This repository is being maintained

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _datetime: https://docs.python.org/3.8/library/datetime.html#datetime-objects
.. _`sqlite3.Row objects`: https://docs.python.org/3/library/sqlite3.html#row-objects

 [ ~ Dependencies scanned by PyUp.io ~ ]
