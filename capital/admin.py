from django.contrib import admin

from capital.models import (
    CapitalsTransaction,
    Currency,
    Savings,
)

TEXT = 'Детальная информация о накоплениях.'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'symbol',
    )
    list_editable = ('symbol',)
    list_filter = ('title',)


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = (
        'capital_type',
        'user',
        'currency',
    )
    list_editable = ('currency',)
    search_fields = ('user',)
    list_filter = (
        'currency',
        'capital_type',
    )
    list_display_links = ('capital_type',)


@admin.register(CapitalsTransaction)
class CapitalsTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'savings',
        'currency',
        'created_at'
    )
    list_editable = (
        'savings',
        'currency'
    )
    search_fields = ('user',)
    list_filter = ('savings',)
    fieldsets = (
        ('Блок-1', {
            'fields': (
                'type',
                'user',
                'savings',
            ),
            'description': '%s' % TEXT,
        }),
        ('Доп. информация', {
            'classes': (
                'wide',
                'extrapretty'
            ),
            'fields': (
                'description',
                'amount',
                'currency',
            ),
        }),
    )
    empty_value_display = 'Не задано'
