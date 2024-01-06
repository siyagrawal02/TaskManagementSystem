from django.urls import path,include

from . import views
from rest_framework import routers
from taskapp.views import UserViewSet,TaskViewSet

router=routers.DefaultRouter()
router.register(r'user',UserViewSet)
router.register(r'task',TaskViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('home/', views.home,name='home'),
    path('logout/', views.logoutuser,name='logoutuser'),
    path('signup/', views.signup,name='signup'),
    path('signup/login/signup/', views.signup,name='signup'),
    path('signup/login/', views.login,name='login'),
     path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('home_after_login/<int:user_id>/',views.home_after_login,name='home_after_login'),
    path('add/', views.addtask, name='addtask'),
    path('delete/<int:taskId>/', views.deltask, name='deltask'),
    path('details/<int:taskId>/', views.details, name='details'),
    path('update/<int:taskId>/', views.update, name='update'),
    
    
]