import datetime
import time
from schedule import repeat, every, run_pending
import datetime
import json
import os
from typing import List
import datetime
from abc import ABC, abstractmethod
from typing import List
import os
from abc import ABC, abstractmethod
import logging
import ratelimit
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
    
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=15, period=40)
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
            unix_data_from = self._get_unix_epoch(date=date_from)
            unix_data_to = self._get_unix_epoch(date=date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_data_from}/{unix_data_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"
    
        return endpoint
    
class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        venv_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(venv_dir, f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json").replace("\\", "/")
    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        print(self.filename)
        with open(self.filename, "a") as f:
            f.write(row) 
    
    def write(self, data: [List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)   
    
    
class DataIngestor(ABC):    
    def __init__(self, writer, coins: List[str], default_start_date: datetime.date) -> None:
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer
        self._checkpoint = self._load_checkpoint()
    
    @property
    def _checkpoint_filename(self) -> str:
        print(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{self.__class__.__name__}.checkpoint").replace('\\', '/')
    
    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")
            
    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None
            
    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint
        
    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass

      
class DaySummaryIngestor(DataIngestor):
    
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))

day_summary_ingestor = DaySummaryIngestor(
        writer=DataWriter, 
        coins=["BTC", "ETH", "LTC"], 
        default_start_date=datetime.date(2023, 1, 1)
        )

@repeat(every(1).seconds)
def job():
    day_summary_ingestor.ingest()
   
while True:
    run_pending()
    time.sleep(0.5)



