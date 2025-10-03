class DiscountCalculator:
    """Calcula descuentos según reglas de negocio"""

    def calculate_discount(self, amount: float) -> float:
        """
        Calcula el porcentaje de descuento según el monto

        Reglas:
        - Menos de $100: 0% descuento
        - $100 - $499: 10% descuento
        - $500 - $999: 15% descuento
        - $1000 o más: 20% descuento
        """
        if amount < 0:
            raise ValueError("El monto no puede ser negativo")

        if amount < 100:
            return 0
        elif amount < 500:
            return 10
        elif amount < 1000:
            return 15
        else:
            return 20

    def apply_discount(self, amount: float, discount_percent: float) -> float:
        """Aplica el descuento al monto y retorna el precio final"""
        if amount < 0 or discount_percent < 0:
            raise ValueError("Los valores no pueden ser negativos")

        discount_amount = amount * (discount_percent / 100)
        final_amount = amount - discount_amount
        return round(final_amount, 2)