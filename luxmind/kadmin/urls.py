from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    

    path('', views.KFront_page,name='KFront_page'),
    path('Login', views.AdminLogin,name='AdminLogin'),
    path('Dashboard', views.AdminDashbard,name='AdminDashbard'),
    path('Writters', views.AdminWritters,name='AdminWritters'),
    path('Writter/<int:id>', views.Writter_Edit,name='Writter_Edit'),
    path('UpdateAccount', views.UpdateAccount,name='UpdateAccount'),

    path('Orders', views.AdminOrders,name='AdminOrders'),
    path('Orders/<int:id>', views.AdminOrder,name='AdminOrder'),
    path('UpdateOrders', views.UpdateOrders,name='UpdateOrders'),

    path('Priceperpage', views.PricePerPage,name='PricePerPage'),
    path('Add/Priceperpage', views.PricePerPage_Add,name='PricePerPage_Add'),
    path('Priceperpage/<int:id>', views.PricePerPage_Add,name='PricePerPage_Edit'),
    path('Priceperpage/delete/<int:id>', views.PricePerPage_Delete,name='PricePerPage_Delete'),

    path('Discpline', views.DisplinePage,name='DisplinePage'),
    path('Add/Discpline', views.Discpline_Add,name='Discpline_Add'),
    path('Discpline/<int:id>', views.Discpline_Add,name='Discpline_Edit'),
    path('Discpline/delete/<int:id>', views.Discpline_Delete,name='Discpline_Delete'),


    path('Paper', views.PaperPage,name='PaperPage'),
    path('Add/Paper', views.Paper_Add,name='Paper_Add'),
    path('Paper/<int:id>', views.Paper_Add,name='Paper_Edit'),
    path('Paper/delete/<int:id>', views.Paper_Delete,name='Paper_Delete'),

    path('PickBid/<int:id>', views.PickBid,name='PickBid'),
    

]