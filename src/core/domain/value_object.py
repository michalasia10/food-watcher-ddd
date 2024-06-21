from decimal import Decimal, ROUND_HALF_UP


class PrecisedFloat(float):
    def __new__(cls, value):
        value = Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return super().__new__(cls, float(value))

    def __iadd__(self, other):
        if isinstance(other, PrecisedFloat):
            result = Decimal(self) + Decimal(other)
        else:
            result = Decimal(self) + Decimal(str(other))

        result = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return PrecisedFloat(float(result))

    def __isub__(self, other):
        if isinstance(other, PrecisedFloat):
            result = Decimal(self) - Decimal(other)
        else:
            result = Decimal(self) - Decimal(str(other))

        result = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return PrecisedFloat(float(result))

    def __itruediv__(self, other):
        if isinstance(other, PrecisedFloat):
            result = Decimal(self) / Decimal(other)
        else:
            result = Decimal(self) / Decimal(str(other))

        result = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return PrecisedFloat(float(result))

    def __mul__(self, other):
        if isinstance(other, PrecisedFloat):
            result = Decimal(self) * Decimal(other)
        else:
            result = Decimal(self) * Decimal(str(other))

        result = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return PrecisedFloat(float(result))

    def __repr__(self):
        return f"{self:.2f}"
