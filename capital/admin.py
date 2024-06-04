from django.contrib import admin

from capital.models import (
    Capital,
    CapitalType,
    CapitalsTransaction,
    Currency,
)

TEXT = 'Детальная информация о накоплениях.'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'symbol')
    list_editable = ('symbol',)
    list_filter = ('title',)


@admin.register(Capital)
class CapitalAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)


@admin.register(CapitalsTransaction)
class CapitalsTransactionAdmin(admin.ModelAdmin):
    list_display = ('capital',)
    search_fields = ('user',)
    list_filter = ('capital',)
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



class CapitalTypeAdmin(admin.ModelAdmin):
    fields = ('title',)


admin.site.register(CapitalType, CapitalTypeAdmin)