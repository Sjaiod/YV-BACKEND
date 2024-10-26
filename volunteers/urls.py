from django.urls import path
from .views import TokenGenarateView,BkashPaymentCreateView,BkassCallBackView,CreateVolentierViwe,StartVolunteerIntakeView,StopVolunteerIntakeView,LoadingView

urlpatterns = [
    path("start_volunteer_intake/",StartVolunteerIntakeView.as_view(),name="Start taking volentiers"),
    path("stop_volunteer_intake/",StopVolunteerIntakeView.as_view(),name="Stop taking volentiers"),
    path("token/",TokenGenarateView.as_view(),name="Genarate token"),
    path("payment/create/",BkashPaymentCreateView.as_view(),name="Bkash Pyment Create"),
    path("payment/callback/",BkassCallBackView.as_view(),name="Bkash Bkash Call Back view"),
    path("create/",CreateVolentierViwe.as_view(),name="Create Volentier"),
    path('loading/', LoadingView.as_view(), name='loading')
]