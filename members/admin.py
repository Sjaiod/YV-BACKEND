from django.contrib import admin
from .models import Member, MemberToken

admin.site.register(Member)
admin.site.register(MemberToken)