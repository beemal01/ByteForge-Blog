from django.urls import path, include
from . import views

urlpatterns = [
    path('createpost/', views.createpost, name='createpost'),
    path('update_post/<slug:slug>/', views.update_post, name='update_post'),
    path('api/blogview/', views.blogview.as_view(), name='blogview'),
    path('api/blogdetails/<slug:slug>/', views.blogdetails.as_view(), name='blogdetails'),
    path('', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('<slug:slug>/', views.inner_post, name='inner_post'),

]
