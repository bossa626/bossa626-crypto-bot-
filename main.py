
from flask import Flask, render_template_string
import threading, time
from data_fetcher import get_top_symbols
from signal_logic import scan_all

app = Flask(__name__)
log_store = []

HTML = """
<html><head><title>Bot Dashboard</title></head>
<body style='background:#121212;color:#fff;font-family:monospace'>
<h2>Crypto Signal Bot</h2>
<ul>
{% for line in logs %}
<li>{{line}}</li>
{% endfor %}
</ul></body></html>
"""

@app.route("/")
def dashboard():
    return render_template_string(HTML, logs=reversed(log_store[-30:]))

def background_worker():
    while True:
        symbols = get_top_symbols()
        results = scan_all(symbols)
        log_store.append(f"[{time.strftime('%H:%M:%S')}] Quét {len(symbols)} coin")
        for r in results:
            log_store.append(r)
        time.sleep(900)

if __name__ == "__main__":
    threading.Thread(target=background_worker).start()
    app.run(host="0.0.0.0", port=5000)
