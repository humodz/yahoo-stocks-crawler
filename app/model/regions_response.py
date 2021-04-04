from typing import List

from pydantic import BaseModel


class RegionsResponse(BaseModel):
    regions: List[str]

    class Config:
        schema_extra = {
            'example': {
                'regions': ['Argentinia', 'Brazil', 'United States', '...']
            }
        }
