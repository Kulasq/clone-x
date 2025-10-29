from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('account/delete/', views.account_delete_view, name='account_delete'),
    path('search/', views.user_search_view, name='user_search'),
    path('<str:username>/follow/', views.follow_user_view, name='follow_user'),
    path('<str:username>/following/', views.following_list_view, name='following_list'),
    path('<str:username>/followers/', views.followers_list_view, name='followers_list'),
    path('<str:username>/', views.public_profile_view, name='public_profile'),
]