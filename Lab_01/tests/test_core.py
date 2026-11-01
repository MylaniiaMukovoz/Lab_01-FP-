"""
test_core.py — Тести для перевірки чистоти функцій та бізнес-логіки.
"""
import pytest
from copy import deepcopy
from core import make_processor, MobileUsage

@pytest.fixture
def sample_data() -> list[MobileUsage]:
    return [
        {"id": 1, "mins": 100, "sms": 10, "mb": 1000, "active": True}
    ]

@pytest.fixture
def processor():
    return make_processor(
        is_active=lambda u: u.get("active", False),
        calc_mins=lambda m: m * 0.5,
        calc_sms=lambda s: s * 1.0,
        calc_mb=lambda mb: mb * 0.1,
        apply_bonus=lambda c: c * 0.9  
    )

def test_no_mutation(sample_data, processor):
    """Перевірка на відсутність мутацій вхідних даних."""
    original = deepcopy(sample_data)
    processor(sample_data)
    
    assert sample_data == original

def test_referential_transparency(sample_data, processor):
    """Перевірка референтної прозорості (однаковий вхід = однаковий вихід)."""
    result1 = processor(sample_data)
    result2 = processor(sample_data)
    
    assert result1 == result2

def test_monthly_cost_calculation(sample_data, processor):
    """Перевірка правильності математичних розрахунків."""
    result = processor(sample_data)
    record = result["records"][0]
    
    assert record["monthly_cost"] == 144.0