from django.db import models

# Create your models here.
# Projects
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/")  # Upload project images
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


# Resume
class Resume(models.Model):
    file = models.FileField(upload_to="resume/")  # Upload resume PDF
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume uploaded on {self.uploaded_at}"
