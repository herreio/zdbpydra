==========
zdbpydra
==========

``zdbpydra`` is a Python package and command line utility that allows to access
JSON-LD-formatted PICA data of the German Union Catalogue of Serials (ZDB)
via their Hydra-based JSON API (beta).

Installation
============

... via SSH
~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+ssh://git@github.com/herreio/zdbpydra.git#egg=zdbpydra

... or via HTTPS
~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+https://github.com/herreio/zdbpydra.git#egg=zdbpydra

Usage Examples
=============

Command Line
~~~~~~~~~~~~

::
    $ zdbpydra --id "..."

::
    usage: zdbpydra [-h] [--id ID] [--query QUERY] [--pica [PICA]]
                [--pretty [PRETTY]]

    Fetch JSON-LD-formatted Pica data from the German Union Catalogue of Serials

    optional arguments:
      -h, --help         show this help message and exit
      --id ID            id of title to fetch (default: None)
      --query QUERY      cql-based search query (default: None)
      --pica [PICA]      fetch pica data only (default: False)
      --pretty [PRETTY]  pretty print output (default: False)

Interpreter
~~~~~~~~~~~

.. code-block:: python

    import zdbpydra
    # fetch serial title data by id
    serial = zdbpydra.title("...")
    # fetch result page for given query
    result_page = zdbpydra.search("")
    # fetch complete result set for given query
    result_set = zdbpydra.scroll("")
    # iterate over complete result set for given query
    for serial in zdbpydra.stream(""):
        print(serial.title)

Background
==========

See `Hydra: Hypermedia-Driven Web APIs <https://github.com/lanthaler/Hydra>`_
by `Markus Lanthaler <https://github.com/lanthaler>`_ for more information
on Hydra APIs in general.

Have a look at the
`API documentation <https://zeitschriftendatenbank.de/services/schnittstellen/json-api>`_
and
`CQL documentation <https://zeitschriftendatenbank.de/services/schnittstellen/hilfe-zur-suche>`_
(both in german)
for more informations on using the ZDB JSON interface.

For details regarding the linked data schema, see the
`local context <https://zeitschriftendatenbank.de/api/context/zdb.jsonld>`_
file.

Informations on the PICA-based ZDB-Format can be found in the corresponding
`cataloguing documentation <https://zeitschriftendatenbank.de/erschliessung/zdb-format>`_
or in the
`PICA+ PICA3 concordance <https://zeitschriftendatenbank.github.io/pica3plus/>`_
(both in german).
