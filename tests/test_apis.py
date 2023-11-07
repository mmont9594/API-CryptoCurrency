import datetime
import pytest
from apis import DaySummaryApi, TradesApi

class TestDaySummaryApi:
    @pytest.mark.parametrize(
        "coin, date, expected", 
        [
            ("BTC", datetime.date(2023, 5, 1), "https://www.mercadobitcoin.net/api/BTC/day-summary/2023/5/1"),
            ("ETH", datetime.date(2023, 5, 1), "https://www.mercadobitcoin.net/api/ETH/day-summary/2023/5/1")
    
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected
             
class TestTradesApi:
    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected", 
        [
            ("TEST", datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 2), 
             "https://www.mercadobitcoin.net/api/TEST/trades/1546311600/1546398000"),
            ("TEST", datetime.datetime(2023, 1, 1), datetime.datetime(2023, 2, 1), 
             "https://www.mercadobitcoin.net/api/TEST/trades/1672542000/1675220400"),
            ("TEST", None, None, 
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", datetime.datetime(2023, 1, 1), None, 
             "https://www.mercadobitcoin.net/api/TEST/trades/1672542000"),
            ("TEST", None, datetime.datetime(2023, 2, 1), 
             "https://www.mercadobitcoin.net/api/TEST/trades"),            
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        actual = TradesApi(coin=coin)._get_endpoint(
            date_from=date_from, 
            date_to=date_to)
        assert actual == expected
        
    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            TradesApi(coin="TEST")._get_endpoint(
                date_from= datetime.datetime(2023, 2, 1), 
                date_to=datetime.datetime(2023, 1, 1)
                )
    
    @pytest.mark.parametrize(
        "date, expected", 
        [
            (datetime.datetime(2019, 1, 1), 1546311600),
            (datetime.datetime(2019, 1, 2), 1546398000),
            (datetime.datetime(2023, 1, 1), 1672542000),
            (datetime.datetime(2023, 2, 1), 1675220400)
        ]
    )        
    def test_get_unix_epoch(self, date, expected):
        actual = TradesApi(coin="TEST")._get_unix_epoch(date)
        assert actual == expected