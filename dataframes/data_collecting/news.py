from duckduckgo_search import ddg
import trafilatura


def scrape_article(url):
    # returns the main article content of a news article URL
    content = trafilatura.fetch_url(url)
    if content:
        return trafilatura.extract(content, include_comments=False)


class News:
    def __init__(self, query):
        self.query = query
        self.sites = ["reuters", "nasdaq.com", "wsj", "marketwatch.com", "zacks.com", "yahoo finance", "ecomomics.com"]
        self.articles, self.links = self.ddg_search()
        self.headlines = self.filter_headlines()

    def ddg_search(self):
        results = []
        for site in self.sites:
            # performs a duckduckgo search with the query and a given site
            results.extend(ddg(f"{self.query} Company site:{site}",
                               region='wt-wt',
                               safesearch='Moderate',
                               time='w'))
        links = []
        # the urls of the results will be returned
        for item in results:
            links.append(item["href"])
        return results, links

    def _headlines(self):
        lines = []
        for article in self.articles:
            line = article["title"]
            lines.append(line)
        return lines

    def filter_headlines(self):
        heads = self._headlines()
        result = []
        for head in heads:
            if self.query in head:
                result.append(head)
        return result


if __name__ == "__main__":
    news = News("Tesla")
    for art in news.headlines:
        print(art)
