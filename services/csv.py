import csv
from typing import Any
from pydantic import TypeAdapter
from ..models.user import ProductPrice
from ..services.userservices import UserService


class GenerateCSV(UserService):
    async def importCsvProductPrice(self, *, file: Any):
        reader = csv.DictReader(
                    (line.decode() for line in file),
                    delimiter=";",
                )
        itemprice = TypeAdapter(list[ProductPrice]).validate_python(reader)
        return await self.addPrice(itemprice = itemprice)