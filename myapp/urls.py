from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('page/', views.page,name='page'),
    path('postpage/',views.postpage,name='postpage'),

    # login-out
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('register/',views.register,name='register'),

    path('detail/<int:page_id>/',views.detail,name='detail'), #Xem Chi Tiet Từng SP
    path('search/', views.search, name='search'),

    path('follow/<int:user_id>/', views.follow_user, name='follow_user'), 
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),


    path('notifications/', views.notifications, name='notifications'),
    

    path('users/', views.user_list, name='user'),
    ]

