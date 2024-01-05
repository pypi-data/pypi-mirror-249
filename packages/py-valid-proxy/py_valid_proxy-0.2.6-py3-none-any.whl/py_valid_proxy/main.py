# -*- coding: utf-8 -*-
# @Author: Suvorinov Oleg
# @Date:   2023-11-13 11:20:47
# @Last Modified by:   Suvorinov Oleg
# @Last Modified time: 2023-12-13 08:43:46

import sys
import argparse
from urllib.parse import urlparse
import pkg_resources
import re

from rich.console import Console

from py_valid_proxy import valid_proxy


def valid_proxy_url(url: str) -> bool:
    regex = r"^(http|https|socks4|socks5):\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"  # noqa
    matches = re.findall(regex, url, re.MULTILINE)
    if matches:
        return True
    return False


def main(args=None):

    _prog = "%(prog)s"
    _version = pkg_resources.get_distribution('py_valid_proxy').version
    _prog_version = f"{_prog} {_version}"

    parser = argparse.ArgumentParser(
        prog='valid_proxy',
        description="Valid the functionality of the proxy server"
    )

    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=5,
        help='The connect timeout is the number of seconds')

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=_prog_version
    )

    parser.add_argument(
        'proxy',
        help='Proxy server URL, '
    )

    args = parser.parse_args()

    console = Console()
    timeout = 5
    if args.timeout:
        timeout = args.timeout

    if args.proxy:
        if not valid_proxy_url(args.proxy):
            console.print(
                f"Oops, something is wrong with the proxy URL {args.proxy}",
                style="red"
            )
            sys.exit(1)

        result = urlparse(args.proxy.lower())
        if not result.scheme or \
                not result.netloc or \
                not result.hostname or \
                not result.port:
            console.print(
                f"Oops, something is wrong with the proxy URL {args.proxy}",
                style="red"
            )
            sys.exit(1)

        try:
            with console.status("Validates..."):
                proxy = valid_proxy(result.hostname, result.port, result.scheme, timeout)  # noqa
        except Exception:
            console.print(f"{args.proxy} ... is dead", style="bold red")
        else:
            console.print(f"{args.proxy} ... is alive", style="bold green")
            console.print(f"anonymity: {proxy.anonymity}")
            console.print(f"country: {proxy.country}")
            console.print(f"response time: {proxy.response_time} (secs)")


if __name__ == '__main__':
    main()
