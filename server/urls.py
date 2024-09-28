
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HOmepage

urlpatterns = [
    path('', HOmepage.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/member/', include('members.urls')),
]

urlpatterns += staticfiles_urlpatterns()
