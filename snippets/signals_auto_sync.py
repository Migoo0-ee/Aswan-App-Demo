from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.apps import apps
from decimal import Decimal
from .models import Payment, Purchase

@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def update_purchase_data(sender, instance, **kwargs):
    """
    Auto-sync purchase stats on every payment change.
    Handles installment count and completion status automatically.
    """
    purchase = instance.purchase
    actual_count = purchase.payments.exclude(payment_method__icontains="تصفية").count()
    has_settlement = purchase.payments.filter(payment_method__icontains="تصفية").exists()
    total_paid = purchase.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    is_finished = has_settlement or total_paid >= purchase.total_amount

    Purchase.objects.filter(pk=purchase.pk).update(
        paid_installments=actual_count,
        is_finished=is_finished
    )

@receiver(post_delete, sender=Payment)
def payment_post_delete_logic(sender, instance, **kwargs):
    """
    Auto-delete linked treasury record when a payment is deleted.
    Uses unique ID signature to find the exact treasury entry.
    """
    try:
        TreasuryModel = apps.get_model('treasury', 'Treasury')
        unique_signature = f" (ID:{instance.id})"
        TreasuryModel.objects.filter(reason__endswith=unique_signature).delete()
    except Exception:
        pass

@receiver(post_save, sender='clients.Purchase')
def subtract_from_treasury_on_purchase(sender, instance, created, **kwargs):
    """
    Auto-deduct from treasury when a new purchase is created.
    Keeps treasury in sync without manual intervention.
    """
    if created:
        try:
            TreasuryModel = apps.get_model('treasury', 'Treasury')
            full_reason = f"شراء منتج: {instance.product_name} للعميل: {instance.client.client_name} (ID:{instance.id})"
            TreasuryModel.objects.create(
                amount=instance.product_price,
                statement='out',
                withdraw_method=instance.payment_method,
                reason=full_reason,
                auto_reason='purchases'
            )
        except Exception:
            pass
