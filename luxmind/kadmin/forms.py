from django import forms
from client.models import PricePerDuration,Discipline,TypePaper
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest as request
from django.forms import HiddenInput
from django.http import HttpRequest as user
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser

class PricePerDurationForm(forms.ModelForm):
    
    class Meta:
       model = PricePerDuration
       fields = ('__all__')
       labels ={
           'WarehouseStatus':'Status',          
           
       }       
       
    def __init__(self, *args, **kwargs):
        super(PricePerDurationForm, self).__init__(*args, **kwargs)

class DisciplineForm(forms.ModelForm):
    
    class Meta:
       model = Discipline
       fields = ('__all__')
       labels ={
           'WarehouseStatus':'Status',          
           
       }       
       
    def __init__(self, *args, **kwargs):
        super(DisciplineForm, self).__init__(*args, **kwargs)


class TypePaperForm(forms.ModelForm):
    
    class Meta:
       model = TypePaper
       fields = ('__all__')
       labels ={
           'WarehouseStatus':'Status',          
           
       }       
       
    def __init__(self, *args, **kwargs):
        super(TypePaperForm, self).__init__(*args, **kwargs)