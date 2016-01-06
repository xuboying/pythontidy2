pythontidy2
===========

Usage
~~~~~

.. code:: python

    python -m pythontidy2 [-t expandtabsize] script.py

Installation
~~~~~~~~~~~~

.. code:: python

    pip install pythontidy2

Description
~~~~~~~~~~~

Tidy python scripts

Not compliant to PEP8

Effect
~~~~~~

From:

.. code:: python

    list = [1, 2, {
       'Alicedefg': '2341',
       'Beth' : "c",
       'Cecil' : '3258',
    }, 4]

To:

.. code:: python

    list = [1, 2, {
                    'Alicedefg' : '2341',
                    'Beth'      : "c",
                    'Cecil'     : '3258',
                    }, 4]

From:

.. code:: python

    doc = ""
    long_variable = ((doc+'\n') if doc else '')
    x = ""

To:

.. code:: python

    doc           = ""
    long_variable = ((doc + '\n') if doc else '')
    x             = ""

License
~~~~~~~

BSD
