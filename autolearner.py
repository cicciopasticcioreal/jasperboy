class AutoLearner:
    """Adjust strategies based on past trade performance."""

    def __init__(self, strategy_selector, history, min_trades=5):
        self.strategy_selector = strategy_selector
        self.history = history
        self.min_trades = min_trades
        self.trades_by_coin = {}

    def record_trade(self, coin, success):
        stats = self.trades_by_coin.setdefault(coin, {'wins': 0, 'losses': 0})
        if success:
            stats['wins'] += 1
        else:
            stats['losses'] += 1

    def review(self, strategies):
        """Check each coin and update strategy if performance is poor."""
        for coin, stats in list(self.trades_by_coin.items()):
            total = stats['wins'] + stats['losses']
            if total < self.min_trades:
                continue
            performance = stats['wins'] / total
            if performance < 0.5:
                # Replace strategy for coin
                strategies[coin] = (
                    self.strategy_selector.select_strategies([coin])[coin]
                )
                # Reset stats
                self.trades_by_coin[coin] = {"wins": 0, "losses": 0}
