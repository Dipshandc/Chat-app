from django.contrib import admin
from .models import CustomUser, UserStatus

admin.site.register(CustomUser)
admin.site.register(UserStatus)
