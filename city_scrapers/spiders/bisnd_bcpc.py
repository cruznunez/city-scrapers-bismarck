from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.parser import parse
import pdb



class BisndBcpcSpider(CityScrapersSpider):
    name = "bisnd_bcpc"
    agency = "Burleigh County Planning Commission"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.burleigh.gov/government/boardscommittees/planning-zoning-commission/"
    ]
    location = {
        "name": "Tom Baker Room, City/County Building",
        "address": "221 N 5th St, Bismarck",
    }


    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        time = response.css(".tbltitle p::text").get()
        link1 = response.css(".info p")[6].css("a::attr(href)").get() # live video coverage
        link2 = response.css(".info p")[7].css("a::attr(href)").get() # live radio coverage
        title1 = response.css(".info p::text")[7].get() # 'Video coverage provided by Dakota Media Access.\xa0 Watch live on Government Access Cable Channels 2 or 602 HD.\xa0 Stream live or replay later at '
        title2 = response.css(".info p::text")[8].get() # 'Stream live radio coverage from KDAK FM 102.5 FM Radio at '
        links = [
            {
                "title": title1.replace('\xa0', ' '),
                "href": link1
            },
            {
                "title": title2,
                "href": link2
            }
        ]
        # pdb.set_trace()
        for item in response.css("table")[1].css("tr"):
            if not item.css("td"):
                continue
            else:
                meeting = Meeting(
                    title="Planning & Zoning Commission Monthly Meeting",
                    description="",
                    classification=self._parse_classification(item),
                    start=self._parse_start(item, time), # at 5:15 PM
                    end=self._parse_end(item),
                    all_day=self._parse_all_day(item),
                    time_notes=self._parse_time_notes(item),
                    location=self.location,
                    links=links,
                    source=response.url,
                )

                meeting["status"] = self._get_status(meeting)
                meeting["id"] = self._get_id(meeting)

                yield meeting

    # def _parse_title(self, item):
    #     """Parse or generate meeting title."""
    #     return ""
    #
    # def _parse_description(self, item):
    #     """Parse or generate meeting description."""
    #     return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return COMMISSION

    def _parse_start(self, item, time):
        """Parse start datetime as a naive datetime object."""
        date_str = item.css("td:first_child::text").get()
        parsed_datetime = parse(f"{date_str} {time}")

        return parsed_datetime

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
