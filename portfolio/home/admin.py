from django.contrib import admin
from .models import Profile,SocialLink,ContactMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(SocialLink)
admin.site.register(ContactMessage)