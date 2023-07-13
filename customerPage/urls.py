from . import views
from django.urls import path
# from django.contrib.auth.views import LogoutView

app_name = 'customerPage'

urlpatterns = [
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),  
    path('profile/', views.Profile, name='profile'),
    path('cancel/', views.Cancel, name='cancel'),
    path('print/', views.Print, name='print'),
    # Use the custom login view
    path('', views.Index, name='index'),
    path('about/', views.About, name='about'),
    path('edit/', views.EditProfileView.as_view(), name='editProfile'),
    path('editpassword/', views.ChangePasswordView.as_view(), name='changePassword'),
    path('contact/', views.Contact, name='contact'),
    
    
   
    
    



]