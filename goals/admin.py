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
        'repeat',
        'pub_date'
    )
    list_editable = (
        'type',
        'repeat'
    )
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
        'is_done',
        'pub_date'
    )
    list_editable = ('is_done',)
    search_fields = ('title',)
    list_filter = ('is_done',)
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
                'is_done',
            ),
        }),
    )
    empty_value_display = 'Не задано'



