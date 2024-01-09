# RSS Scrap

rss-scrap is a command line utility which scraps contents of web pages and
converts them to RSS feeds. Specific web scrapers must be implemented for
each page.

rss-scrap works asynchronously, meaning that many web pages can be scraped
simultaneously.

## Implemented scrappers

- `economist`: The Economist, World This Week section: Politics this week,
  Business this week, Kal's Cartoon (3 separate feeds)
- `wiki_current_events`: Wikipedia Current Events
    - parameter `date`: day (ISO format) from which events should be fetched
      (e.g. `-f wiki_current_events,date=2020-10-27`)
- `gov_pl_gis`: Warnings of Główny Inspektorat Sanitarny (Polish Government Agency)
