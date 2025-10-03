import pytest
from discount_calculator import DiscountCalculator
from purchase_validator import PurchaseValidator


# PRUEBAS DE INTEGRACIÓN - Calculator + Validator
class TestCalculatorValidatorIntegration:
    """Pruebas de integración entre Calculator y Validator"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        self.calculator = DiscountCalculator()
        self.validator = PurchaseValidator()

    def test_valid_purchase_with_discount(self):
        """Flujo: validar compra válida y calcular su descuento"""
        amount = 600
        age = 30

        # Paso 1: Validar
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is True

        # Paso 2: Calcular descuento
        discount = self.calculator.calculate_discount(amount)
        assert discount == 15

        # Paso 3: Aplicar descuento
        final = self.calculator.apply_discount(amount, discount)
        assert final == 510.0

    def test_invalid_purchase_no_discount_applied(self):
        """Flujo: compra inválida no debe proceder a calcular descuento"""
        amount = 500
        age = 16  # Menor de edad

        # Paso 1: Validar
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is False
        assert 'mayor de edad' in validation['message']

        # En un flujo real, no deberíamos continuar al cálculo
        # si la validación falla

    def test_edge_case_exact_boundary(self):
        """Flujo: probar límites exactos de descuentos"""
        # Exactamente $500 debe dar 15% descuento
        amount = 500
        age = 25

        # Validar
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is True

        # Calcular
        discount = self.calculator.calculate_discount(amount)
        assert discount == 15

        # Aplicar
        final = self.calculator.apply_discount(amount, discount)
        assert final == 425.0

    def test_multiple_validations_and_calculations(self):
        """Flujo: procesar varios casos seguidos"""
        test_cases = [
            {'amount': 100, 'age': 25, 'expected_discount': 10, 'expected_final': 90.0},
            {'amount': 500, 'age': 30, 'expected_discount': 15, 'expected_final': 425.0},
            {'amount': 1000, 'age': 40, 'expected_discount': 20, 'expected_final': 800.0},
        ]

        for case in test_cases:
            # Validar
            validation = self.validator.validate_purchase(case['amount'], case['age'])
            assert validation['valid'] is True

            # Calcular
            discount = self.calculator.calculate_discount(case['amount'])
            assert discount == case['expected_discount']

            # Aplicar
            final = self.calculator.apply_discount(case['amount'], discount)
            assert final == case['expected_final']

    def test_maximum_amount_boundary(self):
        """Flujo: probar límite máximo de compra"""
        amount = 10000  # Exactamente el límite
        age = 35

        # Validar (debe pasar)
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is True

        # Calcular (debe tener 20% descuento)
        discount = self.calculator.calculate_discount(amount)
        assert discount == 20

        # Aplicar
        final = self.calculator.apply_discount(amount, discount)
        assert final == 8000.0

    def test_exceeds_maximum_amount(self):
        """Flujo: compra que excede el límite no debe calcular descuento"""
        amount = 10001  # Excede por 1
        age = 35

        # Validar (debe fallar)
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is False
        assert 'excede el máximo' in validation['message']

    def test_minimum_discount_threshold(self):
        """Flujo: compra justo en el umbral mínimo de descuento"""
        amount = 100  # Exactamente $100 (10% descuento)
        age = 18  # Exactamente 18 años

        # Validar
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is True

        # Calcular
        discount = self.calculator.calculate_discount(amount)
        assert discount == 10

        # Aplicar
        final = self.calculator.apply_discount(amount, discount)
        assert final == 90.0

    def test_just_below_discount_threshold(self):
        """Flujo: compra justo debajo del umbral (sin descuento)"""
        amount = 99.99  # Justo debajo de $100
        age = 25

        # Validar
        validation = self.validator.validate_purchase(amount, age)
        assert validation['valid'] is True

        # Calcular (sin descuento)
        discount = self.calculator.calculate_discount(amount)
        assert discount == 0

        # Aplicar (precio sin cambios)
        final = self.calculator.apply_discount(amount, discount)
        assert final == 99.99

# FIXTURES DE PYTEST
@pytest.fixture
def calculator():
    """Fixture para reutilizar calculator"""
    return DiscountCalculator()
@pytest.fixture
def validator():
    """Fixture para reutilizar validator"""
    return PurchaseValidator()