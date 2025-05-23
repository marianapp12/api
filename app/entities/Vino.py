from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Vino(BaseModel):
    wine_name: str = Field(..., min_length=3, max_length=100, example="Chateau Margaux")
    vintage_date: datetime = Field(..., example=datetime(2015, 9, 15))
    country: str = Field(..., min_length=2, max_length=50, example="France")
    description: Optional[str] = Field(
        None,
        example="Chateau Margaux is a famous French winery producing exceptional red wines."
    )


class VinoInDB(Vino):
    id: Optional[str] = Field(alias="_id")
