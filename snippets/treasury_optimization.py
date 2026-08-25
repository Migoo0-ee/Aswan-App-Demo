from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from .models import Treasury

def get_treasury_stats():
    """
    Optimized treasury aggregation using a single DB query.
    Replaces N+1 pattern (fetching all records then looping in Python).
    Uses Coalesce to handle null values safely.
    """
    stats = Treasury.objects.aggregate(
        t_in=Coalesce(Sum('amount', filter=Q(statement='in')), Value(0), output_field=DecimalField()),
        t_out=Coalesce(Sum('amount', filter=Q(statement='out')), Value(0), output_field=DecimalField()),

        v_in=Coalesce(Sum('amount', filter=Q(withdraw_method='vodafon cash', statement='in')), Value(0), output_field=DecimalField()),
        v_out=Coalesce(Sum('amount', filter=Q(withdraw_method='vodafon cash', statement='out')), Value(0), output_field=DecimalField()),

        i_in=Coalesce(Sum('amount', filter=Q(withdraw_method='insta pay', statement='in')), Value(0), output_field=DecimalField()),
        i_out=Coalesce(Sum('amount', filter=Q(withdraw_method='insta pay', statement='out')), Value(0), output_field=DecimalField()),

        c_in=Coalesce(Sum('amount', filter=Q(withdraw_method='cash', statement='in')), Value(0), output_field=DecimalField()),
        c_out=Coalesce(Sum('amount', filter=Q(withdraw_method='cash', statement='out')), Value(0), output_field=DecimalField()),
    )

    return {
        "total_balance": int(stats['t_in'] - stats['t_out']),
        "vodafone_balance": int(stats['v_in'] - stats['v_out']),
        "instapay_balance": int(stats['i_in'] - stats['i_out']),
        "cash_balance": int(stats['c_in'] - stats['c_out']),
    }
