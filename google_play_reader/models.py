"""Models of this library."""

from lxml import html
import requests
import csv
import os

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

class AppDatabase():

    _CSV_HEADER = [
        "package",
        "rating_value",
        "rating_count",
        "downloads"
    ]
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        if not os.path.isfile(self.csv_filename):
            with open(self.csv_filename, 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=self._CSV_HEADER)
                csv_writer.writeheader()

    def already_processed(self, package):
        with open(self.csv_filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return package in (row['package'] for row in csv_reader)
        return False

    def process(self, package):
        if self.already_processed(package):
            print("Skipping {}: already processed.".format(package))
            return
        try:
            app = AppEntry(package)
            rating_value, rating_count = app.get_rating()
            downloads = app.get_downloads()
        except Exception as e:
            print(e)
            print("Warning: could not get info for {}".format(package))
            rating_value = rating_count = downloads = None
        with open(self.csv_filename, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self._CSV_HEADER)
            csv_writer.writerow({
                "package": package,
                "rating_value": rating_value,
                "rating_count": rating_count,
                "downloads": downloads,
            })
        

    def bulk_process(self, packages):
        """Process list of packages"""
        for package in packages:
            print("Collecting info for {}.".format(package))
            self.process(package)

            
             

if __name__ == "__main__":
    app = AppEntry("com.newsblur")
    print(app._get_page_and_tree())
    print(app.get_name())
    bulk = AppDatabase("test.csv")
    print(bulk.already_processed("com.showmehills"))
    bulk.bulk_process(["com.newsblur","eu.siacs.conversations","com.showmehills"])
    
    
