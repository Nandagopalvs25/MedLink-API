from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'student'),
        ('doctor', 'doctor'),
        ('HR', 'HR'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,default='student')
    years_exp=models.IntegerField(blank=True,null=True)
    experience=models.CharField(max_length=200,null=True,blank=True)
    institution_name=models.CharField(max_length=100,null=True,blank=True)
    specialisation=models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.username
    

class Patient(models.Model):
    doctor=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender=models.CharField(max_length=20)


    def __str__(self):
        return self.name
    

class Record(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    date=models.DateField(auto_now_add=True)
    url=models.CharField(max_length=300)

    RECORD_TYPE_CHOICES = (
        ('diagnoses', 'diagnoses'),
        ('medications', 'medications'),
        ('labresult', 'labresult'),
    )

    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES,default='labresult')
    summary=models.TextField(max_length=1000,null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.name

class Post(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    desc=models.CharField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)
    doctors_related=models.ManyToManyField(CustomUser,related_name="doctors_related",null=True,blank=True)
    tags=TaggableManager()


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    comment=models.CharField(max_length=255)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

