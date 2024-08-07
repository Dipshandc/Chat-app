from django.contrib import admin
from .models import CustomUser, UserStatus, UserProfile

admin.site.register(CustomUser)
admin.site.register(UserStatus)
admin.site.register(UserProfile)
