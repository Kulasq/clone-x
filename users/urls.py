from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('<str:username>/', views.public_profile_view, name='public_profile'),
    path('profile/delete-picture/', views.delete_profile_picture_view, name='delete_profile_picture'),
    path('account/delete/', views.account_delete_view, name='account_delete'),
]