"""
app.py — Оболонка побічних ефектів (I/O).
Відповідає за вивід на екран, конфігурацію політик та роботу з даними.
"""
from core import make_processor, MobileUsage

def run() -> None:
    users_data: list[MobileUsage] = [
        {"id": 1, "mins": 100, "sms": 20, "mb": 1024, "active": True},
        {"id": 2, "mins": 50, "sms": 0, "mb": 500, "active": True},
        {"id": 3, "mins": 200, "sms": 50, "mb": 2048, "active": False}, 
    ]

    calc_mins = lambda m: m * 0.50
    calc_sms = lambda s: s * 1.00
    calc_mb = lambda mb: mb * 0.05
    
    apply_bonus = lambda cost: cost * 0.90 if cost > 100 else cost
    is_active = lambda user: user.get("active", False)

    processor = make_processor(
        is_active=is_active,
        calc_mins=calc_mins,
        calc_sms=calc_sms,
        calc_mb=calc_mb,
        apply_bonus=apply_bonus
    )

    result = processor(users_data)

    print(" Звіт по мобільним тарифам ")
    print(f"Оброблено активних абонентів: {result['count']}")
    print(f"Загальний дохід компанії: {result['revenue']:.2f} грн\n")
    
    print("Деталі:")
    for user in result["records"]: 
        print(f"Абонент ID: {user['id']} | До сплати: {user['monthly_cost']:.2f} грн")