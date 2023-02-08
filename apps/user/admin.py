from django.contrib import admin
from apps.user.models import User, EmailVerification
# Register your models here.

class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('id',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id',)

admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)