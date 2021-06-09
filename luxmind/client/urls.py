from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'client'
urlpatterns = [
    
    path('', views.Front_page,name='Front_page'),
    path('Register', views.Register_page,name='Register_page'),
    path('Forgot_Password', views.ForgotPassword,name='ForgotPassword'),
    path('Change_Password', views.ChangePassword,name='ChangePassword'),
    path('logout_urequest', views.logout_urequest,name='logout_urequest'),
    path('CreateClient', views.CreateClient,name='CreateClient'),
    path('LoginClient', views.LoginClient,name='LoginClient'),
    path('Dashboard', views.Dashboard,name='Dashboard'),
    path('FreeEnquiry', views.FreeEnquiry,name='FreeEnquiry'),
    path('OrderPaper', views.OrderPaper,name='OrderPaper'),
    path('UpdatePaper', views.UpdatePaper,name='UpdatePaper'),
    path('UpdatePaper1', views.UpdatePaper1,name='UpdatePaper1'),
    path('UpdatePaper2', views.UpdatePaper2,name='UpdatePaper2'),
    path('upload_file', views.upload_file,name='upload_file'),
    path('PlaceOrder', views.Place_Order,name='Place_Order'),
    path('PlaceEnquiry', views.PlaceEnquiry,name='PlaceEnquiry'),
    path('View/Order/<int:id>', views.View_Order,name='View_Order'),
    path('CSendMessage', views.CSendMessage,name='CSendMessage'),
    path('CompleteOrder/<int:id>', views.CompleteOrder,name='CompleteOrder'),
    path('RaiseDispute', views.RaiseDispute,name='RaiseDispute'),
    path('ImportData', views.ImportData,name='ImportData'),
    path('post_messages', views.post_messages,name='post_messages'),


]