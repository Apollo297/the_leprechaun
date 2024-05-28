from django.contrib import admin

from goals.models import (
    GoalTransaction,
    Goals
)

TEXT = 'Детальная информация о цели.'


@admin.register(GoalTransaction)
class GoalTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'goal',
        'type',
        'created_at'
    )
    list_editable = ('type',)
    search_fields = ('goal', 'user',)
    list_filter = ('type',)


class GoalTransactionInline(admin.StackedInline):
    model = GoalTransaction
    extra = 0


@admin.register(Goals)
class GoalsAdmin(admin.ModelAdmin):
    inlines = (
        GoalTransactionInline,
    )
    list_display = (
        'user',
        'title',
        'term',
        'currency',
        'created_at'
    )
    search_fields = ('title',)
    list_display_links = ('title',)
    fieldsets = (
        ('Блок-1', {
            'fields': (
                'title',
                'user',
                'goal_amount',
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
                'term',
                'currency',
                'accumulated',
            ),
        }),
    )
    empty_value_display = 'Не задано'
