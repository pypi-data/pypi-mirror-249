import argparse
import asyncio
import sys
from importlib.metadata import version

import httpx

from aws_meun.core import unsubscribe_all, unsubscribe_all_async

PROG = "aws-meun"


def _print_result(email: str, response: httpx.Response) -> None:
    try:
        response.raise_for_status()
        print(f"Unsubscribed {email} ({response.http_version} {response.status_code})")
    except httpx.HTTPStatusError as e:
        print(
            f"Failed to unsubscribe {email} ({e.response.http_version} {e.response.status_code})"
        )


async def _run_async(emails: list[str], **kwargs) -> None:
    async for email, response in unsubscribe_all_async(emails, **kwargs):
        _print_result(email, response)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=PROG, description="Unsubscribe from AWS Marketing emails"
    )
    parser.add_argument("--version", action="version", version=version(PROG))
    parser.add_argument(
        "--http2",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="use HTTP/2",
    )
    parser.add_argument(
        "--parallel",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="run requests in parallel",
    )
    parser.add_argument("email", nargs="*", help="email address(es) to unsubscribe")

    args = parser.parse_args()

    if not args.email and not sys.stdin.isatty():
        emails = [email.rstrip() for email in sys.stdin.readlines()]
    else:
        emails = args.email

    if args.parallel:
        asyncio.run(_run_async(emails, http2=args.http2))
    else:
        for email, response in unsubscribe_all(emails, http2=args.http2):
            _print_result(email, response)
