from flask import Flask, jsonify
from .trader import Trader

app = Flask(__name__)
trader = Trader()

@app.route('/')
def index():
    return jsonify({
        'positions': [p.__dict__ for p in trader.positions]
    })

if __name__ == '__main__':
    trader.run()
    app.run(debug=True)
