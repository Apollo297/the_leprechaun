from django.contrib import admin

from capital.models import (
    CapitalType,
    CapitalsTransaction,
    Currency,
    Savings
)

TEXT = 'Детальная информация о накоплениях.'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'symbol')
    list_editable = ('symbol',)
    list_filter = ('title',)


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ('capital_type', 'user')
    search_fields = ('user',)
    list_filter = ('capital_type',)
    list_display_links = ('capital_type',)


@admin.register(CapitalsTransaction)
class CapitalsTransactionAdmin(admin.ModelAdmin):
    list_display = ('capital_type',)
    search_fields = ('user',)
    list_filter = ('capital_type',)
    fieldsets = (
        ('Блок-1', {
            'fields': (
                'type',
                'user',
                'capital_type'
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
                'currency'
            ),
        }),
    )
    empty_value_display = 'Не задано'


@admin.register(CapitalType)
class CapitalTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('currencies',)
