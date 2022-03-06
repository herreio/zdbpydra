==========
zdbpydra
==========

``zdbpydra`` is a Python package and command line utility that allows to access
JSON-LD data (with PICA+ data embedded) from the German Union Catalogue of Serials (ZDB)
via its Hydra-based API (beta).

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

.. code-block:: shell

    # fetch metadata of serial title
    zdbpydra --id "1231031-1"

    # query metadata of serial titles (cql-based)
    zdbpydra --query "psg=ZDB-1-CPO"

.. code-block:: shell

    # print help message
    zdbpydra --help

Help Message
------------

::

    usage: zdbpydra [-h] [--id ID] [--query QUERY] [--scroll [SCROLL]]
                    [--stream [STREAM]] [--pica [PICA]] [--pretty [PRETTY]]

    Fetch JSON-LD data (with PICA+ data embedded) from the German Union Catalogue
    of Serials (ZDB)

    optional arguments:
      -h, --help         show this help message and exit
      --id ID            id of serial title (default: None)
      --query QUERY      cql-based search query (default: None)
      --scroll [SCROLL]  scroll result set (default: False)
      --stream [STREAM]  stream result set (default: False)
      --pica [PICA]      fetch pica data only (default: False)
      --pretty [PRETTY]  pretty print output (default: False)

Interpreter
~~~~~~~~~~~

.. code-block:: python

    import zdbpydra
    # fetch metadata of serial title
    serial = zdbpydra.title("1231031-1")
    # fetch result page for given query
    result_page = zdbpydra.search("psg=ZDB-1-CPO")
    # fetch all result pages for given query
    result_page_set = zdbpydra.scroll("psg=ZDB-1-CPO")
    # iterate all result pages for given query
    for serial in zdbpydra.stream("psg=ZDB-1-CPO"):
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
for more informations on using the ZDB JSON interface. For details regarding
the LD schema, see the
`local context <https://zeitschriftendatenbank.de/api/context/zdb.jsonld>`_
file.

Informations on the PICA-based ZDB-Format can be found in the corresponding
`cataloguing documentation <https://zeitschriftendatenbank.de/erschliessung/zdb-format>`_
or in the
`PICA+/PICA3 concordance <https://zeitschriftendatenbank.github.io/pica3plus/>`_
(both in german).

Terms
=====

ZDB metadata
~~~~~~~~~~~~

    All metadata in the German Union Catalogue of Serials is available free of
    charge for general use under the Creative Commons Zero 1.0 (CC0 1.0) license.
    Most of the holding data in the ZDB is also freely available. A corresponding
    tag is incorporated into the data record itself. (`Source <https://www.dnb.de/EN/zdb>`_)
