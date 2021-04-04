from typing import Dict, Optional

from pydantic import BaseModel

from app.utils import parse_amount


class StockItem(BaseModel):
    symbol: str
    name: str
    price: Optional[str]

    @classmethod
    def from_table_row(cls, data):
        return cls(
            symbol=data['Symbol'],
            name=data['Name'],
            price='{:.2f}'.format(parse_amount(data['Price (Intraday)'])),
        )

    class Config:
        schema_extra = {
            'example':  {
                'symbol': 'NOKA.BA',
                'name': 'Nokia Corporation',
                'price': '557.50',
            }
        }


StocksResponse = Dict[str, StockItem]
