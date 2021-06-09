from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from client.models import PricePerDuration,Discipline,TypePaper,TempPaper,PaperBids
from .forms import PricePerDurationForm,DisciplineForm,TypePaperForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from tutor.models import Writters

def KFront_page(request):
      
    return render(request,"kadmin/loginmain.html")

def AdminDashbard(request):
      
    return render(request,"kadmin/dashboard.html")

def AdminOrders(request):
     context={'list' : TempPaper.objects.all()}
     return render(request,"kadmin/list_orders.html",context)

def AdminOrder(request,id):
    papers=PaperBids.objects.filter(PaperId=id)
    context={'user' : TempPaper.objects.get(pk=id),
    'papers':papers}
    return render(request,"kadmin/View_order.html",context)

def PickBid(request,id):
    
    c = PaperBids.objects.get(pk=id)   
    c.Status="Picked"               
    c.save()
    
    
    return HttpResponseRedirect(reverse('AdminOrders'))

def AdminWritters(request):
     context={'list' : Writters.objects.all()}
     return render(request,"kadmin/list_writters.html",context)

def Writter_Edit(request,id):
     context={'user' : Writters.objects.get(pk=id)}
     return render(request,"kadmin/edit_writters.html",context)

def UpdateOrders(request):
    if request.method=="POST":
        BidOption=request.POST['BidOption']
        orderid=request.POST['orderid']
        c = TempPaper.objects.get(pk=orderid)
        c.BidOption=BidOption                
        c.save()
    
    context={'list' : TempPaper.objects.all()}
    return render(request,"kadmin/list_orders.html",context)

def UpdateAccount(request):
    if request.method=="POST":
        Status=request.POST['Status']            
        DurationPoints=request.POST['DurationPoints']
        LatenessPoints=request.POST['LatenessPoints']            
        DisputePoints=request.POST['DisputePoints']
        RequestPoints=request.POST['RequestPoints']           
        
        AccountType=request.POST['AccountType']            
        Level=request.POST['Level']
        QualityOfWork=request.POST['QualityOfWork']
        
        Email=request.POST['Email']

        if(QualityOfWork == "High School" and Level == "D" ):
            QualityCheckPoints = "0"
        elif(QualityOfWork == "High School" and Level == "C" ):
            QualityCheckPoints = "0" 
        elif(QualityOfWork == "High School" and Level == "B" ):
            QualityCheckPoints = "5" 
        elif(QualityOfWork == "High School" and Level == "A" ):
            QualityCheckPoints = "10" 
        elif(QualityOfWork == "Undergraduate (1-2)" and Level == "D" ):
            QualityCheckPoints = "15" 
        elif(QualityOfWork == "Undergraduate (1-2)" and Level == "C" ):
            QualityCheckPoints = "20" 
        elif(QualityOfWork == "Undergraduate (1-2)" and Level == "B" ):
            QualityCheckPoints = "25" 
        elif(QualityOfWork == "Undergraduate (1-2)" and Level == "A" ):
            QualityCheckPoints = "30" 
        elif(QualityOfWork == "Undergraduate (3-4)" and Level == "D" ):
            QualityCheckPoints = "33" 
        elif(QualityOfWork == "Undergraduate (3-4)" and Level == "C" ):
            QualityCheckPoints = "34" 
        elif(QualityOfWork == "Undergraduate (3-4)" and Level == "B" ):
            QualityCheckPoints = "35" 
        elif(QualityOfWork == "Undergraduate (3-4)" and Level == "A" ):
            QualityCheckPoints = "36" 
        elif(QualityOfWork == "Graduate" and Level == "D" ):
            QualityCheckPoints = "36.5" 
        elif(QualityOfWork == "Graduate" and Level == "C" ):
            QualityCheckPoints = "37"
        elif(QualityOfWork == "Graduate" and Level == "B" ):
            QualityCheckPoints = "37.5" 
        elif(QualityOfWork == "Graduate" and Level == "A" ):
            QualityCheckPoints = "38"
        elif(QualityOfWork == "Graduate" and Level == "D" ):
            QualityCheckPoints = "38.5"
        elif(QualityOfWork == "Graduate" and Level == "C" ):
            QualityCheckPoints = "39"
        elif(QualityOfWork == "Graduate" and Level == "B" ):
            QualityCheckPoints = "39.5"
        else:
            QualityCheckPoints = "40" 

        Score=float(QualityCheckPoints)+float(DurationPoints)+float(DisputePoints)+float(RequestPoints)+float(LatenessPoints)
        c = Writters.objects.get(Email=Email)
        c.Status=Status
        c.AccountType=AccountType
        c.QualityCheckPoints=QualityCheckPoints
        c.Level=Level
        c.QualityOfWork=QualityOfWork
        c.DurationPoints=DurationPoints
        c.DisputePoints=DisputePoints
        c.RequestPoints=RequestPoints
        c.LatenessPoints=LatenessPoints
        c.Score=Score
        c.save()
        
    context={'list' : Writters.objects.all()}
    return render(request,"kadmin/list_writters.html",context)

