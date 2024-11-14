from django.db import models

# Create your models here.
class UserReg(models.Model):
    Name = models.CharField(max_length=20)
    Email = models.EmailField(max_length=20,unique=True)
    Password = models.CharField(max_length=9)
    Phone = models.IntegerField()
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner',blank=True,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True,null=True)

    def __str__(self):
        return self.Name
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
        
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
         return f"Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."