from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Users, PaperBids, Discipline, TypePaper, TempPaper, Documents, PaperSumation, PricePerDuration, \
    PaperMessage, Messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
import re
import random
import string
import requests
import json
from django.core.exceptions import ObjectDoesNotExist
import json as simplejson
from uuid import getnode as get_mac
from django.db.models import DateField, Sum
from django.http import JsonResponse
from datetime import date
from json import dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import socket
from django.template.loader import render_to_string, get_template
import re
import xlrd
import urllib
import json


def post_messages(request):
    if request.method == "POST":
        to = request.POST['to']
        subject = request.POST['subject']
        message = request.POST['message']
        Messages.objects.create(
            to=to,
            subject=subject,
            message=message,
        )
        messages.success(request, 'Message sent successfully.')
        return redirect('client:OrderPaper')


def trial(request):
    return render(request, 'client/basex.html')


def Front_page(request):
    return render(request, "client/login.html")


def Register_page(request):
    return render(request, "client/register.html")


def ForgotPassword(request):
    return render(request, "client/forgot1.html")


def ChangePassword(request):
    if request.method == "POST":
        email = request.POST['login-email']
        password = random.randint(1000000, 10000000)
        try:
            hy = Users.objects.get(Email=email)
            u = User.objects.get(username=email)
            u.set_password(password)
            u.save()

            message1 = Mail(
                from_email='electromartke@gmail.com',
                # to_emails=['juliuszakora@gmail.com'],
                to_emails=[email],
                subject='Password Reset',

                html_content=("Your New Password is " + str(password)),
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
            return render(request, "client/login.html")
        except ObjectDoesNotExist:
            messages.error(request, 'Email Doesnt Exists')
            return render(request, "client/forgot1.html")


def CreateClient(request):
    if request.method == "POST":
        email = request.POST['register-email']
        Name = request.POST['register-name']
        Password = request.POST['register-password']
        try:
            hy = Users.objects.get(Email=email)
            messages.warning(request, 'Email already Exists')
            return render(request, "client/register.html")
        except ObjectDoesNotExist:
            my_form = Users(Email=email,
                            Name=Name)
            my_form.save()

            User.objects.create_user(username=email, password=Password, email=email)
            messages.success(request, 'Account Created Successfully')
            return HttpResponseRedirect(reverse('client:Front_page'))


def LoginClient(request):
    if request.method == "POST":
        email = request.POST['login-email']
        Password = request.POST['login-password']
        user = authenticate(request, username=email, password=Password)
        if user:
            Name = Users.objects.get(Email=email).Name
            userid = Users.objects.get(Email=email).id
            request.session['Email'] = email
            request.session['Name'] = Name
            request.session['Userid'] = userid
            login(request, user)
            messages.success(request, 'Logged in successfully as ' + request.user.username)
            return HttpResponseRedirect(reverse('client:Dashboard'))
        else:
            messages.warning(request, 'Details Dont Match')
            return HttpResponseRedirect(reverse('client:Front_page'))


def logout_urequest(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, "client/login.html")


def Dashboard(request):
    Userid = request.session.get('Userid')
    papers = TempPaper.objects.filter(ipaddress=Userid)

    return render(request, "client/dashboard.html", {
        'papers': papers,

    })


def View_Order(request, id):
    Orderid = TempPaper.objects.get(pk=id).Orderid
    papers = TempPaper.objects.get(pk=id)
    messages = PaperMessage.objects.filter(PaperId=id)
    gfiles = Documents.objects.filter(PaperId=Orderid, PaperType="WPaper")
    request.session['Orderid'] = Orderid

    return render(request, "client/vieworder.html", {
        'papers': papers,
        'messages': messages,
        'gfiles': gfiles,

    })


def FreeEnquiry(request):
    paper = TypePaper.objects.all()
    discpline = Discipline.objects.all()
    mac1 = request.session.get('mac')
    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
        Pit = ""
        gfiles = ""
        sums = ""
        dsum = 0
    else:
        mac = mac1
        try:
            Pit = TempPaper.objects.get(ipaddress=mac)
        except ObjectDoesNotExist:
            Pit = ""
        try:
            gfiles = Documents.objects.filter(ipaddress=mac)
        except ObjectDoesNotExist:
            gfiles = ""

        try:
            sums = PaperSumation.objects.filter(ipaddress=mac)
            dsum = PaperSumation.objects.filter(ipaddress=mac).aggregate(Sum('Amount'))['Amount__sum'] or 0
        except ObjectDoesNotExist:
            sums = ""
            dsum = 0

    return render(request, "client/freeenquiry.html", {
        'paper': paper,
        'discpline': discpline,
        'details': Pit,
        'gfiles': gfiles,
        'sums': sums,
        'dsum': round(dsum, 2),
        'gt': range(1, 8),
    })

    # return render(request,"client/freeenquiry.html")


def OrderPaper(request):
    # paper=TypePaper.objects.all()
    # discpline=Discipline.objects.all()
    mac1 = request.session.get('mac')
    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
        Pit = ""
        gfiles = ""
        sums = ""
        dsum = 0
        paper = TypePaper.objects.all()
        discpline = Discipline.objects.all()
    else:
        mac = mac1
        try:
            Pit = TempPaper.objects.get(ipaddress=mac)
            target = TempPaper.objects.get(ipaddress=mac).AcademicLevel
            if target is None:
                paper = TypePaper.objects.all()
                discpline = Discipline.objects.all()
            else:
                if target == "High School":
                    paper = TypePaper.objects.filter(Highschool=1)
                    discpline = Discipline.objects.filter(Highschool=1)
                elif target == "Undergraduate(1-2Yrs)":
                    paper = TypePaper.objects.filter(Undergrad1=1)
                    discpline = Discipline.objects.filter(Undergrad1=1)
                elif target == "Undergraduate(3-4Yrs)":
                    paper = TypePaper.objects.filter(Undergrad2=1)
                    discpline = Discipline.objects.filter(Undergrad2=1)
                elif target == "Graduate":
                    paper = TypePaper.objects.filter(Grad=1)
                    discpline = Discipline.objects.filter(Grad=1)
                else:
                    paper = TypePaper.objects.filter(PHD=1)
                    discpline = Discipline.objects.filter(PHD=1)
        except ObjectDoesNotExist:
            Pit = ""
            paper = TypePaper.objects.all()
            discpline = Discipline.objects.all()
        try:
            gfiles = Documents.objects.filter(ipaddress=mac)
        except ObjectDoesNotExist:
            gfiles = ""

        try:
            sums = PaperSumation.objects.filter(ipaddress=mac)
            dsum = PaperSumation.objects.filter(ipaddress=mac).aggregate(Sum('Amount'))['Amount__sum'] or 0
        except ObjectDoesNotExist:
            sums = ""
            dsum = 0
    all_messages = Messages.objects.all()
    # ToDo should be something like .filter(user=request.user)??
    return render(request, "client/paper.html", {
        'paper': paper,
        'discpline': discpline,
        'details': Pit,
        'gfiles': gfiles,
        'sums': sums,
        'dsum': round(dsum, 2),
        'gt': range(1, 8),
        'all_messages': all_messages,
    })


def PlaceEnquiry(request):
    TypeOfPaper = request.POST['TypeOfPaper']
    Discipline = request.POST['Discipline']
    AcademicLevel = request.POST['AcademicLevel']
    Pages = request.POST['Pages']
    Spacing = request.POST['Spacing']
    Description = request.POST['Description']
    uploaded_files = request.FILES.getlist('myfile')
    mac1 = request.session.get('mac')
    Userid = request.session.get('Userid')

    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
    else:
        mac = mac1

    for files in uploaded_files:
        filename = files.name
        b4 = Documents(Document=files,
                       FileName=filename,
                       ipaddress=mac
                       )

        b4.save()
    Orderid = random.randint(1000000, 10000000)

    b4 = TempPaper(Description=Description,
                   TypeOfPaper=TypeOfPaper,
                   Discipline=Discipline,
                   Orderid=Orderid,
                   Spacing=Spacing,
                   Pages=Pages,
                   PaymentStatus="Unpaid",
                   OrderStatus="Pending",
                   BidOption="Bid",
                   ipaddress=Userid
                   )

    b4.save()

    Documents.objects.filter(ipaddress=mac).update(UserId=Userid, PaperId=Orderid, PaperType="Cpaper", ipaddress=Userid)
    PaperSumation.objects.filter(ipaddress=mac).delete()
    return redirect('/Dashboard')


def UpdatePaper(request):
    Title = request.GET['Title']
    TypeOfPaper = request.GET['TypeOfPaper']
    Discipline = request.GET['Discipline']
    target = request.GET['Undergraduate']
    PaperFormat = request.GET['PaperFormat']
    timeline = request.GET['timeline']
    pages = request.GET['pages']
    spacing = request.GET['spacing']
    sources = request.GET['sources']
    slides = request.GET['slides']
    slidesources = request.GET['slidesources']
    charts = request.GET['charts']
    fd = request.GET['fd']
    native = request.GET['native']
    smartpaper = request.GET['smartpaper']
    Writersample = request.GET['Writersample']
    Copysources = request.GET['Copysources']
    Progressivedelivery = request.GET['Progressivedelivery']
    mac1 = request.session.get('mac')

    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
    else:
        mac = mac1
    try:
        P = TempPaper.objects.get(ipaddress=mac)
        c = TempPaper.objects.get(ipaddress=mac)
        c.Title = Title
        c.TypeOfPaper = TypeOfPaper
        c.Discipline = Discipline
        c.AcademicLevel = target
        c.PaperFormat = PaperFormat
        c.Timeline = timeline
        c.Pages = pages
        c.Spacing = spacing
        c.Sources = sources
        c.Slides = slides
        c.Slidesources = slidesources
        c.Charts = charts
        c.Description = fd
        c.NativeSpeaker = native
        c.SmartPaper = smartpaper
        c.Writersample = Writersample
        c.Copysources = Copysources
        c.Progressivedelivery = Progressivedelivery
        c.save()

    except ObjectDoesNotExist:
        b4 = TempPaper(Title=Title,
                       TypeOfPaper=TypeOfPaper,
                       Discipline=Discipline,
                       ipaddress=mac
                       )

        b4.save()

    AcademicLevel = TempPaper.objects.get(ipaddress=mac).AcademicLevel
    Timeline = TempPaper.objects.get(ipaddress=mac).Timeline

    if timeline is None:
        p = 0
    else:
        PaperSumation.objects.filter(ipaddress=mac).delete()
        P = PricePerDuration.objects.get(Level=AcademicLevel, Duration=timeline).Amount
        if pages is None:
            pg = 0
        else:
            pg = (float(pages) * float(P))
            desc = str(pages) + " Pages x $" + str(P)
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()

        if charts is None:
            pg = 0
        else:
            pg = ((float(charts) * float(P)) * 0.125)
            desc = str(charts) + " charts x $" + str(pg)
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()

        if native == "native":
            pg = round((float(P) * 0.3 * float(pages)), 2)
            desc = "Native Speaker "
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()

        else:
            pg = 0

        if Progressivedelivery == "Progressivedelivery":

            pg = round((float(P) * 0.1 * float(pages)), 2)
            desc = "Progressive delivery"
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )
            b4.save()
        else:
            pg = 0

        if smartpaper == "smartpaper":

            pg = round((float(P) * 0.2 * float(pages)), 2)
            desc = "Smart Paper"
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()
        else:
            pg = 0

        if Copysources == "Copysources":

            pg = round((float(P) * 0.1 * float(pages)), 2)
            desc = "Copy of Sources"
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()
        else:
            pg = 0

        if Writersample == "Writersample":

            pg = 5
            desc = "Writers Sample"
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()
        else:
            pg = 0

        if slides is None:
            pg = 0
        else:
            pg = ((float(slides) * float(P)) * 0.125)
            desc = str(slides) + " slides x $" + str(pg)
            b4 = PaperSumation(Description=desc,
                               Amount=pg,
                               Status="0",
                               ipaddress=mac
                               )

            b4.save()

        if spacing is None:
            pg = 0
        else:
            if spacing == "Single":
                pg = ((float(pages) * float(P)) * 0.2)

                desc = "Single Spacing"
                b4 = PaperSumation(Description=desc,
                                   Amount=pg,
                                   Status="0",
                                   ipaddress=mac
                                   )

                b4.save()

    data = {
        'is_taken': 'sawasawa'
    }

    return JsonResponse(data)


