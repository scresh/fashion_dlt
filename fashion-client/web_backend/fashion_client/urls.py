from django.urls import path
from state.views import StateView
# from transactions.views import TransactionsView

urlpatterns = [
    path('state/', StateView.as_view()),
    # path('transactions/', TransactionsView.as_view()),

]