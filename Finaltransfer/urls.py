from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('send_file',views.send_file,name="send_file"),
    path('encrypt_data',views.encrypt_data,name="encrypt_data"),
    path('uploadqr', views.uploadqr, name="uploadqr"),
    path('decrypt',views.decrypt,name="decrypt"),
    path('handleSignUp',views.handleSignUp,name="handleSignUp"),
    path('handelLogin',views.handelLogin,name="handelLogin"),
    path('handleLogout',views.handelLogout,name="handelLogout"),
    path('home',views.home,name="home"),
    path('forgot_password',views.forgot_password,name="forgot_password")
]