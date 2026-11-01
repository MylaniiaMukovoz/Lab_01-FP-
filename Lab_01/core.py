"""
core.py - Чисте ядро для розрахунку мобільного тарифу (Варіант 11).
Не містить побічних ефектів, глобальних змінних та мутацій вхідних даних.
"""
from typing import Callable, List, TypedDict, Dict

class MobileUsage(TypedDict, total=False):
    """Тип даних для зберігання інформації про абонента."""
    id: int
    mins: int
    sms: int
    mb: int
    active: bool
    monthly_cost: float 

CalcFn = Callable[[int], float]
BonusFn = Callable[[float], float]
FilterFn = Callable[[MobileUsage], bool]

def calculate_base_cost(usage: MobileUsage, calc_mins: CalcFn, calc_sms: CalcFn, calc_mb: CalcFn) -> float:
    """Обчислює базову вартість на основі витрачених ресурсів."""
    return calc_mins(usage["mins"]) + calc_sms(usage["sms"]) + calc_mb(usage["mb"])

def with_monthly_cost(usage: MobileUsage, cost: float) -> MobileUsage:
    """Повертає новий словник із доданим полем monthly_cost (без мутації оригінального)."""
    return {**usage, "monthly_cost": cost}

def make_processor(
    *, 
    is_active: FilterFn, 
    calc_mins: CalcFn, 
    calc_sms: CalcFn, 
    calc_mb: CalcFn, 
    apply_bonus: BonusFn
) -> Callable[[List[MobileUsage]], Dict[str, object]]:
    """
    Функція вищого порядку (фабрика).
    Приймає набір правил (політик) та повертає налаштовану функцію обробки.
    """
    def process(records: List[MobileUsage]) -> Dict[str, object]:
        processed_records: List[MobileUsage] = []
        total_revenue = 0.0

        for rec in records:
            if not is_active(rec):
                continue
            
            base_cost = calculate_base_cost(rec, calc_mins, calc_sms, calc_mb)
            final_cost = apply_bonus(base_cost)
            
            new_rec = with_monthly_cost(rec, final_cost)
            processed_records.append(new_rec)
            total_revenue += final_cost

        return {
            "count": len(processed_records), 
            "revenue": total_revenue, 
            "records": processed_records
        }
    
    return process