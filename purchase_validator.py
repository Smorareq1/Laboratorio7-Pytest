class PurchaseValidator:
    """Valida compras según reglas de negocio"""

    def __init__(self, max_amount: float = 10000):
        self.max_amount = max_amount

    def validate_purchase(self, amount: float, customer_age: int) -> dict:
        """
        Valida una compra

        Reglas:
        - Monto debe ser positivo
        - Monto no puede exceder el máximo permitido
        - Cliente debe ser mayor de edad (18+)

        Returns:
            dict con 'valid' (bool) y 'message' (str)
        """
        if amount <= 0:
            return {
                'valid': False,
                'message': 'El monto debe ser mayor a cero'
            }

        if amount > self.max_amount:
            return {
                'valid': False,
                'message': f'El monto excede el máximo permitido (${self.max_amount})'
            }

        if customer_age < 18:
            return {
                'valid': False,
                'message': 'El cliente debe ser mayor de edad'
            }

        return {
            'valid': True,
            'message': 'Compra válida'
        }