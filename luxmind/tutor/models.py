from django.db import models

# Create your models here.
class Writters(models.Model):
    
    
    Firstname = models.CharField(max_length=100)
    Middlename = models.CharField(max_length=100,blank=True)
    LastName = models.CharField(max_length=100,blank=True)
    Email = models.CharField(max_length=100,blank=True)
    PhoneNumber = models.CharField(max_length=100,blank=True)
    IdNumber = models.ImageField(upload_to='images/%Y/%M/%D/')
    PassPort = models.ImageField(upload_to='images/%Y/%M/%D/')
    Certificate = models.ImageField(upload_to='images/%Y/%M/%D/')
    School = models.CharField(max_length=100,blank=True)
    Country = models.CharField(max_length=100,blank=True) 
    Gender = models.CharField(max_length=100,blank=True) 
    Language = models.CharField(max_length=100,blank=True) 
    WorkExperience = models.CharField(max_length=100,blank=True) 
    City = models.CharField(max_length=100,blank=True)
    Address = models.CharField(max_length=100,blank=True)
    NightCalls = models.CharField(max_length=100,blank=True)
    ForceAssignments = models.CharField(max_length=100,blank=True)
    SocialMedia = models.CharField(max_length=100,blank=True)
    AdditionalInfo = models.CharField(max_length=5000,blank=True)
    LevelOfEducation = models.CharField(max_length=100,blank=True)
    Status = models.CharField(max_length=100,blank=True)
    AccountType = models.CharField(max_length=100,blank=True)
    QualityCheckPoints = models.CharField(max_length=100,blank=True)
    Level = models.CharField(max_length=100,blank=True)
    QualityOfWork = models.CharField(max_length=100,blank=True)
    DurationPoints = models.CharField(max_length=100,blank=True)
    DisputePoints = models.CharField(max_length=100,blank=True)
    RequestPoints = models.CharField(max_length=100,blank=True)
    LatenessPoints = models.CharField(max_length=100,blank=True)
    Score = models.CharField(max_length=100,blank=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
