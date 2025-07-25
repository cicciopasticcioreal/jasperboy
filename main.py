import threading
from flask import Flask
from trader import Trader

app = Flask(__name__)

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
