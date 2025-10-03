import pytest
from purchase_processor import PurchaseProcessor

# PRUEBAS DEL FLUJO COMPLETO - Los 3 módulos trabajando juntos
class TestPurchaseProcessorFullFlow:
    """Pruebas del flujo completo usando los 3 módulos"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        self.processor = PurchaseProcessor()

    def test_successful_purchase_flow(self):
        """Flujo completo exitoso: validar -> calcular -> aplicar -> registrar"""
        result = self.processor.process_purchase(
            amount=750,
            customer_age=30,
            customer_name="Juan Pérez"
        )

        # Verificar resultado completo
        assert result['success'] is True
        assert result['customer_name'] == "Juan Pérez"
        assert result['customer_age'] == 30
        assert result['original_amount'] == 750
        assert result['discount_percent'] == 15
        assert result['final_amount'] == 637.5
        assert result['savings'] == 112.5
        assert 'procesada exitosamente' in result['message']

        # Verificar que se registró en el sistema
        assert self.processor.get_purchase_count() == 1
        assert self.processor.get_total_sales() == 637.5

    def test_failed_purchase_underage(self):
        """Flujo completo: compra rechazada por menor de edad"""
        result = self.processor.process_purchase(
            amount=500,
            customer_age=17,
            customer_name="María García"
        )

        # Verificar rechazo
        assert result['success'] is False
        assert 'mayor de edad' in result['message']
        assert result['final_amount'] == 0
        assert result['discount_percent'] == 0

        # No debe registrarse como compra exitosa
        assert self.processor.get_purchase_count() == 0
        assert self.processor.get_total_sales() == 0

    def test_failed_purchase_exceeds_limit(self):
        """Flujo completo: compra rechazada por exceder límite"""
        result = self.processor.process_purchase(
            amount=15000,
            customer_age=25,
            customer_name="Carlos López"
        )

        # Verificar rechazo
        assert result['success'] is False
        assert 'excede el máximo' in result['message']

        # No debe contabilizarse
        assert self.processor.get_purchase_count() == 0

    def test_failed_purchase_zero_amount(self):
        """Flujo completo: compra rechazada por monto cero"""
        result = self.processor.process_purchase(
            amount=0,
            customer_age=25,
            customer_name="Pedro Ramírez"
        )

        # Verificar rechazo
        assert result['success'] is False
        assert 'mayor a cero' in result['message']

    def test_multiple_purchases_tracking(self):
        """Flujo completo: procesar múltiples compras y rastrearlas"""
        # Compra 1: exitosa ($100 con 10% = $90)
        result1 = self.processor.process_purchase(100, 25, "Cliente 1")
        assert result1['success'] is True
        assert result1['final_amount'] == 90.0

        # Compra 2: exitosa ($500 con 15% = $425)
        result2 = self.processor.process_purchase(500, 30, "Cliente 2")
        assert result2['success'] is True
        assert result2['final_amount'] == 425.0

        # Compra 3: rechazada (menor de edad)
        result3 = self.processor.process_purchase(50, 16, "Cliente 3")
        assert result3['success'] is False

        # Compra 4: exitosa ($1000 con 20% = $800)
        result4 = self.processor.process_purchase(1000, 40, "Cliente 4")
        assert result4['success'] is True
        assert result4['final_amount'] == 800.0

        # Verificar totales
        assert self.processor.get_purchase_count() == 3  # Solo exitosas

        # Total: $90 + $425 + $800 = $1315
        expected_total = 90.0 + 425.0 + 800.0
        assert self.processor.get_total_sales() == expected_total

    def test_no_discount_purchase_flow(self):
        """Flujo completo: compra sin descuento"""
        result = self.processor.process_purchase(
            amount=50,
            customer_age=25,
            customer_name="Ana Martínez"
        )

        # Sin descuento
        assert result['success'] is True
        assert result['discount_percent'] == 0
        assert result['final_amount'] == 50.0
        assert result['savings'] == 0

    def test_maximum_discount_flow(self):
        """Flujo completo: compra con máximo descuento (20%)"""
        result = self.processor.process_purchase(
            amount=5000,
            customer_age=35,
            customer_name="Roberto Silva"
        )

        # Máximo descuento
        assert result['success'] is True
        assert result['discount_percent'] == 20
        assert result['final_amount'] == 4000.0
        assert result['savings'] == 1000.0

    def test_edge_case_minimum_age_maximum_amount(self):
        """Flujo completo: cliente de 18 años con compra en el límite"""
        result = self.processor.process_purchase(
            amount=10000,
            customer_age=18,
            customer_name="Joven Comprador"
        )

        # Debe ser válida
        assert result['success'] is True
        assert result['discount_percent'] == 20
        assert result['final_amount'] == 8000.0

    def test_purchase_history_persistence(self):
        """Flujo completo: verificar que el historial se mantiene"""
        # Realizar 3 compras
        self.processor.process_purchase(100, 25, "Cliente A")
        self.processor.process_purchase(500, 30, "Cliente B")
        self.processor.process_purchase(1000, 35, "Cliente C")

        # Verificar que todas están registradas
        assert len(self.processor.processed_purchases) == 3

        # Verificar datos de cada compra en el historial
        assert self.processor.processed_purchases[0]['customer_name'] == "Cliente A"
        assert self.processor.processed_purchases[1]['customer_name'] == "Cliente B"
        assert self.processor.processed_purchases[2]['customer_name'] == "Cliente C"

    def test_mixed_successful_and_failed_purchases(self):
        """Flujo completo: mezcla de compras exitosas y fallidas"""
        # Exitosa
        self.processor.process_purchase(200, 25, "Cliente 1")
        # Fallida (menor de edad)
        self.processor.process_purchase(200, 15, "Cliente 2")
        # Exitosa
        self.processor.process_purchase(600, 30, "Cliente 3")
        # Fallida (excede límite)
        self.processor.process_purchase(20000, 40, "Cliente 4")
        # Exitosa
        self.processor.process_purchase(1500, 28, "Cliente 5")

        # Solo 3 compras exitosas
        assert self.processor.get_purchase_count() == 3

        # Calcular total esperado
        # 200 con 10% = 180
        # 600 con 15% = 510
        # 1500 con 20% = 1200
        expected_total = 180.0 + 510.0 + 1200.0
        assert self.processor.get_total_sales() == expected_total

# TESTS DE ESCENARIOS REALES
class TestRealWorldScenarios:
    """Pruebas con escenarios del mundo real"""

    def setup_method(self):
        self.processor = PurchaseProcessor()

    def test_busy_day_simulation(self):
        """Simular un día ocupado con muchas compras"""
        purchases = [
            (150, 22, "Cliente Mañana 1"),
            (75, 19, "Cliente Mañana 2"),
            (800, 45, "Cliente Tarde 1"),
            (2000, 50, "Cliente Tarde 2"),
            (50, 17, "Cliente Menor"),  # Rechazada
            (450, 28, "Cliente Noche 1"),
            (12000, 35, "Cliente Rico"),  # Rechazada (excede límite)
        ]

        successful_count = 0
        for amount, age, name in purchases:
            result = self.processor.process_purchase(amount, age, name)
            if result['success']:
                successful_count += 1

        # 5 compras exitosas de 7 intentos
        assert successful_count == 5
        assert self.processor.get_purchase_count() == 5

    def test_customer_trying_multiple_times(self):
        """Cliente que intenta comprar varias veces"""
        customer = "José Rodríguez"

        # Primer intento: muy poco dinero
        result1 = self.processor.process_purchase(25, 30, customer)
        assert result1['success'] is True
        assert result1['discount_percent'] == 0

        # Segundo intento: alcanza descuento
        result2 = self.processor.process_purchase(550, 30, customer)
        assert result2['success'] is True
        assert result2['discount_percent'] == 15

        # Tercer intento: máximo descuento
        result3 = self.processor.process_purchase(1500, 30, customer)
        assert result3['success'] is True
        assert result3['discount_percent'] == 20

        # Total de compras del cliente
        assert self.processor.get_purchase_count() == 3

# FIXTURES DE PYTEST
@pytest.fixture
def processor():
    """Fixture para reutilizar processor"""
    return PurchaseProcessor()