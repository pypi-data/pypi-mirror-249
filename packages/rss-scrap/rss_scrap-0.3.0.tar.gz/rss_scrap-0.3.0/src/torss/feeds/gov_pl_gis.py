import asyncio
from urllib.parse import urljoin
from datetime import datetime, timezone

from torss.feed import Channel, Feed, Item
from torss.utils import fetch_bs, pub_date_fmt

BASE_URL = "https://www.gov.pl/web/gis/ostrzezenia"


async def get_article(session, li):
    relurl = li.a["href"]
    url = relurl if relurl.startswith("http") else urljoin(BASE_URL, relurl)
    soup = await fetch_bs(session, url)
    article = soup.find("article", id="main-content")

    title = article.h2.text
    date = datetime.strptime(
        article.find(class_="event-date").text, "%d.%m.%Y"
    ).replace(tzinfo=timezone.utc)

    contents = []

    main_photo = article.find(class_="main-photo")
    if main_photo:
        contents.append(str(main_photo))

    contents.append(str(article.find(class_="editor-content")))

    gallery = article.find(class_="gallery")
    if gallery:
        contents.append("<h3>Zdjęcia</h3>")
        contents.append(str(gallery))

    return Item(title, "\n".join(contents), link=url, pub=pub_date_fmt(date))


async def run(session):
    soup = await fetch_bs(session, BASE_URL)
    content = soup.find(class_="article-area")
    if not content:
        return

    ch = Channel("Główny Inspektorat Sanitarny - Ostrzeżenia", BASE_URL)

    article_list = content.article.ul
    tasks = [get_article(session, li) for li in article_list.find_all("li")]
    ch.items = await asyncio.gather(*tasks)

    return Feed(ch, "gov_pl_gis/gis_warnings.xml")
