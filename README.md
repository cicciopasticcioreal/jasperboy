# JasperBoy Trading Bot

This repository contains a simple trading bot prototype implemented in Python.
The bot runs in a background thread while a Flask server is active. A
`SimulationEnvironment` is provided for backtesting and development.

## Features

- Flask web server that can run alongside the trading loop
- Trader executes in a separate thread with graceful shutdown
- Simple simulated market environment for backtesting
- Unit tests to verify basic functionality

## Requirements

- Python 3.8+
- Flask

Install dependencies with:

```bash
pip install -r requirements.txt  # or simply `pip install flask`
```

## Running Locally

```bash
python main.py
```
Use `Ctrl+C` to stop the application. The trader thread will terminate
cleanly when the server is stopped.

## Running in Google Colab

1. Create a new Colab notebook.
2. Upload the repository files or clone the repo with:
   ```python
   !git clone <repository-url>
   %cd jasperboy
   ```
3. Install dependencies:
   ```python
   !pip install flask
   ```
4. Start the bot in a background cell:
   ```python
   import threading, time
   from trader import Trader
   from main import app, stop_event

   t = threading.Thread(target=Trader(stop_event).run, daemon=True)
   t.start()
   app.run(host="0.0.0.0", port=5000)
   ```
   When you stop the cell, the thread will shut down gracefully.

## Running Tests

Run the unit tests with:

```bash
python -m unittest discover tests
```

## Backtesting

The `Backtester` class in `simulation.py` can execute the trader against the
`SimulationEnvironment` for a number of steps:

```python
from trader import Trader
from simulation import SimulationEnvironment, Backtester
import threading

stop_event = threading.Event()
trader = Trader(stop_event, SimulationEnvironment())
backtester = Backtester(trader.env)
results = backtester.run(trader)
print(results)
```

This will produce a sequence of simulated prices processed by the trader.
