from django.urls import path
from transactions.views import TransactionsView
from generator.views import GeneratorView
from validator.views import ValidatorView
from transfer.views import TransferView

urlpatterns = [
    path('transactions/', TransactionsView.as_view()),
    path('generator/', GeneratorView.as_view()),
    path('validator/', ValidatorView.as_view()),
    path('transfer/', TransferView.as_view()),

]