import threading
from flask import Flask, jsonify, render_template_string

from trader import Trader

app = Flask(__name__)


@app.route("/status")
def status() -> str:
    """Return basic trader status."""
    data = {
        "running": not stop_event.is_set(),
        "coins": trader.coins,
        "performance": trader.history.performance(),
    }
    return jsonify(data)


@app.route("/dashboard")
def dashboard() -> str:
    """Simple HTML dashboard with trade history."""
    table = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            t["coin"], t["side"], t["price"]
        )
        for t in trader.history.trades
    )
    html = f"""
    <html>
    <body>
    <h1>Trader Dashboard</h1>
    <p>Running: {not stop_event.is_set()}</p>
    <p>Coins: {', '.join(trader.coins)}</p>
    <p>Performance: {trader.history.performance():.2f}</p>
    <table border='1'>
    <tr><th>Coin</th><th>Side</th><th>Price</th></tr>
    {table}
    </table>
    </body>
    </html>
    """
    return render_template_string(html)


stop_event = threading.Event()
trader = Trader(stop_event)
trader_thread = threading.Thread(target=trader.run, daemon=True)

if __name__ == "__main__":
    trader_thread.start()
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        stop_event.set()
        trader_thread.join()
