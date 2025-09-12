from django.db import models

# Create your models here.

# Store personal contact info (editable from admin)
class ContactInfo(models.Model):
    location = models.CharField(max_length=200, default="India (Noida)")
    email = models.EmailField(default="example@gmail.com")
    phone = models.CharField(max_length=20, default="+91-00000-00000")

    def __str__(self):
        return self.email


# Store messages submitted from the contact form
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
