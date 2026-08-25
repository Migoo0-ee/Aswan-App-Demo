from django.db.models import Sum, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from rest_framework.decorators import api_view
from rest_framework.response import Response
from clients.models import Purchase
from treasury.models import Treasury


@api_view(['GET'])
def report(request):
    """
    Comprehensive financial report API.
    Aggregates profits, balances, salaries, commissions, and remaining amounts
    in minimal DB queries using Django ORM aggregations.
    """
    all_profits = Purchase.objects.all()

    total_net_profit = sum(t.interest_amount for t in all_profits)
    total_clients_amount = sum(t.total_amount for t in all_profits)
    total_paid = sum(t.total_collected for t in all_profits)
    total_remaining = sum(t.remaining_amount for t in all_profits)

    withdraws = Treasury.objects.aggregate(
        total_commisions_in=Coalesce(Sum('amount', filter=Q(auto_reason='comissions', statement='in')), Value(0), output_field=DecimalField()),
        total_commisions_out=Coalesce(Sum('amount', filter=Q(auto_reason='comissions', statement='out')), Value(0), output_field=DecimalField()),

        total_salaries_in=Coalesce(Sum('amount', filter=Q(auto_reason='salaries', statement='in')), Value(0), output_field=DecimalField()),
        total_salaries_out=Coalesce(Sum('amount', filter=Q(auto_reason='salaries', statement='out')), Value(0), output_field=DecimalField()),

        total_personal_in=Coalesce(Sum('amount', filter=Q(auto_reason='personal', statement='in')), Value(0), output_field=DecimalField()),
        total_personal_out=Coalesce(Sum('amount', filter=Q(auto_reason='personal', statement='out')), Value(0), output_field=DecimalField()),

        t_out=Coalesce(Sum('amount', filter=Q(statement='out')), Value(0), output_field=DecimalField()),
    )

    treasury_totals = Treasury.objects.aggregate(
        t_in=Coalesce(Sum('amount', filter=Q(statement='in')), Value(0), output_field=DecimalField()),
        t_out=Coalesce(Sum('amount', filter=Q(statement='out')), Value(0), output_field=DecimalField()),
    )

    return Response({
        "status": "success",
        "data": {
            "total_net_profits": total_net_profit,
            "total_balance": treasury_totals['t_in'] - treasury_totals['t_out'],
            "total_amounts": total_clients_amount,
            "total_paid": total_paid,
            "total_remaining": total_remaining,
            "withdraws": {
                "total_commisions": withdraws['total_commisions_in'] - withdraws['total_commisions_out'],
                "total_salaries": withdraws['total_salaries_in'] - withdraws['total_salaries_out'],
                "total_personal": withdraws['total_personal_in'] - withdraws['total_personal_out'],
                "total_out_all": withdraws['t_out'],
            }
        }
    })
