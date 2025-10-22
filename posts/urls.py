from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.post_create_view, name='post_create'),
    path('', views.post_list_view, name='post_list'),
    path('<int:pk>/', views.post_detail_view, name='post_detail'),
    path('<int:pk>/delete/', views.post_delete_view, name='post_delete'),
    path('<int:pk>/like/', views.like_post_view, name='post_like'),path('<int:pk>/comment/', views.add_comment_view, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment_view, name='delete_comment'),
]