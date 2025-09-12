from django.contrib import admin
from .models import ContactInfo, ContactMessage

# Register your models here.
admin.site.register(ContactInfo)
admin.site.register(ContactMessage)
