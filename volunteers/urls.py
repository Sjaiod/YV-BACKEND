from django.urls import path
from .views import TokenGenarateView,BkashPaymentCreateView,BkassCallBackView

urlpatterns = [
    path("token/",TokenGenarateView.as_view(),name="Genarate token"),
    path("payment/create/",BkashPaymentCreateView.as_view(),name="Bkash Pyment Create"),
    path("payment/callback/",BkassCallBackView.as_view(),name="Bkash Bkash Call Back view")
]