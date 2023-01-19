from collections import OrderedDict

from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce, TruncMonth, TruncYear


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_per_year(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(year=TruncYear('date'))
        .order_by()
        .values('year')
        .annotate(total=Sum('amount'))
        .values_list('year', 'total')
    ))


def summary_per_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(month=TruncMonth('date'))
        .order_by()
        .values('month')
        .annotate(total=Sum('amount'))
        .values_list('month', 'total')
    ))


def total_amount(queryset):
    return sum([float(i) for i in queryset.values_list('amount', flat=True)])


def number_expenses_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Count('id'))
        .values_list('category_name', 's')
    ))