from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from client.models import PricePerDuration,Discipline,TypePaper
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from client.models import Users,PaperBids,Discipline,TypePaper,TempPaper,Documents,PaperSumation,PricePerDuration,PaperMessage
from .models import Writters
import requests
import os
import zipfile
from io import StringIO
import tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.http import JsonResponse
import random
import string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import socket
from django.template.loader import render_to_string, get_template
import re
import xlrd
import urllib
import json

def TutorFront_page(request):
      
    return render(request,"tutor/login.html")

def CreateAccount(request):
      
    return render(request,"tutor/register.html")

def ForgotPassword(request):
      
    return render(request,"tutor/forgot.html")

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request,"tutor/login.html")




def TutorChangePassword(request):
      if request.method=="POST":
            email=request.POST['login-email']
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(12))
            password = result_str
            try:
                  hy=Writters.objects.get(Email=email)
                  u = User.objects.get(username=email)
                  u.set_password(password)
                  u.save() 

                  message1 = Mail(
                  from_email='electromartke@gmail.com',
                  # to_emails=['juliuszakora@gmail.com'],
                  to_emails=[email],
                  subject='Password Reset',
                  
            
                  
                  html_content=("Your New Password is "+ str(password)),
                  )
                  try:
                        # sg = SendGridAPIClient('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')
                        sg = SendGridAPIClient('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')
                        response = sg.send(message1)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                  except Exception as e:
                        print(e.body)
                  
                  messages.error(request, 'Check You Email For the Password')
                  return render(request,"tutor/login.html")
            except ObjectDoesNotExist:
                  messages.error(request, 'Email Doesnt Exists')
                  return render(request,"tutor/forgot.html")

def TakeOrder(request,id):
    userid=request.session.get('Userid')
    c = TempPaper.objects.get(pk=id)
    c.Writter=userid 
    c.OrderStatus="Assigned"               
    c.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))

def SubmitOrder(request,id):
    userid=request.session.get('Userid')
    c = TempPaper.objects.get(pk=id)    
    c.OrderStatus="Finished"               
    c.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))

def AcceptBid(request,id):
    
    c = PaperBids.objects.get(pk=id)   
    c.Status="Accepted"               
    c.save()

    userid=request.session.get('Userid')
    PaperId=PaperBids.objects.get(pk=id).PaperId
    m = TempPaper.objects.get(pk=PaperId)
    m.Writter=userid 
    m.OrderStatus="Assigned"               
    m.save()
    
    
    return HttpResponseRedirect(reverse('CurrentPapers'))

def RejectBid(request,id):
    
    c = PaperBids.objects.get(pk=id)   
    c.Status="Rejected"               
    c.save()
    
    
    return HttpResponseRedirect(reverse('TutorDashboard'))

def BidOrder(request,id):
    userid=request.session.get('Userid')
    Email=request.session.get('Email')   
    
    Title=TempPaper.objects.get(pk=id).Title
    Discipline=TempPaper.objects.get(pk=id).Discipline
    bid="I Bid"
    try:
        n=PaperBids.objects.get(PaperId=id,WritterId=userid)
    except ObjectDoesNotExist:
        my_form = PaperBids(PaperId=id,
                        Title=Title,
                        Discipline=Discipline,
                        Writter=Email,
                        WritterId=userid, 
                        Bid=bid,                            
                        Status="Pending"
                        )      
        my_form.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))

def BidTime(request,id):
    if request.method=="GET":
        Days=request.GET['Days']
        Time=request.GET['Time']
        userid=request.session.get('Userid')
        Email=request.session.get('Email')   
        
        Title=TempPaper.objects.get(pk=id).Title
        Discipline=TempPaper.objects.get(pk=id).Discipline
        bid="I will do it in "+str(Days)+" Days " +str(Time) +" Hours"
        try:
            n=PaperBids.objects.get(PaperId=id,WritterId=userid)
        except ObjectDoesNotExist:
            my_form = PaperBids(PaperId=id,
                            Title=Title,
                            Discipline=Discipline,
                            Writter=Email,
                            WritterId=userid, 
                            Bid=bid,                            
                            Status="Pending"
                            )      
            my_form.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))
    
    context={'list' : TempPaper.objects.all()}
    return render(request,"kadmin/list_orders.html",context)

