from discount_calculator import DiscountCalculator
from purchase_validator import PurchaseValidator


class PurchaseProcessor:
    """Procesa compras de principio a fin"""

    def __init__(self):
        self.calculator = DiscountCalculator()
        self.validator = PurchaseValidator()
        self.processed_purchases = []

    def process_purchase(self, amount: float, customer_age: int, customer_name: str) -> dict:
        """
        Procesa una compra completa

        1. Valida la compra
        2. Calcula el descuento
        3. Aplica el descuento
        4. Registra la transacción

        Returns:
            dict con detalles de la compra procesada
        """
        # Paso 1: Validar
        validation = self.validator.validate_purchase(amount, customer_age)

        if not validation['valid']:
            return {
                'success': False,
                'message': validation['message'],
                'original_amount': amount,
                'final_amount': 0,
                'discount_percent': 0
            }

        # Paso 2 y 3: Calcular y aplicar descuento
        discount_percent = self.calculator.calculate_discount(amount)
        final_amount = self.calculator.apply_discount(amount, discount_percent)

        # Paso 4: Registrar
        purchase_record = {
            'success': True,
            'message': 'Compra procesada exitosamente',
            'customer_name': customer_name,
            'customer_age': customer_age,
            'original_amount': amount,
            'discount_percent': discount_percent,
            'final_amount': final_amount,
            'savings': round(amount - final_amount, 2)
        }

        self.processed_purchases.append(purchase_record)

        return purchase_record

    def get_total_sales(self) -> float:
        """Retorna el total de ventas procesadas"""
        return sum(p['final_amount'] for p in self.processed_purchases if p['success'])

    def get_purchase_count(self) -> int:
        """Retorna el número de compras exitosas"""
        return len([p for p in self.processed_purchases if p['success']])