def AdminLogin(request):
      if request.method=="POST":
            email=request.POST['login-email']            
            Password=request.POST['login-password']
            user=authenticate(request,username=email,password=Password)
            if user:
                #   Name=Users.objects.get(Email=email).Name
                #   userid=Users.objects.get(Email=email).id
                #   request.session['Email'] = email
                #   request.session['Name'] = Name
                #   request.session['Userid'] = userid 
                  login(request,user)
                  return HttpResponseRedirect(reverse('AdminDashbard'))
            else:
                  messages.error(request, 'Details Dont Match')
                  return HttpResponseRedirect(reverse('KFront_page'))


def PricePerPage(request):
     context={'list' : PricePerDuration.objects.all()}
     return render(request,"kadmin/list_pageprice.html",context)

def PricePerPage_Add(request,id=0):
    if request.method=="GET":
        if id==0:
            form = PricePerDurationForm()
        else:
            priceduration=PricePerDuration.objects.get(pk=id)
            form=PricePerDurationForm(instance=priceduration)
        return render(request,"kadmin/add_pageprice.html",{'form':form})
    else:
        if id==0:
            form = PricePerDurationForm(request.POST)

        else:
            priceduration=PricePerDuration.objects.get(pk=id)
            form=PricePerDurationForm(request.POST,instance=priceduration)

        if form.is_valid():        
           form.save()
           messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Priceperpage', message='Save complete')

def PricePerPage_Delete(request,id):
    warehouse_status=PricePerDuration.objects.get(pk=id)
    warehouse_status.delete()
    messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Priceperpage')

def DisplinePage(request):
     context={'list' : Discipline.objects.all()}
     return render(request,"kadmin/list_displine.html",context)


def Discpline_Add(request,id=0):
    if request.method=="GET":
        if id==0:
            form = DisciplineForm()
        else:
            priceduration=Discipline.objects.get(pk=id)
            form=DisciplineForm(instance=priceduration)
        return render(request,"kadmin/add_discpline.html",{'form':form})
    else:
        if id==0:
            form = DisciplineForm(request.POST)

        else:
            priceduration=Discipline.objects.get(pk=id)
            form=DisciplineForm(request.POST,instance=priceduration)

        if form.is_valid():        
           form.save()
           messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Discpline', message='Save complete')

def Discpline_Delete(request,id):
    warehouse_status=Discipline.objects.get(pk=id)
    warehouse_status.delete()
    messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Discpline')


def PaperPage(request):
     context={'list' : TypePaper.objects.all()}
     return render(request,"kadmin/list_paper.html",context)


def Paper_Add(request,id=0):
    if request.method=="GET":
        if id==0:
            form = TypePaperForm()
        else:
            priceduration=TypePaper.objects.get(pk=id)
            form=TypePaperForm(instance=priceduration)
        return render(request,"kadmin/add_paper.html",{'form':form})
    else:
        if id==0:
            form = TypePaperForm(request.POST)

        else:
            priceduration=TypePaper.objects.get(pk=id)
            form=TypePaperForm(request.POST,instance=priceduration)

        if form.is_valid():        
           form.save()
           messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Paper', message='Save complete')

def Paper_Delete(request,id):
    warehouse_status=TypePaper.objects.get(pk=id)
    warehouse_status.delete()
    messages.success(request, 'Successfully Sent The Message!')
    return redirect('/luxmind/Paper')
     
