# Sistema de Descuentos - Pruebas con Pytest

Sistema de gestión de descuentos con pruebas unitarias, de integración y end-to-end.

## 🚀 Instalación

```bash
pip install pytest pytest-cov
```

## ▶️ Ejecutar las Pruebas

```bash
# Desde la carpeta raíz del proyecto
pytest tests/ -v
```

## 📊 Ejecutar con Cobertura

```bash
pytest tests/ --cov --cov-report=html
```

## 📁 Estructura

```
proyecto/
├── discount_calculator.py
├── purchase_validator.py
├── purchase_processor.py
└── tests/
    ├── conftest.py
    ├── test_unit.py
    ├── test_integration.py
    └── test_e2e.py
```