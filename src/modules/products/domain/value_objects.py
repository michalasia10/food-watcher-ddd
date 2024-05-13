from typing import NewType
from uuid import UUID

ProductID = NewType("ProductID", UUID)
DailyUserProductID = NewType("ProductID", UUID)
DailyUserConsID = NewType("DailyUserConsID", UUID)
