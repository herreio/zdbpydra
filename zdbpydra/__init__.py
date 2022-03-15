"""
This package allows to access JSON-LD data (with PICA+ data embedded)
from the German Union Catalogue of Serials (ZDB)
"""

__author__ = "Donatus Herre <donatus.herre@slub-dresden.de>"
__version__ = "0.1.1"

from .client import Hydra
from .docs import PicaParser


def context(headers={}, loglevel=0):
    hydra = Hydra(loglevel=loglevel)
    return hydra.context(headers=headers)


def title(id, pica=False, headers={}, loglevel=0):
    hydra = Hydra(loglevel=loglevel)
    return hydra.title(id, pica=pica, headers=headers)


def search(query, size=10, page=1, headers={}, loglevel=0):
    hydra = Hydra(loglevel=loglevel)
    return hydra.search(query, size=size, page=page, headers={})


def scroll(query, size=10, page=1, headers={}, loglevel=0):
    hydra = Hydra(loglevel=loglevel)
    return hydra.scroll(query, size=size, page=page, headers=headers)


def stream(query, size=10, page=1, headers={}, loglevel=0):
    hydra = Hydra(loglevel=loglevel)
    return hydra.stream(query, size=size, page=page, headers=headers)


def parse_pica(data):
    return PicaParser(data)
