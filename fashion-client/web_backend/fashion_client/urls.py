from django.urls import path
from transactions.views import TransactionsView

urlpatterns = [
    path('transactions/', TransactionsView.as_view()),

]