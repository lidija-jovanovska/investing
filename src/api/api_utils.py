import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class FinancialModelingPrepAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.session = self._create_session()
        self.session_timeout = (5, 10)  # connect timeout, read timeout

    def _create_session(self):
        session = requests.session()
        retries = Retry(
            total=10,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        session.mount(
            "https://financialmodelingprep.com/api/v3", HTTPAdapter(max_retries=retries)
        )
        return session

    def get_market_cap(self, ticker):
        try:
            url = f"https://financialmodelingprep.com/api/v3/market-capitalization/{ticker}?apikey={self.api_key}"
            market_cap = self.session.get(url=url, timeout=self.session_timeout).json()[
                0
            ]["marketCap"]
        except Exception:
            market_cap = None
        return market_cap

    def get_ratios(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?period=annual&apikey={self.api_key}"
        try:
            raw_ratios = self.session.get(url=url, timeout=self.session_timeout).json()[
                0
            ]
        except Exception:
            raw_ratios = dict(symbol=ticker)
        return raw_ratios

    def get_earnings(self, ticker, months=44):
        url = f"https://financialmodelingprep.com/api/v3/historical/earning_calendar/{ticker}?period=annual&apikey={self.api_key}&limit={months}"
        try:
            earnings = self.session.get(url=url, timeout=self.session_timeout)
            if earnings.status_code == 200:
                earnings = earnings.json()
            else:
                earnings = {}
        except Exception:
            earnings = {}
        return earnings

    def get_dividends(self, ticker, months=80):
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ticker}?apikey={self.api_key}&limit={months}"
        try:
            dividends = self.session.get(url=url, timeout=self.session_timeout).json()[
                "historical"
            ]
        except Exception:
            dividends = {}
        return dividends

    def get_ratios_ttm(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={self.api_key}"
        try:
            ratios = self.session.get(url=url, timeout=self.session_timeout).json()[0]
            ratios["symbol"] = ticker
        except Exception:
            ratios = {}
        return ratios

    def get_income_statement(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=quarter&apikey={self.api_key}"
        try:
            income_statement = self.session.get(
                url=url, timeout=self.session_timeout
            ).json()
        except Exception:
            income_statement = {}
        return income_statement

    def get_company_profile(self, ticker):
        url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={self.api_key}"
        try:
            profile = self.session.get(url=url, timeout=self.session_timeout).json()
            if profile and isinstance(profile, list):
                profile = profile[0]
            else:
                profile = {}
        except Exception:
            profile = {}
        return profile
