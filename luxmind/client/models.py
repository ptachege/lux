from django.db import models
from django.conf import settings


class Users(models.Model):
    
    Email = models.EmailField(max_length=100)
    Name = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Name


class PricePerDuration(models.Model):
    DURATION_LIST = (('1 Month', '1 Month'),('14 Days', '14 Days'),('7 Days', '7 Days'),('5 Days', '5 Days'),
    ('3 Days', '3 Days'),('2 Days', '2 Days'),('24 Hours', '24 Hours'),('8 Hours', '8 Hours'),('4 Hours', '4 Hours'))
    LEVEL_LIST = (('High School', 'High School'),('Undergraduate(1-2Yrs)', 'Undergraduate(1-2Yrs)')
    ,('Undergraduate(3-4Yrs)', 'Undergraduate(3-4Yrs)'),('Graduate', 'Graduate'),('PHD', 'PHD'))
    
    Duration = models.CharField(max_length=50, choices=DURATION_LIST, default='14 Days')
    Level = models.CharField(max_length=50, choices=LEVEL_LIST, default='Undergraduate(1-2Yrs)')
    Amount = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Level

class VAT(models.Model):
    
    Country = models.CharField(max_length=100)
    VAT = models.CharField(max_length=100)
    Status = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Country


class Discipline(models.Model):
    Discipline_List = (('All', 'All'),('Tiny', 'Tiny')
    ,('Hard', 'Hard'))
    Status_List = (('Active', 'Active'),('Inactive', 'Inactive'))
    Name = models.CharField(max_length=100)    
    Status = models.CharField(max_length=50, choices=Status_List, default='Active')
    DisciplineType = models.CharField(max_length=50, choices=Discipline_List, default='All') 
    Highschool = models.CharField(max_length=100,blank=True)
    Undergrad1 = models.CharField(max_length=100,blank=True)
    Undergrad2 = models.CharField(max_length=100,blank=True)
    Grad = models.CharField(max_length=100,blank=True)
    PHD = models.CharField(max_length=100,blank=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Name


class TypePaper(models.Model):
    Paper_List = (('Essay', 'Essay'),('Hard Type', 'Hard Type')
    ,('Massive Type', 'Massive Type'))
    Status_List = (('Active', 'Active'),('Inactive', 'Inactive'))
    Name = models.CharField(max_length=100)    
    Status = models.CharField(max_length=50, choices=Status_List, default='Active') 
    PaperType = models.CharField(max_length=50, choices=Paper_List, default='Essay') 
    Highschool = models.CharField(max_length=100,blank=True)
    Undergrad1 = models.CharField(max_length=100,blank=True)
    Undergrad2 = models.CharField(max_length=100,blank=True)
    Grad = models.CharField(max_length=100,blank=True)
    PHD = models.CharField(max_length=100,blank=True)     
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Name


class TempPaper(models.Model):
    
    Title = models.CharField(max_length=1000)
    TypeOfPaper = models.CharField(max_length=100)
    Discipline = models.CharField(max_length=100,blank=True)
    ipaddress = models.CharField(max_length=100,blank=True)
    AcademicLevel = models.CharField(max_length=100,blank=True)
    PaperFormat = models.CharField(max_length=100,blank=True)
    Pages = models.CharField(max_length=100,blank=True)
    Spacing = models.CharField(max_length=100,blank=True)
    Sources = models.CharField(max_length=100,blank=True)
    Slides = models.CharField(max_length=100,blank=True)
    Slidesources = models.CharField(max_length=100,blank=True)
    Charts = models.CharField(max_length=100,blank=True)
    Timeline = models.CharField(max_length=100,blank=True)
    WriterPref = models.CharField(max_length=100,blank=True)
    PaperPref = models.CharField(max_length=100,blank=True)
    Description = models.CharField(max_length=30000,blank=True)
    NativeSpeaker = models.CharField(max_length=100,blank=True)
    SmartPaper = models.CharField(max_length=100,blank=True)
    Writersample = models.CharField(max_length=100,blank=True)
    Copysources = models.CharField(max_length=100,blank=True)
    Progressivedelivery = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,blank=True)
    Orderid = models.CharField(max_length=100,blank=True)
    UserId = models.CharField(max_length=100,blank=True)
    PaymentStatus = models.CharField(max_length=100,blank=True)
    OrderStatus = models.CharField(max_length=100,blank=True)
    BidOption = models.CharField(max_length=100,blank=True)   
    CPPESL = models.CharField(max_length=100,blank=True)
    CPPENL = models.CharField(max_length=100,blank=True)
    ESL = models.CharField(max_length=100,blank=True)
    ENL = models.CharField(max_length=100,blank=True)
    Disputereason = models.CharField(max_length=100,blank=True)
    DisputeMain = models.CharField(max_length=1000,blank=True)
    Writter = models.CharField(max_length=100,blank=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    def __str__(self):
        return self.Title

class Documents(models.Model):
    
    Document = models.ImageField(upload_to='images/%Y/%M/%D/')
    ipaddress = models.CharField(max_length=100)
    PaperId = models.CharField(max_length=100,blank=True)
    FileName = models.CharField(max_length=100,blank=True)
    UserId = models.CharField(max_length=100,blank=True)
    Description = models.CharField(max_length=100,blank=True)
    PaperType = models.CharField(max_length=100,blank=True)
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)


class PaperSumation(models.Model):
    
    
    ipaddress = models.CharField(max_length=100)
    Description = models.CharField(max_length=100,blank=True)
    Amount = models.CharField(max_length=100,blank=True)
    Status = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)


class PaperMessage(models.Model):
    
    
    PaperId = models.CharField(max_length=100)
    Message = models.CharField(max_length=1000,blank=True)
    From = models.CharField(max_length=100,blank=True)
    Status = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)


class PaperBids(models.Model):    
    
    PaperId = models.CharField(max_length=100)
    Title = models.CharField(max_length=1000,blank=True)
    Discipline = models.CharField(max_length=100,blank=True)
    Writter = models.CharField(max_length=100,blank=True)
    WritterId = models.CharField(max_length=100,blank=True)
    Bid = models.CharField(max_length=100,blank=True)
    Status = models.CharField(max_length=100,blank=True)    
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)


class Messages(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    to = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=10000, blank=True)
    message = models.TextField(max_length=100000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.to

