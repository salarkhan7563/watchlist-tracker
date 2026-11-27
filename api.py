import requests


def fetch_live_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol.upper()}"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["chart"]["result"][0]["meta"]["regularMarketPrice"])
    except (requests.RequestException, KeyError, IndexError, TypeError) as error:
        print(f"Could not fetch live price for {symbol.upper()}: {error}")
        return None
