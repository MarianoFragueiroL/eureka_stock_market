from django.urls import path
from .views import SignUpView, StockInfoView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('stock/', StockInfoView.as_view(), name='stock-info'),
]