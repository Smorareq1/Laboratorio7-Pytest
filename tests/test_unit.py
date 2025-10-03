import pytest
from discount_calculator import DiscountCalculator
from purchase_validator import PurchaseValidator


# PRUEBAS UNITARIAS M1
class TestDiscountCalculator:
    """Pruebas unitarias para el calculador de descuentos"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        self.calculator = DiscountCalculator()

    # Pruebas de calculate_discount
    def test_no_discount_below_100(self):
        """Compras menores a $100 no tienen descuento"""
        assert self.calculator.calculate_discount(50) == 0
        assert self.calculator.calculate_discount(99.99) == 0

    def test_10_percent_discount_100_to_499(self):
        """Compras entre $100-$499 tienen 10% descuento"""
        assert self.calculator.calculate_discount(100) == 10
        assert self.calculator.calculate_discount(250) == 10
        assert self.calculator.calculate_discount(499.99) == 10

    def test_15_percent_discount_500_to_999(self):
        """Compras entre $500-$999 tienen 15% descuento"""
        assert self.calculator.calculate_discount(500) == 15
        assert self.calculator.calculate_discount(750) == 15
        assert self.calculator.calculate_discount(999.99) == 15

    def test_20_percent_discount_1000_or_more(self):
        """Compras de $1000 o más tienen 20% descuento"""
        assert self.calculator.calculate_discount(1000) == 20
        assert self.calculator.calculate_discount(5000) == 20

    def test_negative_amount_raises_error(self):
        """Montos negativos deben lanzar error"""
        with pytest.raises(ValueError, match="no puede ser negativo"):
            self.calculator.calculate_discount(-100)

    # Pruebas de apply_discount
    def test_apply_discount_correct_calculation(self):
        """Verificar cálculo correcto del descuento"""
        # $100 con 10% descuento = $90
        assert self.calculator.apply_discount(100, 10) == 90.0
        # $500 con 15% descuento = $425
        assert self.calculator.apply_discount(500, 15) == 425.0
        # $1000 con 20% descuento = $800
        assert self.calculator.apply_discount(1000, 20) == 800.0

    def test_apply_discount_rounding(self):
        """Verificar redondeo a 2 decimales"""
        result = self.calculator.apply_discount(99.99, 10)
        assert result == 89.99

    def test_apply_discount_zero_percent(self):
        """Aplicar 0% descuento no cambia el monto"""
        assert self.calculator.apply_discount(100, 0) == 100.0

    def test_apply_discount_negative_values_raise_error(self):
        """Valores negativos deben lanzar error"""
        with pytest.raises(ValueError):
            self.calculator.apply_discount(-100, 10)
        with pytest.raises(ValueError):
            self.calculator.apply_discount(100, -10)

# PRUEBAS UNITARIAS M2
class TestPurchaseValidator:
    """Pruebas unitarias para el validador de compras"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        self.validator = PurchaseValidator(max_amount=10000)

    def test_valid_purchase(self):
        """Compra válida debe retornar valid=True"""
        result = self.validator.validate_purchase(500, 25)
        assert result['valid'] is True
        assert result['message'] == 'Compra válida'

    def test_zero_amount_invalid(self):
        """Monto cero es inválido"""
        result = self.validator.validate_purchase(0, 25)
        assert result['valid'] is False
        assert 'mayor a cero' in result['message']

    def test_negative_amount_invalid(self):
        """Monto negativo es inválido"""
        result = self.validator.validate_purchase(-50, 25)
        assert result['valid'] is False
        assert 'mayor a cero' in result['message']

    def test_exceeds_max_amount(self):
        """Monto que excede el máximo es inválido"""
        result = self.validator.validate_purchase(15000, 25)
        assert result['valid'] is False
        assert 'excede el máximo' in result['message']

    def test_underage_customer(self):
        """Cliente menor de edad no puede comprar"""
        result = self.validator.validate_purchase(500, 17)
        assert result['valid'] is False
        assert 'mayor de edad' in result['message']

    def test_exactly_18_years_old(self):
        """Cliente de exactamente 18 años puede comprar"""
        result = self.validator.validate_purchase(500, 18)
        assert result['valid'] is True

    def test_custom_max_amount(self):
        """Validador con límite personalizado"""
        validator = PurchaseValidator(max_amount=5000)
        result = validator.validate_purchase(6000, 25)
        assert result['valid'] is False
        assert '5000' in result['message']


# TESTS PARAMETRIZADOS
class TestParametrizedDiscounts:
    @pytest.mark.parametrize("amount,expected_discount", [
        (0, 0),
        (50, 0),
        (99.99, 0),
        (100, 10),
        (250, 10),
        (499.99, 10),
        (500, 15),
        (750, 15),
        (999.99, 15),
        (1000, 20),
        (5000, 20),
    ])
    def test_discount_percentages(self, amount, expected_discount):
        """Probar múltiples montos y sus descuentos esperados"""
        calculator = DiscountCalculator()
        assert calculator.calculate_discount(amount) == expected_discount

# FIXTURES DE PYTEST
@pytest.fixture
def calculator():
    """Fixture para reutilizar calculator en tests"""
    return DiscountCalculator()
@pytest.fixture
def validator():
    """Fixture para reutilizar validator en tests"""
    return PurchaseValidator()