def UpdatePaper1(request):
    Title = request.GET['Title']
    TypeOfPaper = request.GET['TypeOfPaper']
    Discipline = request.GET['Discipline']
    target = request.GET['Undergraduate']
    mac1 = request.session.get('mac')

    request.session['target'] = target
    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
    else:
        mac = mac1
    try:
        P = TempPaper.objects.get(ipaddress=mac)
        c = TempPaper.objects.get(ipaddress=mac)
        c.Title = Title
        c.TypeOfPaper = TypeOfPaper
        c.Discipline = Discipline
        c.AcademicLevel = target

        c.save()

    except ObjectDoesNotExist:
        b4 = TempPaper(Title=Title,
                       TypeOfPaper=TypeOfPaper,
                       Discipline=Discipline,
                       ipaddress=mac
                       )

        b4.save()

    data = {
        'is_taken': 'sawasawa'
    }

    return JsonResponse(data)


def UpdatePaper2(request):
    Description = request.GET['Description']
    id = request.GET['id']

    c = Documents.objects.get(pk=id)
    c.Description = Description

    c.save()

    data = {
        'is_taken': 'sawasawa'
    }

    return JsonResponse(data)


def upload_file(request):
    uploaded_files = request.FILES.getlist('file')
    mac1 = request.session.get('mac')

    if mac1 is None:
        mac = random.randint(1000000, 10000000)
        request.session['mac'] = mac
    else:
        mac = mac1

    for files in uploaded_files:
        filename = files.name
        b4 = Documents(Document=files,
                       FileName=filename,
                       ipaddress=mac
                       )

        b4.save()

    data = {
        'is_taken': 'sawasawa'
    }

    return JsonResponse(data)


