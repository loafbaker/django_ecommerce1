from django.contrib import admin

# Register your models here.
from .models import UserAddress, UserDefaultAddress, UserStripe, EmailConfirmed, EmailMarketingSignUp

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress


admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserDefaultAddress)
admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp']
    class Meta:
        model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)