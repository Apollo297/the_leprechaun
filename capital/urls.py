from django.urls import path

from capital import views

app_name = 'capital'

urlpatterns = [
    path(
        'create/',
        views.TransactionCreateView.as_view(),
        name='create_transaction'
    ),
]
    # path(
    #     '<int:capital_id>/edit/',
    #     views.CapitalUpdateView.as_view(),
    #     name='edit_capital'
    # ),
    # path(
    #     '<int:capital_id>/delete/',
    #     views.CapitalDeleteView.as_view(),
    #     name='delete_capital'
    # ),
    # path(
    #     '<int:pk>/',
    #     views.CapitalDetailView.as_view(),
    #     name='detail_capital'
    # ),

    # path(
    #     '<int:capital_id>/transactions/create/',
    #     views.CapitalTransactionCreateView.as_view(),
    #     name='capital_transaction_create'
    # ),
    # path(
    #     '<int:capital_id>/transactions/',
    #     views.CapitalTransactionListView.as_view(),
    #     name='capital_transaction_list'
    # ),

    # path(
    #     'transactions/<int:transaction_id>/edit/',
    #     views.CapitalTransactionUpdateView.as_view(),
    #     name='capital_transaction_edit'
    # ),
    # path(
    #     'transactions/<int:transaction_id>/delete/',
    #     views.CapitalTransactionDeleteView.as_view(),
    #     name='capital_transaction_delete'
    # ),
    # path(
    #     'transactions/<int:transaction_id>/',
    #     views.CapitalTransactionDetailView.as_view(),
    #     name='capital_transaction_detail'
    # ),

