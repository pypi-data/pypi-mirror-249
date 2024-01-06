class Position:
    def __init__(self, id: int, **kwargs) -> None:
        self.symbol = kwargs.get("symbol", None)
        self.quantity = kwargs.get("quantity", None)
        self.cost_basis = kwargs.get("cost_basis", None)
        self.date_acquired = kwargs.get("date_acquired", None)