def Place_Order(request):
    mac1 = request.session.get('mac')
    Userid = request.session.get('Userid')
    if mac1 is None:
        mac = random.randint(1000000, 10000000)

        request.session['mac'] = mac
    else:
        mac = mac1
        dsum = PaperSumation.objects.filter(ipaddress=mac).aggregate(Sum('Amount'))['Amount__sum'] or 0
        Pages = TempPaper.objects.get(ipaddress=mac).Pages
        CPPESL = ((float(dsum) * 0.3) / float(Pages))
        CPPENL = ((float(dsum) * 0.5) / float(Pages))
        ESL = (float(dsum) * 0.3)
        ENL = (float(dsum) * 0.5)

    Orderid = random.randint(1000000, 10000000)
    c = TempPaper.objects.get(ipaddress=mac)
    c.Amount = dsum
    c.Orderid = Orderid
    c.PaymentStatus = "Paid"
    c.OrderStatus = "Pending"
    c.UserId = Userid
    c.ipaddress = Userid
    c.CPPESL = CPPESL
    c.CPPENL = CPPENL
    c.ESL = ESL
    c.ENL = ENL
    c.save()

    Documents.objects.filter(ipaddress=mac).update(UserId=Userid, PaperId=Orderid, PaperType="Cpaper", ipaddress=Userid)
    PaperSumation.objects.filter(ipaddress=mac).delete()
    # m=Documents.objects.filter(ipaddress=mac)
    # m.UserId=Userid
    # m.PaperId=Orderid
    # m.PaperType="Cpaper"
    # m.ipaddress=Userid
    # m.save()
    return redirect('/Dashboard')


