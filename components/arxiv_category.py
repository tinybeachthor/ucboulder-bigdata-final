from enum import StrEnum

class Category(StrEnum):
    CS_AI = "cs.AI"
    # ...
    CS_MO = "cs.MO"
    # ...
    CS_RO = "cs.RO"

    def __str__(self):
        return f'{self.value}'
