from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
app_name = "adminPage"
urlpatterns = [
    path('adminpage/', views.Home1, name='home'),
    path('createbus/', views.createBus, name='createbus'),
    path('seatbook/', views.seatBook, name='seatBook'),
    path('bookSeat/<int:pk>', views.bookSeat, name='bookSeat'),
    
    



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)