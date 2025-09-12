from django.db import models

# Skills
class Skill(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    level = models.IntegerField()  # e.g., 85 for 85%
    color_class = models.CharField(max_length=50, default="bg-success")  # Bootstrap color

    def __str__(self):
        return self.name

# Tools
class Tool(models.Model):
    name = models.CharField(max_length=50)
    icon_url = models.URLField()
    delay = models.FloatField(default=0)  # animation delay in seconds

    def __str__(self):
        return self.name

# Education
class Education(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    institute = models.CharField(max_length=100)
    icon = models.CharField(max_length=5)  # Emoji icon

    def __str__(self):
        return self.title
