import datetime
from abc import ABC, abstractmethod
import logging
from ratelimit import exception, limits
import requests
from backoff import on_exception, expo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MercadoBitcoinApi(ABC):
    
    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.base_endpoint = 'https://www.mercadobitcoin.net/api'
    
    # Método interno
    @abstractmethod
    def _get_endpoint(self, **kwargs) -> str:
        pass
    
    @on_exception(expo, exception.RateLimitException, max_tries=10)
    @limits(calls=15, period=40)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(url=endpoint)
        response.raise_for_status()
        return response.json()
    
class DaySummaryApi(MercadoBitcoinApi):
    type = 'day-summary'
        
    def _get_endpoint(self, date: datetime.datetime) -> str:
        
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"

class TradesApi(MercadoBitcoinApi):
    type = 'trades'
    
    def _get_unix_epoch(self, date: datetime.datetime):
        return int(date.timestamp())
    
    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:
        if date_from and not date_to:
            unix_data_from = self._get_unix_epoch(date=date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_data_from}"
        elif date_to and date_from:
            if date_from > date_to:
                raise RuntimeError("date_from cannot be greater than date_to")
            unix_data_from = self._get_unix_epoch(date=date_from)
            unix_data_to = self._get_unix_epoch(date=date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_data_from}/{unix_data_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"
    
        return endpoint