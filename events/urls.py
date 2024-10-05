from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Now you have access to:
    # /api/events/ for listing all events
    # /api/events/latest/ for fetching all events ordered by latest
    # /api/events/search/?name=<query> for searching events by name
]