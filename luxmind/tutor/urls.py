from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    

    path('', views.TutorFront_page,name='TutorFront_page'),
    path('LoginTutor', views.LoginTutor,name='LoginTutor'),
    path('ForgotPassword', views.ForgotPassword,name='ForgotPassword'),
    path('logout_request', views.logout_request,name='logout_request'),
    path('TutorChangePassword', views.TutorChangePassword,name='TutorChangePassword'),
    path('New', views.TutorDashboard,name='TutorDashboard'),
    path('Current', views.CurrentPapers,name='CurrentPapers'),
    path('Finished', views.FinishedPaper,name='FinishedPaper'),
    path('Disputes', views.DisputesPaper,name='DisputesPaper'),
    path('Revision', views.RevisionPaper,name='RevisionPaper'),
    path('Bids', views.BidsPapers,name='BidsPapers'),
    path('Paper/<int:id>', views.TutorPaper,name='TutorPaper'),
    path('Create/Account', views.CreateAccount,name='CreateAccount'),
    path('NewAccount', views.NewAccount,name='NewAccount'),
    path('Download/<int:id>', views.DownloadFiles,name='DownloadFiles'),
    path('SendMessage', views.SendMessage,name='SendMessage'),
    path('TakeOrder/<int:id>', views.TakeOrder,name='TakeOrder'),
    path('BidOrder/<int:id>', views.BidOrder,name='BidOrder'),
    path('BidTime/<int:id>', views.BidTime,name='BidTime'),
    path('BidAmount/<int:id>', views.BidAmount,name='BidAmount'),
    path('BidTimeAmount/<int:id>', views.BidTimeAmount,name='BidTimeAmount'),
    path('SubmitOrder/<int:id>', views.SubmitOrder,name='SubmitOrder'),

    path('AcceptBid/<int:id>', views.AcceptBid,name='AcceptBid'),
    path('RejectBid/<int:id>', views.RejectBid,name='RejectBid'),
    path('DeleteFile/<int:id>', views.DeleteFile,name='DeleteFile'),
    path('SubmitFiles', views.SubmitFiles,name='SubmitFiles'),
    
    

]