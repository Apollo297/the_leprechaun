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
        '<int:pk>/',
        views.GoalDetailView.as_view(),
        name='detail_goal'
    ),

    path(
        '<int:goal_id>/transactions/create/',
        views.GoalTransactionCreateView.as_view(),
        name='goal_transaction_create'
    ),
    path(
        '<int:goal_id>/transactions/',
        views.GoalTransactionListView.as_view(),
        name='goal_transaction_list'
    ),

    path(
        'transactions/<int:transaction_id>/edit/',
        views.GoalTransactionUpdateView.as_view(),
        name='goal_transaction_edit'
    ),
    path(
        'transactions/<int:transaction_id>/delete/',
        views.GoalTransactionDeleteView.as_view(),
        name='goal_transaction_delete'
    ),
    path(
        'transactions/<int:transaction_id>/',
        views.GoalTransactionDetailView.as_view(),
        name='goal_transaction_detail'
    ),
]
