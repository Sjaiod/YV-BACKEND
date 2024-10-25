from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HOmepage


urlpatterns = [
    path('', HOmepage.as_view(), name='welcome'),
    path('admin/', admin.site.urls),
    path('api/member/', include('members.urls')),
    path('api/', include('events.urls')),
    path('api/vol/', include('volunteers.urls')),
    ##path('api/donate/', include('donation.urls')),
]

urlpatterns += staticfiles_urlpatterns()
