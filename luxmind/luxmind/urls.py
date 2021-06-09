
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 


urlpatterns = [
    path('admin/', admin.site.urls),   
    path('luxmind/', include('kadmin.urls')),
    path('', include('client.urls')),
    path('Tutor/', include('tutor.urls')),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]

# handler404 = 'client.views.custom_page_not_found_view'
# handler500 = 'client.views.custom_error_view'
# handler403 = 'client.views.custom_permission_denied_view'
# handler400 = 'client.views.custom_bad_request_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
