import os
import sys
import asyncio
import pkgutil
import logging

from typing import Iterable

import aiohttp

from torss.args import ArgumentParser
from torss.feed import Channel, Feed, FeedError

log = logging.getLogger(__name__)

cli = ArgumentParser()
cli.parser.add_argument(
    "-f",
    "--feed",
    action="append",
    default=[],
    dest="feeds",
    help=(
        "name of the feed to fetch. Each feed occupies a single -f option and "
        "can be optionally followed by feed-specific comma-separated options, "
        "e.g. -f economist -f wiki_current_events,date=2022-02-28"
    ),
)
cli.parser.add_argument(
    "-o",
    "--output-dir",
    default="_torss",
    help="path to the directory where torss will store feeds",
)
cli.parser.add_argument(
    "-l",
    "--list-fetchers",
    action="store_true",
    help="list fetchers possible for '-f,--feed' switch and exit"
)
cli.parser.add_argument(
    "--fail-on-error",
    action="store_true",
    help="don't create any feeds when fetching of any of them failed"
)


def get_finders():
    fetchers = {}
    path = os.path.join(os.path.dirname(__file__), "feeds")
    for finder, name, ispkg in pkgutil.iter_modules([path]):
        if name.startswith("_"):
            continue
        fetchers[name] = finder
    return fetchers


def save_feed(ch: Channel, outf: str):
    print("""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>""", file=outf)
    print("""<rss version="2.0">""", file=outf)

    print(format(ch), file=outf)

    print("""</rss>""", file=outf)


def parse_opt(kv):
    key, _, val = kv.partition("=")
    key = key.strip().lower()
    val = val.strip()
    return key, val


def parse_fetcher_options(feeds):
    fetchers = {}
    for feed in feeds:
        fetcher, _, opt_line = feed.partition(",")
        fetcher = fetcher.strip().lower()
        opts = {}

        for kv in opt_line.split(","):
            key, val = parse_opt(kv)
            if key and val:
                opts[key] = val

        fetchers[fetcher] = opts

    return fetchers


def cond_flatten(ls):
    flat = []
    for elem in ls:
        if isinstance(elem, (list, tuple)):
            flat.extend(elem)
        else:
            flat.append(elem)
    return flat


def load_fetcher(name, fetcher_finders):
    finder = fetcher_finders.get(name)
    if finder is None:
        return None

    mod = finder.find_module(name)
    if mod is None:
        return None

    return mod.load_module()


async def fetch_rss(args, requested_fetchers, fetcher_finders):
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []

        for name, opts in requested_fetchers.items():
            mod = load_fetcher(name, fetcher_finders)
            if mod is None:
                log.error("Fetcher for '%s' feed not found", name)
                if args.fail_on_error:
                    sys.exit(1)
                else:
                    continue

            tasks.append(mod.run(session, **opts))

        results = await asyncio.gather(*tasks)
        return cond_flatten(results)


def partition_results(results):
    feeds, errors = [], []
    for r in results:
        if isinstance(r, Feed):
            feeds.append(r)
        elif isinstance(r, FeedError):
            errors.append(r)
        else:
            raise RuntimeError(f"feed parser error: unsupported feed type: {str(type(r))}")
    return feeds, errors


def write_results(output_dir, feeds):
    for feed in feeds:
        feed_file = os.path.join(output_dir, feed.file)
        feed_dir = os.path.dirname(feed_file)
        os.makedirs(feed_dir, exist_ok=True)

        with open(feed_file, "w", encoding="utf-8") as of:
            save_feed(feed.channel, of)


async def main_():
    args = cli.parse_args()

    if args.list_fetchers:
        for name in sorted(get_finders().keys()):
            print(name)

    if not args.feeds:
        return 0

    requested_fetchers = parse_fetcher_options(args.feeds)
    fetcher_finders = get_finders()
    results = await fetch_rss(args, requested_fetchers, fetcher_finders)
    feeds, errors = partition_results(results)

    for e in errors:
        log.error(e.err)
    if errors and args.fail_on_error:
        return 1

    write_results(args.output_dir, feeds)
    return 0 if not errors else 1


def main():
    loop = asyncio.get_event_loop()
    sys.exit(loop.run_until_complete(main_()))
