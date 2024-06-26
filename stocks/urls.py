from django.urls import path
from .views import SignUpView, StockInfoView, LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('stock/', StockInfoView.as_view(), name='stock-info'),
]