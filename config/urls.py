from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from salon.views import add_master
from mathem.views import main, hello
from salon.api_views import (
    SalonListCreateView, 
    SalonRetrieveUpdateDestroyView,
    MasterCreateView,
    MasterListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),

        # api
    path('api/master/add', add_master, name='add_master'),
    path('api/salons/', SalonListCreateView.as_view()),
    path('api/salons/<int:pk>/', SalonRetrieveUpdateDestroyView.as_view()),
    path('api/masters/create/', MasterCreateView.as_view()),
    path('api/masters/<salon_name>/<service_id>', MasterListView.as_view()),
    
    path('main', main, name='main'),
    path('hello', hello, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)