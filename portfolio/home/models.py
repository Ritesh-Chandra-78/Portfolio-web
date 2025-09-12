from django.db import models

# For profile information
class Profile(models.Model):
    full_name     = models.CharField(max_length=100, default='Ritesh Chandra')
    headline      = models.CharField(max_length=200, default='Full-stack developer — Django, Python, responsive UI, and clean UX.')
    hero_greeting = models.CharField(max_length=60, default="Hi, I'm")
    accent_name   = models.CharField(max_length=50, default='Ritesh')
    hero_image    = models.ImageField(upload_to='profile/', blank=True, null=True)
    about_image   = models.ImageField(upload_to='profile/', blank=True, null=True)
    about_text_1  = models.TextField(blank=True)
    about_text_2  = models.TextField(blank=True)
    resume        = models.FileField(upload_to='resume/', blank=True, null=True)
    email         = models.EmailField(blank=True)
    location      = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name

# For  SocialMedia Links 
class SocialLink(models.Model):
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='socials')
    platform  = models.CharField(max_length=30)  # e.g. GitHub, LinkedIn, X
    url       = models.URLField()
    icon_class= models.CharField(max_length=50, help_text='Bootstrap icon class, e.g. "bi bi-github"')

    def __str__(self):
        return f'{self.platform}'
    
    
# home/models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
