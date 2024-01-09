import re
import urllib.parse
import asyncio

from torss.feed import Channel, Feed, Item, FeedError
from torss.utils import fetch_bs, expect


async def fetch_urls(session):
    url = "https://www.economist.com/weeklyedition"

    soup = await fetch_bs(session, url)

    world_this_week = soup.find(re.compile(r"h\d"), string="The world this week")
    expect(world_this_week, "Couldn't get 'The world this week section'")
    section = world_this_week.find_parent("section")

    politics = section.find("a", string=re.compile(r"Politics.*|The world this.*"))
    business = section.find("a", string=re.compile(r"Business.*"))

    # KAL's uses a real typographic apostrophe (KAL’s cartoon) so to be safe,
    # let's skip it entirely with regular expression
    kal = section.find("a", string=re.compile(r"KAL.*cartoon"))

    urljoin = urllib.parse.urljoin

    ret = {}
    if politics:
        ret["politics"] = urljoin(url, politics["href"])
    if business:
        ret["business"] = urljoin(url, business["href"])
    if kal:
        ret["kal"] = urljoin(url, kal["href"])
    return ret


def lead_img_section_filter(tag):
    if tag.name != "section":
        return False

    figures = tag.find_all("figure")
    if len(figures) != 1:
        return False

    paragraphs = tag.find_all("p")
    if len(paragraphs) > 0:
        return False

    fig = figures[0]
    return any(d.name == "img" for d in fig.descendants)


def body_section_filter(tag):
    if tag.name != "section":
        return False

    paragraphs = tag.find_all("p")
    return len(paragraphs) > 0


def body_filter(tag):
    if tag.name == "p":
        return "your browser does" not in tag.text.lower()
    if tag.name in ("h1", "h2", "h3"):
        return tag.text != "Listen on the go"
    if tag.name == "img":
        return True
    return False


async def parse_article(session, url):
    contents = []

    soup = await fetch_bs(session, url)
    main = soup.find("main", id="content")

    lead_section = main.find(lead_img_section_filter)
    if lead_section:
        contents.append(lead_section.find("img"))

    body = main.find(body_section_filter)
    contents.extend(body.find_all(body_filter))

    return "\n".join(str(elem) for elem in contents)


async def fetch_politics(session, urls):
    if "politics" not in urls:
        return FeedError("URL for Politics this week not found on weeklyedition page")

    url = urls["politics"]

    ch = Channel("The Economist: Politics this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Politics this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "economist/politics.xml")


async def fetch_business(session, urls):
    if "business" not in urls:
        return FeedError("URL for Business this week not found on weeklyedition page")

    url = urls["business"]

    ch = Channel("The Economist: Business this week", "https://www.economist.com")
    ch.items.append(
        Item(
            title="Business this week",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "economist/business.xml")


async def fetch_kal(session, urls):
    if "kal" not in urls:
        return FeedError("URL for KAL's cartoon not found on weeklyedition page")

    url = urls["kal"]

    ch = Channel("The Economist: KAL's cartoon", "https://www.economist.com")
    ch.items.append(
        Item(
            title="KAL's cartoon",
            link=url,
            content=await parse_article(session, url),
        )
    )
    return Feed(ch, "economist/kal.xml")


async def run(session, politics=None, business=None, kal=None, **kw):
    if politics is None and business is None and kal is None:
        return FeedError("economist feed must select subfeeds, like economist,politics=1,business=1,kal=1")

    urls = await fetch_urls(session)
    tasks = []

    if politics is not None:
        tasks.append(fetch_politics(session, urls))
    if business is not None:
        tasks.append(fetch_business(session, urls))
    if kal is not None:
        tasks.append(fetch_kal(session, urls))

    feeds = await asyncio.gather(*tasks)
    return feeds
