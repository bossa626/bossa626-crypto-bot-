
from data_fetcher import get_binance_data
from alert_sender import send_alert
import time

def calculate_rsi(prices):
    gains, losses = [], []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i - 1]
        gains.append(max(0, delta))
        losses.append(max(0, -delta))
    avg_gain = sum(gains) / len(gains) if gains else 1
    avg_loss = sum(losses) / len(losses) if losses else 1
    rs = avg_gain / avg_loss if avg_loss != 0 else 100
    return 100 - (100 / (1 + rs))

def volume_signal(symbol):
    data = get_binance_data(symbol, "1d", 10)
    if not data or len(data) < 2:
        return None

    close_prices = [float(c[4]) for c in data]
    volumes = [float(c[5]) for c in data]
    rsi = calculate_rsi(close_prices)
    avg_vol = sum(volumes[:-1]) / (len(volumes) - 1)
    last_vol = volumes[-1]
    macd_cross = close_prices[-2] < close_prices[-1]
    if 35 < rsi < 50 and last_vol > avg_vol * 1.3 and macd_cross:
        return f"#VOLUME_SIGNAL {symbol}\nRSI: {round(rsi,2)} | Volume: +{round((last_vol/avg_vol - 1)*100, 1)}% | MACD: CROSS↑"
    return None

def breakout_signal(symbol):
    data = get_binance_data(symbol, "1d", 20)
    if not data:
        return None
    highs = [float(c[2]) for c in data[:-1]]
    last_close = float(data[-1][4])
    resistance = max(highs[-5:])
    if last_close > resistance:
        return f"#BREAKOUT_ALERT {symbol}\nPrice: {last_close} just broke resistance: {round(resistance,2)}"
    return None

def scan_all(symbols):
    alerts = []
    for sym in symbols:
        vs = volume_signal(sym)
        if vs:
            send_alert(vs)
            alerts.append(vs)
        bs = breakout_signal(sym)
        if bs:
            send_alert(bs)
            alerts.append(bs)
        time.sleep(1)
    return alerts