def BidAmount(request,id):
    if request.method=="GET":
        Amount=request.GET['Amount']        
        userid=request.session.get('Userid')
        Email=request.session.get('Email')   
        
        Title=TempPaper.objects.get(pk=id).Title
        Discipline=TempPaper.objects.get(pk=id).Discipline
        bid="I will do it for "+str(Amount)
        try:
            n=PaperBids.objects.get(PaperId=id,WritterId=userid)
        except ObjectDoesNotExist:
            my_form = PaperBids(PaperId=id,
                            Title=Title,
                            Discipline=Discipline,
                            Writter=Email,
                            WritterId=userid, 
                            Bid=bid,                            
                            Status="Pending"
                            )      
            my_form.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))

def BidTimeAmount(request,id):
    if request.method=="GET":
        Days=request.GET['Days']
        Time=request.GET['Time']
        Amount=request.GET['Amount']
        userid=request.session.get('Userid')
        Email=request.session.get('Email')   
        
        Title=TempPaper.objects.get(pk=id).Title
        Discipline=TempPaper.objects.get(pk=id).Discipline
        bid="I will do it in "+str(Days)+" Days " +str(Time) +" Hours"+" For $"+str(Amount)
        try:
            n=PaperBids.objects.get(PaperId=id,WritterId=userid)
        except ObjectDoesNotExist:
            my_form = PaperBids(PaperId=id,
                            Title=Title,
                            Discipline=Discipline,
                            Writter=Email,
                            WritterId=userid, 
                            Bid=bid,                            
                            Status="Pending"
                            )      
            my_form.save()
    
    context={'list' : TempPaper.objects.all()}
    return HttpResponseRedirect(reverse('TutorDashboard'))

def NewAccount(request):
    if request.method=="POST":
        Firstname=request.POST['Firstname']            
        Middlename=request.POST['Middlename']
        Lastname=request.POST['Lastname']            
        Email=request.POST['Email']
        Phone=request.POST['Phone']            
        Gender=request.POST['Gender']
        School=request.POST['School']            
        Country=request.POST['Country']
        Language=request.POST['Language']            
        WorkExperience=request.POST['WorkExperience']
        City=request.POST['City']            
        Address=request.POST['Address']
        NightCalls=request.POST['NightCalls']            
        ForceAssignments=request.POST['ForceAssignments']
        LevelOfEducation=request.POST['LevelOfEducation']
        SocialMedia=request.POST['SocialMedia']
        AdditionalInfo=request.POST['AdditionalInfo']
        Password=request.POST['Password']
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        file3 = request.FILES['file3']
        try:
            hy=User.objects.get(username=Email)
            messages.error(request, 'Email already Exists')
            return render(request,"tutor/register.html")
        except ObjectDoesNotExist:
            my_form = Writters(Firstname=Firstname,
                            Middlename=Middlename,
                            LastName=Lastname,
                            Email=Email,
                            PhoneNumber=Phone,
                            Gender=Gender,
                            School=School,
                            Country=Country,
                            Language=Language,
                            WorkExperience=WorkExperience,
                            City=City,
                            Address=Address,
                            NightCalls=NightCalls,
                            ForceAssignments=ForceAssignments,
                            LevelOfEducation=LevelOfEducation,
                            SocialMedia=SocialMedia,
                            IdNumber=file1,
                            PassPort=file2,
                            Status="Account Activation pending",
                            DurationPoints="2",
                            LatenessPoints="20",
                            DisputePoints="20",
                            RequestPoints="0",
                            Score="42",
                            Certificate=file3
                        )      
            my_form.save()
            User.objects.create_user(username=Email, password=Password,email=Email)
      
    return render(request,"tutor/login.html")

def LoginTutor(request):
      if request.method=="POST":
            email=request.POST['login-email']            
            Password=request.POST['login-password']
            try:
                n=Writters.objects.get(Email=email)
                user=authenticate(request,username=email,password=Password)
                if user:
                    Email=Writters.objects.get(Email=email).Email
                    AccountType=Writters.objects.get(Email=email).AccountType
                    userid=Writters.objects.get(Email=email).id
                    request.session['Email'] = Email
                    request.session['AccountType'] = AccountType
                    request.session['Userid'] = userid 
                    login(request,user)
                    return HttpResponseRedirect(reverse('TutorDashboard'))
                else:
                    messages.error(request, 'Details Dont Match')
                    return HttpResponseRedirect(reverse('TutorFront_page'))
            except ObjectDoesNotExist:
                messages.error(request, 'Details Dont Match')
                return HttpResponseRedirect(reverse('TutorFront_page'))

