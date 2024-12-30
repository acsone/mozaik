# Copyright 2024 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date

from extendable_pydantic import ExtendableModelMeta
from pydantic import BaseModel


class NewsInputFilter(BaseModel, metaclass=ExtendableModelMeta):

    partner_id: int = None
    start_date_at_least: date = None
    end_date_at_most: date = None
