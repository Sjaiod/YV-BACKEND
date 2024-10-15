# member/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UpdateProfileView,SetAvailabilityView,RegisterMemberView,LoginView,GETallMembersView,MemberInfoView,RoleViewAPI,SearchUserView,SingleImageUploadView,UploadMultipleFileVIEW,DeleteSingleImageView

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('update/', UpdateProfileView.as_view(), name='update_profile'),
    path('availability/', SetAvailabilityView.as_view(), name='set_availability'),
    path('register/', RegisterMemberView.as_view(), name='register_member'),
    path('allmember/',GETallMembersView.as_view(), name='all_members') ,
    path('memberinfo/', MemberInfoView.as_view(), name="MemberInfoView"),
    path('role/', RoleViewAPI.as_view(), name="RoleView"),
    path('search/', SearchUserView.as_view(), name='search-user'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path("imageupload/",SingleImageUploadView.as_view(),name="image-upload"),
    path("singleimagedelete/",DeleteSingleImageView.as_view(),name="delete-single-image"),
    path("multiyimageupload/",UploadMultipleFileVIEW.as_view(),name="muly-file-upload")
]