class Asset:
    def __init__(
        self, symbol: str, name: str, target_price: float, current_price: float = 0.0
    ):
        self.name = name
        self.symbol = symbol.upper()
        self.target_price = target_price
        self.current_price = current_price

    def calculate_difference(self):
        if self.target_price == 0:
            return 0
        else:
            return (self.current_price - self.target_price) / self.target_price * 100

    def __str__(self):
        diff = self.calculate_difference()
        return f"[{self.symbol}] {self.name} | Current: ${self.current_price:.2f} | Target: ${self.target_price:.2f} | ({diff:+.2f}%)"

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "target_price": self.target_price,
            "current_price": self.current_price,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["symbol"],
            data["name"],
            data["target_price"],
            data.get("current_price", 0.0),
        )
