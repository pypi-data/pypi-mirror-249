import io
import urllib
import urllib3

import pandas as pd

from marcuslion.config import api_version
from marcuslion.restcontroller import RestController


class TimeSeries(RestController):
    """
    https://qa1.marcuslion.com/swagger-ui/index.html#/time-series-api-controller
    """

    def __init__(self):
        super().__init__(api_version + "/timeseries/history")

    def list(self, symbol, interval, page_size) -> pd.DataFrame:
        """
        Indicators.list()
        """
        return super().verify_get(symbol + "/" + interval + "/" + str(page_size), {})

    def query(self, ref):
        return super().verify_get_data("query", {"ref", ref})

    def search(self, search) -> pd.DataFrame:
        return super().verify_get_data("search", {"search", search})

    def download(self, ref, params) -> pd.DataFrame:
        """
        Indicators.download(ref, params)
        """
        pass

    def subscribe(self, ref, params):
        """
        Indicators.subscribe(ref, params)
        """
        pass
