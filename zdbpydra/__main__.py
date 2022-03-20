"""
Command line utility for fetching JSON-LD data (with PICA+ data embedded)
from the German Union Catalogue of Serials (ZDB)
"""

import argparse

from . import title, search, stream, scroll
from . import utils
from . import __version__


LOGLEVEL = 0
HEADERS = {"User-Agent": "zdbpydra-cli {0}".format(__version__)}
DESCRIPTION = """
Fetch JSON-LD data (with PICA+ data embedded)
from the German Union Catalogue of Serials (ZDB)
"""


def json_output(raw, pretty):
    if pretty:
        return utils.json_str_pretty(raw)
    else:
        return utils.json_str(raw)


def print_raw(raw, pretty):
    if raw and raw is not None:
        print(json_output(raw, pretty))


def print_result(result, pretty):
    if result and result is not None:
        print_raw(result.raw, pretty)


def main():
    zdbpydra_cli = argparse.ArgumentParser(
        "zdbpydra", description=DESCRIPTION)
    zdbpydra_cli.add_argument(
        "--id", type=str,
        help="id of title to fetch (default: None)",
        default=None)
    zdbpydra_cli.add_argument(
        "--query", type=str,
        help="cql-based search query (default: None)",
        default=None)
    zdbpydra_cli.add_argument(
        "--scroll", type=bool,
        help="scroll result set (default: False)",
        nargs='?', const=True, default=False)
    zdbpydra_cli.add_argument(
        "--stream", type=bool,
        help="stream result set (default: False)",
        nargs='?', const=True, default=False)
    zdbpydra_cli.add_argument(
        "--pica", type=bool,
        help="fetch pica data only (default: False)",
        nargs='?', const=True, default=False)
    zdbpydra_cli.add_argument(
        "--pretty", type=bool,
        help="pretty print output (default: False)",
        nargs='?', const=True, default=False)
    zdbpydra_args = zdbpydra_cli.parse_args()
    if zdbpydra_args.id is None and zdbpydra_args.query is None:
        zdbpydra_cli.print_help()
        return None
    if zdbpydra_args.id is not None:
        result = title(zdbpydra_args.id, pica=zdbpydra_args.pica,
                       headers=HEADERS, loglevel=LOGLEVEL)
        if result:
            print_result(result, zdbpydra_args.pretty)
        return None
    if zdbpydra_args.query is not None:
        if zdbpydra_args.stream:
            for serial in stream(zdbpydra_args.query, size=10,
                                 page=1, headers={}, loglevel=LOGLEVEL):
                if serial:
                    print_result(serial, False)
            return None
        if zdbpydra_args.scroll:
            result = scroll(zdbpydra_args.query, size=10, page=1,
                            headers=HEADERS, loglevel=LOGLEVEL)
            if result and isinstance(result, list):
                result_out = []
                for serial in result:
                    result_out.append(serial.raw)
                print_raw(result_out, zdbpydra_args.pretty)
            return None
        else:
            result = search(zdbpydra_args.query)
            if result and isinstance(result, list):
                result_out = []
                for serial in result:
                    result_out.append(serial.raw)
                print_raw(result_out, zdbpydra_args.pretty)
            return None


if __name__ == '__main__':
    main()