def CSendMessage(request):
    if request.method == "POST":
        message = request.POST['message']
        PaperId = request.POST['PaperId']

        my_form = PaperMessage(PaperId=PaperId,
                               Message=message,
                               From="Student",

                               Status="0"
                               )
        my_form.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def CompleteOrder(request, id):
    c = TempPaper.objects.get(pk=id)
    c.OrderStatus = "Completed"
    c.save()

    context = {'list': TempPaper.objects.all()}
    return redirect('/Dashboard')


def RaiseDispute(request):
    if request.method == "POST":
        reason = request.POST['reason']
        orderid = request.POST['orderid']
        disputes = request.POST['disputes']

        c = TempPaper.objects.get(pk=orderid)
        c.OrderStatus = "Disputed"
        c.Disputereason = reason
        c.DisputeMain = disputes
        c.save()

    return redirect('/Dashboard')


def ImportData(request):
    excel_file = "priceslist.xlsx"
    excel_file1 = "Subjects.xlsx"
    excel_file2 = "typeofpaper.xlsx"
    TypePaper.objects.all().delete()
    Discipline.objects.all().delete()

    book = xlrd.open_workbook(excel_file)
    for sheet in book.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):

            s1 = (sheet.cell(row, 0).value)
            s2 = (sheet.cell(row, 1).value)
            s3 = (sheet.cell(row, 2).value)
            try:
                n = PricePerDuration.objects.get(Level=s1, Duration=s2)
            except ObjectDoesNotExist:
                my_form = PricePerDuration(Level=s1,
                                           Duration=s2,
                                           Amount=s3

                                           )
                my_form.save()

    book1 = xlrd.open_workbook(excel_file1)
    for sheet in book1.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):

            s1 = (sheet.cell(row, 0).value)
            s2 = (sheet.cell(row, 1).value)
            s3 = (sheet.cell(row, 2).value)
            s4 = (sheet.cell(row, 3).value)
            s5 = (sheet.cell(row, 4).value)
            s6 = (sheet.cell(row, 5).value)

            try:
                n = Discipline.objects.get(Name=s1)
            except ObjectDoesNotExist:
                my_form = Discipline(Name=s1,
                                     Highschool=int(s2),
                                     Undergrad1=int(s3),
                                     Undergrad2=int(s4),
                                     Grad=int(s5),
                                     PHD=int(s6),
                                     DisciplineType="All",
                                     Status="Active"

                                     )
                my_form.save()
    book2 = xlrd.open_workbook(excel_file2)
    for sheet in book2.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        for row in range(1, number_of_rows):

            s1 = (sheet.cell(row, 0).value)
            s2 = (sheet.cell(row, 1).value)
            s3 = (sheet.cell(row, 2).value)
            s4 = (sheet.cell(row, 3).value)
            s5 = (sheet.cell(row, 4).value)
            s6 = (sheet.cell(row, 5).value)

            try:
                n = TypePaper.objects.get(Name=s1)
            except ObjectDoesNotExist:
                my_form = TypePaper(Name=s1,
                                    Highschool=int(s2),
                                    Undergrad1=int(s3),
                                    Undergrad2=int(s4),
                                    Grad=int(s5),
                                    PHD=int(s6),
                                    PaperType="Essay",
                                    Status="Active"

                                    )
                my_form.save()

    data = {
        'is_taken': 'sawasawa'
    }

    return JsonResponse(data)
