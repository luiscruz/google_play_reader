"""Models of this library."""

from lxml import html
import requests

class AppEntry(object):
    
    _page = None
    _tree = None
    def __init__(self, package):
        self.package = package
        self._url = "https://play.google.com/store/apps/details?id={}&hl=en".format(package)

    def _get_page_and_tree(self):
        """Return app's page from google play."""
        if self._page is None:
            self._page = requests.get(self._url)
            self._tree = html.fromstring(self._page.content)
        return self._page, self._tree

    def get_rating(self):
        "Get rating value and count of ratings."
        page, tree = self._get_page_and_tree()
        rating = tree.xpath('//div[@itemprop="aggregateRating"]')[0]
        value = rating.xpath('//meta[@itemprop="ratingValue"]')[0].attrib["content"]
        count = rating.xpath('//meta[@itemprop="ratingCount"]')[0].attrib["content"]
        return float(value), int(count)
    
    def get_downloads(self):
        "Get range number of downloads."
        page, tree = self._get_page_and_tree()
        downloads = tree.xpath('//div[@itemprop="numDownloads"]')[0].text
        return downloads.strip()
    
    def get_category(self):
        "Get category of the app."
        page, tree = self._get_page_and_tree()
        downloads = tree.xpath('//span[@itemprop="genre"]')[0].text
        return downloads.strip()
    
    def get_name(self):
        "Get name of the app."
        page, tree = self._get_page_and_tree()
        name = tree.xpath('//div[@class="id-app-title"]')[0].text
        return name.strip()


if __name__ == "__main__":
    app = AppEntry("com.newsblur")
    print(app._get_page_and_tree())
    print(app.get_name())
    
