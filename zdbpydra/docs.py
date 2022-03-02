# -*- coding: utf-8 -*-
"""
Parser classes for JSON-LD data (with PICA+ data embedded) retrieved
from the German Union Catalogue of Serials (ZDB)

For more information on the PICA-based cataloguing format of ZDB, see
https://zeitschriftendatenbank.github.io/pica3plus/ or
https://zeitschriftendatenbank.de/erschliessung/zdb-format (both in german).
"""


class BaseParser:

    def __init__(self, data):
        self.raw = data

    def _names(self):
        if self.raw:
            names = list(self.raw.keys())
            names.sort()
            return names
        return []

    def _field(self, name):
        if self.raw and name in self.raw:
            return self.raw[name]

    def get(self, name):
        return self._field(name)


class ObjectParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def id(self):
        return self._field("id")

    @property
    def type(self):
        return self._field("type")


class ResponseParser(ObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def context(self):
        return self._field("@context")


class SearchResponseParser(ResponseParser):
    """
    Die Metadaten zur Suchanfrage bestehen aus folgenden Schlüsseln:

        `id` - URL der ursprünglich gestellten Suchanfrage
        `freetextQuery` - die Suchterme
        `totalItems` - Absolute Anzahl der Ergebnisse
        `type` - Der Typ einer Ergebnismenge ist immer Collection

    Die eigentlichen Titeldaten werden unter dem Schlüssel `member` in
    einem JSON-Array zusammengefasst. ... die ... Navigation ist unter
    dem Schlüssel `view` als JSON-Objekt zusammengefasst.

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def query(self):
        return self._field("freetextQuery")

    @property
    def total_items(self):
        count = self._field("totalItems")
        if count:
            return int(count)
        return 0

    @property
    def member(self):
        return self._field("member")

    @property
    def view(self):
        return self._field("view")

    @property
    def view__parser(self):
        view = self.view
        if view is not None:
            return ViewResponseParser(view)

    def _field_view(self, field):
        view = self.view
        if type(view) == dict and field in view:
            return view[field]

    def get(self, name, view=False):
        if view:
            return self._field_view(name)
        return self._field(name)

    @property
    def view_first(self):
        return self._field_view("first")

    @property
    def view_next(self):
        return self._field_view("next")

    @property
    def view_last(self):
        return self._field_view("last")


class ViewResponseParser(ObjectParser):
    """
    Die Navigation enthält die Schlüssel:

        `id` - Link zur aktuellen Seite
        `type` - ist immer PartialCollectionView
        `first` - Link zur ersten Seite
        `last` - Link zur letzten Seite
        `totalItems` - Anzahl der Datensätze, die auf der aktuellen Seite angezeigt werden
        `pageIndex` - Nummer der aktuellen Seite
        `numberOfPages` - Anzahl der Ergebnisseiten
        `offset` - Nummer des ersten Datensatzes auf der aktuellen Seite
        `limit` - Maximale Anzahl von Ergebnissen auf einer Seite

    und möglicherweise:

        `previous` - Link zur vorherigen Seite, falls vorhanden
        `next` - Link zur nächsten Seite, falls vorhanden

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def total_items(self):
        return self._field("totalItems")

    @property
    def page_index(self):
        return self._field("pageIndex")

    @property
    def number_of_pages(self):
        return self._field("numberOfPages")

    @property
    def offset(self):
        return self._field("offset")

    @property
    def limit(self):
        return self._field("limit")

    @property
    def first(self):
        return self._field("first")

    @property
    def last(self):
        return self._field("last")

    @property
    def previous(self):
        return self._field("previous")

    @property
    def next(self):
        return self._field("next")


class TitleResponseParser(ResponseParser):
    """
    Jeder Titeldatensatz hat folgende Schlüssel:

        `id` - URL, der den Datensatz identifiziert
        `type` - Liste der Publikationstypen
        `seeAlso` - URL einer RDF-Repräsentation der Daten
        `sameAs` - wie seeAlso
        `identifier` - die ZDB-ID
        `medium`- Medientyp (print, audiovisual, braille, microform, online, electronic)
        `issn` - Liste der gültigen ISSNs
        `title` - Titel der Publikation
        `temporal` - Erscheinungsverlauf
        `publisher`- Publikationsvermerk
        `data` - der PICA-Plus-Datensatz in Form eines JSON-Objekts

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def _id(self):
        return self._field("_id")

    @property
    def data(self):
        return self._field("data")

    @property
    def issn(self):
        return self._field("issn")

    @property
    def medium(self):
        return self._field("medium")

    @property
    def identifier(self):
        return self._field("identifier")

    @property
    def publisher(self):
        return self._field("publisher")

    @property
    def same_as(self):
        return self._field("sameAs")

    @property
    def see_also(self):
        return self._field("seeAlso")

    @property
    def temporal(self):
        return self._field("temporal")

    @property
    def title(self):
        return self._field("title")

    @property
    def data__parser(self):
        data = self._field("data")
        if data is not None:
            return PicaParser(data)

    def _field_pica(self, field):
        data = self.data
        if type(data) == dict and field in data:
            return data[field]

    def get(self, name, pica=True):
        if pica:
            return self._field_pica(name)
        return self._field(name)


class PicaParser(BaseParser):
    """
    For the PICA+ / PICA3 field definitions used by ZDB, see
    https://zeitschriftendatenbank.github.io/pica3plus/
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def idn(self):
        """
        003@/0100 – Identifikationsnummer des Datensatzes (IDN)
        """
        value = self._field("003@")
        if value is not None:
            return value[0][0][0]
