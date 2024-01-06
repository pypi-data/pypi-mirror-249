from typing import List, Optional

from asynctradier.common import Duration, OptionOrderSide, OrderClass, OrderType
from asynctradier.common.order import Order
from asynctradier.common.position import Position
from asynctradier.exceptions import (
    InvalidExiprationDate,
    InvalidOptionType,
    InvalidParameter,
    InvalidStrikeType,
    MissingRequiredParameter,
)
from asynctradier.utils.common import (
    build_option_symbol,
    is_valid_expiration_date,
    is_valid_option_type,
)

from .utils.webutils import WebUtil


class TradierClient:
    def __init__(self, account_id: str, token: str, sandbox: bool = False) -> None:
        self.account_id = account_id
        self.token = token
        base_url = (
            "https://api.tradier.com" if not sandbox else "https://sandbox.tradier.com"
        )
        self.session = WebUtil(base_url, token)

    async def get_positions(self) -> List[Position]:
        url = f"/v1/accounts/{self.account_id}/positions"
        response = await self.session.get(url)
        if response["positions"] == "null":
            positions = []
        else:
            positions = response["positions"]["position"]
        if not isinstance(positions, list):
            positions = [positions]
        for position in positions:
            yield Position(
                **position,
            )

    async def get_order(self, order_id: str) -> Order:
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        params = {"includeTags": "true"}
        response = await self.session.get(url, params=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def buy_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        return await self._option_operation(
            OptionOrderSide.buy_to_open,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def sell_option(
        self,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        return await self._option_operation(
            OptionOrderSide.sell_to_close,
            symbol,
            expiration_date,
            strike,
            option_type,
            quantity,
            order_type,
            order_duration,
            tag,
            price,
            stop,
        )

    async def _option_operation(
        self,
        side: OptionOrderSide,
        symbol: str,
        expiration_date: str,
        strike: float | int,
        option_type: str,
        quantity: int,
        order_type: OrderType = OrderType.market,
        order_duration: Duration = Duration.day,
        tag: Optional[str] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> Order:
        if not is_valid_expiration_date(expiration_date):
            raise InvalidExiprationDate(expiration_date)

        if not is_valid_option_type(option_type):
            raise InvalidOptionType(option_type)

        if not isinstance(strike, float) and not isinstance(strike, int):
            raise InvalidStrikeType(strike)

        if order_type == OrderType.limit and price is None:
            raise MissingRequiredParameter("Price must be specified for limit orders")

        if order_type == OrderType.stop and stop is None:
            raise MissingRequiredParameter("Stop must be specified for stop orders")

        url = f"/v1/accounts/{self.account_id}/orders"
        params = {
            "class": OrderClass.option.value,
            "symbol": symbol,
            "option_symbol": build_option_symbol(
                symbol, expiration_date, strike, option_type
            ),
            "side": side.value,
            "quantity": str(quantity),
            "type": order_type.value,
            "duration": order_duration.value,
            "price": price if price is not None else "",
            "stop": stop if stop is not None else "",
            "tag": tag,
        }
        response = await self.session.post(url, data=params)
        order = response["order"]
        return Order(
            **order,
        )

    async def cancel_order(self, order_id: str | int) -> None:
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        response = await self.session.delete(url)
        order = response["order"]
        return Order(
            **order,
        )

    async def get_orders(self, page: int = 1) -> List[Order]:
        res = []
        page = 1
        while True:
            orders = [order async for order in self._get_orders(page)]
            res += orders
            page += 1
            if len(orders) <= 0:
                break
        return res

    async def _get_orders(self, page: int) -> List[Order]:
        url = f"/v1/accounts/{self.account_id}/orders"
        params = {
            "page": page,
            "includeTags": "true",
        }
        response = await self.session.get(url, params=params)
        if response["orders"] == "null":
            orders = []
        else:
            orders = response["orders"]["order"]

        if not isinstance(orders, list):
            orders = [orders]
        for order in orders:
            yield Order(
                **order,
            )

    async def modify_order(
        self,
        order_id: str | int,
        order_type: Optional[OrderType] = None,
        order_duration: Optional[Duration] = None,
        price: Optional[float] = None,
        stop: Optional[float] = None,
    ) -> None:
        url = f"/v1/accounts/{self.account_id}/orders/{order_id}"
        param = {}
        if order_type is not None:
            param["type"] = order_type.value
        if order_duration is not None:
            param["duration"] = order_duration.value
        if price is not None:
            param["price"] = price
        if stop is not None:
            param["stop"] = stop

        if len(param) == 0:
            raise InvalidParameter("No parameters to modify")
        response = await self.session.put(url)
        order = response["order"]
        return Order(
            **order,
        )
