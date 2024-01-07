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
    path('logout/', views.logoutUser,name='logoutUser'),
    path('signup/', views.signup,name='signup'),
    path('signup/login/signup/', views.signup,name='signup'),
    path('signup/login/', views.login,name='login'),
     path('forgot_password/', views.forgotPassword, name='forgotPassword'),
    path('verifyOtp/', views.verifyOtp, name='verifyOtp'),
    path('reset_password/', views.resetPassword, name='resetPassword'),
    path('taskList/<int:user_id>/',views.taskList,name='taskList'),
    path('add/', views.addTask, name='addTask'),
    path('delete/<int:taskId>/', views.delTask, name='delTask'),
    path('details/<int:taskId>/', views.details, name='details'),
    path('update/<int:taskId>/', views.updateTask, name='updateTask'),
    
    
]