def TutorDashboard(request):

    papers=TempPaper.objects.filter(OrderStatus="Pending")
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
    
      
    return render(request,"tutor/dashboard.html",{
        'papers': papers,
        'dicpline':dicpline,
        'gt':range(1, 8),       
        'AccountType':AccountType,
          
        })

def CurrentPapers(request):
    userid=request.session.get('Userid')    
    papers=TempPaper.objects.filter(Writter=userid,OrderStatus="Assigned")
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
      
    return render(request,"tutor/current.html",{
        'papers': papers,
        'dicpline':dicpline,
        'AccountType':AccountType,
          
        })

def FinishedPaper(request):
    userid=request.session.get('Userid')    
    papers=TempPaper.objects.filter(Writter=userid,OrderStatus="Finished")
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
      
    return render(request,"tutor/finished.html",{
        'papers': papers,
        'dicpline':dicpline,
        'AccountType':AccountType,
          
        })

def DisputesPaper(request):
    userid=request.session.get('Userid')    
    papers=TempPaper.objects.filter(Writter=userid,OrderStatus="Disputed")
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
      
    return render(request,"tutor/disputed.html",{
        'papers': papers,
        'dicpline':dicpline,
        'AccountType':AccountType,
          
        })

def RevisionPaper(request):
    userid=request.session.get('Userid')    
    papers=TempPaper.objects.filter(Writter=userid,OrderStatus="Revision")
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
      
    return render(request,"tutor/revision.html",{
        'papers': papers,
        'dicpline':dicpline,
        'AccountType':AccountType,
          
        })

def BidsPapers(request):
    userid=request.session.get('Userid')    
    papers=PaperBids.objects.filter(WritterId=userid)
    dicpline = Discipline.objects.all()
    AccountType= request.session.get('AccountType')
      
    return render(request,"tutor/bids.html",{
        'papers': papers,
        'dicpline':dicpline,
        'AccountType':AccountType,
          
        })

def TutorPaper(request,id):
    AccountType= request.session.get('AccountType')

    Orderid=TempPaper.objects.get(pk=id).Orderid
    papers=TempPaper.objects.get(pk=id)
    messages=PaperMessage.objects.filter(PaperId=id)
    gfiles=Documents.objects.filter(PaperId=Orderid,PaperType="WPaper")
    request.session['Orderid'] = Orderid
      
    return render(request,"tutor/paperdetails.html",{
        'papers': papers,
        'AccountType':AccountType,
        'messages':messages,
        'gfiles':gfiles,
          
        })

def DownloadFiles(request,id):

    papers=Documents.objects.filter(PaperId=id)
    
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for n in papers:
        filename = n.Document  

        archive.write(filename, 'file%d.png' % 1) # 'file%d.png' will be the
                                                      # name of the file in the
                                                      # zip
    archive.close()

    temp.seek(0)
    wrapper = FileWrapper(temp)

    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'

    return response

def SendMessage(request):
    if request.method=="POST":
        message=request.POST['message']
        PaperId=request.POST['PaperId']            
        
        

        my_form = PaperMessage(PaperId=PaperId,
                            Message=message,
                            From="Tutor",                          
                            
                            Status="0"
                        )      
        my_form.save()
        
      
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteFile(request,id):    
    c = Documents.objects.get(pk=id)   
    c.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def SubmitFiles(request):
      uploaded_files = request.FILES.getlist('file')
      Orderid=request.session.get('Orderid')  
      

      for files in uploaded_files:
            filename = files.name
            b4 = Documents(Document=files, 
                  FileName= filename,
                  PaperId= Orderid,               
                  PaperType="WPaper"
                  )
                  
            b4.save()


      data = {
        'is_taken': 'sawasawa'
      }

      return JsonResponse(data)


      
    