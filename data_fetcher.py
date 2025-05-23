
import requests

def get_binance_data(symbol, interval="1d", limit=100):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def get_top_symbols(limit=20):
    url = "https://api.binance.com/api/v3/ticker/24hr"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers).json()
    filtered = [x for x in response if "USDT" in x["symbol"] and all(k not in x["symbol"] for k in ["UP", "DOWN", "BULL", "BEAR"])]
    sorted_data = sorted(filtered, key=lambda x: float(x["quoteVolume"]), reverse=True)
    return [x["symbol"] for x in sorted_data[:limit]]
