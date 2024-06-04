from django.urls import path

from goals import views

app_name = 'goals'

urlpatterns = [
    path(
        'create/',
        views.GoalCreateView.as_view(),
        name='create_goal'
    ),
    path(
        'my_goals',
        views.GoalsListView.as_view(),
        name='goals_list'
    ),
    path(
        '<int:pk>/',
        views.GoalDetailView.as_view(),
        name='detail_goal'
    ),
    path(
        '<int:pk>/edit/',
        views.GoalUpdateView.as_view(),
        name='edit_goal'
    ),
    path(
        '<int:pk>/delete/',
        views.GoalDeleteView.as_view(),
        name='delete_goal'
    ),
    path(
        '<int:pk>/transactions/create/',
        views.GoalTransactionCreateView.as_view(),
        name='goal_transaction_create'
    ),
    path(
        '<int:pk>/transactions/',
        views.GoalTransactionsListView.as_view(),
        name='goal_transactions_list'
    ),
    path(
        'archive/',
        views.ArchiveGoalListView.as_view(),
        name='archive_goals'
    ),
    path(
        'archive/<int:pk>/delete/',
        views.ArchiveGoalDeleteView.as_view(),
        name='archive_goals_delete'
    )
]
