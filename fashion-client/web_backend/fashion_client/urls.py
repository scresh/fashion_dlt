from django.urls import path
from transactions.views import TransactionsView
from keys.views import KeysView

urlpatterns = [
    path('transactions/', TransactionsView.as_view()),
    path('keys/', KeysView.as_view()),

]